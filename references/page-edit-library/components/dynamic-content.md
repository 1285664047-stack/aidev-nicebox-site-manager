# 产品、文章、FAQ、分类与分页组件规则

修改动态内容区域时读取本文件。动态组件中的展示内容会在预览/发布时被后台数据替换，不能把预览数据固化为静态模板。

## 可修改内容与动态覆盖边界

- 可以修改：组件根节点和模板项的布局、栅格、间距、背景、边框、圆角、阴影、响应式 class；动态字段的外层标签、排列顺序和展示样式；不与动态字段重叠的静态标签、图标和说明文字。
- 可以修改但必须保留系统契约：组件根节点、模板项、字段槽位、分页/分类/附件原型的 `data-type` 层级；已有 `data-typeid`、`data-config` 未知字段、链接占位符和交互锚点。修改后必须重新诊断，不能只凭静态页面外观判断成功。
- 不能把预览值当作静态内容修改：产品/文章/FAQ/分类的名称、图片、价格、摘要、日期、正文、链接、数量、顺序、层级、当前状态和内容 ID 均来自后台数据；直接修改会在下一次编辑预览、临时预览、发布、分页、搜索或切换详情内容时被覆盖。
- 不得删除、改名或移动到错误根节点：`products/product`、`newslist/news`、`faq/faq-item`、`product_detail`、`news_detail` 及其动态字段。字段可以换布局，但必须继续处于对应组件作用域内。
- 运行时可能按真实数据数量删除多余模板项或克隆第一个模板项。模板项的静态装饰会随克隆保留，但模板中的示例名称、图片、价格、摘要和链接不具有持久业务含义。
- 无真实数据且非搜索状态时，预览处理器可能生成模拟产品、文章或 FAQ；搜索无结果时通常输出空列表。必须提示用户模拟内容仅用于展示模板，不能据此判断数据库已有真实内容。
- 用户要求直接修改动态业务内容时提示：`该内容来自后台产品、文章、FAQ 或分类数据，直接修改页面模板会在预览或发布时被覆盖。我可以调整展示样式；如需修改实际内容，应改对应内容记录。`

## data-config 通用规则

- 新增产品列表、文章列表或 FAQ 区域时，必须在对应的 `data-type="products|newslist|faq"` 根节点自动补充合法 JSON `data-config`，不能等待用户另行要求。
- 这里的“根节点”只指动态组件自身，而不是页面、section 片段或用户 selector 的外层根元素：产品配置只能写到 `[data-type="products"]`，文章配置只能写到 `[data-type="newslist"]`，FAQ 配置只能写到 `[data-type="faq"]`。即使动态组件被普通 section 包裹，也不得把 `data-config` 写到普通父节点。
- 新增区域默认关闭分页：`"showpage":"false"`。只有用户明确要求分页时才改为 `"true"`。
- `limit` 必须是大于等于 1 的整数。用户没有指定时，使用新增区域中直接模板项的数量；如果暂时无法确定模板数量，使用 `6`。
- `category_id` 可选。没有指定分类时不要生成该字段，表示全部分类；单分类使用字符串 ID，多分类使用英文逗号分隔字符串，例如 `"5784,5782"`。分类 ID 必须来自实际查询，禁止猜测。
- JSON 内部必须使用双引号。HTML 中优先用单引号包裹整个属性，例如 `data-config='{"limit":6,"showpage":"false"}'`；也可使用正确的 `&quot;` HTML 编码。禁止使用 `{'limit':6}` 这类无效 JSON。
- `modelField` 是后端内部兼容字段。页面修改或新增区域不得自行生成、删除或改变它；已有值与本次需求无关时原样保留。
- 修改现有区域时保留未知配置字段，只更新用户明确要求的 `limit`、`showpage` 或 `category_id`，不得用新对象覆盖整个配置。
- 修改前必须在当前目标范围内定位唯一动态组件。存在多个同类候选且用户没有明确指出时先让用户选择；禁止把配置同步写到所有候选组件。

