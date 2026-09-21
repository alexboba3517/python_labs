s = input(f'in: ')
pr_al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = [str(i) for i in range(10)]
id= 0
step = 0
for i in s:
    id+=1
    if i in pr_al:
        s = s[id-1:]
final = ''
for i in s:
    step+=1
    if i in num:
        break
for i in range(0, len(s), step):
    final += s[i]
print(f'out: {final}')