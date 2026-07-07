import sqlite3
import json
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        self.conn = sqlite3.connect("cache/news_cache.db", check_same_thread=False)  # 修复多线程问题
        self._init_db()
    
    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                url TEXT,
                timestamp TEXT,
                impacts TEXT
            )
        ''')
        self.conn.commit()
    
    def save_news(self, processed_news):
        for news in processed_news:
            impacts = json.dumps(news.get("impacted_industries", []))
            self.conn.execute('''
                INSERT OR REPLACE INTO news (title, summary, url, timestamp, impacts)
                VALUES (?, ?, ?, ?, ?)
            ''', (news["title"], news["summary"], news["url"], news["timestamp"], impacts))
        self.conn.commit()
    
    def get_recent_news(self, hours=24):
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        cursor = self.conn.execute('''
            SELECT title, summary, url, timestamp, impacts 
            FROM news WHERE timestamp > ? ORDER BY timestamp DESC
        ''', (cutoff,))
        rows = cursor.fetchall()
        return [{"title": r[0], "summary": r[1], "url": r[2], "timestamp": r[3], "impacted_industries": json.loads(r[4])} for r in rows]
