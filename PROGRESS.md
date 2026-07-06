# 电商智能客服Agent — 开发进度

> 每完成一步打✅，每改一次代码都git commit

## 开发规划

### Phase 1: 核心框架 [进行中]
- [x] 1.1 项目初始化（git + 目录结构 + PROGRESS.md）
- [ ] 1.2 配置管理（config.yaml + 环境变量 + Pydantic Settings）
- [ ] 1.3 统一消息格式（UnifiedMessage + Platform枚举）
- [ ] 1.4 数据库模型（SQLAlchemy：Shop/Order/Buyer/Conversation/Message）
- [ ] 1.5 FastAPI应用骨架（路由 + 中间件 + 异常处理）
- [ ] 1.6 数据库迁移（Alembic）

### Phase 2: 售后决策引擎 [待开始]
- [ ] 2.1 决策矩阵（Decision枚举 + RefundContext + make_decision）
- [ ] 2.2 恶意退货检测（退货率/频率/金额/账号年龄）
- [ ] 2.3 风控评估API（/api/risk/assess）
- [ ] 2.4 安全规则（日限额/单笔上限/审计日志）

### Phase 3: 平台适配器 [待开始]
- [ ] 3.1 适配器基类（EcommerceAdapter ABC）
- [ ] 3.2 Mock数据层（测试用虚拟数据）
- [ ] 3.3 淘宝适配器（TOP API：OAuth2 + 订单 + 商品 + 售后）
- [ ] 3.4 拼多多适配器（PDD API：OAuth2 + 订单 + 商品 + 售后）
- [ ] 3.5 抖店适配器（飞鸽API：OAuth2 + 订单 + 商品 + 售后 + IM）
- [ ] 3.6 京东适配器（JOS API：基础对接）

### Phase 4: Agent编排层 [待开始]
- [ ] 4.1 L0 意图路由器（意图分类 + 平台识别 + 用户画像）
- [ ] 4.2 L1 售前Agent（商品问答 + 规格查询 + 库存 + 活动）
- [ ] 4.3 L1 售后Agent（退换货 + 改地址 + 物流 + 退款审核）
- [ ] 4.4 L1 推荐Agent（关联推荐 + 凑单 + 上新 + 个性化）
- [ ] 4.5 L1 投诉Agent（情绪安抚 + 赔偿方案 + 转人工）
- [ ] 4.6 L2 整合Agent（结果合并 + 格式化 + 安全审核）
- [ ] 4.7 L3 转人工（工单创建 + 通知推送）

### Phase 5: 知识库与RAG [待开始]
- [ ] 5.1 商品知识库同步脚本（从平台API拉取→结构化文档）
- [ ] 5.2 FAQ知识库（历史高频问答）
- [ ] 5.3 售后政策库（退换货规则 + 平台规则）
- [ ] 5.4 话术库（问候/道歉/推荐/催付模板）
- [ ] 5.5 Dify知识库对接API

### Phase 6: Dify工作流 [待开始]
- [ ] 6.1 Dify环境部署
- [ ] 6.2 Chatflow配置（意图识别→场景分支→RAG→工具调用→回复）
- [ ] 6.3 HTTP工具注册（指向FastAPI服务的各API端点）
- [ ] 6.4 变量记忆配置（用户画像/会话上下文/订单状态）

### Phase 7: 安全层 [待开始]
- [ ] 7.1 Prompt注入检测（独立分类模型）
- [ ] 7.2 JWT认证 + RBAC权限
- [ ] 7.3 API速率限制 + 请求签名
- [ ] 7.4 数据加密 + PII脱敏
- [ ] 7.5 审计日志（全量操作记录）
- [ ] 7.6 输出过滤（防泄露系统提示词/内部信息）

### Phase 8: 部署 [待开始]
- [ ] 8.1 Docker Compose（FastAPI + PostgreSQL + Redis + Dify）
- [ ] 8.2 Nginx反向代理 + HTTPS
- [ ] 8.3 监控（Prometheus + Grafana）
- [ ] 8.4 部署文档 + API文档

---

## Git提交记录

| 日期 | 提交 | 说明 |
|------|------|------|
| 2026-07-06 | init | 项目初始化 |
