---
name: publish-article
description: Create an article draft, show its preview, and publish the saved draft after confirmation
metadata: {"clawdbot":{"emoji":"[ARTICLE]","requires":{"file":["scripts/config.json"]}}}
---

# 添加和发布文章

优先调用 MCP 工具；MCP 不可用时才运行 `publish_article.py`。

## 固定流程

1. 检查站点连接，收集标题、正文、摘要、作者、语言和分类。
2. 正文缺失时可生成正文，但生成内容不会自动保存。
3. 分类 ID 必须来自分类查询结果，不能猜测。
4. 缺少封面时停下来询问：提供/上传可访问的图片 URL，还是 AI 生成封面。
5. 用户选择 AI 后必须继续询问比例：`1:1`、`4:3`、`3:2`、`16:9`、`2:3`、`3:4` 或 `9:16`，不得替用户默认选择。
6. MCP 调用 `nicebox_generate_content_cover` 时传 `aspect_ratio`；API 回退使用 `--ai-cover --cover-ratio 比例`。
7. 无论用户说“保存草稿”还是“直接发布”，都先调用 `nicebox_create_article_draft` 保存草稿。
8. 取得 `article_id` 后调用 `nicebox_generate_content_preview`，展示包含 `id` 和 `newsId` 的完整预览地址。
9. 询问用户是否正式发布。明确确认后，按该 `article_id` 调用 `nicebox_publish_article`；不得重新创建文章。
10. 用户暂不发布时保留草稿并返回文章 ID 与预览地址。

## API 回退

保存草稿并自动生成预览：

```bash
python3 {baseDir}/scripts/publish_article.py \
  --title "文章标题" \
  --content-file "article.html" \
  --cover "https://example.com/cover.jpg" \
  --category-id 1
```

AI 生成封面后保存草稿：

```bash
python3 {baseDir}/scripts/publish_article.py \
  --title "文章标题" \
  --content-file "article.html" \
  --ai-cover \
  --cover-ratio "16:9"
```

用户看过预览并确认后正式发布：

```bash
python3 {baseDir}/scripts/publish_article.py --publish-saved 16817 --confirmed
```

旧命令中的 `--status publish` 仅为参数兼容，不再跳过草稿和预览。
