import React, { useCallback, useEffect, useState } from "react";

/** OpenCode runs locally (Start-Buddy-Coder.cmd) and allows embedding: no X-Frame-Options or frame-ancestors. */
export const OPENCODE_URL = "http://127.0.0.1:4096/";

type Status = "checking" | "online" | "offline";

/** Any HTTP answer means the server is up; an opaque no-cors response is enough. */
export async function probeOpenCode(url: string, fetcher: typeof fetch = fetch): Promise<boolean> {
  try {
    await fetcher(url, { mode: "no-cors", cache: "no-store", signal: AbortSignal.timeout(2500) });
    return true;
  } catch {
    return false;
  }
}

export function BuddyCoderPage() {
  const [status, setStatus] = useState<Status>("checking");
  const [frameKey, setFrameKey] = useState(0);

  const check = useCallback(async () => {
    setStatus("checking");
    setStatus((await probeOpenCode(OPENCODE_URL)) ? "online" : "offline");
  }, []);

  useEffect(() => {
    void check();
  }, [check]);

  // While offline, keep looking so the editor appears as soon as Start-Buddy-Coder.cmd finishes starting.
  useEffect(() => {
    if (status !== "offline") return;
    const timer = setInterval(() => {
      void probeOpenCode(OPENCODE_URL).then((up) => {
        if (up) {
          setStatus("online");
          setFrameKey((key) => key + 1);
        }
      });
    }, 3000);
    return () => clearInterval(timer);
  }, [status]);

  return (
    <section className="buddy-page buddy-coder-embed">
      <div className="buddy-coder-bar">
        <h1>Buddy Coder</h1>
        <span className={"buddy-coder-status " + status} role="status">
          {status === "online" ? "OpenCode đang chạy" : status === "checking" ? "Đang kiểm tra OpenCode…" : "OpenCode chưa chạy"}
        </span>
        <span className="buddy-coder-actions">
          <button type="button" onClick={() => { setFrameKey((key) => key + 1); void check(); }}>Tải lại</button>
          <a href={OPENCODE_URL} target="_blank" rel="noopener noreferrer">Mở tab riêng</a>
        </span>
      </div>
      {status === "offline" ? (
        <div className="buddy-panel buddy-coder-offline">
          <h2>Bật OpenCode trước</h2>
          <p>
            Trên Windows, bấm đúp <code>Start-Buddy-Coder.cmd</code> trong thư mục Buddy và để cửa sổ đó mở.
            Lần đầu nó tải OpenCode nên có thể mất vài phút.
          </p>
          <p>Buddy tự kiểm tra lại mỗi 3 giây và hiện OpenCode ngay khi sẵn sàng.</p>
        </div>
      ) : (
        <iframe
          key={frameKey}
          className="buddy-coder-frame"
          src={OPENCODE_URL}
          title="OpenCode"
          allow="clipboard-read; clipboard-write"
        />
      )}
    </section>
  );
}
