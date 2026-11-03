import { defineConfig, devices } from "@playwright/test";

// 复制到项目根或 tests/ 下，按项目改 baseURL / webServer / 路径。
// 证据统一落项目根 .gate/frontend/（规范包只读，不写运行态）。
// 默认不生成 HTML report / trace / video，避免一次试跑产生大量验证数据；
// 需要排障时再临时打开 trace/video。
export default defineConfig({
  testDir: "./specs",
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  retries: 0,
  reporter: [["list"], ["json", { outputFile: ".gate/frontend/playwright-results.json" }]],
  outputDir: ".gate/frontend/test-results",
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3000",
    trace: "off",
    screenshot: "only-on-failure",
    video: "off",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 } } },
    { name: "tablet", use: { ...devices["Desktop Chrome"], viewport: { width: 768, height: 1024 } } },
    { name: "mobile", use: { ...devices["Desktop Chrome"], viewport: { width: 360, height: 800 } } },
  ],
});
