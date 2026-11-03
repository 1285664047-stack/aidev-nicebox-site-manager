# 表单、搜索、链接与资源规则

## 表单

- 只有 `<form>` 可标记 `data-type="form"`，并保留唯一 `data-itemid`。
- 表单项容器使用 `data-type="form-item"`、唯一 `data-itemid` 和正确的字段类型标记；输入控件必须保留 `name`。
- 常用字段标记：`label`、`input`、`text`、`radio`、`checkbox`、`date`、`select`、`option`、`textarea`、`file-upload`、`help-text`、`validation`、`hidden`。
- 提交按钮保留 `type="submit" data-type="submit" data-href="form-submit"`；重置按钮保留 `type="reset" data-type="reset" data-href="form-reset"`。
- 不新增表单提交 JS、外部 action 或自定义网络请求；系统运行时会接管提交。修改字段后检查 label、name、选项组和验证提示仍一一对应。

## 站内搜索

- 搜索根节点使用 `data-type="searchbox"`、唯一 `data-typeid` 和可解析的 `data-config` JSON。
- 输入框：`input[type="text"][data-type="search-input"]`，不设置 `name`。
- 按钮：`button[type="button"][data-type="search-btn"]`。多类型搜索可使用 `select[data-type="search-select"]`，option 下标与 `data-config.items` 顺序一致。
- 搜索框不得用 `<form>` 包裹，不添加 action/method/onsubmit，不新增搜索跳转 JS。
- `data-config` 的 `type` 只使用运行时支持的 `products` 或 `newslist`；页面 ID 和目标参数沿用系统返回值，不猜测。

## 链接占位符

- 保留系统占位链接及 `href`/`data-href` 配对，例如 `[PAGE_URL@...@PAGE_URL]`；不要提前转换为当前预览 URL 或线上绝对地址。
- 保留 `data-link-type`（如 `productCategory`）和运行时所需的页面/分类/内容标识。
- 新增内部链接时先通过页面或内容查询取得真实 ID，再按现有同类链接格式生成；不能猜测页面 ID。
- 禁止 `javascript:` 等危险协议、未知外部脚本链接和会绕过系统路由的 onclick 跳转。
- “查看更多”按钮继续使用组件规定的 `data-type="link"` 与 `data-href`，不能抢占单项卡片的整卡链接。

## 图片与二维码

- 新图片先调用图片上传能力，并使用返回的稳定 `image_url`。
- 可从 alt、title、data-description、周边文字或区块语义判断为二维码的现有图片，默认完整保留原始 `src`；只有用户明确要求修改二维码本身时才处理。
- 不能用 CSS 滤镜、遮罩或背景色假装修改位图像素。需要去底、重绘或生成图片时应走图片能力，再由用户确认替换。
