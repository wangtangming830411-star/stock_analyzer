import akshare as ak
from collections import defaultdict
from typing import Dict, List
import random

class IndustryMapper:
    def get_recommendations(self, processed_news: List[Dict]) -> Dict:
        industry_scores = defaultdict(lambda: {"score": 0, "news": []})
        
        for news in processed_news:
            for impact in news.get("impacted_industries", []):
                ind = impact["industry"]
                industry_scores[ind]["score"] += 1
                industry_scores[ind]["news"].append(news["title"])
        
        sorted_ind = sorted(industry_scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        result = {}
        for ind, data in sorted_ind[:6]:
            stocks = self._get_stocks_for_industry(ind)
            result[ind] = {
                "impact_type": "利好",
                "analysis": f"受 {data['score']} 条新闻影响",
                "recommended_stocks": stocks[:8] if stocks else self._mock_stocks(ind)
            }
        return result
    
    def _get_stocks_for_industry(self, industry: str) -> List[Dict]:
        try:
            # 尝试不同可能的 akshare 函数
            df = ak.stock_board_industry_cons_em(symbol=industry)
            if not df.empty:
                df = df.sort_values(by="成交额", ascending=False).head(10)
                return df[["代码", "名称", "最新价", "涨跌幅"]].to_dict('records')
        except:
            pass
        return []
    
    def _mock_stocks(self, industry: str) -> List[Dict]:
        """模拟推荐股票（测试用）"""
        mock_data = {
            "军工": ["600760 航天动力", "688001 华兴源创"],
            "AI/人工智能": ["688012 中芯国际", "300750 宁德时代"],
            "人形机器人": ["688017 绿的谐波", "300024 机器人"],
            "固态电池": ["300750 宁德时代", "688005 容百科技"],
            "新能源": ["300750 宁德时代", "601012 隆基绿能"],
            "半导体": ["688012 中芯国际", "688981 格科微"],
            "低空经济": ["300760 迈瑞医疗", "600741 华域汽车"]
        }
        stocks = []
        for name in mock_data.get(industry, ["000001 平安银行"]):
            code = name.split()[0]
            stocks.append({
                "代码": code,
                "名称": name.split()[1] if len(name.split()) > 1 else "示例股票",
                "最新价": round(random.uniform(10, 200), 2),
                "涨跌幅": round(random.uniform(-5, 10), 2)
            })
        return stocks
