import json


class NewsProcessor:
    def __init__(self):
        with open('industry_mapping.json', 'r', encoding='utf-8') as f:
            self.industry_mapping = json.load(f)

    def process_news(self, news_list):
        processed_news = []
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            url = news.get('url', '')
            summary, impacted_industries = self._analyze_news(title, content)
            processed_news.append({
                'title': title,
                'summary': summary if summary else "暂无总结",
                'url': url,
                'impacted_industries': impacted_industries,
            })
        return processed_news

    def _analyze_news(self, title, content):
        """分析新闻，生成总结和匹配受影响行业"""
        text = (title + " " + content)[:500]
        summary = content[:100] if content else title

        impacted = []
        for industry, info in self.industry_mapping.items():
            keywords = info.get("keywords", [])
            for kw in keywords:
                if kw in title or kw in content[:200]:
                    impacted.append({
                        "industry": industry,
                        "impact_type": info.get("typical_impact", "利好"),
                    })
                    break  # 每个行业只匹配一次

        return summary, impacted
