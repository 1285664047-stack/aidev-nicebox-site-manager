---
name: create-page
description: Analyze, preview, and create a new Nicebox page without publishing the website
---

# 新增页面流程

1. 调用 `nicebox_analyze_page_creation`，同时判断页面结构 `page_type` 和业务角色 `element_type`。不得只按名称猜一种类型。
2. 规范组合：普通/关于/联系/详情模板使用 `page`；产品/文章列表使用 `list`；外链使用 `link + normal`。FAQ 使用 `page + normal` 和 FAQ 动态组件。
3. 分析结果存在同名或同类型页面时，展示现有页面并让用户选择修改现有页面或仍新增。只有用户明确选择仍新增，草稿请求才传 `allow_duplicate=true`。
4. 用户没有正文需求时直接创建草稿。服务端先匹配同语言首页的紧邻标题区与内容区；匹配不到时自动根据首页风格、公司真实资料和对应动态组件生成，不要求用户再次授权。
5. 用户有明确文案、图片或布局需求时，生成的 `content_html` 只能包含正文 `section`，不能包含 `html/head/body/header/footer`。图片必须是已经上传云资源库后返回的地址。
6. Header/Footer 始终使用当前语言共享内容，不允许生成或重写。
7. 调用 `nicebox_create_page_draft` 后展示页面类别、内容来源、区域摘要和 `preview_url`。此时页面尚未创建，也未发布。
8. 只有用户查看当前预览并明确确认后，才调用 `nicebox_commit_page_creation`，传新的 `operation_id` 和 `confirmed=true`。
9. 写入响应不明确时使用同一 `operation_id` 查询 `nicebox_get_page_creation_operation`，禁止重复提交。
10. 用户要求调整时重新生成草稿；用户放弃时调用 `nicebox_abandon_page_creation_draft`。
11. 创建成功只说明“页面已创建、尚未发布”。只有用户另行要求网站上线时才进入整站发布流程。

工具顺序：`nicebox_analyze_page_creation` -> `nicebox_create_page_draft` -> `nicebox_get_page_creation_draft`（恢复或复查时） -> `nicebox_commit_page_creation`。放弃使用 `nicebox_abandon_page_creation_draft`，提交结果不明确时使用 `nicebox_get_page_creation_operation`。

禁止使用旧 `createBlankPage` 代替本流程，避免正文失败后留下空页面。
