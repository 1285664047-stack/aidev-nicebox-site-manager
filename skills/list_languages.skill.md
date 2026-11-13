---
name: manage-languages
description: Query and manage Nicebox site languages, migration, default entry, display names, sorting, and deletion
metadata: {"clawdbot":{"emoji":"[LANG]","requires":{"file":["scripts/config.json"]}}}
---

# 多语言管理

## 查询与定位

任何修改前先调用 `nicebox_list_languages`。语言必须使用返回的真实 `locale`，不能把“英文”“中文站”等显示名称直接当代码。结果展示标准名称、自定义名称、排序和默认状态。

“当前语言”只有在本轮上下文能唯一确定时才可复用，否则列出语言让用户选择。API Key、连接或站点改变后，清除旧语言、预检、Hash 和确认。

## 自定义名称与排序

- 调用 `nicebox_update_language_config`，使用列表刚返回的 `config_hash`。
- `changes.custom_name` 修改显示名称；空字符串表示恢复系统标准名称。
- `changes.sort` 为非负整数，值越大越靠前。
- 只传用户要求修改的字段；名称和排序可单独修改，也可一次修改。
- 用户只说“排到第一”时，根据当前列表计算高于现有最大值的新排序，先用自然语言说明预期顺序再更新。

## 整站语言搬迁

以下表达进入本流程：“更换网站语言”“把当前语言所有内容搬迁到另一语言”“把整个中文站改归英文”。只更改内容归属语言，不翻译页面、产品、文章、FAQ、分类或表单文字。

“把这个页面改成英文”走页面管理的单页语言归属流程；“把中文翻译成英文”走翻译/新增语言流程；“把页面入口设置为英文”走下方默认语言流程。

1. 确定源语言和目标语言，调用 `nicebox_preview_language_migration`。
2. 展示源语言将搬迁的页面、区域、产品、文章、FAQ、分类和表单数量，并明确“文字不会翻译”。
3. 目标语言没有内容时，展示默认语言是否会改变，询问是否继续。
4. 目标语言已有内容时，必须让用户选择：
   - 删除目标语言现有内容后完整搬迁：`replace_target`，明确目标内容永久删除。
   - 保留目标数据和共享头尾并合并：`preserve_target`，提醒可能出现重复内容或页面地址调整。
   - 取消。
5. 不得替用户选择。参数确认后生成唯一 `operation_id`，将本次 `preview_token` 原样传给 `nicebox_execute_language_migration`。
6. 目标为空时使用 `move_only`。超时或连接中断时用原 `operation_id` 调用 `nicebox_get_language_operation`，禁止重复提交。
7. 结果说明实际迁移/删除数量、默认语言和入口是否改变、页面地址是否调整、文字未翻译，并提醒重新发布网站后线上地址才更新。

## 删除语言

1. 调用 `nicebox_get_language_delete_impact`。
2. 默认语言禁止删除；提示用户先选择另一种具有有效首页的语言设为默认，不能自动切换。
3. 展示将永久删除的页面、区域、产品、文章、FAQ、分类、表单、提交和回复数量，并明确不可恢复。
4. 必须停下来进行第二次提醒，只有用户针对当前摘要明确确认删除后，才调用 `nicebox_delete_language` 并传 `expected_impact_hash`、唯一 `operation_id` 和 `confirmed=true`。
5. “好的”“看看”“可以吗”不视为删除确认。影响已变化时重新读取并再次确认。
6. 首期一次只删除一种语言。

## 设置默认语言与页面入口

“设为默认语言”“把页面入口设置为英文”“访问网站默认进入英文首页”均进入本流程。该操作不翻译、不搬迁内容，也不自动发布网站。

1. 调用 `nicebox_get_default_language_impact`，检查目标语言唯一首页和文件名变化。
2. 展示当前入口语言、目标入口语言、原首页和目标首页地址变化，并提醒重新发布后线上入口才更新。
3. 必须停下来进行第二次提醒。用户针对当前入口变化明确确认后，调用 `nicebox_set_default_language` 并传 `expected_impact_hash`、唯一 `operation_id` 和 `confirmed=true`。
4. 目标语言没有首页或首页不唯一时停止，提示先创建或修复该语言首页。
5. 写入结果未知时用 `nicebox_get_language_operation` 查询，不重复切换。

## 输出边界

最终只说明实际业务变化和是否需要重新发布。不得展示工具名、接口、Token、Hash、数据库表、原始参数或连接细节。

