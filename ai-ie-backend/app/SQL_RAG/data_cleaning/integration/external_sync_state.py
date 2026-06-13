# -*- coding: utf-8 -*-
"""外部数据源同步状态存储。"""

# 2026-06-13 17:18:04 新增：导入 sqlite3，作用是把同步状态持久化到本地文件；理由是后端重启后不能丢失已同步 point 身份。
import sqlite3
# 2026-06-13 17:18:04 新增：导入 Lock，作用是保护 SQLite 和内存状态；理由是后台同步线程可能和健康检查同时读取状态。
from threading import Lock
# 2026-06-13 17:18:04 新增：导入 datetime/timezone，作用是记录 UTC 同步时间；理由是排查外部库同步延迟需要时间戳。
from datetime import datetime, timezone
# 2026-06-13 17:18:04 新增：导入 Path，作用是定位状态数据库文件；理由是状态文件要固定放在 SQL_RAG 下。
from pathlib import Path
# 2026-06-13 17:18:04 新增：导入 Any，作用是统一状态摘要类型；理由是健康检查返回 dict。
from typing import Any


# 2026-06-13 17:18:04 新增：生成当前 UTC 时间文本；作用是写入状态表；理由是同步状态必须可审计。
def utc_now_text() -> str:
    # 2026-06-13 17:18:04 新增：返回 ISO 时间；作用是跨系统稳定展示；理由是 Windows/SQLite 本地时区不可靠。
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# 2026-06-13 17:18:04 新增：定义内存状态存储；作用是给单测和临时验证使用；理由是测试不应写本地 SQLite。
class InMemoryExternalSyncStateStore:
    # 2026-06-13 17:18:04 新增：初始化内存状态；作用是保存 profile/source_pk 到状态的映射；理由是 worker 测试需要模拟已同步记录。
    def __init__(self) -> None:
        # 2026-06-13 17:18:04 新增：创建锁；作用是保护状态字典；理由是接口和 SQLite 版保持线程安全语义。
        self._lock = Lock()
        # 2026-06-13 17:18:04 新增：创建状态字典；作用是存 row_hash/point_id/status/deleted；理由是同步逻辑只依赖这些字段。
        self._rows: dict[tuple[str, str], dict[str, Any]] = {}

    # 2026-06-13 17:18:04 新增：读取行 hash；作用是判断外部行是否变化；理由是没变化就不重复写 Qdrant。
    def get_row_hash(self, profile_name: str, source_pk: str) -> str:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是避免并发读写；理由是 worker 和测试断言可能交错。
        with self._lock:
            # 2026-06-13 17:18:04 新增：返回 hash 或空；作用是未同步过时触发 upsert；理由是首次同步必须入库。
            return str(self._rows.get((profile_name, source_pk), {}).get("row_hash") or "")

    # 2026-06-13 17:18:04 新增：读取 point id；作用是删除 Qdrant stale point；理由是关系库源行删除后要清理向量点。
    def get_point_id(self, profile_name: str, source_pk: str) -> str:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是保持线程安全；理由是后台同步长期运行。
        with self._lock:
            # 2026-06-13 17:18:04 新增：返回 point id；作用是传给 Qdrant delete；理由是 Qdrant 删除使用 point id。
            return str(self._rows.get((profile_name, source_pk), {}).get("point_id") or "")

    # 2026-06-13 17:18:04 新增：保存同步成功状态；作用是记录 hash 和 point id；理由是下轮轮询可跳过未变化行。
    def save_row_synced(self, profile_name: str, source_pk: str, row_hash: str, point_id: str, status: str) -> None:
        # 2026-06-13 17:18:04 新增：加锁写入；作用是保持状态一致；理由是状态是幂等判断依据。
        with self._lock:
            # 2026-06-13 17:18:04 新增：写入状态；作用是标记该 source_pk 已入库；理由是 Qdrant upsert 成功后才允许保存。
            self._rows[(profile_name, source_pk)] = {
                # 2026-06-13 17:18:04 新增：保存 row_hash；作用是检测修改；理由是外部 PG 未必提供可靠 updated_at。
                "row_hash": row_hash,
                # 2026-06-13 17:18:04 新增：保存 point_id；作用是后续删除；理由是 Qdrant 删除需要稳定 id。
                "point_id": point_id,
                # 2026-06-13 17:18:04 新增：保存状态；作用是健康检查可读；理由是排查同步结果需要。
                "status": status,
                # 2026-06-13 17:18:04 新增：标记未删除；作用是 active 列表过滤；理由是删除后不应再算活跃。
                "deleted": False,
                # 2026-06-13 17:18:04 新增：记录时间；作用是审计；理由是外部实时同步要能看最后更新时间。
                "last_synced_at": utc_now_text(),
            }

    # 2026-06-13 17:18:04 新增：列出活跃 source_pk；作用是 snapshot_diff 删除 stale point；理由是 PG 硬删行后只能靠本地状态发现。
    def list_active_source_pks(self, profile_name: str) -> set[str]:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是返回一致快照；理由是删除判断不能边读边变。
        with self._lock:
            # 2026-06-13 17:18:04 新增：返回未删除 key；作用是和本轮源库 key 比较；理由是找出 Qdrant 旧 point。
            return {source_pk for (row_profile, source_pk), row in self._rows.items() if row_profile == profile_name and not row.get("deleted")}

    # 2026-06-13 17:18:04 新增：标记删除；作用是避免重复删除同一个 stale point；理由是 Qdrant 删除成功后状态也要更新。
    def mark_deleted(self, profile_name: str, source_pk: str) -> None:
        # 2026-06-13 17:18:04 新增：加锁写入；作用是更新删除标记；理由是 snapshot_diff 下轮不应重复删。
        with self._lock:
            # 2026-06-13 17:18:04 新增：读取旧状态；作用是保留 point_id；理由是排查时知道删的是哪个 point。
            row = self._rows.setdefault((profile_name, source_pk), {})
            # 2026-06-13 17:18:04 新增：写 deleted 标记；作用是从 active 列表移除；理由是源库已不存在或软删。
            row["deleted"] = True
            # 2026-06-13 17:18:04 新增：写状态；作用是健康检查可读；理由是区分已同步和已删除。
            row["status"] = "deleted"
            # 2026-06-13 17:18:04 新增：写更新时间；作用是审计删除时间；理由是实时同步要可追踪。
            row["last_synced_at"] = utc_now_text()

    # 2026-06-13 17:18:04 新增：返回 profile 状态摘要；作用是给健康检查展示；理由是用户需要确认后台同步是否在跑。
    def summary(self, profile_name: str) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是汇总当前状态；理由是避免读取半更新数据。
        with self._lock:
            # 2026-06-13 17:18:04 新增：筛选 profile 行；作用是计算该外部库状态；理由是多 profile 共用状态存储。
            rows = [row for (row_profile, _), row in self._rows.items() if row_profile == profile_name]
            # 2026-06-13 17:18:04 新增：返回摘要；作用是健康检查可读；理由是前后端服务要能看到同步状态。
            return {
                "profile": profile_name,
                "tracked_count": len(rows),
                "active_count": sum(1 for row in rows if not row.get("deleted")),
                "deleted_count": sum(1 for row in rows if row.get("deleted")),
                "last_synced_at": max((str(row.get("last_synced_at") or "") for row in rows), default=""),
            }


