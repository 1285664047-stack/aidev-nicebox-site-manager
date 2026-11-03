# 页面修改草稿校验规则

- `VERSION-001/002`：页面版本、Hash 和规则版本必须与读取时一致。
- `SCOPE-001/003`：section 模式必须使用读取返回的 selector，目标之外不得变化。
- `SYSTEM-001`：系统保护 Style/Script 必须保持实质内容不变。
- `SHARED-001`：普通页面草稿不得修改共享 Header/Footer。
- `CSS-001/005`：Tailwind 优先；必要局部 CSS 必须说明原因并限定范围。
- `COMPONENT-001/004`：产品、文章等动态组件必须保留运行时需要的 data-type 结构。
- `IMAGE-001`：新增图片必须来自 `nicebox_upload_images` 登记的当前账号云素材。
- `JS/LINK/FORM`：禁止危险脚本、危险协议、未知外部脚本和外部表单提交。

校验器只返回 errors、warnings、diff_summary、normalized_change 和 validated_change_hash，不修改页面。
