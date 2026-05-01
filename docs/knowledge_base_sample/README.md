# SupportOps Agent 初始知识库样例

这是一套用于 `SupportOps Agent` 的企业知识库种子数据，适合直接用于 RAG、Agent 分类、工单生成和人工确认流程的测试。

## 文件说明

- `FAQ.md`：常见问题与标准答复
- `SOP.md`：标准处理流程与升级规则
- `ProductManual.md`：产品功能说明与使用手册
- `RefundPolicy.md`：退款与售后处理规则
- `ITHelpdeskGuide.md`：内部 IT 支持排障手册
- `historical_tickets.csv`：历史工单模拟数据

## 使用建议

1. 先将 Markdown 和 CSV 文件切分为 chunk；
2. 为每个 chunk 添加 `title`、`category`、`source_file`、`section`、`updated_at` 等 metadata；
3. FAQ 和 SOP 适合优先进入向量库；
4. 历史工单适合用于分类、相似问题检索和工单生成；
5. 产品手册和 IT 手册适合回答产品咨询和排障问题；
6. 退款政策适合高风险问题的审核与人工确认流程。

## 建议分类标签

- 账号与权限
- 登录认证
- 网络与设备
- 产品咨询
- 支付与退款
- 系统故障
- 邮件通知
- 数据导出
- 工单流转
- 移动端

## RAG 切分建议

- Markdown 文档按一级/二级标题切分；
- 每个 chunk 建议控制在 300~800 中文字；
- CSV 工单按单行切分，每行作为一条样本；
- 保留原始标题、来源文件、行号或段落号，方便引用。

## 说明

这套知识库为**演示型合成样例**，不包含真实企业内部数据，可直接用于项目原型和 GitHub 展示。
