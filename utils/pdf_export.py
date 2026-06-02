from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def export_quiz_to_pdf(quiz_result: dict, user_name: str, exports_dir: str) -> str:
    Path(exports_dir).mkdir(parents=True, exist_ok=True)

    subject = quiz_result.get("subject", "Unknown")
    mode = "Complet" if quiz_result.get("mode") == "full" else "Mini"
    safe_date = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
    file_name = f"Quiz_{subject}_{mode}_{safe_date}.pdf"
    output_path = str(Path(exports_dir) / file_name)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 2 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Resultats Quiz Bac Marocain")
    y -= 0.8 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Matiere: {subject}")
    y -= 0.5 * cm
    c.drawString(2 * cm, y, f"Mode: {mode}")
    y -= 0.5 * cm
    c.drawString(2 * cm, y, f"Nom: {user_name}")
    y -= 0.5 * cm
    c.drawString(2 * cm, y, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 0.5 * cm
    c.drawString(
        2 * cm,
        y,
        f"Score: {quiz_result.get('correct_count', 0)}/{quiz_result.get('total_questions', 0)} ({quiz_result.get('score_percent', 0)}%)",
    )
    y -= 0.8 * cm

    details = quiz_result.get("details", [])
    c.setFont("Helvetica", 9)

    for item in details:
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 9)

        c.setFont("Helvetica-Bold", 9)
        c.drawString(2 * cm, y, f"Q{item['id']}: {item['question'][:100]}")
        y -= 0.4 * cm

        c.setFont("Helvetica", 9)
        user_answer = item.get("user_answer") if item.get("user_answer") is not None else "Aucune"
        c.drawString(2 * cm, y, f"Votre reponse: {user_answer}")
        y -= 0.35 * cm
        c.drawString(2 * cm, y, f"Bonne reponse: {item.get('correct')}")
        y -= 0.35 * cm

        expl = item.get("explanation", "")
        c.drawString(2 * cm, y, f"Explication: {expl[:110]}")
        y -= 0.55 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, 1.8 * cm, "Signature: __________________________")
    c.drawString(2 * cm, 1.2 * cm, f"Genere le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    c.save()
    return output_path
