"""CryptoBox - brique 1 : César, substitution, transposition par colonnes.

Toutes les fonctions travaillent sur des lettres majuscules A-Z uniquement.
Aucune bibliothèque de cryptographie n'est utilisée.
"""

import argparse
import sys
import unicodedata

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def normaliser(texte):
    """Met en majuscules, retire accents, espaces et tout caractère hors A-Z."""
    sans_accents = unicodedata.normalize("NFD", texte)
    sans_accents = "".join(c for c in sans_accents if unicodedata.category(c) != "Mn")
    return "".join(c for c in sans_accents.upper() if c in ALPHABET)


# ---------------------------------------------------------------------------
# César : C = (M + k) mod 26
# ---------------------------------------------------------------------------

def cesar_chiffrer(message, k):
    message = normaliser(message)
    return "".join(ALPHABET[(ALPHABET.index(c) + k) % 26] for c in message)


def cesar_dechiffrer(chiffre, k):
    return cesar_chiffrer(chiffre, -k)


def cesar_force_brute(chiffre):
    """Retourne la liste des couples (k, texte) pour les 25 clés k = 1..25."""
    return [(k, cesar_dechiffrer(chiffre, k)) for k in range(1, 26)]


# ---------------------------------------------------------------------------
# Substitution : A -> cle[0], B -> cle[1], ...
# ---------------------------------------------------------------------------

def verifier_cle_substitution(cle):
    cle = normaliser(cle)
    if len(cle) != 26 or set(cle) != set(ALPHABET):
        raise ValueError("La clé de substitution doit contenir les 26 lettres, chacune une seule fois.")
    return cle


def substitution_chiffrer(message, cle):
    cle = verifier_cle_substitution(cle)
    message = normaliser(message)
    return "".join(cle[ALPHABET.index(c)] for c in message)


def substitution_dechiffrer(chiffre, cle):
    cle = verifier_cle_substitution(cle)
    chiffre = normaliser(chiffre)
    return "".join(ALPHABET[cle.index(c)] for c in chiffre)


# ---------------------------------------------------------------------------
# Transposition par colonnes
# ---------------------------------------------------------------------------

def ordre_colonnes(mot_cle):
    """Indices des colonnes dans l'ordre de lecture (ordre alphabétique du mot-clé).

    En cas de lettres répétées, la colonne la plus à gauche passe en premier.
    """
    mot_cle = normaliser(mot_cle)
    if not mot_cle:
        raise ValueError("Le mot-clé de transposition ne peut pas être vide.")
    return sorted(range(len(mot_cle)), key=lambda i: (mot_cle[i], i))


def transposition_chiffrer(message, mot_cle):
    message = normaliser(message)
    ordre = ordre_colonnes(mot_cle)
    n = len(ordre)
    if len(message) % n:
        message += "X" * (n - len(message) % n)
    lignes = [message[i:i + n] for i in range(0, len(message), n)]
    return "".join("".join(ligne[col] for ligne in lignes) for col in ordre)


def transposition_dechiffrer(chiffre, mot_cle):
    chiffre = normaliser(chiffre)
    ordre = ordre_colonnes(mot_cle)
    n = len(ordre)
    if len(chiffre) % n:
        raise ValueError("La longueur du texte chiffré doit être un multiple de la longueur du mot-clé.")
    nb_lignes = len(chiffre) // n
    colonnes = [None] * n
    for rang, col in enumerate(ordre):
        colonnes[col] = chiffre[rang * nb_lignes:(rang + 1) * nb_lignes]
    return "".join(colonnes[c][r] for r in range(nb_lignes) for c in range(n))


# ---------------------------------------------------------------------------
# Vigenère (TP 2)
# ---------------------------------------------------------------------------

def preparer(texte):
    """Majuscules et accents retirés, mais espaces, chiffres et ponctuation conservés.

    Exemple : "Clé à l'école" -> "CLE A L'ECOLE".
    """
    decompose = unicodedata.normalize("NFD", texte)
    sans_accents = "".join(c for c in decompose if unicodedata.category(c) != "Mn")
    return sans_accents.upper().replace("Œ", "OE").replace("Æ", "AE")


