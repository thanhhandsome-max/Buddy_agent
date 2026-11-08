/** @jsxImportSource react */
import { Activity, Camera, Download, FileText, ShieldCheck } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { errorMessage, type BuddyGateway } from "./gateway.ts";
import { PersonSafety } from "./person-safety.tsx";
import { inspectScam } from "./scam-inspector.ts";
import { analyzeSecurityLog, frameChange, MAX_LOG_BYTES, SECURITY_SAMPLE_LOG } from "./security-analysis.ts";
import { FULL_REGION, inWatchSchedule, normalizeRegion, type WatchRegion } from "./security-practical.ts";
import { ConversationLog, SessionPicker, useAgentConversation, useGateway } from "./session.tsx";

export function BuddySecurityPage({ gateway }: { gateway: BuddyGateway }) {
  const [tab, setTab] = useState<"camera" | "cyber">("camera");
  return (
    <section className="buddy-page buddy-security">
      <header><ShieldCheck /><div><h1>Bảo mật</h1><p>Camera Safety và Cyber Security</p></div></header>
      <nav className="buddy-controls" aria-label="Công cụ bảo mật">
        <button aria-pressed={tab === "camera"} onClick={() => setTab("camera")}><Camera size={16} /> Camera Safety</button>
        <button aria-pressed={tab === "cyber"} onClick={() => setTab("cyber")}><ShieldCheck size={16} /> Cyber Security</button>
      </nav>
      {tab === "camera" ? <><BrowserCamera gateway={gateway} /><PairedCamera gateway={gateway} /></> : <CyberSafety gateway={gateway} />}
    </section>
  );
}

