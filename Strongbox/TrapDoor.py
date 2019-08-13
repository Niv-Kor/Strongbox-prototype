import NumeralHandler as nums
import random


class TrapDoor(object):
    def __init__(self):
        self.decryptorKey = None
        self.p = (0, 0)
        self.phi = 0
        self.n = 0
        self.e = 0
        self.d = 0
        self.regenerate()

    # Recalculate all private and public RSA keys
    def regenerate(self):
        self.p = self._generatePrimes(256)

        # calculate n and phi of n
        self.n = self.p[0] * self.p[1]
        self.phi = (self.p[0] - 1) * (self.p[1] - 1)

        # choose a legal e factor
        self.e = self._generateE(self.phi)

        # calculate the d factor
        self.d = self._extendedEuclidean(self.phi, self.e)

    # Calculate d
    def _extendedEuclidean(self, phi, e):
        first = [phi, e]
        second = [phi, 1]

        while True:
            quotient = int(int(first[0]) / int(first[1]))
            firstFormula = first[0] - first[1] * quotient

            if firstFormula < 0:
                firstFormula %= phi

            secondFormula = second[0] - second[1] * quotient

            if secondFormula < 0:
                secondFormula %= phi

            if firstFormula == 1:
                return secondFormula

            first[0] = first[1]
            second[0] = second[1]

            first[1] = firstFormula
            second[1] = secondFormula

    # Generate two prime numbers around the argument n
    def _generatePrimes(self, n):
        primeList = nums.primeList(n / 2, n * 2)

        prime1 = random.choice(primeList)
        primeList.remove(prime1)
        prime2 = random.choice(primeList)

        return prime1, prime2

    def _generateE(self, phi):
        e = 3
        while e % 2 == 0 or not nums.isPrime(e) or phi % e == 0:
            e += 1

        return e

    def setDecryptorKey(self, decKey):
        self.decryptorKey = decKey

    def getPublicKey(self):
        return self.n, self.e

    @staticmethod
    # Get all prime numbers within a range
    def _segmentedSieve(lo, hi):
        # Mark all numbers as prime
        primes = [True] * (hi - lo)

        # Eliminate 0 and 1, if necessary
        for i in range(lo, min(2, hi)):
            primes[i - lo] = False

        ihi = int(hi ** 0.5)
        for i in TrapDoor._potentialPrimes():
            if i > ihi:
                break

            # find first multiple of i: i >= i*i and i >= lo
            ilo = max(i, 1 + (lo - 1) // i) * i

            # determine how many multiples of i >= ilo are in range
            n = 1 + (hi - ilo - 1) // i

            # mark them as composite
            primes[ilo - lo::i] = n * [False]

        return [i for i, v in enumerate(primes, lo) if v]

    @staticmethod
    def _potentialPrimes():
        s = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

        for i in s:
            yield i

        s = (1,) + s[3:]
        j = 30
        while True:
            for i in s:
                yield j + i
            j += 30


