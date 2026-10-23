---
name: seo-geo
description: View SEO/GEO reports, run confirmed detection, and perform confirmed one-click optimization
metadata: {"clawdbot":{"emoji":"[SEO]","requires":{"file":["scripts/config.json"]}}}
---

# SEO/GEO 检测与一键优化

优先使用 MCP；不可用时调用 `python3 {baseDir}/scripts/seo_geo.py ...`。

## 查看报告

- 用户要求查看报告时直接查询已有报告，不启动检测。
- 没有报告时说明情况，并在用户选择检测后执行检测确认流程。

## 启动或重新检测

每一次首次检测、重新检测、优化后复检或发布后复检，都必须先提示：

> 本次检测会消耗 Token 额度，通常需要等待几分钟。检测只生成报告，不会修改或发布网站。是否开始检测？

用户明确确认后才能启动。用户说“重新检测”只是表达意图，不等于确认。启动后保存 `operation_id` 并查询状态，禁止重复启动。

## 一键优化

1. 先查询最新完成报告和真实可优化项。
2. 没有可优化项时直接提醒，不创建任务。
3. 有项目时展示项目、问题数、预计页面数和人工问题数，说明只修改后台、不发布公网。
4. 用户明确确认后启动优化，保存 `operation_id` 并查询到结束。
5. 展示完成、跳过、未解决和失败结果，建议生成预览；发布必须独立确认。

## API 回退命令

```bash
python3 {baseDir}/scripts/seo_geo.py latest
python3 {baseDir}/scripts/seo_geo.py report --report-id 123
python3 {baseDir}/scripts/seo_geo.py optimizable --report-id 123
python3 {baseDir}/scripts/seo_geo.py start-detect
python3 {baseDir}/scripts/seo_geo.py start-detect --confirmed --request-id stable-id
python3 {baseDir}/scripts/seo_geo.py detect-status --operation-id operation-id
python3 {baseDir}/scripts/seo_geo.py start-optimize --report-id 123 --items 15 16 19
python3 {baseDir}/scripts/seo_geo.py start-optimize --report-id 123 --items 15 16 19 --confirmed --request-id stable-id
python3 {baseDir}/scripts/seo_geo.py optimize-status --operation-id operation-id
```
