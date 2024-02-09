#ВЫЧЕСЛЕНИЕ ЧИСЛА ПИ ДО decimal_places ЧИСЕЛ ПОСЛЕ ЗАПЯТОЙ 
from mpmath import mp, sqrt, mpf, pi, log10, fabs

# decimal_place = значение знаков после запятой
decimal_places = 100000 
mp.dps = decimal_places
epsilon = 1/mpf(10**decimal_places)

a = mpf(1)
b = 1/sqrt(mpf(2))

diff = a - b
series = mpf(0)

n = 0
while diff > epsilon:
    n += 1
    arith = (a + b)/2
    geom = sqrt(a*b)
    a, b = arith, geom
    series += 2**(n+1) * (a*a - b*b)
    diff = a - b

my_pi = 4*a*a/(1 - series)

error = fabs(pi - my_pi)
decimal_places = int(-log10(error))

print("Number of steps used: %d" % n)
print("Number of correct decimal places: %d" % decimal_places)
print(pi)
