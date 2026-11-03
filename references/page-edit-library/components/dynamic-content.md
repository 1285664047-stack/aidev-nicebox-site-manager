# 产品、文章、FAQ、分类与分页组件规则

修改动态内容区域时读取本文件。动态组件中的展示内容会在预览/发布时被后台数据替换，不能把预览数据固化为静态模板。

## 产品列表

- 列表容器：`section[data-type="products"]`。
- 单项：`[data-type="product"]`，保留唯一 `data-typeid`。
- 产品字段使用 `data-type="name|img|price|icon|description|link"`。整卡跳转只能有一个有效链接，不嵌套 `<a>`。
- 运行时核心链路至少保留 `products -> product -> name/img/link`；现有模板包含价格、描述、图标时也必须保留对应字段。
- 产品分页容器使用 `data-type="product-pagination"`，不得放到产品列表之外。

## 文章列表

- 列表容器：`section[data-type="newslist"]`。
- 单项：`[data-type="news"]`，保留唯一 `data-typeid`。
- 字段使用 `data-type="img|date|title|excerpt|link"`，整卡跳转只能有一个有效链接，不嵌套 `<a>`。
- 运行时核心链路至少保留 `newslist -> news -> title/img/link`。
- 文章分页容器使用 `data-type="news-pagination"`，不得放到文章列表之外。

## 详情页

- 产品详情根节点保留 `data-type="product_detail"`，字段按现有模板保留 `name`、`price`、`img`、`description`、`content`、参数、缩略图和附件等标记。
- 文章详情根节点保留 `data-type="news_detail"`，字段按现有模板保留 `title`、`date`、`img`、`excerpt`、`content` 等标记。
- 不把相关推荐列表与详情根节点混淆；相关推荐继续使用 `products/product` 或 `newslist/news` 链路。
- 产品附件下载专用标记 `prod_file_download_*` 只在系统明确要求时使用，普通下载按钮不得冒充产品附件组件。

## FAQ 与分类

- FAQ 容器：`[data-type="faq"]`；单项：`[data-type="faq-item"]`；问题与答案分别为 `question`、`answer`。FAQ 不生成详情链接。
- 产品分类容器：`section/aside[data-type="category-list"][data-category="product"]`；分类项为 `category-item`，保留 `itemid`、层级结构、展开控件和交互。
- 只补充缺失标记，不随意改写已有 `data-type` 的含义。

## 重复项增删

- 按目标父容器的直接子节点和 DOM 顺序定位，不以 id 中的数字作为顺序。
- 只增删指定数量；保留其余项目的顺序、标识、文案、图片、链接、class、style 和内部结构。不得为了编号连续而重编号。
- 新项目复用一个相邻项目的完整结构，但必须生成未占用且互不重复的标识。
- 同步静态圆点、Tab、缩略图等一一对应的控制项；动态生成的控制项不手工复制。
- 修改完成后重新诊断组件链路，存在缺失、重复 ID、嵌套链接或字段错位时不能进入预览。
