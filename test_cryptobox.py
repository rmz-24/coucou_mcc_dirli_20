import unittest

from cryptobox import (
    cesar_chiffrer, cesar_dechiffrer, cesar_force_brute,
    substitution_chiffrer, substitution_dechiffrer,
    transposition_chiffrer, transposition_dechiffrer,
    normaliser, preparer,
    vigenere_chiffrer, vigenere_dechiffrer, vigenere_casser,
    vigenere_longueur_probable, indice_coincidence,
)

CLE_SUB = "QWERTYUIOPASDFGHJKLZXCVBNM"


class TestCesar(unittest.TestCase):
    def test_exemple(self):
        self.assertEqual(cesar_chiffrer("BONJOUR", 3), "ERQMRXU")

    def test_aller_retour(self):
        for k in range(26):
            self.assertEqual(cesar_dechiffrer(cesar_chiffrer("ZEBRAXYZ", k), k), "ZEBRAXYZ")

    def test_force_brute(self):
        resultats = cesar_force_brute("ERQMRXU")
        self.assertEqual(len(resultats), 25)
        self.assertIn((3, "BONJOUR"), resultats)


class TestSubstitution(unittest.TestCase):
    def test_exemple(self):
        self.assertEqual(substitution_chiffrer("ATTAQUE", CLE_SUB), "QZZQJXT")

    def test_dechiffrer(self):
        self.assertEqual(substitution_dechiffrer("QZZQJXT", CLE_SUB), "ATTAQUE")

    def test_cle_invalide(self):
        with self.assertRaises(ValueError):
            substitution_chiffrer("A", "ABC")


class TestTransposition(unittest.TestCase):
    def test_exemple(self):
        self.assertEqual(transposition_chiffrer("RENDEZVOUSAMIDI", "PORTE"), "ESIEVMRZANOIDUD")

    def test_dechiffrer(self):
        self.assertEqual(transposition_dechiffrer("ESIEVMRZANOIDUD", "PORTE"), "RENDEZVOUSAMIDI")

    def test_bourrage_x(self):
        chiffre = transposition_chiffrer("BONJOUR", "PORTE")
        self.assertEqual(len(chiffre), 10)
        self.assertEqual(transposition_dechiffrer(chiffre, "PORTE"), "BONJOURXXX")

    def test_lettres_repetees(self):
        self.assertEqual(transposition_dechiffrer(transposition_chiffrer("ATTAQUEALAUBE", "ALLER"), "ALLER")[:13],
                         "ATTAQUEALAUBE")


class TestNormalisation(unittest.TestCase):
    def test_accents_espaces(self):
        self.assertEqual(normaliser("Rendez-vous à midi"), "RENDEZVOUSAMIDI")


import os

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenges", "tp2")


def lire(nom):
    with open(os.path.join(DOSSIER, nom), encoding="utf-8") as f:
        return f.read()


# Texte français d'environ 500 mots : le texte bonus déchiffré.
TEXTE_FR = vigenere_dechiffrer(lire("bonus.txt"), "MUNOIHH")


class TestVigenere(unittest.TestCase):
    def test_exemples(self):
        self.assertEqual(vigenere_chiffrer("ATTAQUE A L'AUBE", "CLE"), "CEXCBYG L P'CFFG")
        self.assertEqual(vigenere_chiffrer("LA CLE, 14H", "TP"), "EP VAX, 14W")

    def test_dechiffrer(self):
        self.assertEqual(vigenere_dechiffrer("CEXCBYG L P'CFFG", "CLE"), "ATTAQUE A L'AUBE")
        self.assertEqual(vigenere_dechiffrer("EP VAX, 14W", "TP"), "LA CLE, 14H")

    def test_preparer(self):
        self.assertEqual(preparer("Clé à l'école"), "CLE A L'ECOLE")

    def test_accents_minuscules(self):
        self.assertEqual(vigenere_chiffrer("attaque à l'aube", "cle"), "CEXCBYG L P'CFFG")

    def test_cle_vide(self):
        with self.assertRaises(ValueError):
            vigenere_chiffrer("ABC", "123")


class TestChallenge(unittest.TestCase):
    def test_flag_vigenere(self):
        self.assertEqual(vigenere_dechiffrer(lire("flag_vigenere.txt").strip(), "KJAMIT"), "HLGLJCDA")

    def test_flag_casseur(self):
        self.assertEqual(vigenere_casser(lire("casseur.txt"), 9), "SFTAUMNJS")

    def test_flag_bonus(self):
        chiffre = lire("bonus.txt")
        L = vigenere_longueur_probable(chiffre)
        self.assertEqual(L, 7)
        self.assertEqual(vigenere_casser(chiffre, L), "MUNOIHH")


class TestCasseur(unittest.TestCase):
    def test_casser_longueur_connue(self):
        for cle in ("CLE", "SOLEIL", "CRYPTOBOX", "ABCDEFGHIJ"):
            chiffre = vigenere_chiffrer(TEXTE_FR, cle)
            self.assertEqual(vigenere_casser(chiffre, len(cle)), cle)

    def test_longueur_inconnue(self):
        for cle in ("SOLEIL", "CRYPTOBOX", "MER"):
            chiffre = vigenere_chiffrer(TEXTE_FR, cle)
            self.assertEqual(vigenere_longueur_probable(chiffre), len(cle))

    def test_indice_coincidence(self):
        self.assertGreater(indice_coincidence(normaliser(TEXTE_FR)), 0.065)
        self.assertLess(indice_coincidence("ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 4), 0.04)


if __name__ == "__main__":
    unittest.main()