## 动态组件禁止嵌套

- 动态列表根节点必须是彼此独立的顶层兄弟区域。禁止 `[data-type="products"]` 嵌套另一个 `products`，禁止 `newslist` 嵌套另一个 `newslist`，禁止 `faq` 或历史 `faqlist` 相互嵌套。
- 独立的产品、文章和 FAQ 列表之间也不得互相包裹。可以放在同一普通布局父容器中，但每个动态列表必须有独立的组件根节点和模板项链路。
- 新增统一使用 `data-type="faq"`；`faqlist` 只作为历史兼容标记识别，不创建新的 `faqlist`。
- 修改时若发现目标组件自身存在嵌套，只修复当前目标内部的嵌套；其他区域的同类问题不报告、不顺手修复。

## 产品列表

- 列表容器：`section[data-type="products"]`。
- 单项：`[data-type="product"]`，保留唯一 `data-typeid`。
- 产品字段使用 `data-type="name|img|price|icon|description|link"`。整卡跳转只能有一个有效链接，不嵌套 `<a>`。
- 运行时核心链路至少保留 `products -> product -> name/img/link`；现有模板包含价格、描述、图标时也必须保留对应字段。
- 产品分页容器使用 `data-type="product-pagination"`，不得放到产品列表之外。
- 新增示例：`data-config='{"limit":6,"showpage":"false"}'`。
- `name`、`img` 的 `src/alt`、`price`、`description`、`icon` 和 `link` 的 `href/onclick` 会由产品数据覆盖，不得作为静态业务内容编辑。卡片内未标记但被识别为站内整卡覆盖链接的 `<a>` 也可能被改写为当前产品详情地址。
- 卡片数量由真实数据和 `data-config.limit` 决定；数据不足时多余模板项会被删除，数据较多时系统会克隆首个模板项并重建动态 `data-typeid`。不要依赖模板项固定数量、固定编号或某张卡片长期对应某个产品。

## 文章列表

- 列表容器：`section[data-type="newslist"]`。
- 单项：`[data-type="news"]`，保留唯一 `data-typeid`。
- 字段使用 `data-type="img|date|title|excerpt|link"`，整卡跳转只能有一个有效链接，不嵌套 `<a>`。
- 运行时核心链路至少保留 `newslist -> news -> title/link`。图片卡片已有 `img` 时必须保留；纯文字紧凑列表可以不含 `img`，不得为了通过校验强行增加无意义图片。
- 文章分页容器使用 `data-type="news-pagination"`，不得放到文章列表之外。
- 新增示例：`data-config='{"limit":6,"showpage":"false"}'`。
- `title`、`date`、`excerpt`、`img` 的 `src/alt`、`link` 的 `href/target/onclick` 会由文章数据和文章类型覆盖。摘要可能依次来自文章简介、SEO 描述或正文截取，不能在模板中写死。
- 卡片数量由真实数据和 `data-config.limit` 决定；多余项会被删除，不足项会克隆首个模板项并重建动态 `data-typeid`。外链或附件文章的打开方式也由运行时决定。

## 详情页

详情页是由产品或文章数据在预览、发布时填充的动态模板，不是普通静态页面。页面身份由数据库页面类型和 HTML 根节点共同确定；修改时必须保持页面类型与根节点一致。根区域建议同时保留区域语义，例如 `data-section-type="product_detail" data-type="product_detail"` 或 `data-section-type="news_detail" data-type="news_detail"`。

### 产品详情

- 根节点必须保留 `data-type="product_detail"`。后端正式识别的动态字段为：
  - `cover`：产品主图，运行时使用产品图片第一张；不能作为普通静态图片替换。
  - `thumbnail`：缩略图列表容器；`thumbnail-item` 是按真实图片数量克隆的单项原型，已有结构不得删除。
  - `title`：产品名称。产品详情使用 `title`，关联产品列表才使用 `name`，两者不能混用。
  - `categoryname`：产品分类名称。
  - `price`：后端按价格和币种格式化。
  - `description`：产品简介，运行时会保留换行。
  - `content`：产品富文本正文，运行时整体替换其子节点。
  - `parameters`：产品参数富文本，运行时整体替换其子节点。
  - `prod_file_download_btn`：绑定第一个产品附件的专用下载按钮。
  - `prod_file_download_list`：完整附件列表容器。
