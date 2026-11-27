# CryptoBox

Classical cipher toolbox, written in pure Python 3 (no cryptography library).

## Brique 1 (TP 1)

- **César**: encrypt, decrypt, brute force over the 25 keys (`C = (M + k) mod 26`)
- **Substitution**: encrypt / decrypt with a 26-letter key alphabet
- **Columnar transposition**: encrypt / decrypt with a keyword (last row padded with `X`)

Input is normalised to uppercase A-Z (accents, spaces and punctuation removed).

## Usage

```bash
python cryptobox.py cesar chiffrer BONJOUR -k 3          # ERQMRXU
python cryptobox.py cesar dechiffrer ERQMRXU -k 3        # BONJOUR
python cryptobox.py cesar brute ERQMRXU                  # 25 candidates

python cryptobox.py substitution chiffrer ATTAQUE -k QWERTYUIOPASDFGHJKLZXCVBNM    # QZZQJXT
python cryptobox.py substitution dechiffrer QZZQJXT -k QWERTYUIOPASDFGHJKLZXCVBNM  # ATTAQUE

python cryptobox.py transposition chiffrer RENDEZVOUSAMIDI -k PORTE     # ESIEVMRZANOIDUD
python cryptobox.py transposition dechiffrer ESIEVMRZANOIDUD -k PORTE   # RENDEZVOUSAMIDI
```

## Tests

```bash
python -m unittest -v
```

## Challenge (binôme 48)

Ciphertext `IDADCFGWGDTD`, encrypted with substitution (`OXNKQBTYURPADGCFHIZSWJMVLE`),
then transposition (`POULET`), then César (unknown k). Layers are removed in reverse order,
testing every César key:

```bash
for k in $(seq 1 25); do
  t=$(python cryptobox.py cesar dechiffrer IDADCFGWGDTD -k $k)
  t=$(python cryptobox.py transposition dechiffrer $t -k POULET)
  echo "$k $(python cryptobox.py substitution dechiffrer $t -k OXNKQBTYURPADGCFHIZSWJMVLE)"
done
```

Only `k = 6` gives readable text: `LUCIOLESBBBB` (the `BBBB` is the `X` padding mapped back
through the substitution). Flag: `BSD{LUCIOLES}`.
