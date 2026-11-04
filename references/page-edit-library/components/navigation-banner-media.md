# 导航、Header、轮播与媒体规则

## 共享 Header、Footer 与导航

- Header/Footer 是站点共享内容，不能作为普通页面 section 保存。修改它们必须明确影响所有页面，并走共享头尾专用读写、预览和回退流程。
- 页面编辑、预览、保存和历史回退时使用当前共享头尾覆盖页面副本；回退页面正文不能回退共享头尾。
- 页面只有一个 `<header>` 和一个 `<footer>`；二者内部及祖先链不嵌套业务 `<section>`。
- PC 导航容器为 `nav[data-type="navs"]`，通常使用 `data-typeid="pc-navs-1"`；移动导航容器为 `#mobile-menu.mobile-menu[data-type="navs"]`，通常使用 `data-typeid="mobile-navs-1"`。保留 `.header-pc-cont`、`.header-mobile-cont` 和 `.max-header-container`；移动端开关通常保留 `.menu-toggle`。
- PC 与移动端各至少保留一个普通状态的 `a[data-type="nav"]` 作为系统克隆模板。导航项保留 `data-type="nav"`、`data-nav-level="1"`、`href` 和 `data-href`；模板可保留唯一 `data-typeid`，但运行时生成的 `pc-nav-*`、`mobile-nav-*` 不能写死。普通模板项不要默认带 `font-bold` 或当前页高亮样式。
- Header 末尾的局部交互脚本应使用 `document.currentScript.closest('header')` 或等价方式取得当前 Header，并在 Header 范围内查询元素。不要把 Header 脚本放入会被重建的导航项，也不要在普通页面正文复制导航监听器。
- Header 相关交互必须跟随共享 Header 保存；不要在普通页面正文复制一份导航监听器。

### 可修改内容与动态所有权

- 可修改并保存到共享 Header：整体布局、背景、边框、阴影、高度、响应式间距；Logo 的尺寸和位置；导航模板项的字体、颜色、间距和 hover class；静态电话、图标、咨询按钮；搜索弹窗外观；汉堡按钮外观和移动菜单动画。
- 可以修改结构或样式但必须保留语义标记：`[data-type="logo"]`、`[data-type="navs"]`、`[data-type="nav"]`、语言切换器、搜索组件及其现有 JS 依赖类名。Logo 图片地址或企业名称优先通过 Logo/企业资料能力修改，直接改 `src` 或文字可能被后续生成覆盖。
- 不得把运行时值当作静态内容修改：导航名称、链接、数量、顺序和层级来自站点页面数据；语言名称和链接来自站点语言配置；二级/三级菜单以及当前页状态由系统重建。需要改变这些业务数据时，改对应页面、排序、层级或语言配置，不硬改 Header HTML。
- 不得写死或依赖运行时标记：`data-page-id`、`data-sub-page-id`、`data-third-page-id`、`pc-nav-*`、动态 `mobile-nav-*`、`#nav-level-2`、`#nav-level-3`、`cur-nav`、`cur-sub-nav`、`cur-third-nav` 以及系统生成的移动端 checkbox id。手写的二/三级菜单外壳会在运行时被删除并重建。
- 语言切换器保留 `data-type="language"`、`data-type="curLanguage"`、`data-type="language-item"`；搜索功能保留 `data-type="searchbox"`、`search-input`、`search-select`、`search-btn`、`data-config` 以及现有弹窗脚本依赖的 class。只修改样式，不伪造动态语言项、搜索配置或结果。
- 前端编辑器禁止直接修改 `[data-type="navs"]` 内 `[data-type="nav"]` 的文字和链接。遇到这类要求时提示：`导航名称、链接、顺序和层级由站点页面数据生成，直接修改 Header 会在预览或发布时被覆盖；请改对应页面或导航配置。`

### 移动端导航定向样式规则

当用户明确要求生成或修改移动端导航，或要求修复移动菜单纵向排列时，只能在当前 Header 的移动导航根容器 `#mobile-menu` 或 `[data-typeid^="mobile-navs-"]` 内操作：

1. 遍历根容器内所有 `a[data-type="nav"]` 和 `.mobile-nav-item`。对每个匹配项的直接父元素追加 `flex flex-col w-full`，只追加缺失 class，不删除或重排原 class。
2. 对每个匹配项自身追加 `block`，只追加缺失 class。`a[data-type="nav"]` 是源模板时，该 class 会传递到系统克隆的一级导航；`.mobile-nav-item` 是运行时多级菜单外壳时，只允许补充该样式，不修改其动态子节点、checkbox、label、链接或 ID。
3. 选择器必须先受移动导航根容器约束，禁止全局修改所有 `[data-type="nav"]` 或 `.mobile-nav-item`。不得改电脑端 `pc-navs-1`、Logo、按钮、搜索、语言、Header 高度、静态 CTA、导航文字、链接、顺序、层级、JS 或任何非移动端导航内容。
4. 修改后确定性校验：移动根容器之外的 HTML 保持不变；每个匹配项直接父元素都包含 `flex flex-col w-full`；每个匹配项自身都包含 `block`；原有 `data-*`、`id`、`href`、`data-href` 和其他 class 完整保留。
5. 如果完整原文中还没有运行时生成的 `.mobile-nav-item`，不得伪造该动态结构；只给移动端 `a[data-type="nav"]` 模板及其直接父元素补 class，并在结果中说明多级外壳将在预览/发布时由系统生成。若运行时再次生成后覆盖手工 class，则应修改导航处理器或其样式规则，不能反复写回渲染结果冒充持久修改。

移动端定向修改前提示：`本次只调整移动端导航的纵向布局 class，不会修改电脑端导航、Logo、按钮、文字、链接、顺序、层级或其他 Header 内容。` 修改后提示：`已为移动端导航项补充 block，并为其直接父容器补充 flex flex-col w-full；其他 Header 内容保持不变。`

## Banner

- 根节点为 `[data-type="banner"]`，单项为顶层 `[data-type="banner-item"]`；字段使用 `title`、`description`、`img`、`link`。
- 图片使用 `<img>`，不得把业务图片只写进 `background-image`。
- 增加轮播项时只插入一个相邻结构副本，新项默认非激活；原有项、激活状态、标识和顺序不变。
- 删除后确保剩余第一项及静态控制项成为唯一激活项；只删除对应的静态圆点/Tab/缩略图，动态控制项不手工增删。
- 批量改文案只替换文字节点，保留 `<br>`、图标、图片、链接、class、style、data 属性和交互。
- 轮播数量由脚本动态读取时不修改脚本，也不提前改运行时计数或进度状态。

## Logo、视频和地图

- Logo 的 `data-type="logo"` 放在完整 Logo 单元上；图片加文字时标在共同父节点。更换 Logo 图片必须先上传，不能把临时地址写入页面。
- 视频区域保留 `data-type="video"` 和实际 `<video>`。修改现有视频时不把它替换为图片，也不破坏系统识别的祖先关系。
- 地图根节点保留 `data-type="map"`、唯一 `data-typeid`、地图品牌/地址等配置；显示容器保留 `data-type="map-container"` 和唯一标识，且桌面与移动高度不能为 0。
- 地图脚本属于地图组件并保留在其作用域内；不得在页面修改中暴露、生成或替换服务端密钥。涉及密钥或地图服务配置时停止代码草稿并提示走系统配置。
