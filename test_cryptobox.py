import unittest

from cryptobox import (
    cesar_chiffrer, cesar_dechiffrer, cesar_force_brute,
    substitution_chiffrer, substitution_dechiffrer,
    transposition_chiffrer, transposition_dechiffrer,
    normaliser,
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


if __name__ == "__main__":
    unittest.main()
