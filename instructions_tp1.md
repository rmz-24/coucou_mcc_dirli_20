## TP 1 · CryptoBox, brique 1 : le message à trois couches

Ce TP comporte **deux parties** : d'abord le **projet** (votre outil CryptoBox), puis le **challenge**, que vous devez résoudre **avec votre propre outil**.

**Partie 1 · Le projet : brique 1 de CryptoBox**

En binôme, dans votre dépôt GitHub, développez un outil qui fonctionne pour **n'importe quel message et n'importe quelle clé**. Codez-le vous-mêmes, sans bibliothèque de cryptographie :

- **César** : chiffrer, déchiffrer, et une **force brute** qui teste les 25 clés
- **Substitution** : chiffrer et déchiffrer avec une clé de 26 lettres
- **Transposition par colonnes** : chiffrer et déchiffrer avec un mot-clé

Le langage et l'interface (terminal, fenêtre, web) sont libres. Cet outil sera complété à chaque séance : soignez-le.

**Conventions à respecter**

- Lettres majuscules A à Z uniquement, sans espaces ni accents
- César : `C = (M + k) mod 26`
- Substitution : la clé est un alphabet de 26 lettres. A est remplacé par la 1re lettre de la clé, B par la 2e, etc.
- Transposition : on écrit le message en lignes sous le mot-clé (la dernière ligne est complétée par des X), on numérote les colonnes dans l'ordre alphabétique des lettres du mot-clé, puis on lit chaque colonne de haut en bas, dans cet ordre.

**Testez votre outil avec ces exemples**

- César, k = 3 : `BONJOUR` donne `ERQMRXU`
- Substitution, clé `QWERTYUIOPASDFGHJKLZXCVBNM` : `ATTAQUE` donne `QZZQJXT`
- Transposition, mot-clé `PORTE` : `RENDEZVOUSAMIDI` donne `ESIEVMRZANOIDUD`

**Partie 2 · Le challenge : un message à trois couches**

Une fois votre outil prêt, utilisez-le pour déchiffrer le message de votre binôme, donné dans votre sujet. Ce message a été chiffré en trois couches : **César** (clé k secrète), **substitution** et **transposition** (clés données dans votre sujet). L'ordre des couches est propre à chaque binôme et indiqué dans votre sujet.

Pour lire le message, retirez les couches dans l'ordre inverse de celui du chiffrement : la dernière couche appliquée est la première à retirer.

**La clé César est ++inconnue++** : retrouvez-la avec votre force brute. Si César n'est pas la dernière couche à retirer, testez chacune des 25 clés en retirant aussi les couches qui suivent, et gardez la seule qui donne un texte lisible.

Le message final contient votre flag.

**À rendre avant la séance 2**

- Le flag, au format `BSD{XXXXXXXX}` (8 lettres majuscules)
- Le lien de votre dépôt GitHub : le code de l'outil doit y être poussé avant la date limite

Le flag prouve que votre outil fonctionne, mais **votre code est aussi évalué** : un flag sans code dans le dépôt ne compte pas.

*Début du TP 2 : 2 binômes tirés au sort présentent leur outil en partage d'écran.*

**Votre message intercepté (binôme 48)**

```
IDADCFGWGDTD
```

**Ordre dans lequel il a été chiffré**

- Couche 1 : **Substitution**, clé `OXNKQBTYURPADGCFHIZSWJMVLE`
- Couche 2 : **Transposition**, mot-clé `POULET`
- Couche 3 : **César**, clé k inconnue (à retrouver par force brute)

Pour déchiffrer : retirez d'abord la couche 3, puis la couche 2, puis la couche 1. Les 8 premières lettres du message déchiffré forment votre flag.

À rendre avant le samedi 5 décembre à 00h41