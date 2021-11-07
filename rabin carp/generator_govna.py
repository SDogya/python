import random

ALPHABET = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)]
# данный код работает неадекватно но зато всетаки генерирует строки



#добавляет гарантированные паттерны в строку
def insert(stroka: str, poz: list, pat: str):
    poz.sort()
    for i in range(len(poz)):

        stroka = stroka[0:poz[i]] + pat + stroka[poz[i] + 1:stroka.__len__() - 1]
        if i + 1 < len(poz):
            poz[i + 1] += pat.__len__()

    return stroka

# генерирует строку
def generate_shit_right_now(stroka: str = None, dlina_stroki: int = random.randrange(100, 100000),
                            pattern: str = None, dlina_pattern=None):
    if stroka != None:
        dlina_stroki = stroka.__len__()
    kolvo_patterna = random.randrange(1, 30)

    if (pattern == None):
        pattern = ""
        if (dlina_pattern == None):

            dlina_pattern = random.randrange(1, 1 + int(dlina_stroki / kolvo_patterna))

            for i in range(dlina_pattern):
                pattern += ALPHABET[random.randrange(0, ALPHABET.__len__())]
        else:

            if (dlina_pattern > dlina_stroki):
                dlina_pattern = random.randrange(1, 1 + int(dlina_stroki / kolvo_patterna))
                for i in range(dlina_pattern):
                    pattern += ALPHABET[random.randrange(0, ALPHABET.__len__())]


            for i in range(dlina_pattern):
                pattern += ALPHABET[random.randrange(0, ALPHABET.__len__())]
    if stroka == None:

        stroka = ""

        danger_zone = [i for i in range(dlina_stroki)]
        danger_zone = random.sample(danger_zone, kolvo_patterna)

        for i in range(dlina_stroki - kolvo_patterna * pattern.__len__()):
            stroka += ALPHABET[random.randrange(0, ALPHABET.__len__())]
        stroka = insert(stroka, danger_zone, pattern)

    x = [stroka, pattern]
    return x
