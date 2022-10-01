from random import randint

f = open('input.txt', 'w')

n = 10000000
f.write('1\n')
f.write(f'{n}\n')

for _ in range(n):
    i = randint(-2147483648, 2147483648)
    j = randint(-2147483648, 2147483648)
    k = randint(-2147483648, 2147483648)
    f.write(f'{i} {j} {k}\n')

f.close()
