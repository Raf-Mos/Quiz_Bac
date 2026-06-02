import json
from pathlib import Path


def load_questions(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Questions file not found: {file_path}")

    # Use utf-8-sig to gracefully handle Windows-generated UTF-8 BOM files.
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    required_subjects = ["Maths", "PC", "SVT"]
    for subject in required_subjects:
        if subject not in data:
            raise ValueError(f"Missing subject in questions data: {subject}")
        if not isinstance(data[subject], list):
            raise ValueError(f"Subject questions must be a list: {subject}")

    return data
