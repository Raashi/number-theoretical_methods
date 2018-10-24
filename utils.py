from operator import add
from functools import reduce

import euclid

MAX_B_SIZE = 5000
MAX_SUBSET = 30


class Vector:
    @staticmethod
    def zero(n):
        return [0] * n

    @staticmethod
    def is_zero(x):
        return all(el == 0 for el in x)

    @staticmethod
    def add(x, y, p):
        return [(xx + yy) % p for xx, yy in zip(x, y)]

    @staticmethod
    def minus(x, y, p):
        return [(xx - yy) % p for xx, yy in zip(x, y)]

    @staticmethod
    def summarise(x, p):
        return reduce(add, x) % p

    @staticmethod
    def mul_scalar(x, alpha, p):
        return [(xx * alpha) % p for xx in x]

    @staticmethod
    def mul(x, y, p):
        assert len(x) == len(y)
        return [(x[i] * y[i]) % p for i in range(len(x))]

    @staticmethod
    def mul_sum(x, y, p):
        return Vector.summarise(Vector.mul(x, y, p), p)


class Matrix:
    @staticmethod
    def zero(n, m):
        return [[0 if i != j else 1 for j in range(m)] for i in range(n)]

    @staticmethod
    def t(a):
        return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]

    @staticmethod
    def column(a, j):
        return [a[i][j] for i in range(len(a))]

    @staticmethod
    def mul(a, b, p):
        assert len(a[0]) == len(b)
        n, m = len(a), len(b[0])
        res = [[Vector.mul_sum(a[row], Matrix.column(b, col), p) for col in range(m)] for row in range(n)]
        return res

    @staticmethod
    def mul_scalar(a, alpha, p):
        return [[a[i][j] * alpha % p for j in range(len(a[0]))] for i in range(len(a))]

    @staticmethod
    def mul_vec(a, x, p):
        # return vec of len(x) = Ax
        return Matrix.t(Matrix.mul(a, Matrix.t([x]), p))[0]

    @staticmethod
    def power(a, deg, p):
        res = Matrix.zero(len(a), len(a))
        for _idx in range(deg):
            res = Matrix.mul(res, a, p)
        return res


class Polynomial:
    @staticmethod
    def ratio(p1, p2, p):
        p1, p2 = p1[:], p2[:]
        q = []
        while len(p1) >= len(p2):
            qi = ratio(p1[0], p2[0], p)
            q.append(qi)
            for j in range(len(p2)):
                p1[j] = (p1[j] - p2[j] * qi) % p
            assert p1[0] == 0
            p1 = p1[1:]
        while len(p1) > 1 and p1[0] == 0:
            p1 = p1[1:]
        return q, p1

    @staticmethod
    def minus(p1, p2, p):
        if len(p1) < len(p2):
            while len(p1) < len(p2):
                p1 = [0] + p1
            while len(p2) < len(p1):
                p2 = [0] + p2
        res = [(p1i - p2i) % p for p1i, p2i in zip(p1, p2)]
        while len(res) > 1 and res[0] == 0:
            res = res[1:]
        return res

    @staticmethod
    def mul(p1, p2, p):
        res = [0] * (len(p1) + len(p2) - 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                res[i + j] = (res[i + j] + p1[i] * p2[j]) % p
        while len(res) > 1 and res[0] == 0:
            res = res[1:]
        return res

    @staticmethod
    def compute(f, v, p):
        res = 0
        for power, fi in enumerate(reversed(f)):
            res = (res + pow(v, power, p) * fi) % p
        return res


def get_inverse(a, m):
    if a == 0:
        return 0
    if euclid.euclid(a, m) != 1:
        raise ValueError('Не существует обратного элемента для a={} по модулю m={}'.format(a, m))
    d, x, y = euclid.eeuclid(a, m)
    assert d == 1
    return x % m


def ratio(p, q, m):
    return (p * get_inverse(q, m)) % m


def fac2k(a):
    k = 0
    while a & 1 == 0:
        a >>= 1
        k += 1
    return a, k


def legendre(a, n):
    a %= n
    if a == 0:
        return 0
    elif a == 1:
        return 1
    return pow(a, (n - 1) // 2, n)


def jacobi(a, n, g=1):
    """Маховенко Е.Б. Теоретико-числовые методы в криптографии, стр 61-62"""
    if a == 0:
        return 0
    elif a == 1:
        return g

    a1, k = fac2k(a)

    if k & 1 == 0 or n % 8 == 1 or n % 8 == 7:
        s = 1
    else:
        s = -1

    if a1 == 1:
        return g * s

    if n % 4 == 3 and a1 % 4 == 3:
        s = -s

    return jacobi(n % a1, a1, g * s)


def generate_base(desired_count):
    base = [2, 3, 5]
    counter = 7
    while len(base) < desired_count:
        for b in base:
            if counter % b == 0:
                break
            if b > counter // 2:
                base.append(counter)
                break
        counter += 1
    return base


def matrix_print(a):
    for row in a:
        print(row)


if __name__ == '__main__':
    pass
