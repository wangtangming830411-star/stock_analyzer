import customtkinter as ctk
import tkinter as tk
from data.news_fetcher import NewsFetcher
from data.news_processor import NewsProcessor
from data.industry_mapper import IndustryMapper

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StockAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("A股消息驱动分析助手 v0.1")
        self.geometry("1300x850")
        
        self.fetcher = NewsFetcher()
        self.processor = NewsProcessor()
        self.mapper = IndustryMapper()
        
        self._create_ui()
    
    def _create_ui(self):
        # 顶部工具栏
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkButton(toolbar, text="🔄 刷新新闻", width=140, height=35, command=self.refresh_data).pack(side="left", padx=10)
        ctk.CTkLabel(toolbar, text="30分钟自动刷新 | 当前热点：AI、机器人、固态电池、低空经济").pack(side="left", padx=10)
        
        # 主内容区：可拖动分割面板
        paned = tk.PanedWindow(self, orient="horizontal", sashwidth=8, bg="#1E1E1E")
        paned.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 左侧新闻
        left_frame = ctk.CTkFrame(paned)
        paned.add(left_frame)
        
        ctk.CTkLabel(left_frame, text="📋 最新新闻总结（含影响标签）", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(8,5))
        
        self.news_text = tk.Text(left_frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.news_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 右侧推荐
        right_frame = ctk.CTkFrame(paned)
        paned.add(right_frame)
        
        ctk.CTkLabel(right_frame, text="🎯 今日影响行业 & 推荐股票", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(8,5))
        
        self.recommend_text = tk.Text(right_frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.recommend_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def refresh_data(self):
        self.news_text.delete(1.0, tk.END)
        self.recommend_text.delete(1.0, tk.END)
        
        self.news_text.insert(tk.END, "🔄 正在获取最新新闻...\n\n")
        self.update()
        
        raw_news = self.fetcher.fetch_all()
        processed = self.processor.process_news(raw_news)
        recommendations = self.mapper.get_recommendations(processed)
        
        # 显示新闻
        self.news_text.insert(tk.END, f"✅ 获取到 {len(processed)} 条新闻\n\n")
        for news in processed[:10]:
            self.news_text.insert(tk.END, f"📰 {news['title']}\n")
            self.news_text.insert(tk.END, f"   总结: {news['summary']}\n")
            impacts = [f"{i['industry']}({i['impact_type']})" for i in news.get("impacted_industries", [])]
            self.news_text.insert(tk.END, f"   影响: {', '.join(impacts) if impacts else '暂无明显行业影响'}\n")
            self.news_text.insert(tk.END, f"   原文: {news['url']}\n\n")
        
        # 显示推荐
        self.recommend_text.insert(tk.END, "🔍 主要影响行业及推荐股票：\n\n")
        for ind, info in recommendations.items():
            self.recommend_text.insert(tk.END, f"📌 {ind} ({info['impact_type']})\n")
            self.recommend_text.insert(tk.END, f"   {info['analysis']}\n")
            self.recommend_text.insert(tk.END, "   推荐股票（5-10只）:\n")
            for stock in info.get("recommended_stocks", [])[:8]:
                self.recommend_text.insert(tk.END, f"     • {stock.get('代码', '')} {stock.get('名称', '')}  {stock.get('最新价', '')} ({stock.get('涨跌幅', '')}%)\n")
            self.recommend_text.insert(tk.END, "\n")

if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.mainloop()
