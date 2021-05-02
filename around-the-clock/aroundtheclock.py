from datetime import datetime


# Here is an interface for an around the clock game. Your task is to hit all double values on board plus both bulls
# in least amount of darts possible.
# You need to enter the number of darts you required to hit the displayed bed.
# All the stats are saved in 'aroundtheclock.txt'.
# You can use analysis.py to get some detailed stats about all registered games.

my_date = datetime.now().strftime('%d-%m-%Y %H:%M')

darts = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11',
         'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', '25', 'BULL']

scores = []
for dart in darts:
    while True:
        try:
            score = int(input(f'{dart} - '))
            break
        except ValueError:
            print(f'Wrong input for D{dart}!')
    scores.append(score)

to_write = my_date + '; ' + '; '.join(('{:3d}'.format(score) for score in scores))
print(f'Challenged completed in {sum(scores)} darts!')
with open('aroundtheclock.txt', 'a') as f:
    f.write(to_write + '\n')
    print('Stats saved.')

