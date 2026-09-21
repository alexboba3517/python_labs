full_name = input(f'ФИО: ')
initials = full_name.split()
print(f'Инициалы: {initials[0][0]}{initials[1][0]}{initials[2][0]}.')
print(f'Длина (символов): {len(initials[0]+initials[1]+initials[2]) + 2}')