function BrowserCamera({ gateway }: { gateway: BuddyGateway }) {
  const video = useRef<HTMLVideoElement>(null);
  const stream = useRef<MediaStream | null>(null);
  const generation = useRef(0);
  const [live, setLive] = useState(false);
  const [starting, setStarting] = useState(false);
  const [armed, setArmed] = useState(false);
  const [evidence, setEvidence] = useState(false);
  const [scheduled, setScheduled] = useState(false);
  const [from, setFrom] = useState("22:00");
  const [to, setTo] = useState("06:00");
  const [region, setRegion] = useState<WatchRegion>(FULL_REGION);
  const [threshold, setThreshold] = useState(12);
  const [change, setChange] = useState(0);
  const [error, setError] = useState("");
  const [events, setEvents] = useState<{ id: string; at: string; message: string; image?: string }[]>([]);

  function addEvent(message: string, image?: string) {
    setEvents((items) => [{ id: crypto.randomUUID(), at: new Date().toISOString(), message, image }, ...items].slice(0, 100));
  }

  function release() {
    generation.current += 1;
    stream.current?.getTracks().forEach((track) => track.stop());
    stream.current = null;
    if (video.current) video.current.srcObject = null;
  }
  useEffect(() => release, []);

  async function start() {
    setError("");
    setStarting(true);
    const request = ++generation.current;
    try {
      if (!navigator.mediaDevices?.getUserMedia) throw new Error("Mở Control UI qua HTTPS hoặc localhost để dùng webcam.");
      const next = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      if (generation.current !== request || !video.current) {
        next.getTracks().forEach((track) => track.stop());
        return;
      }
      stream.current = next;
      video.current.srcObject = next;
      await video.current.play();
      if (generation.current !== request) return;
      setLive(true);
      addEvent("Đã mở webcam.");
    } catch (error) {
      if (generation.current !== request) return;
      release();
      setStarting(false);
      setError(errorMessage(error));
    } finally {
      if (generation.current === request) setStarting(false);
    }
  }

  function stop() {
    release();
    setLive(false);
    setStarting(false);
    setArmed(false);
    setChange(0);
    addEvent("Đã tắt webcam.");
  }

  useEffect(() => {
    if (!live || !armed) return;
    const canvas = document.createElement("canvas");
    canvas.width = 160;
    canvas.height = 90;
    const context = canvas.getContext("2d", { willReadFrequently: true });
    if (!context) return;
    let previous: Uint8ClampedArray | undefined;
    let lastFrame = -1;
    let lastAlert = -Infinity;
    const timer = window.setInterval(() => {
      const player = video.current;
      if (!player || player.readyState < 2 || document.hidden || !inWatchSchedule(scheduled, from, to)) {
        previous = undefined;
        return;
      }
      if (lastFrame === player.currentTime) return;
      lastFrame = player.currentTime;
      context.drawImage(player, player.videoWidth * region.x, player.videoHeight * region.y,
        player.videoWidth * region.width, player.videoHeight * region.height, 0, 0, canvas.width, canvas.height);
      const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
      const percent = previous ? frameChange(previous, pixels) * 100 : 0;
      previous = pixels;
      setChange(percent);
      if (percent >= threshold && performance.now() - lastAlert > 5000) {
        lastAlert = performance.now();
        addEvent(`Chuyển động trong vùng đã chọn (${percent.toFixed(1)}%).`,
          evidence ? canvas.toDataURL("image/jpeg", 0.75) : undefined);
      }
    }, 500);
    return () => window.clearInterval(timer);
  }, [live, armed, scheduled, from, to, region, threshold, evidence]);

  function snapshot() {
    const player = video.current;
    if (!player || player.readyState < 2) return;
    const canvas = document.createElement("canvas");
    canvas.width = player.videoWidth;
    canvas.height = player.videoHeight;
    canvas.getContext("2d")?.drawImage(player, 0, 0);
    saveUrl(canvas.toDataURL("image/jpeg", 0.85), `buddy-camera-${Date.now()}.jpg`);
    addEvent("Đã tải một khung hình webcam.");
  }

  return (
    <section className="buddy-panel">
      <h2><Camera size={19} /> Webcam tại máy</h2>
      <div className="buddy-controls">
        {live || starting ? <button onClick={stop}>Tắt camera</button> : <button onClick={() => void start()}>Bật camera</button>}
        <button disabled={!live} onClick={snapshot}><Download size={15} /> Lưu khung hình</button>
        <label className="buddy-check"><input type="checkbox" checked={armed} disabled={!live} onChange={(event) => setArmed(event.target.checked)} /> Trông khu vực</label>
        <label className="buddy-check"><input type="checkbox" checked={evidence} onChange={(event) => setEvidence(event.target.checked)} /> Lưu ảnh trong nhật ký phiên</label>
      </div>
      {error && <p role="alert">{error}</p>}
      <video ref={video} aria-label="Xem webcam" muted playsInline hidden={!live} />
      <details>
        <summary>Vùng quan sát và lịch</summary>
        <div className="buddy-controls">
          {(["x", "y", "width", "height"] as const).map((key) => (
            <label key={key}>{({ x: "Vị trí ngang", y: "Vị trí dọc", width: "Rộng", height: "Cao" })[key]}
              <input type="number" min={0} max={100} value={Math.round(region[key] * 100)}
                onChange={(event) => setRegion(normalizeRegion({ ...region, [key]: Number(event.target.value) / 100 }))} />
            </label>
          ))}
          <label>Ngưỡng chuyển động (%)<input type="range" min={1} max={100} value={threshold} onChange={(event) => setThreshold(Number(event.target.value))} /><output>{threshold}%</output></label>
          <label className="buddy-check"><input type="checkbox" checked={scheduled} onChange={(event) => setScheduled(event.target.checked)} /> Dùng lịch</label>
          {scheduled && <><label>Từ<input type="time" value={from} onChange={(event) => setFrom(event.target.value)} /></label><label>Đến<input type="time" value={to} onChange={(event) => setTo(event.target.value)} /></label></>}
        </div>
      </details>
      <p role="status">{armed ? `Thay đổi giữa hai khung hình: ${change.toFixed(1)}%` : "Chưa bật theo dõi chuyển động."}</p>
      <PersonSafety video={video} live={live} armed={armed} region={region} scheduled={scheduled}
        from={from} to={to} evidence={evidence} onAlert={addEvent}
        modelUrl={new URL(gateway.href("/assets/buddy-vision/movenet/model.json"), location.origin).href} />
      <details>
        <summary>Nhật ký camera ({events.length})</summary>
        <button disabled={!events.length} onClick={() => setEvents([])}>Xóa nhật ký phiên</button>
        <ul>{events.map((event) => <li key={event.id}><time dateTime={event.at}>{new Date(event.at).toLocaleTimeString("vi-VN")}</time> {event.message}
          {event.image && <img src={event.image} alt="Khung hình ghi nhận sự kiện" loading="lazy" />}</li>)}</ul>
      </details>
    </section>
  );
}

function saveUrl(url: string, filename: string) {
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
}

type CameraNode = { nodeId: string; displayName?: string; connected?: boolean; commands?: string[] };
type NodeCamera = { id: string; name?: string; position?: string };
type SnapPayload = { format?: string; base64?: string; width?: number; height?: number };

