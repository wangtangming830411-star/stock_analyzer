import akshare as ak
import time
from typing import List, Dict
import random

class NewsFetcher:
    def fetch_akshare_news(self, stock_code: str = "000001") -> List[Dict]:
        try:
            df = ak.stock_news_em(stock=stock_code)
            news_list = []
            for _, row in df.iterrows():
                news_list.append({
                    "title": row.get("title", "新闻标题"),
                    "url": row.get("url", ""),
                    "source": "东方财富",
                    "timestamp": row.get("datetime", ""),
                })
            return news_list
        except Exception as e:
            print(f"akshare获取失败，使用模拟数据: {e}")
            return self._mock_news()
    
    def _mock_news(self) -> List[Dict]:
        """模拟数据（测试用）"""
        return [
            {"title": "央行宣布降准0.5个百分点", "url": "https://example.com/1", "source": "模拟", "timestamp": "刚刚"},
            {"title": "固态电池技术取得重大突破", "url": "https://example.com/2", "source": "模拟", "timestamp": "10分钟前"},
            {"title": "军工企业获得大额订单", "url": "https://example.com/3", "source": "模拟", "timestamp": "30分钟前"},
        ]
    
    def fetch_all(self) -> List[Dict]:
        all_news = self.fetch_akshare_news()
        # 补充模拟数据确保有内容
        if len(all_news) == 0:
            all_news = self._mock_news()
        return all_news[:20]
