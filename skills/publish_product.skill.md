---
name: publish-product
description: Create a product draft, show its preview, and publish the saved draft after confirmation
metadata: {"clawdbot":{"emoji":"[PRODUCT]","requires":{"file":["scripts/config.json"]}}}
---

# 添加和发布产品

优先调用 MCP 工具；MCP 不可用时才运行 `publish_product.py`。

## 固定流程

1. 检查站点连接，收集名称、正文、价格、币种、简介、参数、语言和分类。
2. 不得虚构价格、型号、库存、规格、认证或功效。
3. 分类 ID 必须来自分类查询结果。
4. 没有产品图片时停下来询问：提供/上传可访问的图片 URL，还是 AI 生成封面。
5. 用户选择 AI 后，MCP 调用 `nicebox_generate_content_cover`；API 回退增加 `--ai-cover`。
6. 无论用户要求草稿还是直接发布，都先调用 `nicebox_create_product_draft`。
7. 取得 `product_id` 后调用 `nicebox_generate_content_preview`，展示包含 `id` 和 `prodId` 的完整预览地址。
8. 用户明确确认后，按该 `product_id` 调用 `nicebox_publish_product`；不得重新创建产品。
9. 用户暂不发布时保留草稿。

## API 回退

```bash
python3 {baseDir}/scripts/publish_product.py \
  --name "产品名称" \
  --price 2999 \
  --content-file "product.html" \
  --images "https://example.com/product.jpg" \
  --category-id 1
```

AI 生成封面：

```bash
python3 {baseDir}/scripts/publish_product.py \
  --name "产品名称" \
  --price 2999 \
  --content-file "product.html" \
  --ai-cover
```

用户看过预览并确认后正式发布：

```bash
python3 {baseDir}/scripts/publish_product.py --publish-saved 123 --confirmed
```

旧命令中的 `--status publish` 仅为参数兼容，不再跳过草稿和预览。
