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
# Interface en ligne de commande
# ---------------------------------------------------------------------------

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

    return p


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
