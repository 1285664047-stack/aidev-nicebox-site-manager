# 导航、Header、轮播与媒体规则

## 共享 Header、Footer 与导航

- Header/Footer 是站点共享内容，不能作为普通页面 section 保存。修改它们必须明确影响所有页面，并走共享头尾专用读写、预览和回退流程。
- 页面编辑、预览、保存和历史回退时使用当前共享头尾覆盖页面副本；回退页面正文不能回退共享头尾。
- 页面只有一个 `<header>` 和一个 `<footer>`；二者内部及祖先链不嵌套业务 `<section>`。
- PC 导航容器为 `nav[data-type="navs"]`，通常使用 `data-typeid="pc-navs-1"`；移动导航容器为 `.mobile-menu[data-type="navs"]`，通常使用 `mobile-navs-1`。
- 导航项保留 `data-type="nav"`、`data-nav-level`、唯一 `data-typeid`、`href` 和 `data-href`。链接字段由系统转换，不把线上 URL 固化覆盖占位符。
- Header 相关交互必须跟随共享 Header 保存；不要在普通页面正文复制一份导航监听器。

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
