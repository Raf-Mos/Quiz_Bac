import random
import time
from typing import Dict, List, Optional


class QuizModel:
    def __init__(self, questions_data: Dict[str, List[Dict]]):
        self.questions_data = questions_data
        self.current_subject: Optional[str] = None
        self.quiz_mode: str = "full"
        self.questions_list: List[Dict] = []
        self.user_answers: Dict[int, Dict] = {}
        self.current_index: int = 0
        self.current_question_started_at: float = 0.0

    def load_quiz(self, subject: str, mode: str = "full") -> List[Dict]:
        if subject not in self.questions_data:
            raise ValueError(f"Unknown subject: {subject}")
        if mode not in ("full", "mini"):
            raise ValueError("Mode must be 'full' or 'mini'")

        source = list(self.questions_data[subject])
        if mode == "mini":
            selected = random.sample(source, min(10, len(source)))
        else:
            selected = source

        random.shuffle(selected)

        self.current_subject = subject
        self.quiz_mode = mode
        self.questions_list = selected
        self.user_answers = {}
        self.current_index = 0
        self.current_question_started_at = time.time()
        return self.questions_list

    def get_current_question(self) -> Optional[Dict]:
        if 0 <= self.current_index < len(self.questions_list):
            return self.questions_list[self.current_index]
        return None

    def start_question_timer(self) -> None:
        self.current_question_started_at = time.time()

    def save_answer(self, question_id: int, answer: Optional[str]) -> None:
        elapsed = max(0.0, time.time() - self.current_question_started_at)
        self.user_answers[question_id] = {
            "answer": answer,
            "response_time_sec": round(elapsed, 2),
        }

    def go_next(self) -> bool:
        self.current_index += 1
        return self.current_index < len(self.questions_list)

    def calculate_score(self) -> Dict:
        details = []
        for q in self.questions_list:
            qid = q["id"]
            user = self.user_answers.get(qid, {"answer": None, "response_time_sec": 45.0})
            user_answer = user.get("answer")
            is_correct = user_answer == q["correct"]
            details.append(
                {
                    "id": qid,
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"],
                    "explanation": q.get("explanation", ""),
                    "user_answer": user_answer,
                    "response_time_sec": user.get("response_time_sec", 45.0),
                    "is_correct": is_correct,
                }
            )

        # Display and export must follow original order by question id.
        details_sorted = sorted(details, key=lambda x: x["id"])
        correct_count = sum(1 for d in details_sorted if d["is_correct"])
        total = len(details_sorted)
        percent = round((correct_count / total) * 100, 2) if total else 0.0

        return {
            "subject": self.current_subject,
            "mode": self.quiz_mode,
            "correct_count": correct_count,
            "total_questions": total,
            "score_percent": percent,
            "details": details_sorted,
        }
