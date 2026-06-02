import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Callable, Dict

from ui.styles import (
    COLOR_ACCENT,
    COLOR_BG,
    COLOR_DANGER,
    COLOR_MUTED,
    COLOR_PANEL,
    COLOR_PRIMARY,
    COLOR_PRIMARY_DARK,
    COLOR_SUCCESS,
    COLOR_TEXT,
    FONT_BUTTON,
    FONT_SUBTITLE,
    FONT_TEXT,
    FONT_TITLE,
)


class BaseScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_BG)
        self.app = app


class MenuScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        container = tk.Frame(self, bg=COLOR_PANEL, bd=1, relief="solid")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            container,
            text="Quiz Bac Marocain - Option SVT",
            font=FONT_TITLE,
            fg=COLOR_TEXT,
            bg=COLOR_PANEL,
        ).pack(pady=(30, 10))

        tk.Label(
            container,
            text="Choisissez un mode de quiz",
            font=FONT_SUBTITLE,
            fg=COLOR_MUTED,
            bg=COLOR_PANEL,
        ).pack(pady=(0, 25))

        btn_full = tk.Button(
            container,
            text="Quiz Complet (100 Q)",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_PRIMARY_DARK,
            activeforeground="white",
            width=28,
            height=2,
            command=lambda: self.app.go_to_subject_selection("full"),
        )
        btn_full.pack(pady=8)

        btn_mini = tk.Button(
            container,
            text="Mini Quiz (10 Q)",
            font=FONT_BUTTON,
            bg=COLOR_ACCENT,
            fg="white",
            activebackground="#92400e",
            activeforeground="white",
            width=28,
            height=2,
            command=lambda: self.app.go_to_subject_selection("mini"),
        )
        btn_mini.pack(pady=8)

        btn_history = tk.Button(
            container,
            text="Historique",
            font=FONT_BUTTON,
            bg="#334155",
            fg="white",
            activebackground="#1e293b",
            activeforeground="white",
            width=28,
            height=2,
            command=self.app.show_history,
        )
        btn_history.pack(pady=8)

        tk.Label(
            container,
            text="2eme annee Bac Marocain - Filieres scientifiques",
            font=FONT_TEXT,
            fg=COLOR_MUTED,
            bg=COLOR_PANEL,
        ).pack(side="bottom", pady=20)


class SubjectScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.mode_label = tk.Label(
            self,
            text="",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_BG,
        )
        self.mode_label.pack(pady=(25, 5))

        tk.Label(
            self,
            text="Selectionnez la matiere",
            font=FONT_TITLE,
            fg=COLOR_TEXT,
            bg=COLOR_BG,
        ).pack(pady=(0, 20))

        buttons = tk.Frame(self, bg=COLOR_BG)
        buttons.pack()

        for subject in ["Maths", "PC", "SVT"]:
            tk.Button(
                buttons,
                text=subject,
                font=FONT_BUTTON,
                width=20,
                height=2,
                bg=COLOR_PRIMARY,
                fg="white",
                activebackground=COLOR_PRIMARY_DARK,
                activeforeground="white",
                command=lambda s=subject: self.app.start_quiz(s),
            ).pack(pady=8)

        tk.Button(
            self,
            text="Retour",
            font=FONT_BUTTON,
            width=16,
            command=lambda: self.app.show_screen("menu"),
        ).pack(pady=20)

    def set_mode(self, mode: str) -> None:
        mode_text = "Quiz Complet (100 Q)" if mode == "full" else "Mini Quiz (10 Q)"
        self.mode_label.config(text=f"Mode selectionne: {mode_text}")


class QuizScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.remaining_seconds = 45
        self.timer_job = None
        self.selected_answer = tk.StringVar(value="")

        header = tk.Frame(self, bg=COLOR_BG)
        header.pack(fill="x", padx=20, pady=(15, 8))

        self.progress_label = tk.Label(header, text="Q 1/100", font=FONT_SUBTITLE, bg=COLOR_BG, fg=COLOR_TEXT)
        self.progress_label.pack(side="left")

        self.timer_label = tk.Label(header, text="00:45", font=FONT_SUBTITLE, bg=COLOR_BG, fg=COLOR_ACCENT)
        self.timer_label.pack(side="right")

        self.question_label = tk.Label(
            self,
            text="",
            font=FONT_SUBTITLE,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            wraplength=820,
            justify="left",
            padx=20,
            pady=20,
            bd=1,
            relief="solid",
        )
        self.question_label.pack(fill="x", padx=20, pady=(5, 10))

        self.options_frame = tk.Frame(self, bg=COLOR_BG)
        self.options_frame.pack(fill="x", padx=20)

        self.answer_buttons: Dict[str, ttk.Radiobutton] = {}
        for option in ["A", "B", "C", "D"]:
            rb = ttk.Radiobutton(
                self.options_frame,
                text="",
                value=option,
                variable=self.selected_answer,
            )
            rb.pack(anchor="w", pady=5)
            self.answer_buttons[option] = rb

        actions = tk.Frame(self, bg=COLOR_BG)
        actions.pack(fill="x", padx=20, pady=15)

        self.btn_submit = tk.Button(
            actions,
            text="Valider et Suivant",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_PRIMARY_DARK,
            activeforeground="white",
            command=self.submit_answer,
            width=20,
        )
        self.btn_submit.pack(side="left")

        tk.Button(
            actions,
            text="Abandonner",
            font=FONT_BUTTON,
            bg="#374151",
            fg="white",
            activebackground="#1f2937",
            activeforeground="white",
            command=self.confirm_quit,
            width=14,
        ).pack(side="left", padx=10)

        self.mode_info = tk.Label(actions, text="", font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_MUTED)
        self.mode_info.pack(side="right")

    def start(self) -> None:
        self.load_current_question()

    def load_current_question(self) -> None:
        question = self.app.quiz_model.get_current_question()
        if question is None:
            self.finish_quiz()
            return

        self.selected_answer.set("")

        total = len(self.app.quiz_model.questions_list)
        current = self.app.quiz_model.current_index + 1
        self.progress_label.config(text=f"Q {current}/{total}")

        mode_text = "Mode: Complet" if self.app.selected_mode == "full" else "Mode: Mini"
        self.mode_info.config(text=mode_text)

        self.question_label.config(text=f"Q{question['id']}. {question['question']}")

        options = question.get("options", [])
        for idx, option_key in enumerate(["A", "B", "C", "D"]):
            text = options[idx] if idx < len(options) else ""
            self.answer_buttons[option_key].config(text=f"{option_key}) {text}")

        self.app.quiz_model.start_question_timer()
        self.start_timer()

    def start_timer(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)

        self.remaining_seconds = 45
        self.update_timer()

    def update_timer(self) -> None:
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        if self.remaining_seconds <= 5:
            self.timer_label.config(fg=COLOR_DANGER)
        else:
            self.timer_label.config(fg=COLOR_ACCENT)

        if self.remaining_seconds == 0:
            self.submit_answer(timeout=True)
            return

        self.remaining_seconds -= 1
        self.timer_job = self.after(1000, self.update_timer)

    def submit_answer(self, timeout: bool = False) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        question = self.app.quiz_model.get_current_question()
        if question is None:
            self.finish_quiz()
            return

        answer = self.selected_answer.get().strip() or None
        if not timeout and answer is None:
            messagebox.showwarning("Attention", "Veuillez choisir une reponse.")
            self.start_timer()
            return

        self.app.quiz_model.save_answer(question_id=question["id"], answer=answer)
        has_next = self.app.quiz_model.go_next()
        if has_next:
            self.load_current_question()
        else:
            self.finish_quiz()

    def confirm_quit(self) -> None:
        if messagebox.askyesno("Confirmer", "Voulez-vous quitter le quiz ?"):
            if self.timer_job is not None:
                self.after_cancel(self.timer_job)
                self.timer_job = None
            self.app.show_screen("menu")

    def finish_quiz(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.app.show_results()


class ResultScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.current_result = None

        top = tk.Frame(self, bg=COLOR_BG)
        top.pack(fill="x", padx=20, pady=10)

        self.score_label = tk.Label(top, text="", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT)
        self.score_label.pack(side="left")

        actions = tk.Frame(top, bg=COLOR_BG)
        actions.pack(side="right")

        tk.Button(
            actions,
            text="Exporter PDF",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_PRIMARY_DARK,
            activeforeground="white",
            command=self.export_pdf,
        ).pack(side="left", padx=6)

        tk.Button(
            actions,
            text="Retour Menu",
            font=FONT_BUTTON,
            command=lambda: self.app.show_screen("menu"),
        ).pack(side="left", padx=6)

        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.canvas = tk.Canvas(container, bg=COLOR_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable = tk.Frame(self.canvas, bg=COLOR_BG)

        self.scrollable.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def set_results(self, result: Dict) -> None:
        self.current_result = result
        self.score_label.config(
            text=(
                f"{result['subject']} | {('Complet' if result['mode'] == 'full' else 'Mini')} | "
                f"Score: {result['correct_count']}/{result['total_questions']} ({result['score_percent']}%)"
            )
        )

        for child in self.scrollable.winfo_children():
            child.destroy()

        for item in result.get("details", []):
            card = tk.Frame(self.scrollable, bg=COLOR_PANEL, bd=1, relief="solid")
            card.pack(fill="x", pady=5)

            status_text = "Correct" if item["is_correct"] else "Incorrect"
            status_color = COLOR_SUCCESS if item["is_correct"] else COLOR_DANGER

            tk.Label(
                card,
                text=f"Q{item['id']}. {item['question']}",
                font=FONT_SUBTITLE,
                bg=COLOR_PANEL,
                fg=COLOR_TEXT,
                anchor="w",
                justify="left",
                wraplength=780,
            ).pack(fill="x", padx=12, pady=(10, 2))

            user_answer = item["user_answer"] if item["user_answer"] is not None else "Aucune"
            # Display all options and mark correct/user choices
            opts = item.get("options", [])
            user_letter = item.get("user_answer")
            correct_letter = item.get("correct")
            for idx, opt_text in enumerate(opts):
                letter = ["A", "B", "C", "D"][idx]
                badges = []
                fg = COLOR_TEXT
                if letter == correct_letter:
                    badges.append("Bonne reponse")
                    fg = COLOR_SUCCESS
                if user_letter is not None and letter == user_letter:
                    badges.append("Votre choix")
                    # if user chose wrong, emphasize with accent
                    if letter != correct_letter:
                        fg = COLOR_ACCENT

                badge_text = (" (" + ", ".join(badges) + ")") if badges else ""
                tk.Label(
                    card,
                    text=f"{letter}) {opt_text}{badge_text}",
                    font=FONT_TEXT,
                    bg=COLOR_PANEL,
                    fg=fg,
                    anchor="w",
                    justify="left",
                    wraplength=760,
                ).pack(fill="x", padx=12)

            tk.Label(
                card,
                text=f"Explication: {item.get('explanation', '')}",
                font=FONT_TEXT,
                bg=COLOR_PANEL,
                fg=COLOR_MUTED,
                anchor="w",
                justify="left",
                wraplength=780,
            ).pack(fill="x", padx=12, pady=(2, 2))

            tk.Label(
                card,
                text=f"Statut: {status_text}",
                font=FONT_TEXT,
                bg=COLOR_PANEL,
                fg=status_color,
                anchor="w",
            ).pack(fill="x", padx=12, pady=(0, 10))

    def export_pdf(self) -> None:
        if not self.current_result:
            messagebox.showwarning("Attention", "Aucun resultat a exporter.")
            return

        user_name = simpledialog.askstring("Nom", "Entrez votre nom pour le PDF:")
        if not user_name:
            return

        try:
            output = self.app.export_pdf(self.current_result, user_name)
            messagebox.showinfo("PDF", f"PDF genere: {output}")
        except Exception as exc:
            messagebox.showerror("Erreur PDF", f"Impossible de generer le PDF.\n{exc}")


class HistoryScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        header = tk.Frame(self, bg=COLOR_BG)
        header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(header, text="Historique des quiz", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(
            side="left"
        )

        tk.Button(
            header,
            text="Retour Menu",
            font=FONT_BUTTON,
            command=lambda: self.app.show_screen("menu"),
        ).pack(side="right")

        self.tree = ttk.Treeview(
            self,
            columns=("date", "subject", "mode", "score"),
            show="headings",
            height=18,
        )
        self.tree.heading("date", text="Date")
        self.tree.heading("subject", text="Matiere")
        self.tree.heading("mode", text="Mode")
        self.tree.heading("score", text="Score")

        self.tree.column("date", width=180, anchor="center")
        self.tree.column("subject", width=140, anchor="center")
        self.tree.column("mode", width=120, anchor="center")
        self.tree.column("score", width=180, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.app.history_manager.load_history():
            mode = "Complet" if item.get("mode") == "full" else "Mini"
            score = f"{item.get('score_correct', 0)}/{item.get('total_questions', 0)} ({item.get('score_percent', 0)}%)"
            self.tree.insert(
                "",
                "end",
                values=(
                    item.get("created_at", ""),
                    item.get("subject", ""),
                    mode,
                    score,
                ),
            )
