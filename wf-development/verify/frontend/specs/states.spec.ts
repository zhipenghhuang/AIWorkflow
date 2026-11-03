import { test, expect } from "@playwright/test";
import { shot } from "./helpers";

// 模板：为受影响页面补状态断言/截图。每个状态至少一张截图。
// 常见做法：用路由 mock / 测试账号 / 后端开关制造状态。
test.describe("states", () => {
  test.skip(!process.env.APP_READY, "set APP_READY=1 after adapting states");

  const states = ["loading", "empty", "error", "permission"] as const;

  for (const state of states) {
    test(`state: ${state}`, async ({ page }, testInfo) => {
      // TODO: 按项目构造该状态；不要只截默认页。
      await page.goto("/");
      await expect(page.locator("body")).toBeVisible();
      await shot(page, `state-${state}-${testInfo.project.name}`, testInfo);
    });
  }
});
