import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class HistoryManager:
    def __init__(self, history_path: str):
        self.history_path = Path(history_path)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_path.exists():
            self._write_history([])

    def _read_history(self) -> List[Dict]:
        try:
            with self.history_path.open("r", encoding="utf-8-sig") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            return []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_history(self, data: List[Dict]) -> None:
        with self.history_path.open("w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_quiz_result(
        self,
        subject: str,
        mode: str,
        score_correct: int,
        total_questions: int,
        answers: List[Dict],
    ) -> Dict:
        history = self._read_history()
        item = {
            "subject": subject,
            "mode": mode,
            "score_correct": score_correct,
            "total_questions": total_questions,
            "score_percent": round((score_correct / total_questions) * 100, 2) if total_questions else 0,
            "answers": answers,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        history.append(item)
        self._write_history(history)
        return item

    def load_history(self) -> List[Dict]:
        return self._read_history()