def _vigenere(texte, cle, sens):
    cle = normaliser(cle)
    if not cle:
        raise ValueError("La clé de Vigenère doit contenir au moins une lettre.")
    resultat = []
    i = 0  # position dans la clé : n'avance que sur les lettres
    for c in preparer(texte):
        if c in ALPHABET:
            decalage = ALPHABET.index(cle[i % len(cle)])
            resultat.append(ALPHABET[(ALPHABET.index(c) + sens * decalage) % 26])
            i += 1
        else:
            resultat.append(c)
    return "".join(resultat)


def vigenere_chiffrer(message, cle):
    return _vigenere(message, cle, +1)


def vigenere_dechiffrer(chiffre, cle):
    return _vigenere(chiffre, cle, -1)


def colonnes(texte, longueur):
    """Découpe les lettres du texte en `longueur` colonnes (lettres 1, 1+L, 1+2L... puis 2, 2+L...)."""
    lettres = normaliser(texte)
    return [lettres[i::longueur] for i in range(longueur)]


def lettre_plus_frequente(texte):
    """Lettre la plus fréquente ; en cas d'égalité, la première dans l'alphabet."""
    comptes = [texte.count(l) for l in ALPHABET]
    return ALPHABET[comptes.index(max(comptes))]


def vigenere_casser(chiffre, longueur):
    """Retrouve la clé d'un texte français chiffré par Vigenère, connaissant sa longueur.

    Dans chaque colonne, la lettre la plus fréquente est supposée être un E chiffré :
    décalage = lettre - E (mod 26), et la lettre de clé est celle de rang décalage.
    """
    if longueur < 1:
        raise ValueError("La longueur de clé doit être au moins 1.")
    cle = ""
    for col in colonnes(chiffre, longueur):
        if not col:
            raise ValueError("Texte trop court pour cette longueur de clé.")
        decalage = (ALPHABET.index(lettre_plus_frequente(col)) - ALPHABET.index("E")) % 26
        cle += ALPHABET[decalage]
    return cle


def indice_coincidence(texte):
    """Probabilité que deux lettres tirées au hasard soient identiques.

    Environ 0,074 pour du français, 0,038 pour des lettres aléatoires.
    """
    n = len(texte)
    if n < 2:
        return 0.0
    return sum(texte.count(l) * (texte.count(l) - 1) for l in ALPHABET) / (n * (n - 1))


# Fréquences des lettres en français (en %), pour juger si un texte est « lisible ».
FREQUENCES_FR = {
    "A": 8.15, "B": 0.97, "C": 3.15, "D": 3.73, "E": 17.39, "F": 1.12, "G": 0.97,
    "H": 0.85, "I": 7.31, "J": 0.45, "K": 0.02, "L": 5.69, "M": 2.87, "N": 7.12,
    "O": 5.28, "P": 2.80, "Q": 1.21, "R": 6.64, "S": 8.14, "T": 7.22, "U": 6.38,
    "V": 1.64, "W": 0.03, "X": 0.41, "Y": 0.28, "Z": 0.15,
}

# Un texte français donne un score proche de 0 ; un texte mal déchiffré, plusieurs unités.
SEUIL_LISIBLE = 0.2


def score_francais(texte):
    """Distance du khi-deux (normalisée par la longueur) entre le texte et le français."""
    lettres = normaliser(texte)
    n = len(lettres)
    if n == 0:
        return float("inf")
    score = 0.0
    for l in ALPHABET:
        attendu = n * FREQUENCES_FR[l] / 100
        score += (lettres.count(l) - attendu) ** 2 / attendu
    return score / n


def vigenere_candidats(chiffre, l_min=2, l_max=10):
    """Pour chaque longueur L : (L, IC moyen des colonnes, clé, score français, aperçu)."""
    resultats = []
    for L in range(l_min, l_max + 1):
        ic = sum(indice_coincidence(c) for c in colonnes(chiffre, L)) / L
        cle = vigenere_casser(chiffre, L)
        clair = vigenere_dechiffrer(chiffre, cle)
        apercu = " ".join(clair.split())[:60]
        resultats.append((L, ic, cle, score_francais(clair), apercu))
    return resultats


def vigenere_longueur_probable(chiffre, l_min=2, l_max=10):
    """Plus petite longueur L dont le texte déchiffré est lisible (score français < seuil).

    Si aucune ne passe le seuil, on garde celle qui a le meilleur score.
    """
    candidats = vigenere_candidats(chiffre, l_min, l_max)
    for L, _, _, score, _ in candidats:
        if score < SEUIL_LISIBLE:
            return L
    return min(candidats, key=lambda c: c[3])[0]


