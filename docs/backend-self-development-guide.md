# Backend Self-Development Guide

这份文档是给“自己从零开发 `backend/`，把 `backend_sample/` 只当参考实现”的场景准备的。

目标不是直接把代码抄出来，而是建立一套你自己能重复使用的开发方法：

```text
先理解接口 -> 再搭骨架 -> 再做最小闭环 -> 再接 Agent workflow -> 再接真实依赖
```

## 1. 你的开发原则

你现在的项目建议分成两个角色：

```text
backend_sample/   参考实现，只读、对照、学习
backend/          你自己真正手写的新后端
```

推荐工作方式：

1. 先在 `backend/` 自己写一版。
2. 卡住时，再去 `backend_sample/` 对照目录、函数职责和命名方式。
3. 不要整文件复制；最多只借鉴思路、顺序和模块边界。

这样做的好处：

- 你会真正理解为什么这样分层；
- 你能知道每个文件是怎么一步步长出来的；
- 后面面试时你能讲清楚“自己是怎么搭起来的”。

## 2. 学习公式

以后你学任意后端框架或 Agent 框架，都建议按这个顺序：

```text
官网 overview
-> quickstart
-> tutorial
-> API guide
-> examples
-> integrations
```

不要一开始就：

- 搜一堆过期博客；
- 看别人拼好的大项目；
- 先追求“完整功能”而跳过最小例子。

## 3. 这个项目的学习顺序

对 `SupportOps Agent`，建议按下面顺序学和写：

### Phase A：先学 FastAPI 外壳

目标：

- 会创建 `FastAPI()` 应用；
- 会写 `@app.get()` 和 `@app.post()`；
- 会收请求体；
- 会返回 JSON；
- 会用 `uvicorn` 启动服务。

你应该先独立完成：

```text
GET /
GET /api/health
POST /api/chat
```

### Phase B：再学 LangChain 基础

目标：

- 知道 prompt 是怎么组织的；
- 知道 model 是怎么接入的；
- 知道 tool 是怎么被封装的；
- 知道为什么 prompt / model / tool 要分开。

这一步先不要求你做完整 Agent，只要求你理解最小单元。

### Phase C：再学 LangGraph

目标：

- 知道 `State` 是什么；
- 知道 `Node` 是什么；
- 知道 `Edge` 是什么；
- 知道 `Conditional Edge` 是什么；
- 知道 workflow 是怎么根据状态分支的。

你要先从一个最小 graph 开始：

```text
START -> classify_intent -> END
```

不要一上来就写一个七八个节点的完整图。

### Phase D：最后接真实依赖

包括：

- PostgreSQL
- Redis
- Chroma / pgvector
- LangChain provider
- OpenAI / 其他模型 API

核心原则是：

```text
先把结构搭对，再把真实依赖塞进去
```

## 4. 官方资料入口

建议优先只看官方资料。

### FastAPI