function PairedCamera({ gateway }: { gateway: BuddyGateway }) {
  const connection = useGateway(gateway);
  const [nodes, setNodes] = useState<CameraNode[]>([]);
  const [nodeId, setNodeId] = useState("");
  const [devices, setDevices] = useState<NodeCamera[]>([]);
  const [deviceId, setDeviceId] = useState("");
  const [shot, setShot] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [loaded, setLoaded] = useState(false);
  const node = nodes.find((entry) => entry.nodeId === nodeId);

  async function run(operation: () => Promise<void>) {
    setBusy(true);
    setError("");
    try { await operation(); }
    catch (error) { setError(errorMessage(error)); }
    finally { setBusy(false); }
  }

  async function loadNodes() {
    const response = await gateway.request<{ nodes: CameraNode[] }>("node.list", {});
    const available = response.nodes.filter((item) => item.connected && item.commands?.includes("camera.snap"));
    setNodes(available);
    setLoaded(true);
    if (!available.some((item) => item.nodeId === nodeId)) {
      setNodeId("");
      setDevices([]);
      setDeviceId("");
      setShot("");
    }
  }

  async function invoke<T>(command: string, params: object): Promise<T> {
    const response = await gateway.request<{ ok: boolean; payload?: T }>("node.invoke", {
      nodeId, command, params, timeoutMs: 20000, idempotencyKey: crypto.randomUUID(),
      ...(connection.sessionKey ? { sessionKey: connection.sessionKey } : {}),
    });
    if (!response.ok || !response.payload) throw new Error("Node không trả kết quả camera.");
    return response.payload;
  }

  async function loadCameras() {
    const result = await invoke<{
      devices?: NodeCamera[];
      cameras?: Array<{ DeviceId: string; Name?: string }>;
    }>("camera.list", {});
    const cameras = result.devices ?? result.cameras?.map((device) => ({ id: device.DeviceId, name: device.Name })) ?? [];
    setDevices(cameras.filter((camera) => typeof camera.id === "string" && camera.id));
    setDeviceId("");
  }

  async function takePicture() {
    const payload = await invoke<SnapPayload>("camera.snap", { maxWidth: 1280, format: "jpg", ...(deviceId ? { deviceId } : {}) });
    const format = payload.format?.toLowerCase();
    const mime = format === "png" ? "image/png" : format === "jpeg" || format === "jpg" ? "image/jpeg" : "";
    if (!mime || !payload.base64 || !/^[A-Za-z0-9+/]+={0,2}$/u.test(payload.base64)) {
      throw new Error("Node không cung cấp ảnh JPEG/PNG nội tuyến hợp lệ.");
    }
    setShot(`data:${mime};base64,${payload.base64}`);
  }

  return (
    <section className="buddy-panel">
      <h2>Camera từ xa qua Gateway</h2>
      <div className="buddy-controls">
        <button disabled={busy || !connection.connected} onClick={() => void run(loadNodes)}>Tìm node camera</button>
        <label>Node<select value={nodeId} disabled={busy || !connection.connected} onChange={(event) => {
          setNodeId(event.target.value); setDeviceId(""); setDevices([]); setShot("");
        }}>
          <option value="">Chọn node</option>
          {nodes.map((item) => <option key={item.nodeId} value={item.nodeId}>{item.displayName || item.nodeId}</option>)}
        </select></label>
        {node?.commands?.includes("camera.list") && <button disabled={busy || !connection.connected} onClick={() => void run(loadCameras)}>Liệt kê camera</button>}
        {devices.length > 0 && <label>Camera<select value={deviceId} disabled={busy} onChange={(event) => setDeviceId(event.target.value)}>
          <option value="">Camera mặc định</option>
          {devices.map((item) => <option key={item.id} value={item.id}>{item.name || item.position || item.id}</option>)}
        </select></label>}
        <button disabled={!node || busy || !connection.connected} onClick={() => void run(takePicture)}><Camera size={16} /> Chụp ảnh node</button>
      </div>
      {loaded && !nodes.length && <p>Chưa thấy node đã kết nối và công bố lệnh chụp ảnh. <a href={gateway.href("/settings/devices")}>Quản lý thiết bị</a>.</p>}
      {busy && <p role="status">Đang chờ Gateway…</p>}
      {error && <p role="alert">{error}</p>}
      {shot && <><img src={shot} alt="Ảnh chụp từ node đã chọn" /><button onClick={() => saveUrl(shot, `buddy-node-${Date.now()}.${shot.startsWith("data:image/png") ? "png" : "jpg"}`)}>Tải ảnh</button></>}
    </section>
  );
}

