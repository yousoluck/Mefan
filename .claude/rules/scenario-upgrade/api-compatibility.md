# API 兼容性规则
- type: constraint
- severity: error

1. 公共 API 只能新增，不可修改签名。
2. 废弃必须标记 @deprecated 并保留至少一个版本。
3. 新增参数必须加在末尾且提供默认值。
