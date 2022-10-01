from random import randint

f = open('input2.txt', 'w')

f.write('1\n')
m = randint(1, 50000)
n = randint(1, 50000)
k = randint(max(m, n), m+n-1)
# m, n, k = 100, 100, 150
f.write(f'{m} {n} {k}\n')
for _ in range(m):
    f.write(f'{randint(1, 11) // 10 + 1} ')
f.write('\n')
for _ in range(n):
    f.write(f'{randint(1, 11) // 10 + 1} ')
f.write('\n')
f.close()
