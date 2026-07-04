# 文件解析与 DeepSeek 提取入库最终验证报告

本报告仅包含脱敏验收元数据；本轮数据库记录已保留。

```json
{
  "verified_at": "2026-07-04T11:03:37+08:00",
  "audio_sha256": "59b520dda2bdc291b5f1cc990bcc32b7da84437cf1eb147414fb47c0aa06925f",
  "audio_size": 2521277,
  "backend_port": 18320,
  "web_port": 18321,
  "transcription_model": "FunAudioLLM/SenseVoiceSmall",
  "llm_model": "deepseek-ai/DeepSeek-V4-Pro",
  "direct_health": true,
  "web_health": true,
  "proxy_health": true,
  "asset_type_id": "10001",
  "customer_id": "20260704",
  "raw_data_id": "019f2b13e56d76e993283249fdb2afb8",
  "qa_pair_ids": [
    "019f2b14e5027f7b9a5db7534caa0090",
    "019f2b14e50376859eff70303ed3359e",
    "019f2b14e50477af9d6304d6e7623068"
  ],
  "intent_ids": [
    "019f2b14e51073539113387ff3d75015",
    "019f2b14e51176a2884ac420a98648eb",
    "019f2b14e5127cfca5e82501f2729bc6"
  ],
  "pre_counts": {
    "AI_YuanShishuju": 10,
    "AI_Wendajilu": 7,
    "AI_Yitu": 16
  },
  "post_counts": {
    "AI_YuanShishuju": 11,
    "AI_Wendajilu": 10,
    "AI_Yitu": 19
  },
  "deltas": {
    "AI_YuanShishuju": 1,
    "AI_Wendajilu": 3,
    "AI_Yitu": 3
  },
  "transcript_length": 460,
  "field_checks": {
    "raw_all_fields": true,
    "qa_all_fields": true,
    "intent_all_fields": true,
    "child_foreign_keys": true
  },
  "schema_checks": {
    "AI_YuanShishuju": true,
    "AI_Wendajilu": true,
    "AI_Yitu": true
  }
}
```
