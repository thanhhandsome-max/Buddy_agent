import { onSettled } from "solid-js";
import { createRoot } from "react-dom/client";
import { createElement } from "react";
import { BuddyCoderPage } from "../../../buddy-src/coder.tsx";
import { BuddySecurityPage } from "../../../buddy-src/security.tsx";
import type { BuddyGateway, BuddyGatewayState } from "../../../buddy-src/gateway.ts";
import style from "../../../buddy-src/workspace.css?inline";
import type { ApplicationContext } from "../../app/context.ts";
import { useApplication } from "../../lib/reactive/context.ts";

function scopeOf(context: ApplicationContext): string {
  return JSON.stringify([context.gateway.connectionRevision, context.gateway.snapshot.selfUser?.id ?? ""]);
}

function bindBuddyGateway(context: ApplicationContext, scope: string): BuddyGateway {
  const gateway = context.gateway;
  let snapshot: BuddyGatewayState | undefined;

  return {
    snapshot() {
      const current = gateway.snapshot;
      const connected = current.phase === "connected" && current.client !== null && scopeOf(context) === scope;
      const sessionKey = connected ? current.sessionKey : "";
      const agentId = connected ? current.assistantAgentId : null;
      if (!snapshot || snapshot.connected !== connected || snapshot.sessionKey !== sessionKey || snapshot.agentId !== agentId) {
        snapshot = { scope, connected, sessionKey, agentId };
      }
      return snapshot;
    },
    subscribe: (listener) => gateway.subscribe(listener),
    subscribeEvents: (listener) => gateway.subscribeEvents((event) => {
      if (scopeOf(context) === scope) listener(event);
    }, { includeMessageBodies: false }),
    async request<T>(method: string, params?: unknown): Promise<T> {
      const { client, phase } = gateway.snapshot;
      if (phase !== "connected" || !client || scopeOf(context) !== scope) {
        throw new Error("Gateway chưa sẵn sàng. Kiểm tra kết nối và thử lại.");
      }
      const result = await client.request<T>(method, params);
      if (scopeOf(context) !== scope || gateway.snapshot.client !== client) {
        throw new Error("Kết nối Gateway đã đổi trong khi thao tác.");
      }
      return result;
    },
    href: (path) => `${context.basePath}${path}`,
  };
}

function BuddyPage(props: { page: "coder" | "security" }) {
  const context = useApplication();
  let host!: HTMLDivElement;
  onSettled(() => {
    const shadow = host.shadowRoot ?? host.attachShadow({ mode: "open" });
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(style);
    shadow.adoptedStyleSheets = [sheet];
    const root = createRoot(shadow);
    if (props.page === "coder") {
      root.render(createElement(BuddyCoderPage));
      return () => root.unmount();
    }
    let previousScope: string | undefined;
    const render = () => {
      const scope = scopeOf(context);
      if (scope === previousScope) return;
      previousScope = scope;
      root.render(createElement(BuddySecurityPage, { key: scope, gateway: bindBuddyGateway(context, scope) }));
    };
    const stop = context.gateway.subscribe(render);
    render();
    return () => {
      stop();
      root.unmount();
    };
  });
  return <div class="buddy-route-host" ref={host} />;
}

export function CoderPage() {
  return <BuddyPage page="coder" />;
}

export function SecurityPage() {
  return <BuddyPage page="security" />;
}