# ---------------------------------------------------------------------------
# Interface en ligne de commande
# ---------------------------------------------------------------------------

def lire_texte(args):
    if args.fichier:
        with open(args.fichier, encoding="utf-8") as f:
            return f.read()
    if args.texte is None or args.texte == "-":
        return sys.stdin.read()
    return args.texte


def construire_parser():
    p = argparse.ArgumentParser(prog="cryptobox", description="CryptoBox - outils de chiffrement classiques")
    sous = p.add_subparsers(dest="algo", required=True)

    c = sous.add_parser("cesar", help="Chiffrement de César")
    c.add_argument("mode", choices=["chiffrer", "dechiffrer", "brute"])
    c.add_argument("texte")
    c.add_argument("-k", "--cle", type=int, help="clé (0-25), inutile en mode brute")

    s = sous.add_parser("substitution", help="Substitution mono-alphabétique")
    s.add_argument("mode", choices=["chiffrer", "dechiffrer"])
    s.add_argument("texte")
    s.add_argument("-k", "--cle", required=True, help="alphabet de 26 lettres")

    t = sous.add_parser("transposition", help="Transposition par colonnes")
    t.add_argument("mode", choices=["chiffrer", "dechiffrer"])
    t.add_argument("texte")
    t.add_argument("-k", "--cle", required=True, help="mot-clé")

    v = sous.add_parser("vigenere", help="Chiffrement de Vigenère et casseur")
    v.add_argument("mode", choices=["chiffrer", "dechiffrer", "casser"])
    v.add_argument("texte", nargs="?", help="texte (ou '-' / rien pour lire l'entrée standard)")
    v.add_argument("-f", "--fichier", help="lire le texte dans un fichier")
    v.add_argument("-k", "--cle", help="clé (chiffrer / dechiffrer)")
    v.add_argument("-l", "--longueur", type=int,
                   help="longueur de la clé (casser) ; absente = essai de L = 2 à 10")
    v.add_argument("-q", "--quiet", action="store_true", help="casser : n'afficher que la clé")

    return p


def afficher(texte):
    """Affiche un texte sans ajouter de ligne vide s'il finit déjà par un retour à la ligne."""
    print(texte, end="" if texte.endswith("\n") else "\n")


def commande_vigenere(args):
    texte = lire_texte(args)
    if args.mode in ("chiffrer", "dechiffrer"):
        if not args.cle:
            print("Erreur : la clé -k est requise.", file=sys.stderr)
            return 1
        f = vigenere_chiffrer if args.mode == "chiffrer" else vigenere_dechiffrer
        afficher(f(texte, args.cle))
        return 0

    if args.longueur:
        L = args.longueur
    else:
        L = vigenere_longueur_probable(texte)
        if not args.quiet:
            print("Longueur inconnue : essai de L = 2 à 10")
            print(f"  {'L':>2}  {'IC moyen':>8}  {'score FR':>8}  {'clé':<10}  début du texte déchiffré")
            for l, ic, cle, score, apercu in vigenere_candidats(texte):
                marque = " <==" if l == L else ""
                print(f"  {l:>2}  {ic:8.4f}  {score:8.3f}  {cle:<10}  {apercu[:36]}{marque}")
            print()
    cle = vigenere_casser(texte, L)
    if args.quiet:
        print(cle)
        return 0
    print(f"Longueur : {L}")
    print(f"Clé      : {cle}")
    print()
    afficher(vigenere_dechiffrer(texte, cle))
    return 0


def main(argv=None):
    args = construire_parser().parse_args(argv)
    try:
        if args.algo == "cesar":
            if args.mode == "brute":
                for k, texte in cesar_force_brute(args.texte):
                    print(f"k={k:2d} : {texte}")
                return 0
            if args.cle is None:
                print("Erreur : la clé -k est requise.", file=sys.stderr)
                return 1
            f = cesar_chiffrer if args.mode == "chiffrer" else cesar_dechiffrer
            print(f(args.texte, args.cle))
        elif args.algo == "vigenere":
            return commande_vigenere(args)
        elif args.algo == "substitution":
            f = substitution_chiffrer if args.mode == "chiffrer" else substitution_dechiffrer
            print(f(args.texte, args.cle))
        else:
            f = transposition_chiffrer if args.mode == "chiffrer" else transposition_dechiffrer
            print(f(args.texte, args.cle))
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
