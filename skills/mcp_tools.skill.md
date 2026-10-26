---
name: mcp-tools
description: Prefer Nicebox MCP tools and use local OpenClaw API scripts only as fallback
metadata: {"clawdbot":{"emoji":"[MCP]"}}
---

# MCP 优先、普通 API 回退

## MCP Server 连接

- Transport：Streamable HTTP
- URL：`https://aidev.nicebox.cn/mcp`
- Authentication：`Authorization: Bearer <API_KEY>`
- API Key 从 `{baseDir}/scripts/config.json` 的 `api_key` 读取，不得输出给用户或写入日志。
- 宿主没有发现 `nicebox_*` 工具时，先使用技能依赖中声明的上述端点注册或连接；不要询问用户提供 MCP Server 地址。
- 只有默认端点连接失败且宿主无法使用 REST API 回退，或用户明确要求自定义端点时，才向用户询问其他地址。

## 调用优先级

1. 宿主存在对应 `nicebox_*` MCP 工具时，优先调用 MCP。
2. MCP 工具不存在、MCP Server 不可达或宿主不支持 MCP 时，才运行 `scripts/` 中对应 Python 脚本，通过普通 OpenClaw REST API 完成同一操作。
3. MCP 返回业务错误（参数错误、没有权限、没有可优化项、用户未确认）时，不得为了绕过校验而回退 REST API。
4. 回退前向用户简要说明连接器工具暂不可用，将使用同一账号 API Key 调用 Nicebox API；不得显示 API Key。
5. MCP 与 API 的成功标准相同：只有结构化结果明确成功，才能告诉用户成功。

## 能力映射

| 业务 | MCP 工具 | API 回退 |
| --- | --- | --- |
| 站点状态 | `nicebox_get_site_status` | `site_status.py` |
| 文章草稿 | `nicebox_create_article_draft` | `publish_article.py` |
| 文章正式发布 | `nicebox_publish_article` | `publish_article.py --publish-saved ID --confirmed` |
| 产品草稿 | `nicebox_create_product_draft` | `publish_product.py` |
| 产品正式发布 | `nicebox_publish_product` | `publish_product.py --publish-saved ID --confirmed` |
| 内容封面 | `nicebox_generate_content_cover` | 文章/产品脚本的 `--ai-cover` |
| AI Logo | `nicebox_generate_logo` | `generate_logo.py` |
| 内容预览 | `nicebox_generate_content_preview` | 文章/产品脚本保存后自动生成 |
| 最新 SEO/GEO 报告 | `nicebox_get_latest_seo_geo_report` | `seo_geo.py latest` |
| SEO/GEO 报告详情 | `nicebox_get_seo_geo_report` | `seo_geo.py report --report-id ID` |
| 可自动优化项 | `nicebox_get_seo_geo_optimizable_items` | `seo_geo.py optimizable --report-id ID` |
| 启动 SEO/GEO 检测 | `nicebox_start_seo_geo_detection` | `seo_geo.py start-detect --confirmed --request-id ID` |
| 查询检测状态 | `nicebox_get_seo_geo_detection_status` | `seo_geo.py detect-status --operation-id ID` |
| 启动一键优化 | `nicebox_start_seo_geo_optimization` | `seo_geo.py start-optimize ... --confirmed --request-id ID` |
| 查询优化状态 | `nicebox_get_seo_geo_optimization_status` | `seo_geo.py optimize-status --operation-id ID` |

状态查询、检测和优化重试必须继续使用原 `operation_id` 或 `request_id`，不得因为切换通道重复创建任务。

生成文章或产品封面前，先让用户选择图片比例，再向 `nicebox_generate_content_cover` 传 `aspect_ratio`；不得静默使用默认比例。网站 Logo 缺失时提示用户选择提供 URL、AI 生成或暂不设置；选择 AI 后询问 `1:1` 方形或 `5:2` 横版，再调用 `nicebox_generate_logo`，展示候选图并在用户接受后作为企业资料 `logo`。

## 网站生成进度

`nicebox_start_website_generation` 返回 `operation_id` 只表示任务已受理。随后每 15-30 秒调用一次
`nicebox_get_website_generation_status`，向用户展示 `status`、`progress`、`elapsed_seconds` 和 `message`。
`progress_estimated=true` 表示百分比是等待时间估算，只提供进度感知；只有 `status=succeeded` 且首页验证通过才算真正完成。
不得频繁轮询，也不得因等待较久重复启动生成任务。

调用 `nicebox_start_website_generation` 时，`requirement` 必须包含完整的导航与 section 映射约束：一级导航使用 `data-type="nav"`，英文锚点去掉 `#` 后与首页对应 `section id` 完全相同；产品区/项使用 `products`/`product`，新闻区/项使用 `newslist`/`news`。不能只传公司资料或“生成完整网站”，否则后端可能只创建内页记录而无法截取内页正文。
