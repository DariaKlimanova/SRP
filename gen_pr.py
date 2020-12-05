import random


def generator_pr():
    n = 2000
    numbers = list(range(2, n + 1))
    for number in numbers:
        if number != 0:
            for candidate in range(2 * number, n+1, number):
                numbers[candidate-2] = 0
    return list(filter(lambda x: x != 0, numbers))


def generate():
    p = random.randint(0, 1000)
    p = p | (1 << 0)
    return p


def proverka():
    p = generate()
    lp = generator_pr()
    i = 0
    while i < len(lp):
        if p % lp[i] == 0 and p != lp[i]:
            p = generate()
            i = 0
        else:
            i += 1
    return p


def rev_bin(p_):
    r = []
    while p_ > 0:
        r.append(p_ & 1)
        p_ //= 2
    return r


def test(a, p_):
    b = rev_bin(p_ - 1)
    k = 1
    for i in range(len(b) - 1, -1, -1):
        x = k
        k = (k * k) % p_
        if k == 1 and x != 1 and x != p_ - 1:
            return True
        if b[i] == 1:
            k = (k * a) % p_
    if k != 1:
        return True
    return False


def miller(p_):
    z = []
    if p_ == 1:
        z.append('False')
    s = 5
    for j in range(1, s + 1):
        a = random.randint(1, p_ - 1)
        if test(a, p_):
            z.append('False')
        else:
            z.append('True')
    return z


def pr_num():
    p = proverka()
    while True:
        #print(p, miller(p))
        if 'False' in miller(p):
            p = proverka()
        else:
            break
    return p
