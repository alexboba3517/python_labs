m = int(input(f'Минуты: '))
h = m // 60
mm = m % 60
print(f'{h}:{mm:02d}')