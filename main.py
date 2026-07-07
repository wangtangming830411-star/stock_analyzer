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
        self.title("A股消息驱动分析助手 v0.3")
        self.geometry("1350x900")
        
        self.fetcher = NewsFetcher()
        self.processor = NewsProcessor()
        self.mapper = IndustryMapper()
        self.cache = CacheManager()
        
        self.portfolio = []
        
        self._create_ui()
        self.auto_refresh()
    
    def _create_ui(self):
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=8)
        ctk.CTkButton(toolbar, text="🔄 刷新", width=120, command=self.manual_refresh).pack(side="left", padx=10)
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: 新闻
        self.tab_news = self.tabview.add("📋 新闻")
        self.news_text = tk.Text(self.tab_news, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.news_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 2: 推荐
        self.tab_recommend = self.tabview.add("🎯 影响推荐")
        self.recommend_text = tk.Text(self.tab_recommend, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.recommend_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 3: 持仓
        self.tab_portfolio = self.tabview.add("📊 我的持仓")
        self._create_portfolio_ui()
    
    def _create_portfolio_ui(self):
        frame = ctk.CTkFrame(self.tab_portfolio)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="持仓列表", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.portfolio_text = tk.Text(frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.portfolio_text.pack(fill="both", expand=True, pady=5)
        
        add_frame = ctk.CTkFrame(frame)
        add_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(add_frame, text="代码:").pack(side="left", padx=5)
        self.add_code = ctk.CTkEntry(add_frame, width=120)
        self.add_code.pack(side="left", padx=5)
        ctk.CTkButton(add_frame, text="添加", command=self.add_to_portfolio).pack(side="left", padx=5)
    
    def add_to_portfolio(self):
        code = self.add_code.get().strip()
        if code:
            self.portfolio.append({"code": code, "name": "示例", "buy_price": 100, "quantity": 100})
            self.refresh_portfolio()
    
    def refresh_portfolio(self):
        self.portfolio_text.delete(1.0, tk.END)
        for p in self.portfolio:
            self.portfolio_text.insert(tk.END, f"• {p['code']} {p['name']} 买入:{p['buy_price']} 数量:{p['quantity']}\n")
    
    def manual_refresh(self):
        threading.Thread(target=self._refresh_thread, args=(False,), daemon=True).start()
    
    def _refresh_thread(self, use_cache):
        try:
            raw_news = self.fetcher.fetch_all()
            processed = self.processor.process_news(raw_news)
            if not use_cache:
                self.cache.save_news(processed)
            recommendations = self.mapper.get_recommendations(processed)
            
            # 线程安全更新UI
            self.after(0, self._update_ui, processed, recommendations)
        except Exception as e:
            print("刷新错误:", e)
    
    def _update_ui(self, processed, recommendations):
        # 更新新闻 Tab
        self.news_text.delete(1.0, tk.END)
        self.news_text.insert(tk.END, f"✅ {len(processed)} 条新闻\n\n")
        for news in processed[:10]:
            self.news_text.insert(tk.END, f"📰 {news['title']}\n")
            self.news_text.insert(tk.END, f"   总结: {news['summary']}\n")
            impacts = [f"{i['industry']}({i['impact_type']})" for i in news.get("impacted_industries", [])]
            self.news_text.insert(tk.END, f"   影响: {', '.join(impacts) if impacts else '暂无'}\n")
            self.news_text.insert(tk.END, f"   原文: {news.get('url', '')}\n\n")
        
        # 更新推荐 Tab
        self.recommend_text.delete(1.0, tk.END)
        self.recommend_text.insert(tk.END, "🔍 影响推荐：\n\n")
        for ind, info in recommendations.items():
            self.recommend_text.insert(tk.END, f"📌 {ind}\n")
            self.recommend_text.insert(tk.END, f"   {info['analysis']}\n")
            self.recommend_text.insert(tk.END, "   推荐:\n")
            for stock in info.get("recommended_stocks", [])[:8]:
                self.recommend_text.insert(tk.END, f"     • {stock.get('代码')} {stock.get('名称')} {stock.get('最新价')} ({stock.get('涨跌幅')} %)\n")
            self.recommend_text.insert(tk.END, "\n")
    
    def auto_refresh(self):
        def loop():
            while True:
                self._refresh_thread(use_cache=True)
                time.sleep(30 * 60)
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.mainloop()
