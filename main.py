import customtkinter as ctk
from tkinter import Canvas, Scrollbar
from data.news_fetcher import NewsFetcher
from data.news_processor import NewsProcessor
from data.industry_mapper import IndustryMapper
import webbrowser


class LinkLabel(ctk.CTkFrame):
    """可点击的超链接标签"""
    def __init__(self, parent, url, text="📎 查看原文", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.url = url
        btn = ctk.CTkButton(self, text=text, fg_color="transparent",
                            border_width=1, border_color="#53a2d6",
                            text_color="#53a2d6", cursor="hand2",
                            command=lambda: webbrowser.open(url))
        btn.pack(anchor="w")


class NewsCard(ctk.CTkFrame):
    """单条新闻卡片"""
    def __init__(self, parent, news_data: dict, **kwargs):
        super().__init__(parent, fg_color="#2b2b2b", corner_radius=8)

        title = news_data.get('title', '(无标题)')
        summary = news_data.get('summary', '') or ''
        url = news_data.get('url', '') or ''
        impacted = news_data.get('impacted_industries', [])

        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=0)

        lbl_title = ctk.CTkLabel(row1, text=f"📰  {title}", anchor="w",
                                  justify="left", wraplength=900, fg_color="transparent")
        lbl_title.pack(side="left", fill="x", expand=True, padx=10, pady=(8, 2))

        if impacted:
            tags = ", ".join([f"[{it['impact_type']}] {it['industry']}" for it in impacted])
        else:
            tags = "暂无明显影响"

        lbl_tag = ctk.CTkLabel(row1, text=tags, anchor="e",
                                fg_color="transparent", text_color="#d4a726")
        lbl_tag.pack(side="right", padx=(0, 10))

        if summary:
            lbl_sum = ctk.CTkLabel(self, text=f"    总结：{summary}", anchor="w",
                                    justify="left", wraplength=900, fg_color="transparent", text_color="#aaa")
            lbl_sum.pack(fill="x", padx=10, pady=(2, 4))

        if url and url != "nan":
            LinkLabel(self, url).pack(fill="x", padx=10, pady=(2, 6))


class StockCard(ctk.CTkFrame):
    """推荐行业卡片"""
    def __init__(self, parent, industry: str, data: dict, **kwargs):
        super().__init__(parent, fg_color="#2b2b2b", corner_radius=8)

        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=0)

        lbl_ind = ctk.CTkLabel(row1, text=f"🏭  {industry}", anchor="w",
                                fg_color="transparent")
        lbl_ind.pack(side="left", padx=10, pady=(8, 2))

        impact = data.get('impact_type', '利好')
        color = "#4ade80" if impact == "利好" else "#f87171"
        lbl_impact = ctk.CTkLabel(row1, text=f"[{impact}]", anchor="e",
                                   fg_color="transparent", text_color=color)
        lbl_impact.pack(side="right", padx=(0, 10))

        analysis = data.get('analysis', '')
        if analysis:
            lbl_analysis = ctk.CTkLabel(self, text=f"    {analysis}", anchor="w",
                                         fg_color="transparent", text_color="#aaa")
            lbl_analysis.pack(fill="x", padx=10, pady=(2, 4))

        stocks = data.get('recommended_stocks', [])
        if not stocks:
            ctk.CTkLabel(self, text="     (暂无推荐)", anchor="w",
                         fg_color="transparent").pack(fill="x", padx=10)
        else:
            for s in stocks[:8]:
                code = s.get("代码", "") if isinstance(s, dict) else str(s)
                name = s.get("名称", "") if isinstance(s, dict) else ""
                price = s.get("最新价", "N/A") if isinstance(s, dict) else ""
                change = s.get("涨跌幅", "N/A") if isinstance(s, dict) else ""
                change_color = "#4ade80" if float(change) >= 0 else "#f87171"

                row = ctk.CTkFrame(self, fg_color="transparent")
                row.pack(fill="x", padx=10)

                ctk.CTkLabel(row, text=f"  {code}  {name}", anchor="w",
                              fg_color="transparent").pack(side="left")

                ctk.CTkLabel(row, text=f"¥{price}  ", anchor="center",
                              fg_color="transparent").pack(side="left")

                ctk.CTkLabel(row, text=f"{change}%", anchor="e",
                              fg_color="transparent", text_color=change_color).pack(side="right")

        ctk.CTkLabel(self, fg_color="#2b2b2b").pack(fill="x", pady=(0, 8))


