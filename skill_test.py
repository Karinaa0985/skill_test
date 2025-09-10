import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
import hashlib
from datetime import datetime
import json

EXCEL_FILE = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "skill_test_records.xlsx")
os.makedirs(os.path.dirname(EXCEL_FILE), exist_ok=True)

# ---------------------------
# Utility functions
# ---------------------------
def ensure_excel_structure():
    # If file doesn't exist, create it with two sheets: users and results
    if not os.path.exists(EXCEL_FILE):
        users_df = pd.DataFrame(columns=["username","password_hash","name","email","created_at"])
        results_df = pd.DataFrame(columns=["username","language","score","total","date","details_json"])
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
            users_df.to_excel(writer, sheet_name="users", index=False)
            results_df.to_excel(writer, sheet_name="results", index=False)

# ✅ Call after definition
ensure_excel_structure()
print("Excel file created at:", os.path.abspath(EXCEL_FILE))

def read_users():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name="users", engine="openpyxl")
    except Exception:
        return pd.DataFrame(columns=["username","password_hash","name","email","created_at"])

def read_results():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name="results", engine="openpyxl")
    except Exception:
        return pd.DataFrame(columns=["username","language","score","total","date","details_json"])

def save_user(user_row: dict):
    ensure_excel_structure()
    try:
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, engine="openpyxl")
    except Exception:
        all_sheets = {}

    users = all_sheets.get("users", pd.DataFrame(columns=["username","password_hash","name","email","created_at"]))
    results = all_sheets.get("results", pd.DataFrame(columns=["username","language","score","total","date","details_json"]))

    users = pd.concat([users, pd.DataFrame([user_row])], ignore_index=True)

    temp_file = EXCEL_FILE.replace(".xlsx", "_tmp.xlsx")
    with pd.ExcelWriter(temp_file, engine="openpyxl", mode="w") as writer:
        users.to_excel(writer, sheet_name="users", index=False)
        results.to_excel(writer, sheet_name="results", index=False)
    os.replace(temp_file, EXCEL_FILE)


def append_result(result_row: dict):
    ensure_excel_structure()
    try:
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, engine="openpyxl")
    except Exception:
        all_sheets = {}

    users = all_sheets.get("users", pd.DataFrame(columns=["username","password_hash","name","email","created_at"]))
    results = all_sheets.get("results", pd.DataFrame(columns=["username","language","score","total","date","details_json"]))

    results = pd.concat([results, pd.DataFrame([result_row])], ignore_index=True)

    temp_file = EXCEL_FILE.replace(".xlsx", "_tmp.xlsx")
    with pd.ExcelWriter(temp_file, engine="openpyxl", mode="w") as writer:
        users.to_excel(writer, sheet_name="users", index=False)
        results.to_excel(writer, sheet_name="results", index=False)
    os.replace(temp_file, EXCEL_FILE)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

QUESTION_BANK = {
    "Python": [
        {"q":"What is the keyword to define a function in Python?","opts":["func","def","function","define"],"ans":1},
        {"q":"Which data-type is immutable?","opts":["list","set","dict","tuple"],"ans":3},
        {"q":"What does 'len()' return?","opts":["number of bytes","number of elements","type of variable","none"],"ans":1},
        {"q":"How do you create a virtual environment?","opts":["python -m venv venv","create venv","venv create","pip venv"],"ans":0},
        {"q":"Which symbol starts a comment?","opts":["//","#","/*","--"],"ans":1},
        {"q":"Which is used to handle exceptions?","opts":["try/except","if/else","switch","for"],"ans":0},
        {"q":"Which method adds an item to a list?","opts":["append()","add()","put()","insertItem()"],"ans":0},
        {"q":"Which built-in type is for key:value pairs?","opts":["list","tuple","dict","set"],"ans":2},
        {"q":"Which statement is used to import modules?","opts":["include","import","require","using"],"ans":1},
        {"q":"What is the output of: 2**3 ?","opts":["6","8","9","5"],"ans":1}
    ],
    "C": [
        {"q":"Which file is needed for printf()?","opts":["<stdio.h>","<conio.h>","<stdlib.h>","<string.h>"],"ans":0},
        {"q":"What is the return type of main in C?","opts":["void","int","main","char"],"ans":1},
        {"q":"Which operator is used for address-of?","opts":["*","&","%","$"],"ans":1},
        {"q":"Which function allocates memory dynamically?","opts":["malloc","alloc","new","create"],"ans":0},
        {"q":"Which loop runs at least once?","opts":["for","while","do-while","if"],"ans":2},
        {"q":"C is which type of language?","opts":["High-level","Low-level","Middle-level","Assembly"],"ans":2},
        {"q":"How do you include a header in C?","opts":["#include <file>","#import file","include file","using file"],"ans":0},
        {"q":"Which function to compare strings?","opts":["strcmp","strcomp","compare","str_eq"],"ans":0},
        {"q":"Which is not a valid storage class?","opts":["auto","register","static","mutable"],"ans":3},
        {"q":"What is size of int (typical on 32-bit)?","opts":["2 bytes","4 bytes","8 bytes","1 byte"],"ans":1}
    ],
    "Java": [
        {"q":"Java is which type of language?","opts":["Compiled only","Interpreted only","Both compiled and interpreted","Raw code"],"ans":2},
        {"q":"Which method is entry point?","opts":["main()","start()","init()","run()"],"ans":0},
        {"q":"Which keyword is used for inheritance?","opts":["implements","extends","inherits","uses"],"ans":1},
        {"q":"Which collection allows duplicate elements?","opts":["Set","Map","List","None"],"ans":2},
        {"q":"What is JVM?","opts":["Java Variable Machine","Java Virtual Machine","Java Vendor Module","Just VM"],"ans":1},
        {"q":"Which is not primitive type?","opts":["int","float","String","boolean"],"ans":2},
        {"q":"Which keyword creates objects?","opts":["make","new","create","init"],"ans":1},
        {"q":"Which package contains ArrayList?","opts":["java.util","java.lang","java.io","java.net"],"ans":0},
        {"q":"What is the default value of boolean?","opts":["true","false","0","1"],"ans":1},
        {"q":"Which symbol terminates statements?","opts":[".",";","/","#"],"ans":1}
    ]
}


class SkillTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skill Test Manipulator")
        self.root.geometry("600x500")
        self.root.configure(bg="#F5F5DC")  # beige background
        self.current_user = None
        self.build_login_screen()

    # Clear all widgets
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ------------------- Login Screen -------------------
    def build_login_screen(self):
        self.clear()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#F5F5DC")
        frame.pack(expand=True)

        tk.Label(frame, text="Skill Test Manipulator", font=("Arial", 20), bg="#F5F5DC").pack(pady=10)
        tk.Label(frame, text="Username", bg="#F5F5DC").pack()
        self.login_username = tk.Entry(frame)
        self.login_username.pack()
        tk.Label(frame, text="Password", bg="#F5F5DC").pack()
        self.login_password = tk.Entry(frame, show="*")
        self.login_password.pack()

        btn_frame = tk.Frame(frame, bg="#F5F5DC")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Login", width=12, command=self.login, bg="#007BFF", fg="white").grid(row=0,column=0,padx=5)
        tk.Button(btn_frame, text="Register", width=12, command=self.register_screen, bg="#007BFF", fg="white").grid(row=0,column=1,padx=5)
        tk.Button(btn_frame, text="Quit", width=12, command=self.root.quit, bg="#007BFF", fg="white").grid(row=0,column=2,padx=5)

    # ------------------- Register Screen -------------------
    def register_screen(self):
        self.clear()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#F5F5DC")
        frame.pack(expand=True)

        tk.Label(frame, text="Register", font=("Arial", 18), bg="#F5F5DC").pack(pady=8)
        tk.Label(frame, text="Full name", bg="#F5F5DC").pack()
        name = tk.Entry(frame); name.pack()
        tk.Label(frame, text="Email", bg="#F5F5DC").pack()
        email = tk.Entry(frame); email.pack()
        tk.Label(frame, text="Username", bg="#F5F5DC").pack()
        username = tk.Entry(frame); username.pack()
        tk.Label(frame, text="Password", bg="#F5F5DC").pack()
        password = tk.Entry(frame, show="*"); password.pack()

        def do_register():
            u = username.get().strip()
            p = password.get()
            nm = name.get().strip()
            em = email.get().strip()

            if not (u and p):
                messagebox.showerror("Error","Username and password required")
                return

            # Email validation
            if "@" not in em:
                messagebox.showerror("Error","Invalid email address. Must contain '@'.")
                return

            # Password validation
            if not any(c.isupper() for c in p):
                messagebox.showerror("Error","Password must contain at least one uppercase letter.")
                return
            if not any(c.isdigit() for c in p):
                messagebox.showerror("Error","Password must contain at least one number.")
                return

            users = read_users()
            if u in list(users["username"].astype(str)):
                messagebox.showerror("Error","Username already exists")
                return

            row = {
                "username": u,
                "password_hash": hash_password(p),
                "name": nm,
                "email": em,
                "created_at": datetime.now().isoformat()
            }
            save_user(row)
            messagebox.showinfo("Success","Registered! Please login.")
            self.build_login_screen()

        btn_frame = tk.Frame(frame, bg="#F5F5DC")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Create Account", command=do_register, bg="#007BFF", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=self.build_login_screen, bg="#007BFF", fg="white").pack(side="left", padx=5)

    # ------------------- Login Function -------------------
    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        if not username or not password:
            messagebox.showerror("Error","Enter username and password")
            return
        users = read_users()
        users = users.fillna("")
        matched = users.loc[users["username"] == username]
        if matched.empty:
            messagebox.showerror("Error","User not found")
            return
        stored_hash = matched.iloc[0]["password_hash"]
        if stored_hash != hash_password(password):
            messagebox.showerror("Error","Incorrect password")
            return
        self.current_user = username
        self.build_main_menu()

    # ------------------- Main Menu -------------------
    def build_main_menu(self):
        self.clear()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#F5F5DC")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Welcome, {self.current_user}", font=("Arial",16), bg="#F5F5DC").pack(pady=6)

        tk.Label(frame, text="Choose language to take the test:", bg="#F5F5DC").pack(pady=4)
        lang_frame = tk.Frame(frame, bg="#F5F5DC"); lang_frame.pack(pady=4)
        for lang in QUESTION_BANK.keys():
            tk.Button(lang_frame, text=lang, width=12, command=lambda l=lang: self.start_quiz(l), bg="#007BFF", fg="white").pack(side="left", padx=8)

        tk.Button(frame, text="View Progress", width=15, command=self.view_progress, bg="#007BFF", fg="white").pack(pady=10)
        tk.Button(frame, text="Logout", width=12, command=self.logout, bg="#007BFF", fg="white").pack(pady=6)

    def logout(self):
        self.current_user = None
        self.build_login_screen()

    # ------------------- Progress Report -------------------
    def view_progress(self):
        results = read_results()
        user_results = results[results["username"] == self.current_user]

        if user_results.empty:
            messagebox.showinfo("Progress", "No test results found yet.")
            return

        win = tk.Toplevel(self.root)
        win.title("Your Progress")
        win.geometry("600x400")
        win.configure(bg="#F5F5DC")

        cols = ["language", "score", "total", "date"]
        tree = ttk.Treeview(win, columns=cols, show="headings")
        tree.pack(fill="both", expand=True)

        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")

        for _, row in user_results.iterrows():
            tree.insert("", "end", values=[row["language"], row["score"], row["total"], row["date"]])

    # ------------------- Quiz -------------------
    def start_quiz(self, language):
        questions = QUESTION_BANK.get(language, [])[:10]
        if not questions:
            messagebox.showerror("No Questions","No questions for this language.")
            return

        quiz_window = tk.Toplevel(self.root)
        quiz_window.title(f"Quiz - {language}")
        quiz_window.geometry("700x500")
        quiz_window.configure(bg="#F5F5DC")
        quiz_window.lift()
        quiz_window.grab_set()

        state = {"language": language, "questions": questions, "index":0, "score":0, "answers":[]}

        q_label = tk.Label(quiz_window, text="", wraplength=650, font=("Arial",14), bg="#F5F5DC")
        q_label.pack(pady=12)

        selected = tk.IntVar(value=-1)
        rbuttons = []
        for i in range(4):
            r = tk.Radiobutton(quiz_window, text="", variable=selected, value=i, anchor="w", bg="#F5F5DC")
            rbuttons.append(r)
            r.pack(anchor="w", padx=20, pady=4)

        progress_label = tk.Label(quiz_window, text="", bg="#F5F5DC")
        progress_label.pack(pady=6)

        def show_question():
            idx = state["index"]
            if idx >= len(state["questions"]):
                finish_quiz()
                return
            q = state["questions"][idx]
            q_label.config(text=f"Q{idx+1}. {q['q']}")
            for i, opt in enumerate(q["opts"]):
                rbuttons[i].config(text=f"{i+1}. {opt}", value=i)
            selected.set(-1)
            progress_label.config(text=f"Question {idx+1} of {len(state['questions'])}")

        def next_q():
            idx = state["index"]
            sel = selected.get()
            if sel == -1:
                if not messagebox.askyesno("Skip?","You did not answer this question. Skip?"):
                    return
            q = state["questions"][idx]
            got_point = 1 if sel == q["ans"] else 0
            state["score"] += got_point
            state["answers"].append({"q": q["q"], "selected": int(sel) if sel != -1 else None, "correct": q["ans"]})
            state["index"] += 1
            show_question()

        def finish_quiz():
            total = len(state["questions"])
            score = state["score"]
            messagebox.showinfo("Quiz Finished", f"You scored {score}/{total}")
            append_result({
                "username": self.current_user,
                "language": language,
                "score": score,
                "total": total,
                "date": datetime.now().isoformat(),
                "details_json": json.dumps(state["answers"])
            })
            quiz_window.destroy()

        btn_frame = tk.Frame(quiz_window, bg="#F5F5DC")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Next", width=12, command=next_q, bg="#007BFF", fg="white").pack(side="left", padx=8)
        tk.Button(btn_frame, text="Finish", width=12, command=finish_quiz, bg="#007BFF", fg="white").pack(side="left", padx=8)

        show_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = SkillTestApp(root)
    root.mainloop()
