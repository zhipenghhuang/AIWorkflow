import { test, expect } from "@playwright/test";
import { shot, assertNoHorizontalScroll } from "./helpers";

// 模板：三视口截图 + 无意外横向滚动。项目已有 viewport 项目时可直接用 project.name。
test.describe("responsive", () => {
  test.skip(!process.env.APP_READY, "set APP_READY=1 after adapting pages");

  for (const pagePath of ["/"]) {
    test(`responsive ${pagePath}`, async ({ page }, testInfo) => {
      await page.goto(pagePath);
      await expect(page.locator("body")).toBeVisible();
      await assertNoHorizontalScroll(page);
      await shot(page, `responsive-${testInfo.project.name}-${pagePath.replace(/\W+/g, "_")}`, testInfo);
    });
  }
});
