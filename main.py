import customtkinter as ctk
import tkinter as tk
from data.news_fetcher import NewsFetcher
from data.news_processor import NewsProcessor
from data.industry_mapper import IndustryMapper
from data.cache_manager import CacheManager
import threading
import time
import json

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
        
        self.portfolio = []  # 持仓列表: [{"code": , "name": , "buy_price": , "quantity": }]
        
        self._create_ui()
        self.auto_refresh()
    
    def _create_ui(self):
        # 顶部工具栏
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkButton(toolbar, text="🔄 刷新", width=100, command=self.refresh_data).pack(side="left", padx=5)
        
        # Tab 切换
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
        
        # Tab 3: 我的持仓
        self.tab_portfolio = self.tabview.add("📊 我的持仓")
        self._create_portfolio_ui()
    
    def _create_portfolio_ui(self):
        frame = ctk.CTkFrame(self.tab_portfolio)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="持仓列表（手动添加测试）", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.portfolio_text = tk.Text(frame, wrap="word", bg="#2B2B2B", fg="#E0E0E0", font=("Microsoft YaHei", 11))
        self.portfolio_text.pack(fill="both", expand=True, pady=5)
        
        # 添加持仓输入
        add_frame = ctk.CTkFrame(frame)
        add_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(add_frame, text="代码:").pack(side="left", padx=5)
        self.add_code = ctk.CTkEntry(add_frame, width=100)
        self.add_code.pack(side="left", padx=5)
        ctk.CTkButton(add_frame, text="添加持仓", command=self.add_to_portfolio).pack(side="left", padx=5)
    
    def add_to_portfolio(self):
        code = self.add_code.get().strip()
        if code:
            self.portfolio.append({"code": code, "name": "示例股票", "buy_price": 100, "quantity": 100})
            self.refresh_portfolio()
    
    def refresh_portfolio(self):
        self.portfolio_text.delete(1.0, tk.END)
        self.portfolio_text.insert(tk.END, "持仓列表：\n\n")
        for p in self.portfolio:
            self.portfolio_text.insert(tk.END, f"• {p['code']} {p['name']}  买入价:{p['buy_price']}  数量:{p['quantity']}\n")
    
    def refresh_data(self, use_cache=False):
        # ... (保持之前逻辑，更新新闻和推荐 tab)
        # 为简洁，这里省略完整refresh_data，实际运行时可复制之前版本逻辑
        self.status_label = ctk.CTkLabel(self, text="刷新完成")  # 简化
        print("刷新数据...")
    
    def auto_refresh(self):
        def loop():
            while True:
                self.refresh_data(use_cache=True)
                time.sleep(30 * 60)
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.mainloop()
