# SupportOps Agent：企业知识库驱动的智能客服与工单处理 Agent

## 1. 项目定位

SupportOps Agent 是一个面向企业客服、售后支持和内部 IT Helpdesk 场景的 RAG-Augmented Workflow Agent 系统。系统能够基于企业知识库理解用户问题，自动检索 FAQ、SOP、产品文档和历史工单，生成带依据的回复；对于无法直接解决的问题，系统可以自动创建工单、判断优先级、推荐责任部门，并在涉及高风险操作时请求人工确认。

本项目不是简单的知识库问答机器人，而是一个具备“检索、判断、规划、工具调用、工单流转、人工确认和处理追踪”的企业级 Agent 应用。

## 2. 企业需求背景

企业客服和 IT 支持场景中存在大量重复性问题，例如账号登录失败、权限申请、系统报错、产品使用咨询、售后流程咨询等。传统处理方式依赖人工客服或运维人员手动查文档、判断问题类型、创建工单并跟进状态，容易出现响应慢、知识不统一、处理流程不透明等问题。

SupportOps Agent 的目标是将这些流程自动化：

- 使用 RAG 检索企业知识库，减少大模型幻觉；
- 使用 Agent 判断问题类型和处理路径；
- 使用工具调用创建工单、查询状态、分派责任人；
- 使用人工确认机制控制高风险操作；
- 使用执行日志和处理报告提升可观测性。

## 3. 核心价值

### 3.1 对企业的价值

- 降低重复客服和 IT 支持成本；
- 缩短用户问题响应时间；
- 提升 FAQ、SOP、历史工单等知识资产复用率；
- 提升工单分类、分派和跟进效率；
- 为客服质检和知识库优化提供数据依据。

### 3.2 对简历和面试的价值

本项目能够体现以下能力：

- RAG 知识库构建；
- Agent 工作流设计；
- Function Calling / Tool Calling；
- 多 Agent 协同；
- Human-in-the-loop 风控；
- 企业业务流程建模；
- 前后端工程实现；
- 可观测性与审计设计。

## 4. 项目目标

### 4.1 MVP 目标

第一版需要实现以下能力：

1. 支持上传企业 FAQ、SOP、产品文档、历史工单等知识文件；
2. 支持对文档进行切分、向量化和检索；
3. 支持用户自然语言提问；
4. Agent 自动判断问题类型；
5. Agent 调用 RAG 检索相关资料；
6. Agent 生成带来源依据的用户回复；
7. 对无法解决的问题自动创建模拟工单；
8. 工单支持分类、优先级、责任部门和状态管理；
9. 涉及高风险操作时进入人工确认流程；
10. 生成 Markdown 格式处理报告。

### 4.2 进阶目标

后续可以扩展：

- 多轮追问；
- 历史对话记忆；
- 工单 SLA 预警；
- 客服质检；
- 知识库自动补全建议；
- 多渠道接入，例如网页、企业微信、钉钉、飞书；
- 接真实 Jira、Zendesk、飞书多维表格或自建工单系统。

## 5. 使用场景

### 5.1 客服支持场景

用户问题：

> 我购买的服务无法登录，提示账号权限不足，应该怎么处理？

Agent 执行流程：

1. 判断为账号/权限类问题；
2. 检索知识库中的登录失败 FAQ 和权限申请 SOP；
3. 判断是否需要用户补充账号、系统名称和错误截图；
4. 如果信息足够，生成处理建议；
5. 如果需要人工处理，创建权限工单；
6. 输出用户回复和内部工单摘要。

### 5.2 IT Helpdesk 场景

用户问题：

> VPN 连不上，公司内网打不开。

Agent 执行流程：

1. 判断为网络/VPN 类问题；
2. 检索 VPN 排障 SOP；
3. 追问操作系统、错误码、网络环境；
4. 给出排障步骤；
5. 若仍无法解决，创建 IT 工单并分派给网络组。

### 5.3 售后服务场景

用户问题：

> 这个订单能不能退款？

Agent 执行流程：

1. 判断为退款/售后类问题；
2. 检索退款政策；
3. 根据政策判断是否可自动回复；
4. 涉及退款操作时触发人工确认；
5. 生成工单和处理建议。

### 5.4 产品咨询场景

用户问题：

> 你们系统支持多人协同和权限管理吗？

Agent 执行流程：

