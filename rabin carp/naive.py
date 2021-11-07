def brute_force(stroka: str, patt: str):
    result = []
    if patt.__len__() > stroka.__len__():
        return result

    leg = patt.__len__() if patt.__len__() != 0 else 1
    for main in range(stroka.__len__() - leg + 1):
        pravda = True
        for pat in range(patt.__len__()):
            if pat == 0 and stroka[main + leg - 1] != patt[-1]:
                pravda = False
                break
            if stroka[main + pat] != patt[pat]:
                pravda = False
                break

        if pravda == True:
            result.append(main)

    return result


PRIME = 101
K = 2**32

def rabinus_karpus(stroka: str, patt: str):
    hashP = ph(patt)
    l_p = patt.__len__()
    l_s = stroka.__len__()
    hashS = ph(stroka[0:l_p])
    pp = PRIME ** l_p
    result = []
    for i in range(l_s - (l_p - 1 if l_p != 0 else 0)):  # ах как мне нравятся костыли
        if hashP == hashS:
            result.append(i)
        if i != l_s - l_p: # ах как мне нравятся костыли
            hashS = (PRIME * hashS - pp * ph(stroka[i]) + ph(stroka[i + l_p])) % K
    return result

def ph(s: str):
    f = 0
    m = s.__len__()
    for i in range(len(s)):
        f += (PRIME ** (m - i)) * ord(s[i])
    return f% K