class SectionFrame(ctk.CTkFrame):
    """带标题和滚动区域的板块"""
    def __init__(self, parent, title: str):
        super().__init__(parent)

        header = ctk.CTkFrame(self, height=28, fg_color="#1a1a3e")
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=title, font=("Arial", 13, "bold"),
                      anchor="w").pack(fill="y")

        # Canvas + Scrollbar 手动实现滚动
        canvas = Canvas(self, highlightthickness=0, bg="#1a1a1a")
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        inner = ctk.CTkFrame(canvas, fg_color="#1a1a1a")
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw", width=1)

        def configure_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", configure_scrollregion)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        def on_scroll(event):
            if hasattr(event, 'delta'):
                delta = int(-1 * (event.delta / 120))
            elif hasattr(event, 'num'):
                delta = -1 if event.num == 4 else 1
            else:
                return "break"
            canvas.yview_scroll(delta, "units")

        # 确保 scrollregion 在内容变化后更新
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.scroll = inner
        self.canvas_widget = canvas


class StockAnalyzerApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("A股消息驱动分析助手")
        ctk.set_appearance_mode("dark")

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = int(sw * 0.85), int(sh * 0.9)
        self.geometry(f"{w}x{h}")

        # ===== 顶部刷新栏 =====
        top_bar = ctk.CTkFrame(self, height=45)
        top_bar.pack(fill="x", padx=10, pady=(8, 4))
        top_bar.pack_propagate(False)

        self.refresh_btn = ctk.CTkButton(top_bar, text="🔄 刷新", width=100, height=32,
                                          command=self.on_refresh)
        self.refresh_btn.pack(side="left", padx=10, pady=6)

        self.status_label = ctk.CTkLabel(top_bar, text="就绪", anchor="w")
        self.status_label.pack(side="left", padx=10)

        # ===== 主体：grid 布局，三个板块纵向排列 =====
        pw = ctk.CTkFrame(self, fg_color="#1a1a1a")
        pw.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        pw.grid_columnconfigure(0, weight=1)
        pw.grid_rowconfigure(1, weight=45)
        pw.grid_rowconfigure(3, weight=30)
        pw.grid_rowconfigure(5, weight=25)

        # --- 新闻区 (row 1) ---
        self.news_section = SectionFrame(pw, "📰  财经新闻")
        self.news_section.grid(row=1, column=0, sticky="nsew")

        # --- 分割线 (row 2) ---
        ctk.CTkFrame(pw, height=3, fg_color="#444").grid(row=2, column=0, sticky="ew", pady=(1, 1))

        # --- 推荐区 (row 3) ---
        self.rec_section = SectionFrame(pw, "🏭  影响推荐")
        self.rec_section.grid(row=3, column=0, sticky="nsew")

        # --- 分割线 (row 4) ---
        ctk.CTkFrame(pw, height=3, fg_color="#444").grid(row=4, column=0, sticky="ew", pady=(1, 1))

        # --- 持仓区 (row 5) ---
        self.port_section = SectionFrame(pw, "💼  我的持仓")
        self.port_section.grid(row=5, column=0, sticky="nsew")

        # ===== 持仓占位内容 =====
        ctk.CTkLabel(self.port_section.scroll, text="💼 持仓功能开发中...",
                      font=("Arial", 14), text_color="#888").pack(pady=30)

        # 初始化
        self.news_processor = NewsProcessor()
        self.industry_mapper = IndustryMapper()

    def on_refresh(self):
        """统一刷新"""
        self.status_label.configure(text="正在获取数据...")
        self.after(50, self._do_refresh)

    def _do_refresh(self):
        try:
            fetcher = NewsFetcher()
            raw_news = fetcher.fetch_news(limit=50)

            processed = self.news_processor.process_news(raw_news)
            count = len(processed)

            recommendations = self.industry_mapper.get_recommendations(processed)
            rec_count = len(recommendations)

            self.status_label.configure(text=f"✅ {count} 条新闻 | {rec_count} 个行业推荐")

            self._render_news(processed)
            self._render_recommendations(recommendations)
        except Exception as e:
            import traceback
            self.status_label.configure(text=f"❌ {e}")
            print(traceback.format_exc())

    def _render_news(self, processed):
        scroll = self.news_section.scroll
        for widget in scroll.winfo_children():
            widget.destroy()

        if not processed:
            ctk.CTkLabel(scroll, text="暂无新闻数据", font=("Arial", 14),
                          text_color="#888").pack(pady=30)
            return

        for n in processed:
            NewsCard(scroll, n).pack(fill="x", padx=8, pady=(0, 4))

    def _render_recommendations(self, recommendations):
        scroll = self.rec_section.scroll
        for widget in scroll.winfo_children():
            widget.destroy()

        if not recommendations:
            ctk.CTkLabel(scroll, text="暂无推荐数据", font=("Arial", 14),
                          text_color="#888").pack(pady=30)
            return

        for industry, data in recommendations.items():
            StockCard(scroll, industry, data).pack(fill="x", padx=8, pady=(0, 4))


if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.after(200, app.on_refresh)
    app.mainloop()
