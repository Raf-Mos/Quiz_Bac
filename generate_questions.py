import json
import math
from pathlib import Path


LETTERS = ["A", "B", "C", "D"]

PREFIXES = [
    "Calculer",
    "Déterminer",
    "Trouver",
    "Donner",
    "Quelle est",
]


MATH_TOPICS = [
    "Limites et continuite",
    "Derivation et etude des fonctions",
    "Suites numeriques",
    "Fonctions primitives",
    "Fonctions logarithmiques",
    "Nombres complexes (Partie 1)",
    "Fonctions exponentielles",
    "Nombres complexes (Partie 2)",
    "Calcul integral",
    "Equations differentielles",
    "Geometrie dans l'espace",
    "Denombrement et probabilites",
]

PC_TOPICS = [
    "Ondes mecaniques progressives",
    "Ondes mecaniques progressives periodiques",
    "Propagation des ondes lumineuses",
    "Transformations nucleaires",
    "Noyau (masse et energie)",
    "Dipole RC",
    "Dipole RL",
    "Oscillations libres d'un circuit RLC",
    "Transformations lentes et rapides",
    "Suivi temporel et vitesse de reaction",
    "Transformations chimiques reversibles",
    "Etat d'equilibre d'un systeme chimique",
    "Reactions acide-base",
    "Lois de Newton",
    "Chute libre verticale",
    "Mouvement d'un projectile",
    "Mouvement de rotation",
    "Systemes mecaniques oscillants",
    "Aspects energetiques des oscillations",
    "Evolution spontanee d'un systeme chimique",
    "Piles et production d'energie",
    "Esterification et hydrolyse",
]

SVT_TOPICS = [
    "Consommation de la matiere organique et flux d'energie",
    "Expression du materiel genetique et genie genetique",
    "Transfert de l'information genetique et genetique humaine",
    "Variation et genetique des populations",
    "Formation des chaines de montagnes et tectonique des plaques",
    "Immunologie",
]


def format_num(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.3f}".rstrip("0").rstrip(".")


def make_options(correct: str, distractors, qid: int, subject_seed: int):
    unique = []
    for item in [correct] + list(distractors):
        s = str(item)
        if s not in unique:
            unique.append(s)
    while len(unique) < 4:
        unique.append(f"{correct} ({len(unique)})")

    wrongs = [x for x in unique if x != str(correct)]
    wrongs = wrongs[:3]

    correct_index = (qid + subject_seed) % 4
    options = [None, None, None, None]
    options[correct_index] = str(correct)

    wi = 0
    for i in range(4):
        if options[i] is None:
            options[i] = wrongs[wi]
            wi += 1

    return options, LETTERS[correct_index]


