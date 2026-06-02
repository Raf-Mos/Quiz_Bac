from pathlib import Path

from app import QuizApp


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    app = QuizApp(base_dir)
    app.mainloop()


if __name__ == "__main__":
    main()
