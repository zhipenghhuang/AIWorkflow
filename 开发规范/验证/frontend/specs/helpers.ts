import { Page, TestInfo } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

// 运行态证据落项目根 .gate/，规范包 验证/ 只读。
export const evidenceDir = path.resolve(process.cwd(), ".gate/frontend");

export function ensureEvidenceDir(): void {
  fs.mkdirSync(evidenceDir, { recursive: true });
}

export type Diagnostics = {
  consoleErrors: string[];
  pageErrors: string[];
  failedRequests: string[];
};

export function trackDiagnostics(page: Page): Diagnostics {
  const diag: Diagnostics = { consoleErrors: [], pageErrors: [], failedRequests: [] };
  page.on("console", (msg) => {
    if (msg.type() === "error") diag.consoleErrors.push(msg.text());
  });
  page.on("pageerror", (err) => diag.pageErrors.push(String(err)));
  page.on("requestfailed", (req) => {
    const failure = req.failure();
    diag.failedRequests.push(`${req.method()} ${req.url()} :: ${failure?.errorText || "failed"}`);
  });
  return diag;
}

export async function shot(page: Page, name: string, testInfo?: TestInfo): Promise<void> {
  ensureEvidenceDir();
  const file = path.join(evidenceDir, `${name}.jpg`);
  await page.screenshot({ path: file, type: "jpeg", quality: 70, fullPage: true });
  // 不再 attach 到 HTML report（会复制一份图片，放大验证数据）；文件本身就是证据。
}

export function assertNoDiagnostics(diag: Diagnostics): void {
  if (diag.consoleErrors.length) throw new Error(`console errors:\n${diag.consoleErrors.join("\n")}`);
  if (diag.pageErrors.length) throw new Error(`page errors:\n${diag.pageErrors.join("\n")}`);
  if (diag.failedRequests.length) throw new Error(`failed requests:\n${diag.failedRequests.join("\n")}`);
}

export function assertNoHorizontalScroll(page: Page): Promise<void> {
  return page.evaluate(() => {
    const doc = document.documentElement;
    if (doc.scrollWidth > doc.clientWidth + 1) {
      throw new Error(`horizontal scroll: scrollWidth=${doc.scrollWidth} clientWidth=${doc.clientWidth}`);
    }
  });
}
