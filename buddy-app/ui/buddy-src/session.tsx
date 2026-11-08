/** @jsxImportSource react */
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import type { SessionsCreateResult } from "../../packages/gateway-protocol/src/schema/sessions.js";
import type { BuddyGateway } from "./gateway.ts";
import { errorMessage } from "./gateway.ts";

type SessionRow = { key: string; label?: string; displayName?: string; title?: string; permissionMode?: string };
type Message = { role?: string; content?: string | Array<{ type?: string; text?: string }> };
type ChatEvent = { sessionKey?: string; runId?: string; state?: string; errorMessage?: string };

export function useGateway(gateway: BuddyGateway) {
  return useSyncExternalStore(gateway.subscribe, gateway.snapshot);
}

export function SessionPicker(props: {
  gateway: BuddyGateway;
  value: string;
  onChange: (value: string) => void;
  title: string;
  disabled?: boolean;
  readOnly?: boolean;
}) {
  const { gateway, title, value, onChange, readOnly } = props;
  const connection = useGateway(gateway);
  const [sessions, setSessions] = useState<SessionRow[]>([]);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (!connection.connected) return;
    let active = true;
    void gateway.request<{ sessions: SessionRow[] }>("sessions.list", { limit: 100 })
      .then(({ sessions }) => {
        if (active) {
          setSessions(readOnly ? sessions.filter((session) => session.permissionMode === "read-only") : sessions);
          setError("");
        }
      })
      .catch((error: unknown) => { if (active) setError(errorMessage(error)); });
    return () => { active = false; };
  }, [connection.connected, gateway, readOnly]);

  async function createSession() {
    setCreating(true);
    setError("");
    try {
      const session = await gateway.request<SessionsCreateResult>("sessions.create", {
        displayName: title,
        idempotencyKey: crypto.randomUUID(),
        ...(readOnly ? { permissionMode: "read-only" } : {}),
        ...(connection.agentId ? { agentId: connection.agentId } : {}),
      });
      setSessions((rows) => [{ key: session.key, displayName: title }, ...rows]);
      onChange(session.key);
    } catch (error) {
      setError(errorMessage(error));
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="buddy-controls">
      <label>
        Phiên làm việc
        <select value={value} disabled={props.disabled || !connection.connected} onChange={(event) => onChange(event.target.value)}>
          <option value="">Chọn một phiên</option>
          {value && !sessions.some((row) => row.key === value) && <option value={value}>{value}</option>}
          {sessions.map((row) => <option key={row.key} value={row.key}>{row.displayName || row.title || row.label || row.key}</option>)}
        </select>
      </label>
      <button type="button" disabled={props.disabled || creating || !connection.connected} onClick={() => void createSession()}>
        {creating ? "Đang tạo phiên…" : "Phiên mới"}
      </button>
      {error && <p role="alert">{error}</p>}
    </div>
  );
}

export function useAgentConversation(gateway: BuddyGateway, sessionKey: string) {
  const { connected } = useGateway(gateway);
  const [messages, setMessages] = useState<Message[]>([]);
  const [runId, setRunId] = useState("");
  const [error, setError] = useState("");
  const currentRun = useRef("");

  useEffect(() => {
    if (!connected || !sessionKey) return;
    let active = true;
    let request = 0;
    function refresh() {
      const revision = ++request;
      void gateway.request<{ messages: Message[]; inFlightRun?: { runId: string } }>("chat.history", {
        sessionKey, limit: 50,
      }).then((result) => {
        if (!active || revision !== request) return;
        setMessages(result.messages);
        if (result.inFlightRun?.runId && !currentRun.current) {
          currentRun.current = result.inFlightRun.runId;
          setRunId(result.inFlightRun.runId);
        }
      }).catch((error: unknown) => {
        if (active && revision === request) setError(errorMessage(error));
      });
    }
    const unsubscribe = gateway.subscribeEvents((frame) => {
      if (frame.event !== "chat" || !frame.payload || typeof frame.payload !== "object") return;
      const event = frame.payload as ChatEvent;
      if (event.sessionKey !== sessionKey) return;
      if (event.state !== "final" && event.state !== "error" && event.state !== "aborted") return;
      if (event.runId === currentRun.current) {
        currentRun.current = "";
        setRunId("");
        if (event.state === "error") setError(event.errorMessage ?? "Agent không hoàn tất lượt chạy.");
      }
      refresh();
    });
    refresh();
    return () => { active = false; unsubscribe(); };
  }, [connected, gateway, sessionKey]);

  async function send(message: string) {
    if (!sessionKey || currentRun.current || !message.trim()) return false;
    const idempotencyKey = crypto.randomUUID();
    currentRun.current = idempotencyKey;
    setRunId(idempotencyKey);
    setError("");
    try {
      await gateway.request("chat.send", { sessionKey, message: message.trim(), idempotencyKey, deliver: false });
      return true;
    } catch (error) {
      if (currentRun.current === idempotencyKey) {
        currentRun.current = "";
        setRunId("");
      }
      setError(errorMessage(error));
      return false;
    }
  }

  async function stop() {
    try {
      await gateway.request("chat.abort", { sessionKey, runId: currentRun.current });
    } catch (error) {
      setError(errorMessage(error));
    }
  }

  return { messages, running: Boolean(runId), error, send, stop };
}

export function ConversationLog({ messages }: { messages: Message[] }) {
  return (
    <div className="buddy-transcript" aria-live="polite">
      {messages.map((message, index) => {
        const content = typeof message.content === "string"
          ? message.content
          : message.content?.filter((part) => part.type === "text").map((part) => part.text).join("\n");
        return content ? (
          <article key={index}>
            <strong>{message.role === "user" ? "Bạn" : message.role === "assistant" ? "Buddy" : message.role}</strong>
            <div>{content}</div>
          </article>
        ) : null;
      })}
    </div>
  );
}