1. 判断为产品咨询；
2. 检索产品文档；
3. 生成结构化答复；
4. 如果用户表现出购买意向，创建销售线索工单。

## 6. 系统架构

```text
User / Customer
      |
      v
Web Chat UI / Admin Console
      |
      v
FastAPI Backend
      |
      v
Agent Orchestrator
      |
      |-- Intent Agent
      |-- RAG Agent
      |-- Action Agent
      |-- Risk Agent
      |-- Reply Agent
      |
      v
Tool Layer
      |
      |-- retrieve_knowledge
      |-- classify_ticket
      |-- create_ticket
      |-- assign_ticket
      |-- query_ticket_status
      |-- request_human_approval
      |-- generate_customer_reply
      |-- generate_internal_summary
      |
      v
Data Layer
      |
      |-- Vector Database
      |-- PostgreSQL / SQLite
      |-- Redis Cache
      |-- File Storage
      |-- Trace Logs
```

## 7. Agent 角色设计

### 7.1 Intent Agent

负责理解用户问题和业务意图。

主要职责：

- 判断用户问题类型；
- 识别是否为咨询、故障、投诉、退款、权限、账号等场景；
- 提取关键实体，例如系统名称、订单号、错误码、账号、时间、截图描述；
- 判断信息是否充足，必要时生成追问问题。

输出示例：

```json
{
  "intent": "account_permission_issue",
  "category": "账号与权限",
  "missing_fields": ["系统名称", "错误提示截图"],
  "need_follow_up": true
}
```

### 7.2 RAG Agent

负责检索企业知识库。

主要职责：

- 根据用户问题生成检索 query；
- 检索 FAQ、SOP、产品文档和历史工单；
- 返回相关片段和来源；
- 判断检索结果是否足够支撑回答；
- 为 Reply Agent 提供证据。

### 7.3 Action Agent

负责调用业务工具。

主要职责：

- 创建工单；
- 查询工单状态；
- 修改工单状态；
- 推荐责任部门；
- 生成内部处理摘要；
- 触发消息通知。

### 7.4 Risk Agent

负责风险判断和人工确认。

主要职责：

- 判断操作风险等级；
- 识别是否涉及权限变更、退款、删除数据、重置密码等敏感操作；
- 决定是否需要人工审批；
- 记录审批结果。

风险等级示例：

- 低风险：知识库回复、查询工单；
- 中风险：创建工单、修改工单优先级；
- 高风险：重置密码、变更权限、退款、关闭账号；
- 禁止操作：删除用户数据、绕过审批直接处理资金或权限。

### 7.5 Reply Agent

负责生成最终回复。

主要职责：

- 面向用户生成清晰、礼貌、可执行的答复；
- 面向客服或运维生成内部摘要；
- 在回答中附带知识来源；
- 对不确定内容明确说明；
- 对需要人工介入的问题提供工单编号和后续流程。

## 8. RAG 知识库设计

### 8.1 知识来源

可以准备以下示例数据：

- `FAQ.md`：常见问题；
- `SOP.md`：标准处理流程；
- `ProductManual.pdf`：产品手册；
- `RefundPolicy.md`：退款政策；
- `ITHelpdeskGuide.md`：IT 排障手册；
- `HistoricalTickets.csv`：历史工单。

### 8.2 文档处理流程

```text
上传文档
  ↓
文本解析
  ↓
清洗与分段
  ↓
生成 embedding
  ↓
写入向量数据库
  ↓
检索相关片段
  ↓
交给 Agent 生成回答或决策
```

### 8.3 切分策略

建议采用：

- Markdown 按标题切分；
- PDF 按页和段落切分；
- CSV 历史工单按行切分；
- 每个 chunk 控制在 300-800 中文字；
- 每个 chunk 保留来源、标题、页码、更新时间等 metadata。

### 8.4 检索策略

MVP 阶段：

- 向量相似度检索 Top-K；
- 返回来源标题和片段；
- 由模型判断是否足够回答。

进阶阶段：

- Hybrid Search：关键词 + 向量检索；
- Rerank：二次排序；
- Query Rewrite：根据用户问题改写检索 query；
- 多轮检索：信息不足时继续查找。

## 9. 工单系统设计

### 9.1 工单字段

```text
Ticket
- id
- title
- description
- category
- priority
- department
- status
- user_id
- source_conversation_id
- suggested_solution
- created_at
- updated_at
```

### 9.2 工单分类

