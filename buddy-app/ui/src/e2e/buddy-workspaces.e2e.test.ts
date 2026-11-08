import { writeFile } from "node:fs/promises";
import path from "node:path";
import { expect, it } from "vitest";
import { createControlUiE2eArtifactDir } from "../test-helpers/control-ui-e2e-artifacts.ts";
import { takeControlUiViewportScreenshot } from "../test-helpers/control-ui-e2e-screenshot.ts";
import {
  installMockGateway,
  waitForControlUiRoute,
} from "../test-helpers/control-ui-e2e.ts";
import { createControlUiE2eSuite } from "./control-ui-e2e-suite.test-support.ts";

const suite = createControlUiE2eSuite({ name: "Buddy workspace routes" });

suite.define(() => {
  it("links to native OpenCode and keeps sample log analysis local in Security", () =>
    suite.withPage({ viewport: { width: 1280, height: 800 }, locale: "en-US" }, async ({ page }) => {
      const proofDir = process.env.OPENCLAW_CAPTURE_UI_PROOF === "1"
        ? createControlUiE2eArtifactDir("buddy-workspaces")
        : undefined;
      await installMockGateway(page);
      await page.goto(suite.server.baseUrl + "buddy/coder");
      await waitForControlUiRoute(page, { pathname: "/buddy/coder", routeId: "buddy-coder" });
      const workspace = page.locator(".buddy-route-host");
      const coderHeading = workspace.getByRole("heading", { name: "Buddy Coder", exact: true });
      await coderHeading.waitFor();
      const coderLink = workspace.getByRole("link", { name: "Mở Buddy Coder trong tab mới" });
      await expect.poll(() => coderLink.getAttribute("href")).toBe("http://127.0.0.1:4096/");
      expect(await coderLink.getAttribute("target")).toBe("_blank");
      expect(await page.title()).toContain("Buddy");
      if (proofDir) {
        await writeFile(path.join(proofDir, "coder.png"), await takeControlUiViewportScreenshot(page, workspace, [coderHeading, coderLink]));
      }

      await page.goto(suite.server.baseUrl + "buddy/security");
      await waitForControlUiRoute(page, { pathname: "/buddy/security", routeId: "buddy-security" });
      await workspace.getByRole("button", { name: "Cyber Security" }).click();
      await workspace.getByRole("button", { name: "Dùng log mẫu" }).click();
      await workspace.getByRole("button", { name: "Phân tích", exact: true }).click();
      const finding = workspace.getByText("Nhật ký kiểm toán bị xóa", { exact: false });
      await finding.waitFor();
      if (proofDir) {
        await finding.scrollIntoViewIfNeeded();
        await writeFile(path.join(proofDir, "security.png"), await takeControlUiViewportScreenshot(page, workspace, [finding]));
      }
    }),
  );
});
