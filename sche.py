

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import datetime
import json

class ScheduleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("日程安排")
        self.schedule_list = []
        self.reminder_days = 3
        self.create_widgets()

        self.right_frame = ttk.Frame(padding=(10, 10))
        self.right_frame.pack(side="right", fill="both", expand=True)


    def create_widgets(self):
        # 创建日程列表
        self.schedule_tree = ttk.Treeview(self.root, columns=("content", "start", "end", "note"), show="headings")
        self.schedule_tree.heading("content", text="日程内容")
        self.schedule_tree.heading("start", text="开始时间")
        self.schedule_tree.heading("end", text="截止时间")
        self.schedule_tree.heading("note", text="备注")
        self.schedule_tree.column("content", width=200, anchor="center")
        self.schedule_tree.column("start", width=100, anchor="center")
        self.schedule_tree.column("end", width=100, anchor="center")
        self.schedule_tree.column("note", width=200, anchor="center")
        self.schedule_tree.pack(padx=10, pady=10)
        # 添加滚动条
        scroll_bar = ttk.Scrollbar(self.root, orient="vertical", command=self.schedule_tree.yview)
        scroll_bar.pack(side="right", fill="y")
        self.schedule_tree.configure(yscrollcommand=scroll_bar.set)
        # 创建日程输入框
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)
        content_label = tk.Label(input_frame, text="日程内容：")
        content_label.grid(row=0, column=0, padx=5, pady=5)
        self.content_entry = tk.Entry(input_frame)
        self.content_entry.grid(row=0, column=1, padx=5, pady=5)
        start_label = tk.Label(input_frame, text="开始时间：")
        start_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_year_var = tk.StringVar(value=datetime.date.today().strftime("%Y"))
        self.start_month_var = tk.StringVar(value=datetime.date.today().strftime("%m"))
        self.start_day_var = tk.StringVar(value=datetime.date.today().strftime("%d"))
        start_year_option = tk.OptionMenu(input_frame, self.start_year_var, *range(2020, 2031))
        start_year_option.grid(row=1, column=1, padx=5, pady=5)
        start_month_option = tk.OptionMenu(input_frame, self.start_month_var, *range(1, 13))
        start_month_option.grid(row=1, column=2, padx=5, pady=5)
        start_day_option = tk.OptionMenu(input_frame, self.start_day_var, *range(1, 32))
        start_day_option.grid(row=1, column=3, padx=5, pady=5)
        end_label = tk.Label(input_frame, text="截止时间：")
        end_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_year_var = tk.StringVar(value=datetime.date.today().strftime("%Y"))
        self.end_month_var = tk.StringVar(value=datetime.date.today().strftime("%m"))
        self.end_day_var = tk.StringVar(value=datetime.date.today().strftime("%d"))
        end_year_option = tk.OptionMenu(input_frame, self.end_year_var, *range(2020, 2031))
        end_year_option.grid(row=2, column=1, padx=5, pady=5)
        end_month_option = tk.OptionMenu(input_frame, self.end_month_var, *range(1, 13))
        end_month_option.grid(row=2, column=2, padx=5, pady=5)
        end_day_option = tk.OptionMenu(input_frame, self.end_day_var, *range(1, 32))
        end_day_option.grid(row=2, column=3, padx=5, pady=5)
        note_label = tk.Label(input_frame, text="备注：")
        note_label.grid(row=3, column=0, padx=5, pady=5)
        self.note_entry = tk.Entry(input_frame)
        self.note_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
        # 创建按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10)
        add_button = tk.Button(button_frame, text="添加", command=self.add_schedule)
        add_button.pack(side="left", padx=5)
        delete_button = tk.Button(button_frame, text="删除", command=self.delete_schedule)
        delete_button.pack(side="left", padx=5)
        modify_button = tk.Button(button_frame, text="修改", command=self.modify_schedule)
        modify_button.pack(side="left", padx=5)
        save_button = tk.Button(button_frame, text="保存", command=self.save_schedule)
        save_button.pack(side="left", padx=5)
        load_button = tk.Button(button_frame, text="读取", command=self.load_schedule)
        load_button.pack(side="left", padx=5)

    def add_schedule(self):
        content = self.content_entry.get()
        start_date = datetime.date(int(self.start_year_var.get()), int(self.start_month_var.get()), int(self.start_day_var.get()))
        end_date = datetime.date(int(self.end_year_var.get()), int(self.end_month_var.get()), int(self.end_day_var.get()))
        note = self.note_entry.get()
        schedule = {"content": content, "start": str(start_date), "end": str(end_date), "note": note}
        self.schedule_list.append(schedule)
        self.schedule_tree.insert("", "end", values=(content, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), note))

    def delete_schedule(self):
        selected = self.schedule_tree.selection()
        if len(selected) == 0:
            messagebox.showinfo("提示", "请选择要删除的日程！")
        else:
            confirm = messagebox.askyesno("提示", "确定要删除选中的日程吗？")
            if confirm:
                for item in selected:
                    self.schedule_list.pop(int(self.schedule_tree.index(item)))
                    self.schedule_tree.delete(item)

    def modify_schedule(self):
        selected = self.schedule_tree.selection()
        if len(selected) == 0:
            messagebox.showinfo("提示", "请选择要修改的日程！")
        elif len(selected) > 1:
            messagebox.showinfo("提示", "一次只能修改一个日程！")
        else:
            content = self.content_entry.get()
            start_date = datetime.date(int(self.start_year_var.get()), int(self.start_month_var.get()),
                                       int(self.start_day_var.get()))
            end_date = datetime.date(int(self.end_year_var.get()), int(self.end_month_var.get()),
                                     int(self.end_day_var.get()))
            note = self.note_entry.get()
            schedule = {"content": content, "start": str(start_date), "end": str(end_date), "note": note}
            index = int(self.schedule_tree.index(selected[0]))
            self.schedule_list[index] = schedule
            self.schedule_tree.item(selected[0], values=(
            content, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), note))

    def save_schedule(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                for schedule in self.schedule_list:
                    f.write(f"{schedule['content']}|{schedule['start']}|{schedule['end']}|{schedule['note']}\n")

    def load_schedule(self):
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if filename:
            self.schedule_list.clear()
            self.schedule_tree.delete(*self.schedule_tree.get_children())
            with open(filename, "r") as f:
                for line in f:
                    fields = line.strip().split("|")
                    content = fields[0]
                    start_date = datetime.datetime.strptime(fields[1], "%Y-%m-%d").date()
                    end_date = datetime.datetime.strptime(fields[2], "%Y-%m-%d").date()
                    note = fields[3]
                    schedule = {"content": content, "start": str(start_date), "end": str(end_date),
                                "note": note}
                    self.schedule_list.append(schedule)
                    self.schedule_tree.insert("", "end", values=(
                    content, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), note))

    def check_reminder(self):
        today = datetime.date.today()
        for schedule in self.schedule_list:
            end_date = datetime.datetime.strptime(schedule["end"], "%Y-%m-%d").date()
            delta = (end_date - today).days
            if delta == self.check_days_input:
                messagebox.showinfo("提醒", f"日程'{schedule['content']}'即将到期！")
        self.root.after(1000 * 60 * 60 * 24, self.check_reminder)

    def run(self):
        self.root.mainloop()


app = ScheduleApp()
app.run()
