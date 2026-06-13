:setvar EXTERNAL_DB_NAME "External_database"
:setvar EXTERNAL_DB_USER "dev"
:setvar EXTERNAL_DB_PASSWORD "123456"

-- 2026-06-11 19:42:30 新增原因：如果 External_database 不存在则创建，作用是模拟别人外部关系型数据库。
IF DB_ID(N'$(EXTERNAL_DB_NAME)') IS NULL
BEGIN
    -- 2026-06-11 19:42:30 新增原因：动态拼接库名，作用是安全处理 SQLCMD 传入的数据库名。
    DECLARE @createExternalDbSql nvarchar(max) = N'CREATE DATABASE ' + QUOTENAME(N'$(EXTERNAL_DB_NAME)');
    -- 2026-06-11 19:42:30 新增原因：执行建库语句，作用是生成 External_database。
    EXEC (@createExternalDbSql);
END
GO

-- 2026-06-11 19:42:30 新增原因：如果外部库业务登录不存在则创建，作用是转换脚本不直接使用 SA。
IF SUSER_ID(N'$(EXTERNAL_DB_USER)') IS NULL
BEGIN
    -- 2026-06-11 19:42:30 新增原因：动态拼接登录创建语句，作用是复用 docker compose 中的 EXTERNAL_DB_USER。
    DECLARE @createExternalLoginSql nvarchar(max) =
        N'CREATE LOGIN ' + QUOTENAME(N'$(EXTERNAL_DB_USER)') +
        N' WITH PASSWORD = ' + QUOTENAME(N'$(EXTERNAL_DB_PASSWORD)', '''') +
        N', CHECK_POLICY = OFF, CHECK_EXPIRATION = OFF';
    -- 2026-06-11 19:42:30 新增原因：执行登录创建语句，作用是给 External_database 转换脚本提供账号。
    EXEC (@createExternalLoginSql);
END
GO

-- 2026-06-11 19:42:30 新增原因：切换到 External_database，作用是后续对象全部落在模拟外部库。
USE [$(EXTERNAL_DB_NAME)];
GO

-- 2026-06-11 19:42:30 新增原因：如果库内用户不存在则创建，作用是把 server login 映射到 External_database。
IF USER_ID(N'$(EXTERNAL_DB_USER)') IS NULL
BEGIN
    -- 2026-06-11 19:42:30 新增原因：动态拼接用户创建语句，作用是兼容 SQLCMD 变量。
    DECLARE @createExternalUserSql nvarchar(max) =
        N'CREATE USER ' + QUOTENAME(N'$(EXTERNAL_DB_USER)') +
        N' FOR LOGIN ' + QUOTENAME(N'$(EXTERNAL_DB_USER)');
    -- 2026-06-11 19:42:30 新增原因：执行用户创建语句，作用是让 dev 能访问 External_database。
    EXEC (@createExternalUserSql);
END
GO

-- 2026-06-11 19:42:30 新增原因：只在用户还不是 db_owner 时授权，作用是初始化脚本可重复执行。
IF IS_ROLEMEMBER(N'db_owner', N'$(EXTERNAL_DB_USER)') <> 1
BEGIN
    -- 2026-06-11 19:42:30 新增原因：给外部库业务用户授权，作用是允许转换脚本读取和维护样例表。
    ALTER ROLE db_owner ADD MEMBER [$(EXTERNAL_DB_USER)];
END
GO

-- 2026-06-11 19:42:30 新增原因：创建截图字段对应的外部 QA 表，作用是跳过原清洗入库也能模拟外部库接入。
IF OBJECT_ID(N'dbo.external_qa_samples', N'U') IS NULL
BEGIN
    -- 2026-06-11 19:42:30 新增原因：定义外部表结构，作用是保留截图 JSON 的所有业务字段。
    CREATE TABLE dbo.external_qa_samples (
        -- 2026-06-12 14:40:11 新增原因：普通序号字段，作用是参与 standard_question + id 向量化并进入 payload。
        id int NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：外部行主键，作用是转换成稳定 chunk_id。
        external_id int NOT NULL PRIMARY KEY,
        -- 2026-06-11 19:42:30 新增原因：用户原始问题字段，作用是进入 retrieval_text 和 text payload。
        question nvarchar(500) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：问题场景字段，作用是生成 scene 和关键词。
        question_scene nvarchar(500) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：标准回答字段，作用是 RAG 返回证据正文。
        answer nvarchar(max) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：归一化问题字段，作用是 canonical_question 和关键词索引。
        standard_question nvarchar(500) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：回答完整度字段，作用是保留外部质量标签。
        answer_completeness nvarchar(100) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：客户侧原文证据字段，作用是保留截图 evidence.customer_text。
        customer_text nvarchar(max) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：客服侧原文证据字段，作用是保留截图 evidence.service_text。
        service_text nvarchar(max) NOT NULL,
        -- 2026-06-11 19:42:30 新增原因：创建时间字段，作用是模拟外部库审计信息。
        created_at datetime2(0) NOT NULL CONSTRAINT DF_external_qa_samples_created_at DEFAULT SYSUTCDATETIME(),
        -- 2026-06-11 19:42:30 新增原因：更新时间字段，作用是后续增量同步可判断外部行变化。
        updated_at datetime2(0) NOT NULL CONSTRAINT DF_external_qa_samples_updated_at DEFAULT SYSUTCDATETIME()
    );
END
GO

-- 2026-06-12 14:40:11 新增原因：兼容已经存在但缺少 id 的旧表，作用是不用删卷也能升级 External_database。
IF COL_LENGTH(N'dbo.external_qa_samples', N'id') IS NULL
BEGIN
    -- 2026-06-12 14:40:11 新增原因：先添加可空 id，作用是旧表有数据时 ALTER TABLE 不失败。
    ALTER TABLE dbo.external_qa_samples ADD id int NULL;
END
GO

-- 2026-06-12 14:40:11 新增原因：用 external_id 回填旧行 id，作用是改成非空列前不留下 NULL。
UPDATE dbo.external_qa_samples SET id = external_id WHERE id IS NULL;
GO

-- 2026-06-12 14:40:11 新增原因：把 id 固化为非空列，作用是和新建表结构保持一致。
IF EXISTS (
    SELECT 1
    FROM sys.columns
    WHERE object_id = OBJECT_ID(N'dbo.external_qa_samples')
      AND name = N'id'
      AND is_nullable = 1
)
BEGIN
    -- 2026-06-12 14:40:11 新增原因：执行 NOT NULL 约束变更，作用是确保三条样例都有明确序号。
    ALTER TABLE dbo.external_qa_samples ALTER COLUMN id int NOT NULL;
END
GO

-- 2026-06-11 19:57:10 新增原因：补齐现有 Qdrant 同步链路依赖表，作用是 External_database 转 Qdrant 后能回写同步状态。
IF OBJECT_ID(N'dbo.rag_rag_sync_state', N'U') IS NULL
BEGIN
    -- 2026-06-11 19:57:10 新增原因：沿用原 getai 同步状态表结构，作用是复用 update_sqlserver_sync_state 不分叉逻辑。
    CREATE TABLE dbo.rag_rag_sync_state (
        -- 2026-06-11 19:57:10 新增原因：同步记录主键，作用是同一 document_id 和 collection 可重复覆盖。
        sync_id nvarchar(80) NOT NULL PRIMARY KEY,
        -- 2026-06-11 19:57:10 新增原因：文档 ID 字段，作用是记录 External_database 表级文档来源。
        document_id nvarchar(80) NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：内容 hash 字段，作用是判断外部库内容是否变化。
        content_hash nvarchar(64) NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：同步目标字段，作用是记录 qdrant:sql_External_database。
        sync_target nvarchar(120) NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：同步状态字段，作用是标记 synced 或异常状态。
        sync_status nvarchar(40) NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：chunk 数量字段，作用是记录本次外部库转换条数。
        chunk_count int NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：是否需要重建索引字段，作用是兼容原 RAG 同步状态契约。
        needs_reindex bit NOT NULL,
        -- 2026-06-11 19:57:10 新增原因：同步消息字段，作用是保存 Qdrant 写入摘要。
        sync_message nvarchar(max) NULL,
        -- 2026-06-11 19:57:10 新增原因：创建时间字段，作用是保留同步状态审计信息。
        created_at datetime2(0) NOT NULL CONSTRAINT DF_external_rag_sync_state_created_at DEFAULT SYSUTCDATETIME(),
        -- 2026-06-11 19:57:10 新增原因：更新时间字段，作用是 MERGE 更新时记录最近同步时间。
        updated_at datetime2(0) NOT NULL CONSTRAINT DF_external_rag_sync_state_updated_at DEFAULT SYSUTCDATETIME()
    );
END
GO

-- 2026-06-11 19:42:30 新增原因：删除固定三条样例旧数据，作用是初始化脚本重复运行时保持结果确定。
DELETE FROM dbo.external_qa_samples WHERE external_id IN (1, 2, 3);
GO

-- 2026-06-11 19:42:30 新增原因：插入截图第一条二次工艺 QA，作用是验证外部库到 Qdrant 的标准字段映射。
INSERT INTO dbo.external_qa_samples (
    id, -- 2026-06-12 14:40:11 新增原因：写入第一条普通序号，作用是参与 standard_question + id 向量化。
    external_id,
    question,
    question_scene,
    answer,
    standard_question,
    answer_completeness,
    customer_text,
    service_text
) VALUES (
    1, -- 2026-06-12 14:40:11 新增原因：第一条普通序号值，作用是满足用户要求的 1/2/3 编号。
    1,
    N'二次工艺流程不对，是后补的，不是发出去的时候做',
    N'二次工艺外发流程，涉及到加工单的创建和收货',
    N'正常流程是发出去的时候先做好二次工艺单，把价格数量保存起来，打单给外发部门。等有差异再反馈。二次工艺应该由外发部门先建单，再按实际差异处理。',
    N'二次工艺的正确操作流程是什么？',
    N'完整',
    N'那也就是相当于我们现在的二次公益，是相当于你们的流程之后对补的。，他不是说再发出去的时候做',
    N'你要发出去的时候先做好那个二次公益单，然后把那个价格数量保存起来，先把那个单打起来，然后给到那个发货'
);
GO

-- 2026-06-11 19:42:30 新增原因：插入截图第二条采购单权限 QA，作用是验证权限类问题也能进入统一 CanonicalChunk。
INSERT INTO dbo.external_qa_samples (
    id, -- 2026-06-12 14:40:11 新增原因：写入第二条普通序号，作用是参与 standard_question + id 向量化。
    external_id,
    question,
    question_scene,
    answer,
    standard_question,
    answer_completeness,
    customer_text,
    service_text
) VALUES (
    2, -- 2026-06-12 14:40:11 新增原因：第二条普通序号值，作用是满足用户要求的 1/2/3 编号。
    2,
    N'系统里采购单导出来后，其他人看不到，导致漏下单',
    N'采购流程，采购订单单的创建和权限管理',
    N'可能是权限设置问题，设置了私有权导致单据不共享。需要检查权限设置，确保单据共享。',
    N'采购单导出后其他人看不到怎么办？',
    N'部分完整',
    N'小兵呢，他以为我没下，因为我的单就没导嘛，然后呢去系统，其实我有一张单就导出来了。在我的电脑里面系统里看不到',
    N'有可能是设置了私有私有权了，就是单据不共享。知道吧？那这个就是另外外一回事了，就不是说看不到，所以说要检查权限'
);
GO

-- 2026-06-11 19:42:30 新增原因：插入截图第三条 BOM 变更 QA，作用是验证业务流程类问题进入外部 collection。
INSERT INTO dbo.external_qa_samples (
    id, -- 2026-06-12 14:40:11 新增原因：写入第三条普通序号，作用是参与 standard_question + id 向量化。
    external_id,
    question,
    question_scene,
    answer,
    standard_question,
    answer_completeness,
    customer_text,
    service_text
) VALUES (
    3, -- 2026-06-12 14:40:11 新增原因：第三条普通序号值，作用是满足用户要求的 1/2/3 编号。
    3,
    N'BOM表变更频繁，刷新单据很繁琐',
    N'BOM管理和采购流程，销售订单单和采购申请单的变更',
    N'系统设计上不能自动刷新，必须人为主动刷新，以避免不可控的变更。操作繁琐是必要的，为了确保变更的可控性和可追踪性。',
    N'BOM变更频繁导致刷新单据繁琐怎么办？',
    N'完整',
    N'系统不智能的，就是随便改了一个东西，就要刷很多单，能不能就刷两三个地方要刷三三个销售订单单，采购申请',
    N'系统你就刷最新的嘛..所以你没办法去说哎，我要让你人为的主观的去判断，我是要改这张去下这张？是不是对吧'
);
GO

-- 2026-06-11 19:42:30 新增原因：输出样例数量，作用是 docker logs 能直接看到 External_database 初始化结果。
SELECT COUNT(1) AS external_sample_rows FROM dbo.external_qa_samples;
GO
