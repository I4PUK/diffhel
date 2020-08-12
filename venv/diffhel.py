import random as rand
import math


# Алгоритм Евклида(нахождение наибольшего общего делителя)
def NOD(a, b):
    if (b == 0):
        return a
    return NOD(b, a % b)


# Генерация m простых чисел
def generatePrimes(m):
    if m < 2: return None
    a = []
    a.append(2)
    a.append(3)
    cnt = 2
    n = 5
    while (cnt < m):
        flag = True
        for i in a:
            if n % i == 0:
                flag = False
                break
        if flag:
            a.append(n)
            cnt += 1
        n += 2
    return a


# Тест простоты числа Рабин - Миллера, возвращает истину если число простое
def RabinMillerTest(n, r=15):
    if n != int(n):
        return False
    n = int(n)

    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):
        a = rand.randrange(2, n)
        if trial_composite(a):
            return False

    return True


# Проверка на простое число:
def IsPrime(n, primes):
    for i in primes:
        if n == i: return True
        if n % i == 0: return False
    return RabinMillerTest(n)


# Генерация простого числа с заданым количеством двоичных знаков
def GenPrimeB(numsig, primes):
    while (True):
        res = 1
        for _ in range(numsig - 1):
            res <<= 1
            res |= rand.randint(0, 2)
        res |= 1  # делаем нечётным
        if IsPrime(res, primes): return res


# Вычисляет  a^n mod m. Бинарное возведение в степень  по модулю
def ModExp(a, n, m):
    res = 1
    p = a % m
    while n:
        if (n & 1):
            res = (res * p) % m
        n >>= 1
        p = (p * p) % m
    return res


# Генерация открытых ключей
def GenerateGPQ(N, numsig, primes):
    q = GenPrimeB(numsig, primes)
    while True:
        n = rand.randint(2, N + 1)
        p = n * q + 1
        if IsPrime(p, primes): break
    while True:
        a = rand.randint(2, p)
        g = ModExp(a, n, p)
        if g != 1: return g, p, q


class keys:
    def __init__(part, name, g, p, q):
        part.name = name
        part.g = g
        part.p = p
        part.q = q
        part.X = rand.randint(2, p)  # закрытый ключ < p
        part.Y = 0
        part.K = 0

    def genY(part):
        return ModExp(part.g, part.X % part.q, part.p)

    def genKey(part):
        part.K = ModExp(part.Y, part.X, part.p)


rand.seed()
primes = generatePrimes(150)
g, p, q = GenerateGPQ(100, 64, primes)
print('g =', g, 'p =', p, 'q =', q)

a = keys('a', g, p, q)
b = keys('b', g, p, q)

b.Y = a.genY()
a.Y = b.genY()
print('Открытый ключ a: ', a.Y)
print('Открытый ключ b: ', b.Y)
a.genKey()
b.genKey()
print(a.K)
print(b.K)
if a.K == b.K:
    print("Закрытые ключи совпали")
else:
    print("Закрытые ключи не совпали")