function CyberSafety({ gateway }: { gateway: BuddyGateway }) {
  const [input, setInput] = useState("");
  const [report, setReport] = useState<ReturnType<typeof analyzeSecurityLog>>();
  const [text, setText] = useState("");
  const [domain, setDomain] = useState("");
  const [scam, setScam] = useState<ReturnType<typeof inspectScam>>();
  const [error, setError] = useState("");
  const [sessionKey, setSessionKey] = useState("");
  const [running, setRunning] = useState(false);
  const uploadRevision = useRef(0);
  function changeLog(value: string) {
    uploadRevision.current += 1;
    setInput(value);
    setReport(undefined);
  }

  async function upload(file: File) {
    const revision = ++uploadRevision.current;
    try {
      if (file.size > MAX_LOG_BYTES) throw new Error("Tệp nhật ký vượt giới hạn 1 MB.");
      const content = await file.text();
      if (revision !== uploadRevision.current) return;
      if (content.includes("\0")) throw new Error("Chọn nhật ký dạng TXT, LOG hoặc JSONL.");
      changeLog(content);
      setError("");
    } catch (error) {
      if (revision === uploadRevision.current) setError(errorMessage(error));
    }
  }

  return (
    <>
      <section className="buddy-panel">
        <h2><Activity size={19} /> Phân tích nhật ký</h2>
        <label>Nhật ký<textarea rows={7} value={input} onChange={(event) => changeLog(event.target.value)} /></label>
        <div className="buddy-controls">
          <label>Mở tệp log<input type="file" accept=".txt,.log,.jsonl" onChange={(event) => {
            const file = event.target.files?.[0];
            event.target.value = "";
            if (file) void upload(file);
          }} /></label>
          <button onClick={() => changeLog(SECURITY_SAMPLE_LOG)}>Dùng log mẫu</button>
          <button disabled={!input.trim()} onClick={() => {
            setError("");
            try { setReport(analyzeSecurityLog(input)); }
            catch (error) { setError(errorMessage(error)); }
          }}>Phân tích</button>
          {report && <button onClick={() => {
            const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }));
            saveUrl(url, "buddy-security-report.json");
            window.setTimeout(() => URL.revokeObjectURL(url), 1000);
          }}>Xuất JSON</button>}
        </div>
        {report && <>
          <p role="status">{report.findings.length} dấu hiệu trên {report.lines} dòng{report.truncated ? " · đầu vào đã được giới hạn" : ""}.</p>
          <ul>{report.findings.map((item) => <li key={item.id}>
            <strong>{item.title} · dòng {item.line}</strong><pre>{item.evidence}</pre><p>{item.recommendation}</p>
          </li>)}</ul>
        </>}
      </section>
      <section className="buddy-panel">
        <h2><FileText size={19} /> Kiểm tra tin nhắn và liên kết</h2>
        <label>Tên miền chính thức để đối chiếu<input value={domain} onChange={(event) => { setDomain(event.target.value); setScam(undefined); }} /></label>
        <label>Nội dung cần kiểm tra<textarea rows={4} maxLength={20000} value={text} onChange={(event) => { setText(event.target.value); setScam(undefined); }} /></label>
        <button disabled={!text.trim()} onClick={() => {
          setError("");
          try { setScam(inspectScam(text, domain)); }
          catch (error) { setError(errorMessage(error)); }
        }}>Kiểm tra tại máy</button>
        {scam && <><p role="status">{scam.signals.length} dấu hiệu. {scam.scope}</p>
          <ul>{scam.signals.map((signal, index) => <li key={signal.id + index}>
            <strong>{signal.title}</strong><p>{signal.evidence}</p><p>{signal.action}</p>
          </li>)}</ul></>}
      </section>
      {error && <p role="alert">{error}</p>}
      <section className="buddy-panel">
        <h2>Rà soát bảo mật dự án với agent</h2>
        <SessionPicker gateway={gateway} value={sessionKey} title="Rà soát bảo mật" onChange={setSessionKey} disabled={running} readOnly />
        {sessionKey && <SecurityReview key={sessionKey} gateway={gateway} sessionKey={sessionKey} onRunning={setRunning} />}
      </section>
    </>
  );
}

function SecurityReview({ gateway, sessionKey, onRunning }: { gateway: BuddyGateway; sessionKey: string; onRunning: (running: boolean) => void }) {
  const [prompt, setPrompt] = useState("");
  const { connected } = useGateway(gateway);
  const conversation = useAgentConversation(gateway, sessionKey);
  useEffect(() => { onRunning(conversation.running); }, [conversation.running, onRunning]);
  return (
    <form className="buddy-form" onSubmit={(event) => {
      event.preventDefault();
      void conversation.send(`Rà soát phòng thủ trong workspace của phiên. Chỉ đọc và báo cáo bằng chứng, đường dẫn và cách khắc phục. Yêu cầu: ${prompt}`)
        .then((sent) => { if (sent) setPrompt(""); });
    }}>
      <label>Phạm vi rà soát<textarea rows={3} value={prompt} onChange={(event) => setPrompt(event.target.value)} /></label>
      <div className="buddy-controls">
        <button disabled={!prompt.trim() || !connected || conversation.running}>Gửi phạm vi cho agent</button>
        {conversation.running && <button type="button" disabled={!connected} onClick={() => void conversation.stop()}>Dừng rà soát</button>}
      </div>
      {conversation.error && <p role="alert">{conversation.error}</p>}
      <ConversationLog messages={conversation.messages} />
    </form>
  );
}
