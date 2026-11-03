# 动态组件与复杂页面修改

修改产品、文章、FAQ、分类、搜索、分页、详情模板或表单前，必须先调用 `nicebox_diagnose_page_components`。MCP 不可用时使用：

```bash
python scripts/api_tool.py nicebox_diagnose_page_components --args-json '{"page_id":123,"target_selector":"#target"}'
```

## 诊断结果

- `errors`：必须修复后才能校验草稿，不能删除动态字段来规避。
- `components`：展示组件类型、选择器、模板项数量和有效性。
- `scripts[].ownership=local`：仅当属于当前目标区域时才可随区域修改。
- `shared`：同时服务多个区域，提供上下文但原样保留。
- `unknown`：无法可靠确认归属，原样保留。
- `other`：明确属于其他区域，不纳入当前修改。

## 组件硬规则

- 产品：`products -> product -> link + img + name/title`，单项只能有一个链接，不能写死产品 ID。
- 文章：`newslist -> news -> link + img + title`，保留日期、摘要和分页结构。
- FAQ：`faq -> faq-item -> question + answer`，保留展开收起交互。
- 分类：`category-list[data-category=product|news] -> category-item[itemid]`。
- 搜索：保留合法 `data-config`、`search-input`、`search-btn`；multi 模式必须有 `search-select`，不能用 form 包裹或新增搜索 JS。
- 表单：`data-type=form` 只能在 form 标签；保留 `data-itemid/data-sign`，字段必须有 name；提交按钮必须是 `type=submit data-href=form-submit`，不新增表单 JS。
- 产品/文章详情：保留动态标题和 `content`，不能把某条预览数据固化进模板。

表单确认保存时服务端会同步表单关联表并把新 `data-sign` 回填页面 HTML。组件草稿通过后仍执行 `validate -> preview -> 用户确认 -> commit`，保存不等于发布。
