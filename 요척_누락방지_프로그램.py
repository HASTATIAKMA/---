import tkinter as tk
from tkinter import ttk, messagebox

# 상의 / 하의별 구성품
CATEGORIES = {
    "상의": [
        ("겉감", ["앞판", "뒤판", "소매", "칼라/후드", "덧장/플랩"]),
        ("안감", ["몸판안감", "소매안감", "포켓안감"]),
        ("심지", ["몸판심지", "소매심지", "칼라/후드심지", "기타심지"]),
        ("오비심지", ["앞오비심지", "뒤오비심지"]),
        ("배색", ["배색"]),
        ("포켓", ["앞주머니", "뒤주머니"]),
        ("오비", ["앞오비", "뒤오비"]),
        ("뎅고", ["뎅고"]),
        ("부속", ["테이프/고무/끈", "기타부속"]),
    ],
    "하의": [
        ("겉감", ["앞판", "뒤판", "벨트/오비", "덧장/플랩"]),
        ("안감", ["몸판안감", "소매안감", "포켓안감"]),
        ("심지", ["몸판심지", "오비심지", "기타심지"]),
        ("오비심지", ["앞오비심지", "뒤오비심지"]),
        ("배색", ["배색"]),
        ("포켓", ["앞주머니", "뒤주머니"]),
        ("오비", ["앞오비", "뒤오비"]),
        ("뎅고", ["뎅고"]),
        ("부속", ["테이프/고무/끈", "기타부속"]),
    ],
}

FONT = ("맑은 고딕", 11)
FONT_BOLD = ("맑은 고딕", 11, "bold")
HEADER_FONT = ("맑은 고딕", 12, "bold")
BIG_FONT = ("맑은 고딕", 13)
SMALL_FONT = ("맑은 고딕", 10)

