# Quiz Bac Marocain — 2ème année SVT (Option SVT)

Application QCM en Python (Tkinter) pour préparer le Bac 2ème année (option SVT).

Principales fonctionnalités
- Mode « Quiz Complet » : 100 questions par matière (Maths / PC / SVT)
- Mode « Mini Quiz » : 10 questions aléatoires par matière
- Minuteur : 45 secondes par question (auto-avance)
- Correction : affichée uniquement à la fin, toutes les questions avec explications
- Historique local sauvegardé dans `data/history.json`
- Export PDF des résultats (nom utilisateur, date/heure, espace signature) via `reportlab`

Structure du projet
```
Quiz_Bac/
├── main.py
├── app.py
├── generate_questions.py   # Générateur de la banque (300 Q)
├── build_exe.bat           # Script pour reconstruire l'exécutable
├── QuizBacSVT.exe         # EXE double-clic (généré)
├── data/
│   ├── questions.json     # Banque de 300 questions (100 par matière)
│   └── history.json       # Historique des quiz
├── dist/                  # Sortie PyInstaller
├── exports/               # PDFs générés
├── models/
├── ui/
└── utils/
```

Prérequis
- Windows (testé)
- Python 3.8+ (recommandé 3.12)
- Dépendances Python (si exécution via `python`):

```powershell
pip install reportlab
# (optionnel pour rebuild) pip install pyinstaller
```

Exécuter l'application
- Via Python (en ouvrant le dossier et en lançant) :

```powershell
python main.py
```

- Via l'exécutable (double-clic ou terminal) :

```powershell
.\QuizBacSVT.exe
```

Regénérer la banque de questions
- Pour reconstruire `data/questions.json` avec les énoncés alignés au programme 2ème Bac :

```powershell
python generate_questions.py
```

Reconstruction de l'exécutable
- Le script `build_exe.bat` installe (si besoin) et lance `PyInstaller` puis place l'EXE dans `dist/`.

```powershell
# (déjà fourni) Double-cliquer sur build_exe.bat ou dans le terminal:
.\build_exe.bat
```

Notes importantes
- Encodage JSON : les fichiers sont maintenant gérés en UTF-8 sans BOM; le loader utilise `utf-8-sig` pour tolérer un BOM éventuel.
- Le générateur répartit les réponses correctes sur A/B/C/D pour éviter un biais.
- PDF export utilise `reportlab` et génère des fichiers dans `exports/`.

Fichiers utiles
- `generate_questions.py` : personnaliser les templates et régénérer toutes les questions
- `data/questions.json` : éditable manuellement si vous voulez modifier/ajouter des questions
- `build_exe.bat` : reconstruire l'exécutable
- `launch_quiz.bat` : lance l'exe si présent

Prochaines améliorations possibles
- Ajouter minuteur visuel optionnel ou désactivable
- Ajouter gestion utilisateurs (noms, profils) + export CSV
- Améliorer les énoncés pour coller précisément aux sujets d'examen

Si tu veux, je peux ajouter une icône personnalisée pour `QuizBacSVT.exe` et un raccourci sur le Bureau.
