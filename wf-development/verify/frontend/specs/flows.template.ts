import { expect, Page, Route, test } from "@playwright/test";

/**
 * 交互流用例模板（复制到 specs/flows/<页面>.spec.ts 后按项目改）。
 *
 * 标题必须是：[FLOW:<flow-id>][T:<transition>] 或 [FLOW:<flow-id>][I:<invariant>]，并带 [CASE:<case-id>]。
 * 例：test("[FLOW:user-delete][T:T2][CASE:user-delete-cancel] cancel closes without request", ...)
 *
 * 一级证据：用 page.route mock 成功/失败/延迟，断言状态迁移与副作用。
 * 二级证据：另写一条不打 mock 的真实入口 happy path（可在 e2e 主链跑）。
 * 禁止 test.skip；未适配时先删模板或改成真实断言，不得留 skip 过门。
 */

const API = "**/api/users/**";

async function mockDelete(page: Page, mode: "ok" | "fail" | "slow") {
  await page.route(API, async (route: Route) => {
    if (route.request().method() !== "DELETE") return route.continue();
    if (mode === "fail") {
      return route.fulfill({ status: 500, body: JSON.stringify({ message: "boom" }) });
    }
    if (mode === "slow") {
      await new Promise((r) => setTimeout(r, 800));
    }
    return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }) });
  });
}

test.describe("user-delete flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/users");
    // 项目按真实入口调整；ready 用页面标题/数据行，不用全文包含。
    await expect(page.getByRole("heading", { name: /用户/ })).toBeVisible();
  });

  test("[FLOW:user-delete][T:T2][CASE:user-delete-cancel] cancel/esc/overlay closes without write", async ({ page }) => {
    await mockDelete(page, "ok");
    let writes = 0;
    page.on("request", (req) => {
      if (req.method() === "DELETE") writes += 1;
    });
    await page.getByRole("button", { name: "删除" }).first().click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await page.getByRole("button", { name: "取消" }).click();
    await expect(page.getByRole("dialog")).toBeHidden();
    expect(writes).toBe(0);
    // 重开必须重置：再开一次，错误/输入不应残留
    await page.getByRole("button", { name: "删除" }).first().click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await expect(page.getByText(/上次错误/)).toHaveCount(0);
  });

  test("[FLOW:user-delete][T:T3][CASE:user-delete-double] confirm submits once", async ({ page }) => {
    await mockDelete(page, "slow");
    let writes = 0;
    page.on("request", (req) => {
      if (req.method() === "DELETE") writes += 1;
    });
    await page.getByRole("button", { name: "删除" }).first().click();
    const ok = page.getByRole("button", { name: /确认|删除/ }).last();
    await ok.click();
    await expect(ok).toBeDisabled();
    await ok.click({ force: true }).catch(() => {});
    await expect(page.getByRole("dialog")).toBeHidden();
    expect(writes).toBe(1);
  });

  test("[FLOW:user-delete][T:T5][CASE:user-delete-fail] failure keeps dialog open", async ({ page }) => {
    await mockDelete(page, "fail");
    await page.getByRole("button", { name: "删除" }).first().click();
    await page.getByRole("button", { name: /确认|删除/ }).last().click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await expect(page.getByText(/失败|错误/)).toBeVisible();
  });
});