# 2026-06-13 17:18:04 新增：定义 SQLite 状态存储；作用是服务重启后继续保留外部库同步状态；理由是实时同步不能退回离线一次性脚本。
class SQLiteExternalSyncStateStore:
    # 2026-06-13 17:18:04 新增：初始化 SQLite 存储；作用是创建状态数据库；理由是后台 worker 长期运行需要持久化。
    def __init__(self, database_path: Path) -> None:
        # 2026-06-13 17:18:04 新增：保存数据库路径；作用是后续连接复用；理由是状态文件位置由 manager 决定。
        self.database_path = database_path
        # 2026-06-13 17:18:04 新增：创建锁；作用是串行化 SQLite 写入；理由是 SQLite 单文件写入需要保护。
        self._lock = Lock()
        # 2026-06-13 17:18:04 新增：确保父目录存在；作用是第一次启动也能建库；理由是 runtime_logs 可能不存在。
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        # 2026-06-13 17:18:04 新增：初始化表结构；作用是保证状态表存在；理由是后端服务启动不再手工建表。
        self._init_schema()

    # 2026-06-13 17:18:04 新增：打开 SQLite 连接；作用是集中设置 row_factory；理由是摘要读取需要按列名访问。
    def _connect(self) -> sqlite3.Connection:
        # 2026-06-13 17:18:04 新增：创建连接；作用是访问状态数据库；理由是每个方法短连接避免长期锁。
        connection = sqlite3.connect(self.database_path)
        # 2026-06-13 17:18:04 新增：设置 row_factory；作用是返回 sqlite3.Row；理由是字段访问更清晰。
        connection.row_factory = sqlite3.Row
        # 2026-06-13 17:18:04 新增：返回连接；作用是给调用方上下文管理；理由是 SQLite 资源要及时关闭。
        return connection

    # 2026-06-13 17:18:04 新增：初始化表结构；作用是持久化 source_pk/hash/point_id；理由是实时同步状态不能丢。
    def _init_schema(self) -> None:
        # 2026-06-13 17:18:04 新增：加锁建表；作用是避免并发初始化；理由是服务启动可能多线程健康检查。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是执行 DDL；理由是 SQLite 表需要首次创建。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：创建状态表；作用是记录每个外部库主键对应 point；理由是删除和幂等依赖该表。
                connection.execute(
                    """
CREATE TABLE IF NOT EXISTS external_source_sync_state (
    profile_name TEXT NOT NULL,
    source_pk TEXT NOT NULL,
    row_hash TEXT NOT NULL,
    point_id TEXT NOT NULL,
    status TEXT NOT NULL,
    deleted INTEGER NOT NULL DEFAULT 0,
    last_synced_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (profile_name, source_pk)
);
"""
                )
                # 2026-06-13 17:18:04 新增：创建 profile 索引；作用是加快健康检查和 snapshot_diff；理由是多外部库共用同一状态库。
                connection.execute("CREATE INDEX IF NOT EXISTS idx_external_sync_profile_deleted ON external_source_sync_state(profile_name, deleted);")

    # 2026-06-13 17:18:04 新增：读取行 hash；作用是判断是否需要重新 upsert；理由是未变化行不能无限重写 Qdrant。
    def get_row_hash(self, profile_name: str, source_pk: str) -> str:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是保持 SQLite 访问串行；理由是状态库是单文件。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是查询状态；理由是短连接减少锁持有。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：查询 row_hash；作用是幂等比较；理由是外部库变化检测需要本地快照。
                row = connection.execute(
                    "SELECT row_hash FROM external_source_sync_state WHERE profile_name = ? AND source_pk = ? AND deleted = 0",
                    (profile_name, source_pk),
                ).fetchone()
        # 2026-06-13 17:18:04 新增：返回 hash 或空；作用是未同步时触发写入；理由是首次同步必须入库。
        return str(row["row_hash"] if row else "")

    # 2026-06-13 17:18:04 新增：读取 point id；作用是删除旧 Qdrant point；理由是 source_pk 到 point_id 的映射必须持久化。
    def get_point_id(self, profile_name: str, source_pk: str) -> str:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是避免并发访问；理由是 SQLite 单文件要谨慎。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是查询 point_id；理由是删除 Qdrant 需要它。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：查询 point_id；作用是定位向量点；理由是硬删源行后只能靠本地状态找回。
                row = connection.execute(
                    "SELECT point_id FROM external_source_sync_state WHERE profile_name = ? AND source_pk = ?",
                    (profile_name, source_pk),
                ).fetchone()
        # 2026-06-13 17:18:04 新增：返回 point_id 或空；作用是没有历史时跳过删除；理由是状态表可能没有旧记录。
        return str(row["point_id"] if row else "")

    # 2026-06-13 17:18:04 新增：保存同步成功状态；作用是持久化 row_hash/point_id；理由是重启后继续增量同步。
    def save_row_synced(self, profile_name: str, source_pk: str, row_hash: str, point_id: str, status: str) -> None:
        # 2026-06-13 17:18:04 新增：生成当前时间；作用是写入同步时间；理由是健康检查展示最后同步。
        now_text = utc_now_text()
        # 2026-06-13 17:18:04 新增：加锁写入；作用是避免并发 UPSERT 冲突；理由是状态是同步正确性的根。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是执行 UPSERT；理由是同一 source_pk 可被修改后重复同步。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：写入或更新状态；作用是标记已同步；理由是 Qdrant 成功后才能记录。
                connection.execute(
                    """
INSERT INTO external_source_sync_state(profile_name, source_pk, row_hash, point_id, status, deleted, last_synced_at, updated_at)
VALUES (?, ?, ?, ?, ?, 0, ?, ?)
ON CONFLICT(profile_name, source_pk) DO UPDATE SET
    row_hash = excluded.row_hash,
    point_id = excluded.point_id,
    status = excluded.status,
    deleted = 0,
    last_synced_at = excluded.last_synced_at,
    updated_at = excluded.updated_at;
""",
                    (profile_name, source_pk, row_hash, point_id, status, now_text, now_text),
                )

    # 2026-06-13 17:18:04 新增：列出活跃 source_pk；作用是 snapshot_diff 检测硬删除；理由是源库删除不会主动通知我们。
    def list_active_source_pks(self, profile_name: str) -> set[str]:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是拿到一致快照；理由是删除差异计算需要稳定输入。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是查询活跃状态；理由是 SQLite 短连接安全。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：查询未删除 key；作用是和源库现有 key 比较；理由是发现 stale point。
                rows = connection.execute(
                    "SELECT source_pk FROM external_source_sync_state WHERE profile_name = ? AND deleted = 0",
                    (profile_name,),
                ).fetchall()
        # 2026-06-13 17:18:04 新增：返回 key 集合；作用是供 worker 计算差集；理由是集合差异最直接。
        return {str(row["source_pk"]) for row in rows}

    # 2026-06-13 17:18:04 新增：标记删除；作用是持久化删除状态；理由是 Qdrant 删除后下轮不应重复删。
    def mark_deleted(self, profile_name: str, source_pk: str) -> None:
        # 2026-06-13 17:18:04 新增：生成当前时间；作用是记录删除同步时间；理由是排查 stale point 清理需要。
        now_text = utc_now_text()
        # 2026-06-13 17:18:04 新增：加锁写入；作用是保护状态更新；理由是 SQLite 写入需要串行。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是执行 UPDATE；理由是删除不需要抹掉历史 point id。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：更新删除标记；作用是从 active 集合移除；理由是避免重复删除 Qdrant。
                connection.execute(
                    """
UPDATE external_source_sync_state
SET deleted = 1, status = 'deleted', updated_at = ?, last_synced_at = ?
WHERE profile_name = ? AND source_pk = ?;
""",
                    (now_text, now_text, profile_name, source_pk),
                )

    # 2026-06-13 17:18:04 新增：返回 profile 摘要；作用是暴露给健康检查；理由是用户要看到后台同步是否持续运行。
    def summary(self, profile_name: str) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：加锁读取；作用是保持摘要一致；理由是状态可能正被 worker 更新。
        with self._lock:
            # 2026-06-13 17:18:04 新增：打开连接；作用是查询统计；理由是健康检查不应加载全部数据。
            with self._connect() as connection:
                # 2026-06-13 17:18:04 新增：查询聚合统计；作用是返回 tracked/active/deleted；理由是同步状态需要可观测。
                row = connection.execute(
                    """
SELECT
    COUNT(*) AS tracked_count,
    SUM(CASE WHEN deleted = 0 THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN deleted = 1 THEN 1 ELSE 0 END) AS deleted_count,
    MAX(last_synced_at) AS last_synced_at
FROM external_source_sync_state
WHERE profile_name = ?;
""",
                    (profile_name,),
                ).fetchone()
        # 2026-06-13 17:18:04 新增：返回摘要 dict；作用是给 manager/status 使用；理由是不要暴露 SQLite row 给上层。
        return {
            "profile": profile_name,
            "tracked_count": int(row["tracked_count"] or 0),
            "active_count": int(row["active_count"] or 0),
            "deleted_count": int(row["deleted_count"] or 0),
            "last_synced_at": str(row["last_synced_at"] or ""),
        }
