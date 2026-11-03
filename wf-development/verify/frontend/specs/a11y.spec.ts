import { test, expect } from "@playwright/test";

// 模板：安装 @axe-core/playwright 后启用；AXE_READY=1 才跑。
test.describe("a11y", () => {
  test.skip(!process.env.AXE_READY, "install @axe-core/playwright and set AXE_READY=1");

  test("no WCAG A/AA violations on key page", async ({ page }) => {
    // @ts-ignore optional dependency
    const { AxeBuilder } = await import("@axe-core/playwright");
    await page.goto("/");
    await expect(page.locator("body")).toBeVisible();
    const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    if (results.violations.length) {
      throw new Error(
        results.violations
          .map((v: any) => `${v.id}: ${v.help} (${v.nodes.length} node(s))`)
          .join("\n"),
      );
    }
  });
});
