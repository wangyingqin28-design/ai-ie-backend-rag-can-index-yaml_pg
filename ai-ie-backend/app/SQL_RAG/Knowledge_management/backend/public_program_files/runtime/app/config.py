# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# 配置文件
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from pathlib import Path
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from dotenv import load_dotenv
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
import os
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from pydantic import Field
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from typing import Annotated, Any, AsyncGenerator, Dict, Generator, Optional
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from pydantic_settings import BaseSettings
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from app.vectorstore.connector import VectorStoreConnectorAdaptor
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
import json
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from sqlalchemy import create_engine
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
from pydantic_settings import BaseSettings
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
BASE_DIR = Path(__file__).resolve().parent.parent
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
load_dotenv(os.path.join(BASE_DIR, ".env"), verbose=True)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义封装数据或行为的类；理由依据：公共程序层所有；本行属于类 Config
class Config(BaseSettings):
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Debug mode
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    debug: bool = Field(False, alias="DEBUG")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # mssql atomic fields
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_host: str = Field("krauss", alias="DB_HOST")
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    #db_port: int = Field(1433, alias="DB_PORT")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_port: int = Field(5432, alias="DB_PORT")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_db: str = Field("AIERP", alias="DB_NAME")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_user: str = Field("ai_ie_dev", alias="DB_USER")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_password: str = Field("dev2024", alias="DB_PASSWORD")
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    #db_driver: str = Field("ODBC Driver 17 for SQL Server", alias="DB_DRIVER")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Redis atomic fields
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    redis_host: str = Field("yulith", alias="REDIS_HOST")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    redis_port: int = Field(6379, alias="REDIS_PORT")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    redis_user: str = Field("default", alias="REDIS_USER")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    redis_password: str = Field("password", alias="REDIS_PASSWORD")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Database
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    database_url: Optional[str] = Field(None, alias="DATABASE_URL")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Database connection pool settings
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_pool_size: int = Field(10, alias="DB_POOL_SIZE")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_max_overflow: int = Field(10, alias="DB_MAX_OVERFLOW")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_pool_timeout: int = Field(60, alias="DB_POOL_TIMEOUT")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_pool_recycle: int = Field(3600, alias="DB_POOL_RECYCLE")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    db_pool_pre_ping: bool = Field(True, alias="DB_POOL_PRE_PING")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Celery
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_broker_url: Optional[str] = Field(None, alias="CELERY_BROKER_URL")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_result_backend: Optional[str] = Field(None, alias="CELERY_RESULT_BACKEND")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_beat_scheduler: str = "django_celery_beat.schedulers:DatabaseScheduler"
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_worker_send_task_events: bool = True
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_task_send_sent_event: bool = True
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    celery_task_track_started: bool = True
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Vector DB
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    vector_db_type: str = Field("qdrant", alias="VECTOR_DB_TYPE")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    vector_db_context: str = Field(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
        '{"url":"http://127.0.0.1", "port":6333, "distance":"Cosine"}', alias="VECTOR_DB_CONTEXT"
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于类 Config
    )
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    EDITOR_BASE_URL: str =Field("")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Memory backend
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    memory_redis_url: Optional[str] = Field(None, alias="MEMORY_REDIS_URL")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    # Embedding
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_max_chunks_in_batch: int = Field(10, alias="EMBEDDING_MAX_CHUNKS_IN_BATCH")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_service_url: str = Field("https://api.siliconflow.cn/v1", alias="EMBEDDING_SERVICE_URL")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_model_tags: str = Field('{"multimodal": false}', alias="EMBEDDING_MODEL_TAGS")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_model: str = Field('BAAI/bge-m3', alias="EMBEDDING_MODEL")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_model_service_provider: str = Field('siliconflow', alias="EMBEDDING_MODEL_SERVICE_PROVIDER")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_custom_llm_provider: str = Field('openai', alias="EMBEDDING_CUSTOM_LLM_PROVIDER")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_service_api_key: str = Field('', alias="EMBEDDING_SERVICE_API_KEY")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    embedding_dimensions: Optional[int] = Field(None, alias="EMBEDDING_DIMENSIONS")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    #models
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    model_llm: str =Field("deepseek-ai/DeepSeek-V4-Pro", alias="MODEL_LLM")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    model_embedding: str = Field("Qwen/Qwen3-Embedding-4B", alias="MODEL_EMBED")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于类 Config
    #vlm
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    LLM_MODEL:str =Field("deepseek-ai/DeepSeek-V4-Pro",alias="VLM_LLM_MODEL")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    VISION_MODEL:str = Field("Qwen/Qwen3.5-397B-A17B",alias="VISION_MODEL")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    EMBEDDING_MODEL:str = Field("Qwen/Qwen3-VL-Embedding-8B",alias="EMBEDDING_MODEL_VLM")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于类 Config
    AUDIO_TRANSCRIPTION_MODEL:str =Field("FunAudioLLM/SenseVoiceSmall",alias="AUDIO_TRANSCRIPTION_MODEL")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 Config
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
    def __init__(self, **kwargs):
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        super().__init__(**kwargs)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # DATABASE_URL
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # if not self.database_url:
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #     self.database_url = (
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #         f"mssql+pyodbc://{self.db_user}:{self.db_password}"
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #         f"@{self.db_host}:{self.db_port}/{self.db_db}"
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #         f"?driver={self.db_driver.replace(' ', '+')}&"
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #         "trusted_connection=no&"
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #         "encrypt=no"
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        #     )
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        if not self.database_url:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            self.database_url = (
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
                f"@{self.db_host}:{self.db_port}/{self.db_db}"
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # CELERY_BROKER_URL
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        if not self.celery_broker_url:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            self.celery_broker_url = (
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
                f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/2"
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # CELERY_RESULT_BACKEND
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        if not self.celery_result_backend:
            # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            # self.celery_result_backend = self.celery_broker_url
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            self.celery_result_backend = (
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
                f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/3"
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        # MEMORY_REDIS_URL
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
        if not self.memory_redis_url:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            self.memory_redis_url = (
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
                f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/1"
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 Config.__init__
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
def get_sync_database_url(url: str):
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    """Convert async database URL to sync version."""
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    if url.startswith("mssql+aioodbc://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
        return url.replace("mssql+aioodbc://", "mssql+pyodbc://")
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    if url.startswith("postgresql+asyncpg://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    if url.startswith("postgres://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
        return url.replace("postgres://", "postgresql+psycopg2://")
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    if url.startswith("sqlite+aiosqlite://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
        return url.replace("sqlite+aiosqlite://", "sqlite://")
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_sync_database_url
    return url
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
def get_async_database_url(url: str):
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    """Convert sync database URL to async version."""
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    if url.startswith("mssql+pyodbc://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
        return url.replace("mssql+pyodbc://", "mssql+aioodbc://")
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    if url.startswith("postgresql+psycopg2://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    #PostgreSQL 标准简写，不指定驱动
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    # if url.startswith("postgresql://"):
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    #     return url.replace("postgresql://", "postgresql+asyncpg://")
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    if url.startswith("sqlite://"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
        return url.replace("sqlite://", "sqlite+aiosqlite://")
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_async_database_url
    return url
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
def new_async_engine():
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
    return create_async_engine(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        get_async_database_url(settings.database_url),
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        echo=settings.debug,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        pool_size=settings.db_pool_size,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        max_overflow=settings.db_max_overflow,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        pool_timeout=settings.db_pool_timeout,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        pool_recycle=settings.db_pool_recycle,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
        pool_pre_ping=settings.db_pool_pre_ping,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 new_async_engine
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
def new_sync_engine():
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
    return create_engine(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        get_sync_database_url(settings.database_url),
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        echo=settings.debug,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        pool_size=settings.db_pool_size,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        max_overflow=settings.db_max_overflow,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        pool_timeout=settings.db_pool_timeout,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        pool_recycle=settings.db_pool_recycle,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
        pool_pre_ping=settings.db_pool_pre_ping,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 new_sync_engine
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
settings = Config()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# Database connection pool settings from configuration
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
async_engine = new_async_engine()
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
sync_engine = new_sync_engine()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 get_async_session
async def get_async_session(engine=None) -> AsyncGenerator[AsyncSession, None]:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 get_async_session
    if engine is None:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 get_async_session
        engine = async_engine
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 get_async_session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    # [2026-07-03 16:33:01] 作用：限定文件、会话或异步资源生命周期；理由依据：公共程序层所有；本行属于异步函数 get_async_session
    async with async_session() as session:
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 get_async_session
        yield session
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
def get_sync_session(engine=None) -> Generator[Session, None, None]:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
    if engine is None:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
        engine = sync_engine
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
    sync_session = sessionmaker(engine)
    # [2026-07-03 16:33:01] 作用：限定文件、会话或异步资源生命周期；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
    with sync_session() as session:
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_sync_session
        yield session
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.config 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
def get_vector_db_connector(collection: str) -> VectorStoreConnectorAdaptor:
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
    # todo: specify the collection for different user
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
    # one person one collection
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
    ctx = json.loads(settings.vector_db_context)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
    ctx["collection"] = collection
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_vector_db_connector
    return VectorStoreConnectorAdaptor(settings.vector_db_type, ctx=ctx)