- 产品附件列表内部标记为 `prod_file_download_item`、`prod_file_download_item_icon`、`prod_file_download_item_name`、`prod_file_download_item_url`；无附件时后端生成 `prod_file_download_empty`。历史错误拼写 `prod_file_downloaw_*` 只用于兼容旧模板，新代码必须使用 `download` 正确拼写。
- `prod_file_download_btn` 只在确实需要产品附件下载时使用。普通按钮或普通下载链接不得冒充该组件；按钮初始 `data-href` 可为空，运行时由后端填写。
- 产品详情允许把标题/图库区域与正文/参数区域拆成多个**顶层兄弟** `product_detail` 根节点，后端会逐个填充。禁止把一个 `product_detail` 嵌套到另一个根节点内；嵌套根节点会被后端跳过以避免重复替换。
- 页面可以缺少某些可选字段，但修改现有模板时不得删除已有动态字段。最低建议保留 `title`、`cover`、`description`、`content`；有多图、参数或附件能力时同时保留对应链路。
- 产品详情中的实际标题、分类、价格、简介、主图地址和正文都会被覆盖。缩略图数量、`data-image`、`src/alt`、激活/非激活边框 class 和显示状态会按真实图片重建；可以修改缩略图原型样式，不能固定某张图片或激活项。
- 附件按钮的 `data-href` 和附件列表的项目、文件名、图标、URL、数量及空状态会按真实附件重建。只能修改原型布局和样式，不能把预览附件写死。

### 文章/新闻详情

- 根节点必须保留 `data-type="news_detail"`。后端正式识别的动态字段为：
  - `title`：文章标题。
  - `publish`：格式化后的发布时间；详情页不是列表字段 `date`。
  - `author`：作者；数据为空时后端可能移除其外层显示节点。
  - `source_container`：来源整体容器；`source`：来源名称。存在 `source_url` 时运行时可生成来源链接。
  - `views`：浏览量。
  - `cover`：文章封面；不能作为普通静态图片替换。
  - `description`：文章摘要；详情页不是列表字段 `excerpt`。
  - `content`：文章富文本正文，运行时整体替换其子节点。
- 当前新闻详情处理器只填充页面中**第一个** `news_detail` 根节点。新闻详情的标题、发布时间、作者、来源、封面、摘要和正文必须放在同一个根节点内；不得像产品详情一样拆成多个顶层 `news_detail` 区域，否则后续区域不会获得动态数据。
- 若模板没有 `source_container` 但存在合适的作者结构，后端可能动态创建来源区域。修改作者和来源结构时必须保留二者的容器关系，不得只保留静态“来源”文案。
- 最低建议保留 `title`、`publish`、`content`；现有模板包含作者、来源、浏览量、封面或摘要时必须保留相应动态槽位。
- 文章详情中的标题、发布时间、作者、来源、浏览量、封面、摘要和正文都会被覆盖。作者为空时其父显示节点可能被删除；来源为空时 `source_container` 可能被删除，有来源链接时 `source` 会动态包装成链接。
- 模板缺少来源容器但存在合适作者结构时，运行时可能克隆作者结构创建 `source_container`。因此不要依赖作者/来源节点数量恒定，也不要把静态“作者：”“来源：”文案与动态字段拆散。

### 详情正文、FAQ 与关联列表

