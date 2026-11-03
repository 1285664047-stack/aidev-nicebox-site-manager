# 页面结构、样式与系统保护规则

修改页面代码时读取本文件。它只约束页面修改，不用于从零生成整站。

## 修改边界

- 代码由 WorkBuddy/当前宿主在对话上下文中修改；Nicebox MCP 或普通 API 只负责读取、诊断、校验、预览和保存。
- `sections` 只用于定位，提交校验的 `before_html` 必须是本次 `full` 返回的完整原文，`after_html` 必须是只替换目标范围后的完整文档。
- 只修改用户指定范围。保留未点名的标签层级、文本、属性、图片、链接、交互和响应式行为。
- 删除 `data-*` 属性不等于删除元素。仅删除指定属性，并保持修改前后的标签名称和顺序一致。
- 普通页面修改不得改共享 Header/Footer；共享头尾必须走专用流程。不能修改 `tailwind.config`、全站主题色、全站字体或站点级 `html_config`。

## Section 与容器

- 每个业务 `section` 保留或补充准确的 `data-section-type`。标题区域单独使用 `title`，内容区域使用实际类型；不要把标题与内容强行合并到一个 section。
- Header/Footer 不拆成标题区与内容区。常用类型包括 `banner`、`image_text`、`about`、`company_culture`、`develop_course`、`group_show`、`contact_us`、`common_problem`、`counter`、`param_table`、`option_switch`、`prod_list`、`news_list`、`product_detail`、`news_detail`、`message_form`。
- 内容宽度沿用 `max-header-container`、`max-content-container`、`max-footer-container`。桌面/移动宽度只能通过专用宽度工具修改，不能直接改写宽度 Style。

## 样式与响应式

- 优先使用现有 Tailwind CSS class。非必要不新增 `<style>`、行内 `style` 或外部 CSS。
- 如 Tailwind 无法合理表达且确有必要，新增样式必须限制在目标区域，说明原因和选择器，不得使用污染全站的标签级或通配选择器。
- 保留现有旧 CSS；不要顺手清理、格式化或改写与需求无关的样式。
- 新增响应式样式只使用无前缀的移动端基础类与 `md:` 桌面端覆盖类，并保持现有页面的响应式语义。不要把生成阶段的严格布局偏好机械用于旧页面重构。
- 图片和视频保持 `object-cover` 等既有适配规则。修改图片容器背景不等于替换图片；只有用户明确要求并提供或生成新图片时才能更换 `src`。

## 不可修改的系统节点

以下节点内容、顺序和语义必须原样保护，不得格式化、替换或 Tailwind 化：

- `<script>` 中的 `tailwind.config`
- `<style id="systemDefaultStyle260918">`
- `<script id="disableJumpScript">`

以下节点不能删除或转换为 Tailwind，只能由专用宽度流程根据宽度字段受控重建：

- `<style id="contentWidthSettings">`
- `<style id="contentMobileWidthSettings">`

新增图片必须先使用上传图片能力进入当前账号云素材库，只把返回的稳定 `image_url` 写入草稿。禁止本地路径、`blob:`、Base64、临时附件地址和短期签名地址。
