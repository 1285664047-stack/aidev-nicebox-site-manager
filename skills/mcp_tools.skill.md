---
name: mcp-tools
description: Prefer Nicebox MCP tools and use local OpenClaw API scripts only as fallback
metadata: {"clawdbot":{"emoji":"[MCP]"}}
---

# MCP 优先、普通 API 回退

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
| 内容预览 | `nicebox_generate_content_preview` | 文章/产品脚本保存后自动生成 |
| 最新 SEO/GEO 报告 | `nicebox_get_latest_seo_geo_report` | `seo_geo.py latest` |
| SEO/GEO 报告详情 | `nicebox_get_seo_geo_report` | `seo_geo.py report --report-id ID` |
| 可自动优化项 | `nicebox_get_seo_geo_optimizable_items` | `seo_geo.py optimizable --report-id ID` |
| 启动 SEO/GEO 检测 | `nicebox_start_seo_geo_detection` | `seo_geo.py start-detect --confirmed --request-id ID` |
| 查询检测状态 | `nicebox_get_seo_geo_detection_status` | `seo_geo.py detect-status --operation-id ID` |
| 启动一键优化 | `nicebox_start_seo_geo_optimization` | `seo_geo.py start-optimize ... --confirmed --request-id ID` |
| 查询优化状态 | `nicebox_get_seo_geo_optimization_status` | `seo_geo.py optimize-status --operation-id ID` |

状态查询、检测和优化重试必须继续使用原 `operation_id` 或 `request_id`，不得因为切换通道重复创建任务。

## 网站生成进度

`nicebox_start_website_generation` 返回 `operation_id` 只表示任务已受理。随后每 15-30 秒调用一次
`nicebox_get_website_generation_status`，向用户展示 `status`、`progress`、`elapsed_seconds` 和 `message`。
`progress_estimated=true` 表示百分比是等待时间估算，只提供进度感知；只有 `status=succeeded` 且首页验证通过才算真正完成。
不得频繁轮询，也不得因等待较久重复启动生成任务。
