# SupportOps Agent

SupportOps Agent 是一个面向企业客服、售后支持和内部 IT Helpdesk 场景的 RAG + Agent 工单处理系统。

项目目标不是只做一个知识库问答 demo，而是按真实产品后端的方式，逐步实现：

```text
知识库上传 -> 文档向量化 -> RAG 检索 -> Agent 判断 -> 自动回复/创建工单 -> 人工确认 -> Trace 展示 -> 报告导出
```

当前阶段：已完成项目文档、API 文档、知识库样例，以及第一版 FastAPI + LangGraph 后端骨架。

## 技术路线

第一版采用 production-style modular monolith，也就是生产级模块化单体。

部署形态先保持一个 FastAPI 后端服务，但内部按照真实线上项目拆分模块。Agent 编排从第一版开始使用 LangGraph / LangChain 生态：

```text
FastAPI          对外提供 HTTP API
LangGraph        编排 Agent 状态图和多步骤工作流
LangChain        连接模型、工具、Prompt 和外部集成
PostgreSQL       存储正式业务数据
Redis            存储缓存、任务状态和短期执行状态
Chroma           存储知识库向量
```

```text
API Router       路由、请求参数、响应结构
Schema           请求体、响应体和校验规则
Service          业务逻辑
Agent            LangGraph 状态图，负责意图识别、RAG、风险判断、回复生成
Tool             Agent 可调用的业务动作
Repository       数据库读写
Model            数据库表结构
Core             配置、日志、错误处理、安全、通用响应
DB               数据库连接、Session、迁移入口
Tests            单元测试、API 测试、集成测试
```

## 环境要求

本机需要准备：

```text
Git
Conda
Python 3.11
Node.js 20+
npm
Docker Desktop
Docker Compose
```

检查命令：

```bash
git --version
conda --version
node --version
npm --version
docker --version
docker info
docker compose version
```

说明：

- `docker --version` 只表示 Docker CLI 存在。
- `docker info` 能看到 `Server:` 才表示 Docker Desktop 后台真正可用。
- `docker compose version` 用于确认多服务编排工具可用。

## 后端环境准备

建议为本项目创建独立 Conda 环境：

```bash
conda create -n supportops-agent python=3.11
conda activate supportops-agent
python --version
```

安装后端依赖：

```bash
cd /Users/chenylnti/codefile/intership/SupportOps-Agent/backend
python -m pip install -r requirements-dev.txt
```

如果使用 zsh 手动安装带 `[]` 的包，需要加引号，例如：

```bash
python -m pip install "uvicorn[standard]"
```

## 启动后端

进入后端目录并激活 Conda 环境：

```bash
cd /Users/chenylnti/codefile/intership/SupportOps-Agent/backend
conda activate supportops-agent
```

启动 FastAPI 开发服务：

```bash
python -m uvicorn app.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/api/health
```

预期根路径响应：

```json
{
  "message": "SupportOps Agent API is running"
}
```

预期健康检查响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "ok",
    "service": "supportops-agent",
    "version": "0.1.0",
    "environment": "development"
  }
}
```

## LangGraph Agent 工作流

当前 `/api/chat` 已经接入一个完整教学版 LangGraph workflow：

```text
START
  |
  v
normalize_input
  |
  v
classify_intent
  |
  v
retrieve_context
  |
  v
assess_risk
  |
  +-- high risk ------> create_approval_request
  |                         |
  |                         v
  +-- need ticket ----> create_support_ticket
  |                         |
  |                         v
  +-- reply only ------> generate_reply
  |
  v
END
```

当前流程使用主流 LangGraph 状态图结构，但节点内部先用本地规则和 mock 工具实现，保证没有 API Key 也能运行。后续接入真实模型时，主要替换节点内部实现，不需要推翻图结构。

- `normalize_input`：清洗用户输入。
- `classify_intent`：识别用户问题类型、分类、风险等级和缺失字段。
- `retrieve_context`：模拟 RAG 检索，返回知识库片段。
- `assess_risk`：判断优先级、是否需要建单、是否需要人工审批。
- `create_approval_request`：模拟创建人工确认请求。
- `create_support_ticket`：模拟创建工单。
- `generate_reply`：使用 LangChain `ChatPromptTemplate` 组织回复上下文，并生成最终回复。
- `trace`：记录每个 Agent 步骤的执行结果。

## 运行测试

```bash
cd /Users/chenylnti/codefile/intership/SupportOps-Agent/backend
conda activate supportops-agent
python -m pytest tests
```

当前测试覆盖：

- `GET /`
- `GET /api/health`
- `POST /api/chat`

## 当前后端目录结构

```text
backend/
  app/
    main.py
    agents/
      supportops_graph.py
    core/
      config.py
      exceptions.py
      responses.py
    api/
      router.py
      routes/
        chat.py
        health.py
    schemas/
      chat.py
      common.py
  tests/
    test_health.py
  requirements.txt
  requirements-dev.txt
```

目录说明：

- `main.py`：FastAPI 应用入口。
- `agents/`：Agent 工作流，目前使用 LangGraph。
- `core/`：项目通用基础设施，例如配置、响应格式、异常处理。
- `api/`：API 路由入口。
- `api/routes/`：具体接口模块。
- `schemas/`：请求和响应数据结构。
- `tests/`：自动化测试。
- `requirements.txt`：运行依赖。
- `requirements-dev.txt`：开发和测试依赖。

## 当前已实现接口

### 服务根路径

```http
GET /
```

用于快速确认服务启动。

### 健康检查

```http
GET /api/health
```

用于确认 API 服务状态。后续会扩展为数据库、Redis、Chroma 等依赖服务的连接检查。

### Agent 对话

```http
POST /api/chat
```

请求示例：

```json
{
  "message": "我想申请退款"
}
```

当前响应会返回意图、分类、风险等级和 LangGraph trace。
高风险场景会额外返回 `approval` 和 `ticket`。

## 项目文档

- `SupportOps-Agent项目文档.md`：项目定位、系统架构、技术栈、开发计划。
- `SupportOps-Agent后端API文档.md`：后端接口设计。
- `docs/knowledge_base_sample/`：演示知识库样例。

## Git 开发流程

查看当前状态：

```bash
git status --short --branch
```

提交本次改动：

```bash
git add .
git commit -m "chore: initialize backend skeleton"
git push
```

以后在另一台设备同步：

```bash
git pull
```

## 下一步计划

1. 跑通后端依赖安装和 API 测试。
2. 启动 FastAPI 服务并访问 `/api/health`、`/api/chat`。
3. 添加 Docker Compose，启动 PostgreSQL、Redis、Chroma。
4. 接入 SQLAlchemy、Alembic 和基础数据库连接检查。
5. 将当前 mock RAG、mock Ticket、mock Approval 替换为数据库和真实工具调用。
6. 将规则版意图识别和回复生成替换为 LLM + Tool Calling。
