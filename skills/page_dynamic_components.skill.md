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
- 文章：`newslist -> news -> link + title`；图片卡片保留 `img`，纯文字紧凑列表允许无图，并保留已有日期、摘要和分页结构。
- FAQ：`faq -> faq-item -> question + answer`，保留展开收起交互。
- 分类：`category-list[data-category=product|news] -> category-item[itemid]`。
- 搜索：保留合法 `data-config`、`search-input`、`search-btn`；multi 模式必须有 `search-select`，不能用 form 包裹或新增搜索 JS。
- 表单：`data-type=form` 只能在 form 标签；内部必须有 `data-type=title` 的非空标题、至少一个带 `data-itemid/date-element` 的 `form-item`，控件必须有唯一 name，并且只能有一个 `type=submit data-type=submit data-href=form-submit` 按钮。新增表单不自行生成 `data-sign`，已有表单必须原样保留 `data-sign`，不新增表单 JS。
- 产品详情：读取规则库中的正式字段，保留 `product_detail` 根节点以及已有的 `cover/thumbnail/thumbnail-item/title/categoryname/price/description/content/parameters` 和附件链路。允许多个顶层兄弟 `product_detail` 区域，禁止相互嵌套。
- 文章详情：保留第一个 `news_detail` 根节点内已有的 `title/publish/author/source_container/source/views/cover/description/content`。当前后端只填充第一个根节点，不得把标题和正文拆成多个顶层 `news_detail` 区域。
- 详情正文和参数是运行时富文本槽位，FAQ 会由后端追加；不能把某条预览数据、内容 ID 或预览地址固化进模板。关联列表必须留在 `content` 外并继续使用标准产品/文章列表链路。

表单确认保存时服务端扫描完整页面表单，提取标题、字段、按钮和验证规则，按 `data-sign` 创建或更新 `forms`，并把新签名回填页面 HTML。草稿与临时预览不创建表单。组件草稿通过后仍执行 `validate -> preview -> 用户确认 -> commit`，保存不等于发布；保存后以服务端最终页面版本为准。
