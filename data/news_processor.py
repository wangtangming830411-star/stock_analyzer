import json
from typing import List, Dict

class NewsProcessor:
    def __init__(self):
        with open("industry_mapping.json", 'r', encoding='utf-8') as f:
            self.mapping = json.load(f)
    
    def process_news(self, raw_news: List[Dict]) -> List[Dict]:
        processed = []
        for news in raw_news:
            text = (news.get("title", "") + " " + news.get("content", ""))[:500]
            summary = text[:200] + "..." if len(text) > 200 else text
            impacts = self._detect_impacts(text)
            
            processed.append({
                "title": news.get("title", "无标题"),
                "summary": summary,
                "url": news.get("url", ""),
                "timestamp": news.get("timestamp", ""),
                "impacted_industries": impacts
            })
        return processed
    
    def _detect_impacts(self, text: str) -> List[Dict]:
        impacts = []
        text_lower = text.lower()
        for industry, data in self.mapping.items():
            if any(kw.lower() in text_lower for kw in data["keywords"]):
                impacts.append({
                    "industry": industry,
                    "impact_type": data["typical_impact"]
                })
        return impacts
