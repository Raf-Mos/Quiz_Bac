# Résumé de la conversation et des actions (abrégé)

Objectif initial
- L'utilisateur a demandé une petite application de quiz QCM couvrant 3 matières scientifiques (Maths, PC, SVT) pour la 2ème année Bac Marocain (option SVT). Chaque matière : 100 questions.
- Spécifications clefs : minuteur 45s par question, corrections affichées uniquement à la fin, export PDF, mini-quiz (10 questions), UI graphique (Tkinter), stockage JSON.

Décisions prises
- Technologie : Python + Tkinter (GUI native).
- Stockage : `data/questions.json` (JSON) et `data/history.json` pour historique.
- Export PDF : `reportlab`.
- Mini-quiz : 10 questions aléatoires sélectionnées parmi les 100.
- Résultats affichés en ordre original par ID (Q1..Qn), même si quiz est affiché en ordre aléatoire.

Travail effectué (étapes principales)
1. Création de la structure de projet et fichiers de base (`app.py`, `main.py`, `models/`, `ui/`, `utils/`).
2. Implémentation de `QuizModel` (support mode `full`/`mini`), `HistoryManager`, et loader JSON (`utils/json_loader.py`).
3. UI : `ui/screens.py` comprenant `MenuScreen`, `SubjectScreen`, `QuizScreen`, `ResultScreen`, `HistoryScreen`.
4. Ajout de `utils/pdf_export.py` pour exporter les résultats en PDF (`reportlab`).
5. Génération initiale de `data/questions.json` via script PowerShell, puis remplacement par `generate_questions.py` pour produire des questions de niveau 2ème Bac selon le programme fourni.
6. Correction d'un bug d'encodage (UTF-8 BOM) : lecture en `utf-8-sig` et réécriture des JSON sans BOM.
7. Installation de Python via `winget` sur la machine et packaging avec `PyInstaller` pour produire `dist/QuizBacSVT.exe` et copie en racine `QuizBacSVT.exe`.

Bugs / problèmes rencontrés et solutions
- Erreur de décodage JSON (BOM) : fixe en lisant avec `utf-8-sig` et en réécrivant les fichiers en UTF-8 sans BOM.
- Absence initiale de Python dans le PATH : j'ai détecté l'exécutable Python installé (`C:\Users\mosta\AppData\Local\Programs\Python\Python312\python.exe`) et utilisé ce chemin pour installer les dépendances et builder l'exe.

Fichiers importants créés
- `main.py`, `app.py`
- `models/quiz_model.py`, `models/history_model.py`
- `ui/screens.py`, `ui/styles.py`
- `utils/json_loader.py`, `utils/pdf_export.py`
- `generate_questions.py` (générateur aligné au programme 2Bac)
- `build_exe.bat`, `launch_quiz.bat`
- `data/questions.json` (300 questions), `data/history.json`
- `QuizBacSVT.exe` (dans `dist/` et à la racine)
- `README.md`, `CONVERSATION_SUMMARY.md` (ce fichier)

Vérifications et résultats
- La banque a été régénérée avec `generate_questions.py` et contient 300 questions.
- Répartition des bonnes réponses vérifiée : A/B/C/D ≈ 25/25/25/25 par matière.
- EXE construit avec `PyInstaller` et placé dans `dist/` puis copié à la racine.

Commandes utiles
- Lancer en Python:
```powershell
python main.py
```

- Lancer l'exécutable:
```powershell
.\QuizBacSVT.exe
```

- Régénérer la banque de questions:
```powershell
python generate_questions.py
```

- Rebuild EXE (reconstruction):
```powershell
.\build_exe.bat
```

Consignes pour la suite
- Modifier/affiner les templates dans `generate_questions.py` pour enrichir les énoncés.
- Ajouter une icône et un raccourci bureau si souhaité.
- Ajouter tests unitaires pour la logique de `QuizModel` si nécessaire.

Si tu veux que je fasse autre chose (améliorer énoncés, ajouter option timer off, export CSV, icône, etc.), dis lequel je commence en priorité.