可设置以下类别：

- 账号与权限；
- 登录与认证；
- 产品咨询；
- 支付与退款；
- 系统故障；
- 网络与设备；
- 数据问题；
- 人工服务。

### 9.3 优先级规则

- P0：大面积系统不可用、资金风险、数据安全风险；
- P1：核心功能不可用、重要客户受影响；
- P2：普通功能异常、单个用户受影响；
- P3：咨询、建议、低风险问题。

### 9.4 状态流转

```text
新建 -> 待分派 -> 处理中 -> 等待用户补充 -> 已解决 -> 已关闭
```

## 10. 工具函数设计

### 10.1 RAG 工具

```python
def retrieve_knowledge(query: str, top_k: int = 5) -> list:
    """检索企业知识库，返回相关片段、来源和相似度。"""
```

### 10.2 意图识别工具

```python
def classify_ticket(message: str) -> dict:
    """识别问题类型、优先级和是否需要追问。"""
```

### 10.3 工单创建工具

```python
def create_ticket(title: str, category: str, priority: str, description: str) -> dict:
    """创建工单并返回工单编号。"""
```

### 10.4 工单分派工具

```python
def assign_ticket(ticket_id: str, department: str) -> dict:
    """将工单分派给指定部门。"""
```

### 10.5 状态查询工具

```python
def query_ticket_status(ticket_id: str) -> dict:
    """查询工单当前状态。"""
```

### 10.6 人工确认工具

```python
def request_human_approval(action: str, risk_level: str, reason: str) -> dict:
    """对高风险操作发起人工确认。"""
```

### 10.7 回复生成工具

```python
def generate_customer_reply(context: dict) -> str:
    """生成面向用户的最终回复。"""
```

## 11. 技术栈

第一版直接按照企业级 MVP 设计，采用 `FastAPI + Vue3 + PostgreSQL + Redis + Chroma + Docker Compose` 的一体化架构，保证项目既能快速开发，又具备较强的工程化展示效果。

### 11.1 后端技术栈

- Python 3.11；
- FastAPI；
- Uvicorn；
- Pydantic；
- SQLAlchemy；
- Alembic；
- PostgreSQL；
- Redis；
- ChromaDB；
- OpenAI API 或其他大模型 API；
- Function Calling / Tool Calling；
- RAG；
- Docker；
- Docker Compose。

### 11.2 前端技术栈

- Vue3；
- Vite；
- Element Plus；
- Axios；
- Pinia；
- Vue Router；
- Nginx；
- Docker。

### 11.3 AI 与 RAG 技术栈

- 对话/推理模型 API；
- Embedding API；
- LangGraph；
- LangChain；
- ChromaDB 向量数据库；
- 文档切分与向量化；
- Top-K 语义检索；
- Query Rewrite；
- RAG 证据引用；
- Multi-Agent Workflow；
- Human-in-the-loop；
- Agent Trace。

### 11.4 数据库与缓存

- PostgreSQL：存储正式业务数据，包括文档元数据、工单、会话、消息、审批、Trace、报告和系统配置；
- Redis：存储临时状态和缓存，包括文档向量化任务状态、RAG 检索缓存、Agent 执行状态、审批等待状态和短期会话缓存；
- ChromaDB：存储知识库文档向量，支持 FAQ、SOP、产品手册和历史工单的语义检索。

### 11.5 数据与文档处理

- PyMuPDF / pdfplumber；
- python-docx；
- pandas；
- Markdown parser；
- tiktoken 或其他 token 统计工具；
- 文档 metadata 管理；
- CSV 历史工单解析。

### 11.6 容器化与部署

- Docker：封装后端、前端和基础设施服务；
- Docker Compose：统一编排 `backend`、`frontend`、`postgres`、`redis`、`chroma` 服务；
- Nginx：承载前端静态资源并可反向代理后端接口；
- `.env`：统一管理数据库、Redis、Chroma 和 AI API 配置。

### 11.7 可观测性

- Agent Trace；
- Tool Call Logs；
- 工单流转日志；
- Redis 任务状态；
- 用户反馈记录；
- 处理报告导出；
- 后端健康检查接口。

### 11.8 第一版运行服务

```text
frontend   Vue3 + Nginx，负责用户界面
backend    FastAPI，负责 API、Agent 编排和工具调用
postgres   PostgreSQL，负责业务数据持久化
redis      Redis，负责缓存、任务状态和 Agent 临时状态
chroma     ChromaDB，负责知识库向量检索
```