- First Steps: [https://fastapi.tiangolo.com/tutorial/first-steps/](https://fastapi.tiangolo.com/tutorial/first-steps/)
- Learn: [https://fastapi.tiangolo.com/learn/](https://fastapi.tiangolo.com/learn/)

### LangGraph

- Overview: [https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)
- Quickstart: [https://docs.langchain.com/oss/python/langgraph/quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- Graph API: [https://docs.langchain.com/oss/python/langgraph/use-graph-api](https://docs.langchain.com/oss/python/langgraph/use-graph-api)

### LangChain

- Install: [https://docs.langchain.com/oss/python/langchain/install](https://docs.langchain.com/oss/python/langchain/install)
- Overview: [https://docs.langchain.com/oss/python/langchain/overview](https://docs.langchain.com/oss/python/langchain/overview)
- Integrations: [https://docs.langchain.com/oss/python/integrations/providers/overview](https://docs.langchain.com/oss/python/integrations/providers/overview)

## 5. 自己开发时的固定下笔顺序

这部分最重要。以后你自己写后端，建议每次都按这个顺序来。

### Step 1：先定义接口，不写业务逻辑

先列出你要暴露的接口：

```text
GET /
GET /api/health
POST /api/chat
```

如果以后扩展，再加：

```text
POST /api/documents/upload
POST /api/documents/search
POST /api/tickets
```

先把输入输出想清楚，再写代码。

### Step 2：先搭目录，不急着写实现

建议先创建：

```text
backend/
  app/
    main.py
    core/
    api/
      routes/
    schemas/
    agents/
    tools/
  tests/
```

目录先出来，脑子里才会有模块边界。

### Step 3：只写最小后端骨架

第一次只写这几个文件：

```text
app/main.py
app/core/config.py
app/core/responses.py
app/core/exceptions.py
app/api/router.py
app/api/routes/health.py
```

目标只有一个：

```text
服务能启动
浏览器能访问 /
浏览器能访问 /api/health
```

### Step 4：再写 `/api/chat`

这时先不要接 Agent。

先做到：

- 有 `ChatRequest`；
- 路由能接收 `message`；
- 能返回固定内容。

这样你能单独确认：

- request body 没问题；
- schema 没问题；
- route 没问题。

### Step 5：把 Agent workflow 单独写在 `agents/`

不要把 Agent 逻辑直接写在 route 里。

建议先写最小 graph：

```text
START -> classify_intent -> END
```

然后让 `/api/chat` 去调用：

```text
run_supportops_agent(message)
```

### Step 6：每个 node 只做一件事

例如：

- `normalize_input`：只清洗输入
- `classify_intent`：只做分类
- `retrieve_context`：只做检索
- `assess_risk`：只做风险判断
- `generate_reply`：只做回复生成

这是你后期维护 LangGraph 最重要的习惯。

### Step 7：tools 先写 mock 版

一开始不要急着接数据库和向量库。

先写：

- `knowledge_tools.py`
- `ticket_tools.py`
- `approval_tools.py`

先返回假数据，把 workflow 跑通。

以后再替换成真实依赖：

- mock knowledge -> Chroma / pgvector
- mock ticket -> PostgreSQL
- mock approval -> approvals 表

### Step 8：每完成一层就验证

养成这个节奏：

```text
写一点 -> 跑一下 -> 再写一点
```

不要这样：

```text
先写十几个文件 -> 最后一起运行
```

每一层对应的验证方式：

- 写完 `main.py`：启动 `uvicorn`
- 写完 `/api/health`：浏览器访问接口
- 写完 schema：发一个 POST 请求
- 写完 graph：直接在 Python 里调用 workflow
- 写完 route：写 pytest

## 6. 你可以照抄的开发节奏

如果你准备自己从零重写 `backend/`，建议按下面的节奏：

### Day 1

- 建立目录结构；
- 写 `main.py`；
- 写 `config.py`；
- 写 `responses.py`；
- 写 `health.py`；
- 启动 FastAPI；
- 打开 `/` 和 `/api/health`。

### Day 2

- 写 `schemas/chat.py`；
- 写 `api/routes/chat.py`；
- 先返回固定结果；
- 写 `tests/test_health.py` 和最小 chat 测试。

### Day 3

- 写最小 LangGraph；
- 先做 `START -> classify_intent -> END`；
- 让 `/api/chat` 接到 graph。

### Day 4

- 增加 `normalize_input`；
- 增加 `retrieve_context`；
- 增加 `generate_reply`；
- 加 trace。

### Day 5

- 加 `assess_risk`；
- 加 `create_support_ticket`；
- 加 `create_approval_request`；
- 把 graph 扩成完整工作流。

### Day 6+

- 接 PostgreSQL；
- 接 Redis；
- 接 Chroma；
- 用真实依赖替换 mock tools。

## 7. 遇到不会写时怎么办

你自己开发时，不要直接问“整个项目怎么做”，而要把问题切小。

推荐你每次只问自己一个问题：

### 我当前卡在哪一层？

例如：

- 是 route 不会写？
- 是 schema 不知道怎么定义？
- 是 graph 不会加 node？
- 是 conditional edge 不会分支？
- 是 tool 不知道返回什么结构？

问题越小，越容易解决。

### 推荐的排查顺序

```text
先看报错
-> 定位是 route / schema / graph / tool 哪一层
-> 看官方 quickstart 是否有对应例子
-> 再回到你的代码里改最小一处
```

## 8. 怎么使用 `backend_sample/`

`backend_sample/` 的正确用途是：

### 可以看什么

- 看目录结构怎么分层；
- 看文件命名方式；
- 看函数职责怎么拆；
- 看 route 怎么调用 graph；
- 看 graph 怎么调用 tools。

### 不建议怎么用

- 不要整文件复制到 `backend/`；
- 不要边看边抄到一个字不差；
- 不要还没自己想清楚就直接改名字提交。

### 最好的用法

1. 先自己写。
2. 卡住时只打开对应参考文件。
3. 看它解决的是哪一类问题。
4. 合上参考，再自己重写一遍。

## 9. 一个长期有效的开发公式

以后你自己写项目，脑子里一直用这条公式就够了：

```text
先定义接口
-> 再定义输入输出
-> 再写最小实现
-> 再接 workflow
-> 再接 tools
-> 最后接真实数据库和模型
```

再简化一点，就是：

```text
先壳子
-> 再骨架
-> 再最小功能
-> 再完整工作流
-> 再真实依赖
```

## 10. 你下一步该怎么做

如果你接下来要自己创建新的 `backend/`，建议你现在只做下面几件事：

1. 在仓库根目录新建 `backend/`。
2. 只创建目录，不写复杂逻辑。
3. 先完成：
   - `app/main.py`
   - `app/core/config.py`
   - `app/core/responses.py`
   - `app/api/routes/health.py`
4. 启动后端并访问 `/api/health`。
5. 完成后，再开始写 `/api/chat`。

如果你能自己完成到这一步，后面 LangGraph 的学习就会顺很多。

