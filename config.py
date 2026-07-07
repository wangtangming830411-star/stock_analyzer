import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()
CACHE_DIR = PROJECT_ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_DB = CACHE_DIR / "news_cache.db"

MAPPING_FILE = PROJECT_ROOT / "industry_mapping.json"
REFRESH_INTERVAL_MINUTES = 30

print("✅ 配置加载完成 - 项目根目录:", PROJECT_ROOT)