class App:
    def __init__(self, root):
        self.root = root
        root.title("요척 누락 방지 관리 프로그램")
        root.geometry("1280x820")
        root.minsize(1050, 700)

        self.data = {}
        self.edit_widget = None
        self.current_tab = "상의"

        self.style = ttk.Style()
        try:
            self.style.theme_use("vista")
        except Exception:
            pass
        self.style.configure(".", font=FONT)
        self.style.configure("TLabel", font=FONT)
        self.style.configure("TButton", font=FONT, padding=6)
        self.style.configure("TNotebook.Tab", font=HEADER_FONT, padding=(18, 8))
        self.style.configure("Treeview", font=FONT, rowheight=32)
        self.style.configure("Treeview.Heading", font=HEADER_FONT, padding=6)

        self.build_header()
        self.build_tabs()
        self.build_bottom_summary()

    def build_header(self):
        top = ttk.LabelFrame(self.root, text="기본 정보", padding=12)
        top.pack(fill="x", padx=12, pady=(12, 6))

        fields = ["스타일명", "품번", "원단", "작업자"]
        self.info_entries = {}
        for i, name in enumerate(fields):
            ttk.Label(top, text=name, font=FONT_BOLD).grid(
                row=0, column=i * 2, padx=(4, 7), pady=5, sticky="w"
            )
            e = ttk.Entry(top, width=20, font=BIG_FONT)
            e.grid(row=0, column=i * 2 + 1, padx=(0, 18), pady=5, sticky="ew")
            self.info_entries[name] = e
            top.columnconfigure(i * 2 + 1, weight=1)

    def build_tabs(self):
        outer = ttk.Frame(self.root, padding=(12, 6, 12, 4))
        outer.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(outer)
        self.notebook.pack(fill="both", expand=True)

        for tab_name in ["상의", "하의"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.build_table(frame, tab_name)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def build_table(self, parent, tab_name):
        cols = ("구분", "구성품", "패턴 확인", "요척 입력", "패턴 개수", "비고")
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True, padx=4, pady=4)

        tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        widths = [110, 190, 120, 120, 120, 360]
        for col, width in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=70,
                        anchor="center" if col != "비고" else "w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.data[tab_name] = {"tree": tree, "rows": {}}

        for category, items in CATEGORIES[tab_name]:
            for item in items:
                iid = tree.insert("", "end", values=(category, item, "□", "□", "", ""))
                self.data[tab_name]["rows"][iid] = {
                    "category": category,
                    "item": item,
                    "pattern_ok": False,
                    "yield_ok": False,
                    "count": 0,
                    "note": "",
                }

        tree.bind("<Button-1>", lambda e, tab=tab_name: self.on_click(e, tab))
        tree.bind("<Double-1>", lambda e, tab=tab_name: self.start_inline_edit(e, tab))
        tree.bind("<Configure>", lambda e, tab=tab_name: self.close_editor())

    def build_bottom_summary(self):
        bottom = ttk.LabelFrame(self.root, text="항목별 총 패턴 개수", padding=8)
        bottom.pack(fill="x", padx=12, pady=(4, 12))

        self.summary_tree = ttk.Treeview(
            bottom, columns=("구분", "상의", "하의"), show="headings", height=5
        )
        self.summary_tree.heading("구분", text="구분")
        self.summary_tree.heading("상의", text="상의")
        self.summary_tree.heading("하의", text="하의")
        self.summary_tree.column("구분", width=170, anchor="w")
        self.summary_tree.column("상의", width=130, anchor="center")
        self.summary_tree.column("하의", width=130, anchor="center")
        self.summary_tree.pack(side="left", fill="x", expand=True)

        self.summary_total = ttk.Label(
            bottom, text="전체 합계: 0", font=("맑은 고딕", 14, "bold")
        )
        self.summary_total.pack(side="right", padx=18)

        self.update_summary()

    def on_tab_changed(self, _event=None):
        self.close_editor()
        self.current_tab = self.notebook.tab(self.notebook.select(), "text")
        self.update_summary()

    def on_click(self, event, tab_name):
        tree = self.data[tab_name]["tree"]
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        iid = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not iid:
            return

        # 패턴 확인 / 요척 입력은 클릭하면 바로 체크
        if col in ("#3", "#4"):
            self.close_editor()
            row = self.data[tab_name]["rows"][iid]
            if col == "#3":
                row["pattern_ok"] = not row["pattern_ok"]
            else:
                row["yield_ok"] = not row["yield_ok"]
            self.refresh_row(tab_name, iid)
            self.update_summary()

    def start_inline_edit(self, event, tab_name):
        tree = self.data[tab_name]["tree"]
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        iid = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not iid:
            return

        # 패턴 개수 / 비고만 인라인 편집
        if col not in ("#5", "#6"):
            return

        self.close_editor()
        bbox = tree.bbox(iid, col)
        if not bbox:
            return
        x, y, w, h = bbox
        row = self.data[tab_name]["rows"][iid]

        if col == "#5":
            value = str(row["count"] or "")
            entry = tk.Entry(tree, font=BIG_FONT, justify="center")
            entry.insert(0, value)
            entry.place(x=x, y=y, width=w, height=h)
            entry.select_range(0, "end")
            entry.focus_set()
            entry.bind("<Return>", lambda e: self.save_inline_count(tab_name, iid, entry))
            entry.bind("<Escape>", lambda e: self.close_editor())
            entry.bind("<FocusOut>", lambda e: self.save_inline_count(tab_name, iid, entry))
            self.edit_widget = entry

        elif col == "#6":
            value = row["note"]
            entry = tk.Entry(tree, font=FONT)
            entry.insert(0, value)
            entry.place(x=x, y=y, width=w, height=h)
            entry.select_range(0, "end")
            entry.focus_set()
            entry.bind("<Return>", lambda e: self.save_inline_note(tab_name, iid, entry))
            entry.bind("<Escape>", lambda e: self.close_editor())
            entry.bind("<FocusOut>", lambda e: self.save_inline_note(tab_name, iid, entry))
            self.edit_widget = entry

    def save_inline_count(self, tab_name, iid, entry):
        if self.edit_widget is not entry:
            return
        raw = entry.get().strip()
        try:
            count = int(raw) if raw else 0
            if count < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("입력 확인", "패턴 개수는 0 이상의 숫자로 입력해 주세요.")
            entry.focus_set()
            return

        self.data[tab_name]["rows"][iid]["count"] = count
        self.close_editor()
        self.refresh_row(tab_name, iid)
        self.update_summary()

    def save_inline_note(self, tab_name, iid, entry):
        if self.edit_widget is not entry:
            return
        self.data[tab_name]["rows"][iid]["note"] = entry.get()
        self.close_editor()
        self.refresh_row(tab_name, iid)

    def close_editor(self):
        if self.edit_widget is not None:
            try:
                self.edit_widget.destroy()
            except tk.TclError:
                pass
            self.edit_widget = None

    def refresh_row(self, tab_name, iid):
        row = self.data[tab_name]["rows"][iid]
        tree = self.data[tab_name]["tree"]
        tree.item(
            iid,
            values=(
                row["category"],
                row["item"],
                "✓" if row["pattern_ok"] else "□",
                "✓" if row["yield_ok"] else "□",
                row["count"] if row["count"] else "",
                row["note"],
            ),
        )

    def update_summary(self):
        self.summary_tree.delete(*self.summary_tree.get_children())
        categories = []
        for tab_name in ["상의", "하의"]:
            for cat, _items in CATEGORIES[tab_name]:
                if cat not in categories:
                    categories.append(cat)

        overall = 0
        for cat in categories:
            values = []
            for tab_name in ["상의", "하의"]:
                total = sum(
                    row["count"]
                    for row in self.data[tab_name]["rows"].values()
                    if row["category"] == cat
                )
                values.append(total)
                overall += total
            self.summary_tree.insert("", "end", values=(cat, values[0], values[1]))

        self.summary_total.config(text=f"전체 합계: {overall}")

    def reset(self):
        if not messagebox.askyesno("초기화", "입력한 내용을 모두 초기화할까요?"):
            return

        self.close_editor()
        for e in self.info_entries.values():
            e.delete(0, "end")

        for tab_name in self.data:
            for iid, row in self.data[tab_name]["rows"].items():
                row["pattern_ok"] = False
                row["yield_ok"] = False
                row["count"] = 0
                row["note"] = ""
                self.refresh_row(tab_name, iid)

        self.update_summary()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
