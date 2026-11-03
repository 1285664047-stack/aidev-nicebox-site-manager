---
name: page-code-validate
description: Draft and deterministically validate Nicebox page code changes without saving
metadata: {"clawdbot":{"emoji":"[EDIT]"}}
---

# 页面修改草稿与校验

本阶段由宿主 AI/WorkBuddy 在对话上下文中修改代码，Nicebox 只执行确定性校验。校验通过仍然没有保存、预览写入或发布。

## 流程

1. 按 `page_code_read.skill.md` 选定页面并依次读取 metadata 和 sections/full。
2. 明确目标区域和用户要求，只修改 `target_selector` 对应区域；复杂跨区域任务才使用 `target_type=full`。
3. 修改前排除共享 Header/Footer 和系统保护节点。业务样式优先使用 Tailwind class。
4. 新图片先调用 `nicebox_upload_images`，只能把返回的稳定 `image_url` 写入草稿。
5. 生成完整 `after_html` 后展示修改摘要，调用 `nicebox_validate_page_change`。传入读取时的页面版本、Hash 和规则版本，不得用预览 HTML 作为 `before_html`。
6. 校验失败时根据结构化 errors 修正草稿并重新校验；不能绕过错误。校验通过时说明“尚未保存”。
7. MCP 不可用时使用普通 API 同名回退；业务校验失败不是网络失败，不得通过回退绕过。

## 宽度专用流程

页面宽度不能通过 after_html 修改。先读取 `nicebox_get_page_width_settings`，取得用户确认的桌面端/移动端宽度后调用 `nicebox_preview_page_width_settings`。该工具也只生成预览数据，不保存。

## 强制规则

- 不修改 `tailwind.config`、全站主题、全站字体、`systemDefaultStyle260918` 或 `disableJumpScript`。
- 不直接编辑 `contentWidthSettings` 或 `contentMobileWidthSettings`。
- 非必要不新增 `<style>`、行内 `style` 或外部 CSS；确需局部 CSS 时提供原因和范围，禁止全局标签或通配选择器。
- 不删除动态组件必需的 `data-type` 链路，不把具体产品/文章预览数据固化到模板。
- 不新增危险脚本、危险 URL、外部表单提交或未知外部脚本。
- 本阶段不调用页面保存、页面预览写入、回退或发布工具。

详细规则见 `../references/page-code-validation-rules.md`，提示词见 `../prompts/page-edit-draft.md`。