def gen_math(topic: str, qid: int):
    k = qid
    if topic == "Limites et continuite":
        a = (k % 7) + 2
        b = (k % 5) + 1
        c = (k % 6) + 1
        d = (k % 4) + 3
        question = (
            f"Soit la fonction f définie sur R par f(x) = ({a}x + {b})/({c}x + {d}). "
            "Déterminer la limite de f(x) lorsque x→+∞ et justifier la réponse en une phrase."
        )
        correct = format_num(a / c)
        distractors = [format_num(c / a), format_num((a + b) / (c + d)), format_num(a + c)]
        explanation = "Pour une fraction rationnelle de même degré, la limite en +∞ est le rapport des coefficients dominants a/c."
    elif topic == "Derivation et etude des fonctions":
        a = (k % 5) + 2
        b = (k % 4) + 1
        x0 = (k % 3) + 1
        question = (
            f"Soit f définie par f(x) = {a}x^2 - {b}x + 1. (a) Déterminer f'(x). "
            f"(b) Calculer f'({x0}) et expliquer brièvement la méthode."
        )
        correct = format_num(2 * a * x0 - b)
        distractors = [format_num(a * x0 - b), format_num(2 * a - b), format_num(2 * a * x0 + b)]
        explanation = "f'(x)=2ax-b. On remplace ensuite x par x0 pour obtenir f'(x0)."
    elif topic == "Suites numeriques":
        u1 = (k % 6) + 1
        r = (k % 5) + 2
        n = (k % 8) + 3
        question = (
            f"On considère la suite arithmétique de premier terme u1 = {u1} et raison r = {r}. "
            f"Calculer u{n} et justifier la formule utilisée."
        )
        correct = str(u1 + (n - 1) * r)
        distractors = [str(u1 + n * r), str(u1 + (n - 2) * r), str((n - 1) * r)]
        explanation = "Pour une suite arithmétique, u_n = u1 + (n-1)r."
    elif topic == "Fonctions primitives":
        a = (k % 7) + 1
        n = (k % 4) + 1
        question = (
            f"Donner une primitive F de la fonction f définie par f(x) = {a}x^{n} (n entier naturel), en indiquant la constante d'intégration."
        )
        coef = a / (n + 1)
        correct = f"F(x)={format_num(coef)}x^{n+1}+C"
        distractors = [
            f"F(x)={format_num(a*n)}x^{n-1}+C",
            f"F(x)={format_num(a)}x^{n+1}+C",
            f"F(x)={format_num(coef)}x^{n}+C",
        ]
        explanation = "La primitive de ax^n est a/(n+1) x^(n+1) + C, pour n != -1."
    elif topic == "Fonctions logarithmiques":
        a = (k % 4) + 2
        question = (
            f"Résoudre l'équation ln(x) = {a} dans R^+. Donner la solution et préciser la condition sur x."
        )
        correct = f"x=e^{a}"
        distractors = [f"x={a}e", f"x=ln({a})", f"x=e^-{a}"]
        explanation = "On applique l'exponentielle: x = e^a, et on rappelle que x>0."
    elif topic == "Nombres complexes (Partie 1)":
        a = (k % 5) + 1
        b = (k % 4) + 2
        question = (
            f"Soit z = {a} + {b}i. (a) Calculer le module |z|. (b) Justifier la formule utilisée."
        )
        correct = format_num(math.sqrt(a * a + b * b))
        distractors = [str(a + b), format_num(abs(a - b)), str(a * b)]
        explanation = "|a+bi| = sqrt(a^2+b^2)."
    elif topic == "Fonctions exponentielles":
        a = (k % 5) + 2
        question = (
            f"Résoudre sur R l'équation e^(2x) = {a}. Indiquer la méthode utilisée et donner la solution."
        )
        correct = f"x=(1/2)ln({a})"
        distractors = [f"x=2ln({a})", f"x=ln({a})", f"x=ln({a})/4"]
        explanation = "On prend le logarithme puis on divise par 2: x = (1/2) ln(a)."
    elif topic == "Nombres complexes (Partie 2)":
        a = (k % 4) + 1
        b = (k % 3) + 2
        question = (
            f"Soit z = {a} + {b}i. Donner le conjugué de z et montrer brièvement qu'il permet d'obtenir un réel en multipliant z par son conjugué."
        )
        correct = f"{a}-{b}i"
        distractors = [f"-{a}+{b}i", f"{a}+{b}i", f"-{a}-{b}i"]
        explanation = "Le conjugué de a+bi est a-bi ; z*conj(z)=a^2+b^2 est réel."
    elif topic == "Calcul integral":
        a = (k % 6) + 1
        question = (
            f"Calculer I = ∫_0^1 {a} x^2 dx. Présenter les étapes du calcul et donner la valeur exacte."
        )
        correct = format_num(a / 3)
        distractors = [format_num(a / 2), format_num(a), format_num(3 * a)]
        explanation = "∫x^2 dx = x^3/3 ; évaluer entre 0 et 1 donne I = a/3."
    elif topic == "Equations differentielles":
        lam = (k % 4) + 1
        y0 = (k % 5) + 2
        question = (
            f"Résoudre l'équation différentielle y' = {lam} y et trouver la solution vérifiant y(0) = {y0}. "
            "Justifier la méthode choisie."
        )
        correct = f"y={y0}e^{lam}t"
        distractors = [f"y={lam}e^{y0}t", f"y={y0}+{lam}t", f"y={y0}e^{-lam}t"]
        explanation = "La solution générale est y = C e^{λ t}; appliquer y(0)=y0 donne C=y0."
    elif topic == "Geometrie dans l'espace":
        a = (k % 4) + 1
        b = (k % 5) + 1
        c = (k % 6) + 1
        question = (
            f"Soient u = ({a}, {b}, 0) et v = (0, {c}, {b}) dans R^3. Calculer le produit scalaire u·v et expliquer la formule utilisée."
        )
        correct = str(b * c)
        distractors = [str(a * c + b * b), str(a + b + c), str(a * b * c)]
        explanation = "u·v = a*0 + b*c + 0*b = b c."
    else:  # Denombrement et probabilites
        n = (k % 6) + 5
        question = (
            f"Une classe compte {n} élèves. Combien de binômes distincts peut-on former (ordre non significatif) ? "
            "Donnez la formule et expliquez le raisonnement."
        )
        correct = str(n * (n - 1) // 2)
        distractors = [str(n * (n - 1)), str(n + 2), str(2 * n)]
        explanation = "Nombre de combinaisons C(n,2) = n(n-1)/2."

    return question, correct, distractors, explanation


def gen_pc(topic: str, qid: int):
    k = qid
    if topic == "Ondes mecaniques progressives":
        d = (k % 90) + 110
        t = (k % 5) + 1
        question = f"Une perturbation parcourt {d} m en {t} s. La vitesse de propagation vaut :"
        correct = format_num(d / t)
        distractors = [format_num(t / d), format_num(d * t), format_num(d - t)]
        explanation = "La vitesse de propagation est v=d/t."
    elif topic == "Ondes mecaniques progressives periodiques":
        f = (k % 15) + 5
        question = f"Pour une onde periodique de frequence f={f} Hz, la periode T vaut :"
        correct = format_num(1 / f)
        distractors = [str(f), format_num(f / 2), format_num(2 / f)]
        explanation = "T=1/f."
    elif topic == "Propagation des ondes lumineuses":
        n = (k % 4) + 1.2
        question = f"Dans un milieu d'indice n={format_num(n)}, la vitesse de la lumiere vaut :"
        correct = "v=c/n"
        distractors = ["v=c*n", "v=n/c", "v=c+n"]
        explanation = "Dans un milieu transparent: v=c/n."
    elif topic == "Transformations nucleaires":
        question = "Lors d'une desintegration beta-, il y a emission de :"
        correct = "Un electron et un antineutrino"
        distractors = ["Un positon et un neutrino", "Un proton", "Un photon gamma uniquement"]
        explanation = "La beta- emet e- et antineutrino electronique."
    elif topic == "Noyau (masse et energie)":
        dm = ((k % 8) + 1) * 1e-30
        question = "La relation entre defaut de masse et energie de liaison est :"
        correct = "E=dm*c^2"
        distractors = ["E=dm/c^2", "E=dm*c", "E=dm+mc^2"]
        explanation = "Relation d'Einstein: E=dm c^2."
    elif topic == "Dipole RC":
        r = (k % 5 + 1) * 1000
        c = (k % 4 + 1) * 1e-6
        tau = r * c
        question = f"Pour R={r} ohm et C={c:.0e} F, la constante de temps tau vaut :"
        correct = format_num(tau)
        distractors = [format_num(r / c), format_num(c / r), format_num(r + c)]
        explanation = "Pour un dipole RC, tau=RC."
    elif topic == "Dipole RL":
        l = (k % 6 + 1) * 0.1
        r = (k % 5 + 1) * 10
        tau = l / r
        question = f"Pour L={l} H et R={r} ohm, la constante de temps tau vaut :"
        correct = format_num(tau)
        distractors = [format_num(l * r), format_num(r / l), format_num(l + r)]
        explanation = "Pour un dipole RL, tau=L/R."
    elif topic == "Oscillations libres d'un circuit RLC":
        question = "Dans un circuit RLC libre faiblement amorti, la tension est :"
        correct = "Pseudo-periodique amortie"
        distractors = ["Strictement constante", "Lineaire croissante", "Exponentielle pure non oscillante"]
        explanation = "Le regime libre sous-amorti donne des oscillations amorties."
    elif topic == "Transformations lentes et rapides":
        question = "Une transformation est dite quasi-statique lorsqu'elle est :"
        correct = "Suffisamment lente"
        distractors = ["Instantanee", "Toujours irreversible", "Toujours adiabatique"]
        explanation = "Une evolution lente permet de passer par des etats d'equilibre successifs."
    elif topic == "Suivi temporel et vitesse de reaction":
        question = "La vitesse volumique de reaction s'exprime generalement en :"
        correct = "mol.L^-1.s^-1"
        distractors = ["J.s^-1", "m.s^-1", "kg.m^-3"]
        explanation = "La vitesse de reaction est une variation de concentration par unite de temps."
    elif topic == "Transformations chimiques reversibles":
        question = "Une reaction reversible est caracterisee par :"
        correct = "Deux sens direct et inverse"
        distractors = ["Un seul sens", "Une vitesse nulle", "Absence de reactifs"]
        explanation = "La reaction peut evoluer dans les deux sens."
    elif topic == "Etat d'equilibre d'un systeme chimique":
        question = "A l'equilibre chimique, on a :"
        correct = "vitesse_directe = vitesse_inverse"
        distractors = ["reactifs nuls", "produits nuls", "temperature nulle"]
        explanation = "L'equilibre dynamique correspond a l'egalite des vitesses."
    elif topic == "Reactions acide-base":
        question = "Selon Brønsted, un acide est une espece qui :"
        correct = "Cede un proton H+"
        distractors = ["Capte un electron", "Cede un neutron", "Augmente toujours le pH"]
        explanation = "Un acide de Brønsted est donneur de proton."
    elif topic == "Lois de Newton":
        m = (k % 5) + 1
        a = (k % 6) + 1
        question = f"Pour un solide de masse {m} kg et acceleration {a} m/s^2, la resultante vaut :"
        correct = str(m * a) + " N"
        distractors = [str(m + a) + " N", str(m / a) + " N", str(a) + " N"]
        explanation = "Deuxieme loi de Newton: somme(F)=m.a."
    elif topic == "Chute libre verticale":
        question = "En chute libre sans frottements, l'acceleration est :"
        correct = "g vers le bas"
        distractors = ["nulle", "variable sinusoidale", "horizontale"]
        explanation = "La seule force est le poids, donc a=g vers le bas."
    elif topic == "Mouvement d'un projectile":
        question = "Sans frottement de l'air, la trajectoire d'un projectile est :"
        correct = "Parabolique"
        distractors = ["Circulaire", "Rectiligne uniforme", "Exponentielle"]
        explanation = "Sous gravite uniforme, x(t) est affine et y(t) quadratique."
    elif topic == "Mouvement de rotation":
        question = "La relation fondamentale de la dynamique de rotation est :"
        correct = "Somme(M) = J*alpha"
        distractors = ["Somme(F)=J*alpha", "Somme(M)=m*a", "P=J*omega"]
        explanation = "Autour d'un axe fixe, la somme des moments dynamiques vaut J alpha."
    elif topic == "Systemes mecaniques oscillants":
        question = "Pour un oscillateur harmonique ideal, la periode propre depend de :"
        correct = "Parametres du systeme (m,k)"
        distractors = ["Amplitude initiale uniquement", "Couleur du ressort", "Pression atmospherique seulement"]
        explanation = "Exemple ressort-masse: T=2pi*sqrt(m/k)."
    elif topic == "Aspects energetiques des oscillations":
        question = "Dans un oscillateur non amorti, l'energie mecanique totale est :"
        correct = "Conservee"
        distractors = ["Toujours nulle", "Strictement croissante", "Strictement decroissante"]
        explanation = "Sans dissipation, l'energie mecanique reste constante."
    elif topic == "Evolution spontanee d'un systeme chimique":
        question = "L'evolution spontanee d'un systeme chimique se fait vers :"
        correct = "Un etat d'equilibre"
        distractors = ["Un etat impossible", "Toujours reactifs purs", "Temperature absolue nulle"]
        explanation = "Le systeme evolue spontanement vers l'equilibre thermodynamique."
    elif topic == "Piles et production d'energie":
        question = "Dans une pile qui debite, l'energie chimique est convertie en :"
        correct = "Energie electrique"
        distractors = ["Energie nucleaire", "Energie lumineuse uniquement", "Aucune energie"]
        explanation = "Une pile transforme une energie chimique en energie electrique."
    else:  # Esterification et hydrolyse
        question = "L'esterification entre un acide carboxylique et un alcool forme :"
        correct = "Un ester et de l'eau"
        distractors = ["Un acide fort", "Un sel uniquement", "Du dioxygene"]
        explanation = "Reaction classique: acide carboxylique + alcool <-> ester + eau."

    return question, correct, distractors, explanation


def gen_svt(topic: str, qid: int):
    if topic == "Consommation de la matiere organique et flux d'energie":
        question = (
            "Dans un écosystème aquatique, expliquer quel rôle joue la respiration cellulaire dans la production d'énergie pour la cellule. "
            "Quelle molécule est principalement formée lors de ce processus ?"
        )
        correct = "ATP"
        distractors = ["ADN", "Uree", "Acide lactique uniquement"]
        explanation = "La respiration cellulaire transfère l'énergie vers l'ATP, molécule stockant l'énergie utilisable par la cellule."
    elif topic == "Expression du materiel genetique et genie genetique":
        question = (
            "Décrire brièvement les étapes principales de l'expression d'un gène allant de l'ADN à la protéine. "
            "Indiquer l'ordre correct des étapes."
        )
        correct = "Transcription puis traduction"
        distractors = ["Replication puis mitose", "Meiose puis fecondation", "Traduction puis replication"]
        explanation = "L'ADN est transcrit en ARNm (transcription), puis l'ARNm est traduit en protéine (traduction)."
    elif topic == "Transfert de l'information genetique et genetique humaine":
        question = (
            "Expliquez comment la méiose contribue à la diversité génétique chez les organismes diploïdes. "
            "Citer deux mécanismes intervenant."
        )
        correct = "Brassage inter et intrachromosomique"
        distractors = ["Copie identique stricte", "Absence de recombinaison", "Suppression totale des genes"]
        explanation = "Le crossing-over (brassage intrachromosomique) et l'assortiment indépendant des chromosomes (brassage interchromosomique) augmentent la diversité."
    elif topic == "Variation et genetique des populations":
        question = (
            "Dans le modèle de Hardy–Weinberg, quelle hypothèse sur les accouplements est nécessaire pour conserver les fréquences génotypiques ?"
        )
        correct = "Accouplements au hasard"
        distractors = ["Selection naturelle forte", "Mutation tres elevee", "Population tres petite"]
        explanation = "L'équilibre suppose panmixie (accouplements au hasard), absence de sélection, grande population et pas de migration ni de mutation."
    elif topic == "Formation des chaines de montagnes et tectonique des plaques":
        question = (
            "Expliquer comment la convergence de plaques lithosphériques conduit à la formation de chaînes de montagnes. "
            "Donner un exemple."
        )
        correct = "Convergence de plaques lithospheriques"
        distractors = ["Divergence oceanique", "Absence de mouvements", "Evaporation des oceans"]
        explanation = "La collision ou la subduction entre plaques provoque plissement et surrection; exemple: Himalaya (collision Inde-Asie)."
    else:  # Immunologie
        question = (
            "Quel est le rôle principal des lymphocytes B dans la réponse immunitaire adaptative ? "
            "Donner une phrase d'explication."
        )
        correct = "Production d'anticorps"
        distractors = ["Phagocytose rapide", "Contraction musculaire", "Synthese de chlorophylle"]
        explanation = "Les LB se différencient en plasmocytes qui sécrètent des anticorps spécifiques ciblant les antigènes."

    return question, correct, distractors, explanation


def build_subject(subject_name: str, topics, generator, seed: int, seen_global: set):
    questions = []
    pos = 0
    # generate 100 questions, ensure uniqueness of (question + options)
    while len(questions) < 100:
        pos += 1
        base_qid = pos
        topic = topics[(pos - 1) % len(topics)]

        attempt = 0
        max_attempts = 50
        while True:
            qid = base_qid + attempt
            q_text, correct, distractors, explanation = generator(topic, qid)
            # add small variation prefix if not already starting with one
            prefix = PREFIXES[qid % len(PREFIXES)]
            if not any(q_text.startswith(p) for p in PREFIXES):
                q_text = f"{prefix} : {q_text}"

            options, correct_letter = make_options(correct, distractors, qid, seed)
            # use normalized question text as uniqueness key (ignore punctuation/case)
            key = q_text.strip().lower()
            if key not in seen_global:
                seen_global.add(key)
                questions.append(
                    {
                        "id": len(questions) + 1,
                        "topic": topic,
                        "question": q_text,
                        "options": options,
                        "correct": correct_letter,
                        "explanation": explanation,
                    }
                )
                break
            attempt += 1
            if attempt >= max_attempts:
                # force uniqueness by appending a variant tag
                q_text_variant = q_text + f" (variante {attempt})"
                options, correct_letter = make_options(correct, distractors, qid + attempt, seed)
                key = q_text_variant.strip().lower()
                if key not in seen_global:
                    seen_global.add(key)
                    questions.append(
                        {
                            "id": len(questions) + 1,
                            "topic": topic,
                            "question": q_text_variant,
                            "options": options,
                            "correct": correct_letter,
                            "explanation": explanation,
                        }
                    )
                    break
                # if still colliding, keep incrementing attempts until accepted

    return questions


def main():
    seen = set()
    payload = {
        "Maths": build_subject("Maths", MATH_TOPICS, gen_math, seed=0, seen_global=seen),
        "PC": build_subject("PC", PC_TOPICS, gen_pc, seed=1, seen_global=seen),
        "SVT": build_subject("SVT", SVT_TOPICS, gen_svt, seed=2, seen_global=seen),
    }

    out_path = Path("data") / "questions.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("questions.json regenerated:", sum(len(v) for v in payload.values()), "questions")


if __name__ == "__main__":
    main()