### 11.9 Docker Compose 编排示例

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
      - chroma

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: supportops
      POSTGRES_USER: supportops
      POSTGRES_PASSWORD: supportops
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  postgres_data:
  chroma_data:
```

### 11.10 Redis 第一版使用方式

Redis 在第一版中不存储正式业务数据，只负责缓存、任务状态和临时执行状态。

#### 文档向量化任务状态

```text
doc_task:{task_id} = processing / completed / failed
```

#### RAG 检索缓存

```text
rag_cache:{query_hash} = 检索结果 JSON
```

#### Agent 执行状态

```text
agent_trace:{trace_id} = 当前执行步骤 JSON
```

#### 审批等待状态

```text
approval_waiting:{approval_id} = pending
```

### 11.11 PostgreSQL 第一版数据职责

PostgreSQL 存储正式业务数据：

```text
documents          文档元数据
document_chunks    文档切分片段元数据
tickets            工单主表
ticket_comments    工单备注
conversations      会话表
messages           消息表
approvals          人工审批表
trace_steps        Agent 执行步骤
reports            处理报告
settings           系统配置
```

### 11.12 第一版不做的内容

为了控制复杂度，第一版暂不引入：

- Kubernetes；
- 微服务拆分；
- Celery 分布式任务队列；
- 真实企业微信/钉钉/飞书接入；
- 多租户权限系统；
- 复杂客服坐席系统。

第一版重点是跑通以下闭环：

```text
知识库上传 -> 文档向量化 -> RAG 检索 -> Agent 判断 -> 自动回复/创建工单 -> 人工确认 -> Trace 展示 -> 报告导出
```

### 11.13 生产级后端落地原则

第一版后端采用 **production-style modular monolith（生产级模块化单体）**。也就是说，代码部署形态先保持一个 FastAPI 后端服务，但内部按照真实线上系统的边界拆分模块，避免写成只适合演示的脚本式项目。

Agent 编排从第一版开始引入 `LangGraph / LangChain`：

- FastAPI 负责 HTTP API、鉴权、参数校验、错误处理；
- LangGraph 负责 Agent 状态图、多步骤执行、条件分支、trace 和 human-in-the-loop；
- LangChain 负责模型调用、工具封装、Prompt 模板和外部集成；
- RAG 检索结果、工单工具和风险审批都作为 LangGraph 节点或 Tool 接入。

选择模块化单体的原因：

- 适合个人项目和 MVP 快速推进；
- 保留清晰的业务边界，后续可以平滑拆成微服务；
- 比过早引入微服务、Kubernetes 和复杂消息队列更容易一次跑通；
- 更符合真实团队从 0 到 1 建设 AI 产品后端的常见路径。

后端分层约定：

```text
API Router       只负责路由、请求参数、响应结构
Schema           定义请求体、响应体和校验规则
Service          承载业务逻辑，例如文档、工单、审批、报告
Agent            使用 LangGraph 承载意图识别、RAG、风险判断、回复生成等 AI 编排
Tool             封装可被 Agent 调用的业务动作
Repository       封装数据库读写，避免业务层直接写 SQL
Model            定义数据库表结构
Core             配置、日志、错误处理、安全、通用响应
DB               数据库连接、Session、迁移入口
Tests            单元测试、API 测试、集成测试
```

核心工程要求：

- 配置通过 `.env` 管理，禁止把 API Key、数据库密码写死在代码里；
- 所有数据库结构变化必须通过 Alembic migration 管理；
- 所有 API 返回统一响应结构；
- 所有异常走统一错误处理，避免把内部堆栈直接暴露给前端；
- 每次 Agent 执行需要记录 trace，方便定位工具调用和模型输出问题；
- 上传文件必须限制类型、大小和存储路径；
- 后端启动后必须能检查 PostgreSQL、Redis、Chroma 的连接状态；
- 第一版就保留测试目录，至少覆盖健康检查、核心 service 和主要 API。

### 11.14 本地开发环境准备

本项目第一版建议使用 macOS / Linux 开发环境，核心依赖如下：

```text
Git              拉取代码、提交代码、同步 GitHub
Python 3.11+     运行 FastAPI 后端
Node.js 20+      运行 Vue3 前端
Docker           启动 PostgreSQL、Redis、Chroma 等基础服务
Docker Compose   编排多个本地服务
```

本地检查命令：

```bash
git --version
python3 --version
node --version
npm --version
docker --version
docker compose version
```

这些命令只做环境检查，不会修改项目文件：

- `git --version`：确认 Git 是否可用；
- `python3 --version`：确认 Python 版本是否满足后端要求；
- `node --version`：确认 Node.js 是否满足前端要求；
- `npm --version`：确认 Node 包管理器是否可用；
- `docker --version`：确认 Docker 客户端是否安装；
- `docker compose version`：确认 Docker Compose 是否可用。

推荐的第一阶段开发节奏：

```text
先验证本机工具链 -> 创建后端骨架 -> 创建虚拟环境 -> 安装依赖 -> 跑通健康检查 -> 再接数据库和缓存
```

## 12. AI API 准备方案

### 12.1 是否一定需要 AI API

如果要做一个真正可演示的 RAG + Agent 项目，建议准备 AI API。

原因：

- 需要大模型完成意图识别、任务规划、回复生成和工具调用；
- 需要 embedding 模型完成文档向量化；
- 如果没有 API，也可以用本地开源模型，但部署成本和调试成本更高。

因此，MVP 最推荐使用云端 AI API。

### 12.2 最少需要几个 API

最少需要 2 类 API：

1. **对话/推理模型 API**
   - 用于 Intent Agent、RAG Agent、Risk Agent、Reply Agent；
   - 负责问题理解、工具选择、答案生成和报告生成。

2. **Embedding API**
   - 用于知识库向量化；
   - 负责将 FAQ、SOP、PDF、历史工单转成向量，写入 FAISS/Chroma。

也就是说，最少准备：

```text
1 个大模型对话 API + 1 个 embedding API
```

### 12.3 推荐准备几个 API Key

实际开发建议准备 1 个平台账号即可，因为同一个平台通常可以同时调用对话模型和 embedding 模型。

推荐配置：

```text
OPENAI_API_KEY=你的 API Key
MODEL_NAME=用于推理/对话的模型
EMBEDDING_MODEL=用于向量化的模型
```

如果想提高容错，可以准备 2 套：

```text
主模型 API：用于 Agent 推理和生成
备用模型 API：用于限流或成本控制时切换
```

但 MVP 阶段不需要多平台，只需要一套即可。

### 12.4 API 用在项目哪里

| 模块 | 是否需要 AI API | 用途 |
|---|---|---|
| 文档上传 | 否 | 解析文件、切分文本 |
| 文档向量化 | 是 | 调用 embedding 模型 |
| 知识库检索 | 否/部分需要 | FAISS/Chroma 本地检索不需要，query 改写可用模型 |
| 意图识别 | 是 | 判断问题类型、优先级、是否追问 |
| Agent 规划 | 是 | 决定下一步调用哪个工具 |
| 工单创建 | 否 | 调用本地函数或数据库 |
| 风险判断 | 是 | 判断是否需要人工确认 |
| 回复生成 | 是 | 生成用户回复和内部摘要 |
| 报告生成 | 是 | 输出 Markdown 处理报告 |

### 12.5 成本控制建议

MVP 阶段可以这样控制成本：

- 文档不要太大，准备 5-10 份示例文档即可；
- 向量化只在上传时做一次，不要每次问答都重复 embedding；
- 检索 Top-K 控制在 3-5；
- 对话上下文只放必要片段；
- Agent 步骤不要无限循环，限制最多 5-8 步；
- 报告生成使用一次性总结，不要多轮生成。

### 12.6 没有 API 时的替代方案

如果暂时没有 API，也可以这样做：

- Embedding 使用本地模型，例如 bge-small-zh、bge-m3；
- 对话模型使用本地 Ollama 模型；
- 先把 Agent 逻辑和工具调用框架写好；
- 等有 API 后替换模型调用层。

但注意：

- 本地模型效果不一定稳定；
- 工具调用能力需要自己约束输出 JSON；
- 部署和显存要求更高；
- 面试演示时云端 API 通常更稳。

## 13. MVP 开发计划

第一版按照生产级模块化单体开发，默认使用 Docker Compose 编排 `backend`、`frontend`、`postgres`、`redis`、`chroma` 五个服务。开发顺序优先保证后端工程基础稳定，再逐步接入 RAG、Agent 和前端页面。

### Phase 0：本地环境准备

- 检查 Git、Python、Node.js、Docker 和 Docker Compose；
- 确认 GitHub 仓库可以正常 `pull` / `push`；
- 确认 Docker Desktop 已启动；
- 确认本机 8000、5173、5432、6379、8001 端口没有冲突；
- 创建 `.env.example`，只提交示例配置，不提交真实密钥；
- 编写 `README.md` 的本地启动说明。

### Phase 1：后端工程骨架

- 创建 `backend/` 目录；
- 创建 Python 虚拟环境；
- 编写 `backend/requirements.txt`；
- 创建 FastAPI 应用入口；
- 安装并接入 LangGraph / LangChain；
- 建立 `core`、`api`、`schemas`、`services`、`repositories`、`models`、`db`、`agents`、`tools` 目录；
- 实现统一响应结构；
- 实现统一异常处理；
- 实现结构化日志基础配置；
- 实现 `GET /` 和 `GET /api/health`；
- 实现最小 LangGraph workflow，并接入 `POST /api/chat`；
- 将 LangGraph workflow 拆为输入规范化、意图识别、RAG 检索、风险判断、审批、建单、回复生成等节点；
- 使用 `pytest` 覆盖健康检查接口。

### Phase 2：基础设施接入

- 创建 `docker-compose.yml`；
- 启动 PostgreSQL、Redis、ChromaDB；
- 配置 SQLAlchemy 数据库连接；
- 配置 Alembic 数据库迁移；
- 实现数据库连接检查接口；
- 实现 Redis 连接检查接口；
- 实现 Chroma 连接检查逻辑；
- 保证后端启动时可以读取 `.env` 配置。

### Phase 3：业务数据模型与基础 API

- 建立 `documents`、`document_chunks` 表；
- 建立 `tickets`、`ticket_comments` 表；
- 建立 `conversations`、`messages` 表；
- 建立 `approvals`、`trace_steps`、`reports` 表；
- 实现文档、工单、会话的 repository；
- 实现工单创建、列表、详情、状态更新 API；
- 为核心 service 编写单元测试。

### Phase 4：知识库上传与解析

- 实现 Markdown/TXT/PDF/CSV 上传；
- 校验上传文件类型和大小；
- 保存文档 metadata 到 PostgreSQL；
- 使用后台任务解析文档；
- 按标题、段落或 CSV 行切分 chunk；
- 保存 chunk metadata；
- 使用 Redis 记录文档处理任务状态；
- 实现任务状态查询接口。

### Phase 5：Embedding 与 Chroma RAG 检索

- 封装 embedding service；
- 将文档 chunk 写入 ChromaDB；
- 将 chunk metadata 写入 PostgreSQL；
- 实现 `POST /api/documents/search`；
- 使用 Redis 缓存高频检索结果；
- 返回检索片段、来源文件、相似度和 metadata；
- 添加无 API Key 时的降级或 mock 模式。

### Phase 6：Agent Chat 工作流

- 实现 Intent Agent；
- 实现 RAG Agent；
- 实现 Reply Agent；
- `/api/chat` 支持意图识别、知识库检索和带来源回复；
- 将 Agent 执行步骤写入 `trace_steps`；
- 将当前执行状态写入 Redis；
- 限制 Agent 最大步骤数，避免无限循环；
- 为 chat workflow 编写集成测试。

### Phase 7：工单工具调用与人工确认

- 实现 `create_ticket`、`assign_ticket`、`query_ticket_status` 工具；
- Agent 根据问题自动创建工单；
- 实现 Risk Agent；
- 高风险操作进入人工确认；
- 实现审批通过和拒绝接口；
- 记录审批日志和工具调用 trace。

### Phase 8：前端、报告与项目包装

- 创建 Vue3 + Vite 前端；
- 完成 Chat、知识库、工单、审批、Trace 页面；
- 实现 Markdown 处理报告生成；
- 支持报告导出；
- 完善 README、接口说明和演示脚本；
- 准备一键启动演示流程；
- 补充简历描述和项目截图。

## 14. 演示数据准备

### 14.1 FAQ 示例

可以准备以下问题：

- 账号登录失败怎么办？
- 忘记密码如何处理？
- 如何申请系统权限？
- VPN 无法连接怎么办？
- 如何提交退款申请？
- 系统报 500 错误怎么办？

### 14.2 SOP 示例

可以准备以下流程：

- 账号权限申请 SOP；
- 密码重置 SOP；
- VPN 故障排查 SOP；
- 退款审核 SOP；
- 系统故障升级 SOP。

### 14.3 历史工单示例

准备 CSV：

```csv
id,title,category,priority,department,status,solution
T001,账号无法登录,账号与权限,P2,IT支持组,已解决,重置密码并检查账号状态
T002,VPN连接失败,网络与设备,P2,网络组,已解决,更新 VPN 客户端并重启网络服务
T003,申请管理员权限,账号与权限,P1,IT支持组,处理中,等待直属主管审批
```

## 15. 项目目录建议

```text
supportops-agent/
  backend/
    app/
      core/
        config.py
        logging.py
        responses.py
        exceptions.py
        security.py
      api/
        deps.py
        router.py
        routes/
          health.py
          chat.py
          documents.py
          tickets.py
          approvals.py
          traces.py
          reports.py
          settings.py
      schemas/
        common.py
        health.py
        chat.py
        document.py
        ticket.py
        approval.py
        trace.py
        report.py
      agents/
        intent_agent.py
        rag_agent.py
        action_agent.py
        risk_agent.py
        reply_agent.py
      tools/
        rag_tools.py
        ticket_tools.py
        approval_tools.py
        report_tools.py
      services/
        llm_service.py
        embedding_service.py
        vector_store_service.py
        document_service.py
        ticket_service.py
        redis_service.py
        trace_service.py
        approval_service.py
        report_service.py
      repositories/
        document_repository.py
        ticket_repository.py
        conversation_repository.py
        approval_repository.py
        trace_repository.py
        report_repository.py
      models/
        base.py
        ticket.py
        document.py
        conversation.py
        approval.py
        trace.py
        report.py
      db/
        session.py
        base.py
        migrations.py
      main.py
    tests/
      test_health.py
      test_tickets.py
      test_documents.py
    alembic/
    alembic.ini
    Dockerfile
    requirements.txt
    requirements-dev.txt
  frontend/
    src/
      views/
        ChatView.vue
        KnowledgeBaseView.vue
        TicketView.vue
        ApprovalView.vue
        TraceView.vue
        ReportView.vue
      api/
        chat.js
        documents.js
        tickets.js
        approvals.js
        traces.js
      main.js
    Dockerfile
    nginx.conf
    package.json
  docs/
    FAQ.md
    SOP.md
    demo_tickets.csv
  docker-compose.yml
  .env.example
  .gitignore
  README.md
