import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from models.history_model import HistoryManager
from models.quiz_model import QuizModel
from ui.screens import HistoryScreen, MenuScreen, QuizScreen, ResultScreen, SubjectScreen
from ui.styles import APP_TITLE, COLOR_BG, WINDOW_MIN_H, WINDOW_MIN_W
from utils.pdf_export import export_quiz_to_pdf
from utils.json_loader import load_questions


class QuizApp(tk.Tk):
    def __init__(self, base_dir: Path):
        super().__init__()

        self.base_dir = base_dir
        self.data_dir = self.base_dir / "data"
        self.exports_dir = self.base_dir / "exports"

        self.title(APP_TITLE)
        self.configure(bg=COLOR_BG)
        self.geometry("1100x760")
        self.minsize(WINDOW_MIN_W, WINDOW_MIN_H)

        try:
            questions_data = load_questions(str(self.data_dir / "questions.json"))
        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible de charger les questions:\n{exc}")
            self.destroy()
            raise

        self.quiz_model = QuizModel(questions_data)
        self.history_manager = HistoryManager(str(self.data_dir / "history.json"))
        self.selected_mode = "full"

        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.screens = {}
        for name, cls in {
            "menu": MenuScreen,
            "subject": SubjectScreen,
            "quiz": QuizScreen,
            "result": ResultScreen,
            "history": HistoryScreen,
        }.items():
            frame = cls(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.screens[name] = frame

        self.show_screen("menu")

    def show_screen(self, screen_name: str) -> None:
        frame = self.screens[screen_name]
        frame.tkraise()
        if screen_name == "history":
            self.screens["history"].refresh()

    def go_to_subject_selection(self, mode: str) -> None:
        self.selected_mode = mode
        self.screens["subject"].set_mode(mode)
        self.show_screen("subject")

    def start_quiz(self, subject: str) -> None:
        try:
            self.quiz_model.load_quiz(subject, self.selected_mode)
        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible de demarrer le quiz:\n{exc}")
            return

        self.show_screen("quiz")
        self.screens["quiz"].start()

    def show_results(self) -> None:
        result = self.quiz_model.calculate_score()
        self.history_manager.save_quiz_result(
            subject=result["subject"],
            mode=result["mode"],
            score_correct=result["correct_count"],
            total_questions=result["total_questions"],
            answers=result["details"],
        )
        self.screens["result"].set_results(result)
        self.show_screen("result")

    def export_pdf(self, result: dict, user_name: str) -> str:
        return export_quiz_to_pdf(result, user_name, str(self.exports_dir))

    def show_history(self) -> None:
        self.show_screen("history")
