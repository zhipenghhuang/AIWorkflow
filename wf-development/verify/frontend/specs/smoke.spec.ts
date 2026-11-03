import { test, expect } from "@playwright/test";
import { trackDiagnostics, assertNoDiagnostics, shot, assertNoHorizontalScroll } from "./helpers";

// 模板：按项目改路径/断言。APP_READY=1 才跑，避免未适配时误报。
test.describe("smoke", () => {
  test.skip(!process.env.APP_READY, "set APP_READY=1 after adapting baseURL/selectors");

  test("main path + console/network clean", async ({ page }, testInfo) => {
    const diag = trackDiagnostics(page);
    await page.goto("/");
    await expect(page.locator("body")).toBeVisible();
    await assertNoHorizontalScroll(page);
    await shot(page, `smoke-${testInfo.project.name}`, testInfo);
    assertNoDiagnostics(diag);
  });
});