```

## 16. 简历描述

```latex
\item \textbf{项目名称}: SupportOps Agent：企业知识库驱动的智能客服与工单处理系统
\item \textbf{技术栈}: Python、FastAPI、OpenAI API、RAG、Function Calling、ChromaDB、PostgreSQL、Redis、Vue3、Element Plus、Docker Compose
\item \textbf{项目描述}: 面向企业客服与 IT 支持场景，设计并实现带 RAG 能力的智能工单 Agent，支持企业知识库检索、用户问题理解、工单自动分类、处理建议生成和人工确认流程。
\item \textbf{核心工作}: 构建 FAQ、SOP、历史工单等知识库检索模块，结合 Intent Agent、RAG Agent、Action Agent 和 Risk Agent 完成问题分类、知识检索、工单创建、任务分派和风险判断。
\item \textbf{项目亮点}: 系统能够根据用户问题自动检索相关文档并生成带来源依据的回复，对于无法直接解决的问题自动创建工单并推荐责任部门；涉及权限变更、账号重置等高风险操作时引入 Human-in-the-loop 审批机制。
\item \textbf{工程实践}: 使用 Docker Compose 编排 FastAPI、Vue3、PostgreSQL、Redis 与 ChromaDB 服务，基于 Redis 实现任务状态管理和 RAG 检索缓存，支持知识库上传、向量检索、Agent 工具调用日志、工单状态追踪和 Markdown 处理报告导出。
```

## 17. 项目亮点总结

- 贴近企业客服、售后和 IT Helpdesk 真实需求；
- 同时体现 RAG、Agent、Function Calling 和业务流程自动化；
- 相比普通知识库问答，多了工单创建、任务分派、风险判断和人工确认；
- 具有明确业务价值：降低重复客服成本、提升响应速度、沉淀知识资产；
- 数据和业务流程可以自造，适合个人快速开发和面试演示。
