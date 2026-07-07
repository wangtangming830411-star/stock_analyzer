import customtkinter as ctk
import tkinter as tk
from data.news_fetcher import NewsFetcher
from data.news_processor import NewsProcessor
from data.industry_mapper import IndustryMapper
from data.cache_manager import CacheManager
import threading
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StockAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("A股消息驱动分析助手 v0.2")
        self.geometry("1300x850")
        
        self.fetcher = NewsFetcher()
        self.processor = NewsProcessor()
        self.mapper = IndustryMapper()
        self.cache = CacheManager()
        
        self._create_ui()
        self.auto_refresh()  # 启动自动刷新
    
    def _create_ui(self):
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkButton(toolbar, text="🔄 手动刷新", width=140, height=35, command=self.refresh_data).pack(side="left", padx=10)
        self.status_label = ctk.CTkLabel(toolbar, text="就绪")
        self.status_label.pack(side="left", padx=10)
        
        paned = tk.PanedWindow(self, orient="horizontal", sashwidth=8, bg="#1E1E1E")
        paned.pack(fill="both", expand=True, padx=10, pady=5)
        
        left_frame = ctk.CTkFrame(paned)
        paned.add(left_frame)
        ctk.CTkLabel(left_frame, text="📋 最新新闻总结", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(8,5))
        self.news_text = tk.Text(left_frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.news_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        right_frame = ctk.CTkFrame(paned)
        paned.add(right_frame)
        ctk.CTkLabel(right_frame, text="🎯 今日影响 & 推荐", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(8,5))
        self.recommend_text = tk.Text(right_frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.recommend_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def refresh_data(self, use_cache=False):
        self.news_text.delete(1.0, tk.END)
        self.recommend_text.delete(1.0, tk.END)
        self.status_label.configure(text="正在刷新...")
        self.update()
        
        if use_cache:
            processed = self.cache.get_recent_news()
        else:
            raw_news = self.fetcher.fetch_all()
            processed = self.processor.process_news(raw_news)
            self.cache.save_news(processed)
        
        recommendations = self.mapper.get_recommendations(processed)
        
        # 显示新闻
        self.news_text.insert(tk.END, f"✅ 显示 {len(processed)} 条新闻\n\n")
        for news in processed[:10]:
            self.news_text.insert(tk.END, f"📰 {news['title']}\n")
            self.news_text.insert(tk.END, f"   总结: {news['summary']}\n")
            impacts = [f"{i['industry']}({i['impact_type']})" for i in news.get("impacted_industries", [])]
            self.news_text.insert(tk.END, f"   影响: {', '.join(impacts) if impacts else '暂无'}\n")
            self.news_text.insert(tk.END, f"   原文: {news.get('url', '')}\n\n")
        
        # 显示推荐
        self.recommend_text.insert(tk.END, "🔍 主要影响行业及推荐：\n\n")
        for ind, info in recommendations.items():
            self.recommend_text.insert(tk.END, f"📌 {ind} ({info['impact_type']})\n")
            self.recommend_text.insert(tk.END, f"   {info['analysis']}\n")
            self.recommend_text.insert(tk.END, "   推荐股票:\n")
            for stock in info.get("recommended_stocks", [])[:8]:
                self.recommend_text.insert(tk.END, f"     • {stock.get('代码', '')} {stock.get('名称', '')} {stock.get('最新价', '')} ({stock.get('涨跌幅', '')}%)\n")
            self.recommend_text.insert(tk.END, "\n")
        
        self.status_label.configure(text="刷新完成")
    
    def auto_refresh(self):
        """后台自动刷新"""
        def refresh_loop():
            while True:
                self.refresh_data(use_cache=True)
                time.sleep(30 * 60)  # 30分钟
        threading.Thread(target=refresh_loop, daemon=True).start()

if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.mainloop()
