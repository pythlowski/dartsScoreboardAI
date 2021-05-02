darts = [0 for i in range(22)]
games = 0


with open('aroundtheclock.txt', 'r') as f:
    _ = f.readline()
    lines = f.readlines()
    games = len(lines)

    for line in lines:
        sum = 0
        bull_and_25 = 0
        data = line.split(';')

        assert len(data) == 23

        for i, n in enumerate(data[1:]):
            number = int(n)
            darts[i] += number
            if i < 20:
                sum += number
            else:
                bull_and_25 += number
        print(f'{data[0]} - Darts needed for doubles: ({sum}), bull and 25: ({bull_and_25}), overall: ({sum + bull_and_25})')

print('Averages:')
for i, dart in enumerate(darts):
    if i < 20:
        dart_name = f'D{i+1}'
    elif i == 20:
        dart_name = '25'
    else:
        dart_name = 'BULL'

    print(f'{dart_name}: {dart/games}')


