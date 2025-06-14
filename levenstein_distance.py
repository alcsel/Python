import numpy as np

def min(a,b,c):
    if a < b and a < c:
        return a
    elif b < a and b < c:
        return b
    else:
        return c

def max(a,b):
    if a > b:
         return a
    else:
        return b

def normalize(x,size):
    if len(x) < size:
        fark = size - len(x)
        for i in range(fark):
            x = x + " "
    return x

def levenshtein_distance(a,b):
    K= np.zeros((len(a)+1,len(b)+1))
    A_len = len(a)
    B_len = len(b)
    for i in range(A_len+1):
        K[i][0] = i
    for j in range(B_len+1):
        K[0][j] = j

    for i in range(1, A_len+1):
        for j in range(1, B_len+1):
            if a[i-1] == b[j-1]:
                K[i][j] = K[i-1][j-1]
            else:
                silme = K[i-1][j] + 1
                ekleme = K[i][j-1] + 1
                yerdegistirme = K[i-1][j-1] + 1
                K[i][j] = min(silme, ekleme, yerdegistirme)
    return K[A_len][B_len]

print("Levenshtein Mesafe Hesaplama")
a = input("Birinci kelimeyi giriniz: ")
b = input("İkinci kelimeyi giriniz: ")
max_len = max(len(a), len(b))
kelime1 = normalize(a, max_len)
kelime2 = normalize(b, max_len)
mesafe = levenshtein_distance(kelime1, kelime2)
print(f"{kelime1} ve {kelime2} arasındaki Levenshtein mesafesi: {mesafe}")
benzerlik = 1 - (mesafe / max_len)
print(f"{kelime1} ve {kelime2} arasındaki benzerlik oranı: {benzerlik:.2f}")
