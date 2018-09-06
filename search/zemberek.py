from jpype import *
import pandas as pd
from .geniusScraper import getLyrics


df_polarityLexicon = pd.read_excel("search/Polarity_PN.xlsx")

def isVowel(char):
    vowels = ["a", "e", "ı", "i", "o", "ö", "u", "ü"]
    if char in vowels:
        return True
    else:
        return False


def kalin(char):
    vowels = ["a", "ı", "o", "u"]
    if char in vowels:
        return True
    else:
        return False


def ince(char):
    vowels = ["e", "i", "ö", "ü"]
    if char in vowels:
        return True
    else:
        return False


def mastar(word):
    i = -1
    while i < 0:
        letter = word[i]
        if isVowel(letter):
            i = 0
            lastVowel = letter
            if kalin(lastVowel):
                mastar = word + "mak"
                return mastar
            elif ince(lastVowel):
                mastar = word + "mek"
                return mastar
        else:
            i = i - 1


def polarityScore(word, root, flag):
    row = df_polarityLexicon[df_polarityLexicon['Synonyms'] == word]

    if row.empty:
        row = df_polarityLexicon[df_polarityLexicon['Synonyms'] == root]
        if row.empty:
            return False
        else:
            if "p" in row["PolarityLabel"].values[0]:  # Birden fazla ise ne yapılacak?
                score = row["posValue"].values[0]
            else:
                score = row["negValue"].values[0] * -1
        if flag:
            return score * -1
        else:
            return score
    else:
        if "p" in row["PolarityLabel"].values[0]:  # Birden fazla ise ne yapılacak?
            score = row["posValue"].values[0]
        else:
            score = row["negValue"].values[0] * -1
        if flag:
            return score * -1
        else:
            return score


#words = ["zenginlik", "suçlu", "ölmemiş", "evsiz"]


def getFinalScore(kelimeler, zemberek):
    df_lyrics = pd.DataFrame(columns=["Word", "Score"])

    for kelime in kelimeler:
        dictionaryForm = kelime
        negativityFlag = False
        polarity = 0
        if kelime.strip() > '':
            yanit = zemberek.kelimeCozumle(kelime)
            if yanit:
                #print("{}".format(yanit[0]))
                result = str(yanit[0])
                root = result.split(" ")[3]
                rootType = result.split(" ")[4]
                rootType = rootType[:-1]
                rootType = rootType[4:]
                if rootType == "FIIL":
                    dictionaryForm = mastar(root)
                #print("Sözlük hali: " + dictionaryForm)

                #print(result.split(" ")[6][6:])
                i = 8
                while i <= len(result.split()):
                    suffix = result.split(" ")[i]
                    #print(suffix)
                    if "OLUMSUZLUK" in suffix or "YOKLUK" in suffix:
                        negativityFlag = True
                    i = i + 2
                polarity = polarityScore(dictionaryForm, root, negativityFlag)
                #print("Polarity Score: ", polarity)
                #print()
            else:
                print("{} ÇÖZÜMLENEMEDİ".format(kelime))


            df_lyrics.loc[len(df_lyrics)] = [kelime, polarity]

    #shutdownJVM()  # JVM kapat

    return df_lyrics["Score"].mean()


# song_title = "Dön Bebeğim"
# artist_name = "Tarkan"
# words = getLyrics(song_title, artist_name)
# print("OVERALL SCORE OF THE SONG: ", getFinalScore(words))
