import hashlib
import random
from gen_pr import *


def global_print(*names):
    x = lambda s: ["{}", "0x{:x}"][hasattr(s, "real")].format(s)
    print("".join("{} = {}\n".format(name, x(globals()[name])) for name in names))
    return None


def H(*args):
    a = "".join(str(a) for a in args)
    return int(hashlib.sha256(a.encode("utf-8")).hexdigest(), 16)


def cryptrand(n: int = 1024):
    return random.SystemRandom().getrandbits(n) % N


q = pr_num()    # простое число
N = 2*q+1       # 2*q+1, где q - простое

# генератор по mod N: для любого 0 < X < N существует единственный x такой, что g^x mod N = X
for i in range(N, 1, -1):
    for x in range(N):
        if x == pow(i, x, N):
            g = i
            break
k = 3   # множитель

print("H, N, g, и k известны и клиенту, и серверу:")
global_print("H", "N", "g", "k")

print("На сервере хранятся (I, s, v)")
# На клиенте генерируются и затем отсылаются на сервер:
I = "person"        # Имя
p = "password"      # Пароль
s = cryptrand(64)   # Соль (случайная строка)
x = H(s, I, p)      # Приватный ключ
v = pow(g, x, N)    # Верификатор пароля
global_print("I", "p", "s", "x", "v")

print("Клиент отправляет на сервер A и I:")
a = cryptrand()     # Генерирует случайное число a
while True:         # Сервер должен убедиться, что A != 0
    A = pow(g, a, N)
    if A != 0:
        break
global_print("I", "A")

# сервер генерирует случайное число b и вычисляет B
print("Сервер отправляет соль и число B клиенту")
b = cryptrand()
while True:     # Проверяет, что B != 0
    B = (k * v + pow(g, b, N)) % N
    if B != 0:
        break
global_print("s", "B")

print("Обе стороны вычислят параметр u")
while True:     # проверка, что u != 0, иначе процесс прерывается
    u = H(A, B)
    if u != 0:
        break
global_print("u")

print("Клиент вычисляет общий ключ сессии")
x = H(s, I, p)
S_c = pow(B - k * pow(g, x, N), a + u * x, N)
K_c = H(S_c)
global_print("S_c", "K_c")

print("Сервер вычисляет общий ключ сессии")
S_s = pow(A * pow(v, u, N), b, N)
K_s = H(S_s)
global_print("S_s", "K_s")
# Ключи должны быть одинаковые

print("Клиент отправляет на сервер M")
M_c = H(H(N) ^ H(g), H(I), S_c, A, B, K_c)
global_print("M_c")

print("Сервер сверяет M клиента со своим. Если M совпадают, сервер отправляет клиенту R")
M_s = H(H(N) ^ H(g), H(I), S_s, A, B, K_s)
R_s = H(A, M_c, K_s)
global_print("M_s")
R_c = H(A, M_s, K_c)

print("Отправка R")
print()
print("R клиента:")
global_print("R_c")
print("R сервера:")
global_print("R_s")