- `content` 和产品 `parameters` 是运行时富文本 HTML 槽位，不是普通文本。不得把某条预览产品或文章的数据写死，不得把固定业务组件放入这些槽位内部，因为填充时会清空原子节点。
- 产品和文章的 `faq_items` 会由后端转换为 FAQ 并追加到 `content` 末尾；模板不需要预先写死同一批 FAQ。没有 `content` 时 FAQ 才追加到详情根节点末尾。
- 相关推荐不属于详情字段，不得放进动态 `content`。关联产品继续使用 `products -> product -> link + img + name`；相关文章继续使用 `newslist -> news -> link + img + title`，并遵守本文件的 `data-config` 规则，详情页默认 `"showpage":"false"`。
- 详情链接保留系统占位符：产品使用 `[PAGE_URL@detail_page_id@pid={产品ID}@PAGE_URL]`，文章使用 `[PAGE_URL@detail_page_id@newsid={文章ID}@PAGE_URL]`；已有具体详情页 ID 形态也应原样保留。编辑态保留占位符，预览/发布时由后端解析，禁止写死预览 URL 或当前内容 ID。
- 可以修改动态槽位的外层布局、顺序、间距和样式，但不得删除、改名或把动态 `data-type` 改成静态内容。修改后必须重新诊断组件链路，确认详情根节点、动态字段、富文本槽位、附件/缩略图原型和关联列表仍有效。

## FAQ 与分类

- FAQ 容器：`[data-type="faq"]`；单项：`[data-type="faq-item"]`；问题与答案分别为 `question`、`answer`。FAQ 不生成详情链接。
- 新增 FAQ 根节点同样必须包含 `data-config`，默认示例为 `data-config='{"limit":4,"showpage":"false"}'`。
- 产品分类容器：`section/aside[data-type="category-list"][data-category="product"]`；分类项为 `category-item`，保留 `itemid`、层级结构、展开控件和交互。
- 只补充缺失标记，不随意改写已有 `data-type` 的含义。
- FAQ 的问题、答案、项目数量和克隆后的 `data-typeid` 会被覆盖；`faq-open`、`aria-expanded` 和答案节点的 `hidden` 状态也会被运行时同步，通常第一项展开、其余项收起。可以修改手风琴结构、图标和动画样式，不能固定某条业务问答或展开状态。
- 分类列表运行时会以首个分类项为样式模板，删除原分类项、清空分类导航容器，再根据数据库分类树生成名称、链接、层级、`itemid` 和 `data-typeid`。只能修改分类容器和首个模板项样式，不能静态修改分类业务内容、数量、顺序、ID 或层级。
- 分类容器内脚本不是普通静态内容。现有处理器只会有条件保留其识别的分类展开脚本；不要在分类容器内增加无关业务脚本，也不要依赖某个运行时分类节点绑定的独立监听器。

## 分页覆盖规则

- 分页是运行时管理结构。每次处理列表时，系统会先删除现有 `.pagination-container`、`.pagination`、`.page-navigation`、`.page-nav`、`product-pagination` 和 `news-pagination`，再按真实总数、当前页和 `limit` 决定是否重建。
- 可以修改 `data-config.limit` 和 `showpage`，也可以修改由系统支持的分页模板样式；不能直接修改页码、当前状态、上一页/下一页文本与链接、按钮数量或把静态内容放进分页容器，这些都会被删除或覆盖。
- 用户要求修改页码或分页链接时提示：`分页由真实数据总数、每页数量和当前页动态生成，直接修改页面中的页码或链接不会保留。我可以调整每页数量、是否分页或分页外观。`

## 重复项增删

- 按目标父容器的直接子节点和 DOM 顺序定位，不以 id 中的数字作为顺序。
- 只增删指定数量；保留其余项目的顺序、标识、文案、图片、链接、class、style 和内部结构。不得为了编号连续而重编号。
- 新项目复用一个相邻项目的完整结构，但必须生成未占用且互不重复的标识。
- 同步静态圆点、Tab、缩略图等一一对应的控制项；动态生成的控制项不手工复制。
- 修改完成后重新诊断组件链路，存在缺失、重复 ID、嵌套链接或字段错位时不能进入预览。
