---
name: manage-pages
description: Query and manage existing pages without editing page HTML
metadata: {"clawdbot":{"emoji":"[PAGE]"}}
---

# 页面管理

本流程只处理现有页面的列表、筛选、排序、复制、删除、显示隐藏、语言归属、文件名、页面名称和 TDK。页面正文或布局修改转入页面代码修改流程；新增页面转入新增页面流程。

## 定位

1. 使用 `nicebox_list_pages`：编号用 `id` 精确查询，名称用 `keyword` 模糊查询；可用 `locale`、`element_type`、`status` 筛选，每页20条。
2. 多条候选时只展示“编号、名称、语言、类型、文件名、状态、排序”让用户选择；唯一后复用页面编号。
3. 需要读取完整管理字段或能力限制时调用 `nicebox_get_page_management_detail`。外链页面不能修改文件名或 TDK。

## 无需二次确认

目标和新值明确后直接执行，不再询问确认：

- 排序：先读取管理详情取得最新同级顺序摘要，再调用 `nicebox_update_page_sort`；只调整同级位置，不改变父级。若同级顺序已变化，只刷新后重试，不要求用户重复确认。
- 复制：`nicebox_copy_pages`，使用本次操作唯一的内部 `operation_id`；只复制明确页面，不递归复制子页面，不发布网站。超时重试必须复用同一个值，不能重复复制。
- 显示/隐藏：`nicebox_update_page_status`，同步共享导航，但不发布网站。
- 文件名：`nicebox_update_page_filename`，只允许字母、数字、下划线和横杠；冲突时提示更换。
- 页面名称和 TDK：`nicebox_update_page_settings`，只传用户要求修改的字段，未传字段保持不变。

不得为了统一流程给以上操作增加“是否确认”。缺少新位置、新状态或新值时，只补问缺失参数。

## 删除，必须二次提醒

1. 调用 `nicebox_check_page_deletion`。
2. 展示将删除的页面及全部子孙页面、首页保护、详情模板关联内容和替代模板；不展示 `impact_hash`。
3. 等待用户明确确认。取消或目标改变时不写入。
4. 确认后把原 `impact_hash` 作为 `expected_impact_hash`，生成本次操作唯一的内部 `operation_id`，调用 `nicebox_delete_pages(confirmed=true)`；超时重试复用同一个值。
5. 返回影响已变化时重新检查、展示并确认，不能沿用旧确认。

## 更改语言，必须二次提醒

1. 调用 `nicebox_check_page_locale_change`。
2. 展示必须一起迁移的完整父子树、当前语言和目标语言，并明确说明页面名称、HTML、链接文本和 TDK不会自动翻译。
3. 用户实际要求“翻译”时转入翻译流程，不能用更改语言代替。
4. 明确确认后携带原 `impact_hash` 和本次操作唯一的内部 `operation_id` 调用 `nicebox_update_page_locale(confirmed=true)`；超时重试复用同一个值。
5. 影响变化时重新检查和确认。

## 结果

只报告页面业务结果和必要提醒。文件名变化提示重新发布后线上地址更新；所有页面管理保存均不得表述为网站已经发布。不要输出工具名、接口、Hash、参数或通信方式。
