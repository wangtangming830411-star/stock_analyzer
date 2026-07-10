import akshare as ak


class NewsFetcher:
    def fetch_news(self, limit=50):
        """从多个来源获取财经新闻"""
        news_list = []

        # 1. 央视快讯（宏观政策类）
        try:
            df = ak.news_cctv()
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    title = str(row.get("title", ""))
                    content = str(row.get("content", ""))
                    date_str = str(row.get("date", ""))
                    news_list.append({
                        'title': title,
                        'content': content[:500],  # 截断过长内容
                        'url': '',
                    })
        except Exception as e:
            print(f"Error fetching CCTV news: {e}")

        # 2. stock_news_em（个股公告类，作为补充）
        try:
            df = ak.stock_news_em()
            if df is not None and not df.empty:
                for _, row in df.head(20).iterrows():
                    title = str(row.get("新闻标题", ""))
                    content = str(row.get("新闻内容", ""))
                    url = str(row.get("新闻链接", ""))
                    news_list.append({
                        'title': title,
                        'content': content[:500],
                        'url': url,
                    })
        except Exception as e:
            print(f"Error fetching stock news: {e}")

        return news_list[:limit]  # 限制返回数量
