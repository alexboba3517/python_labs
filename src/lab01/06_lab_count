n = int(input(f'in_1:'))
full_time = 0
part_time = 0
def form(x):
    surname, name, age, education = x.split()
    if education == 'True':
        return 1
    else:
        return 0
for i in range(n):
    x = input(f'in_{i+2}:')
    if form(x) == 1:
        full_time += 1
    else:
        part_time += 1
print(f'out: {full_time} {part_time}')