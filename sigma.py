from darts.game import *
import matplotlib.pyplot as plt

MODE = 501
FIRST_TO = 25000
sigmas = np.arange(.7, 5, .1)
avgs = []
for sigma in sigmas:
    bot = PlayerBot(alias='bot', mode=MODE, sigma=sigma, fast=True)
    bot2 = PlayerBot(alias='bot', mode=MODE, sigma=sigma, fast=True)
    game = Game([bot, bot2], first_to=FIRST_TO)
    game.start()
    print(sigma, (bot.average()+bot2.average())/2, bot.checkout_percentage())
    avgs.append((bot.average()+bot2.average())/2)

plt.plot(avgs, sigmas)

p = np.polyfit(avgs, sigmas, 8)
print(p)


def get_sigma(avg):
    plen = len(p)
    return sum([factor * avg ** (plen - i - 1) for i, factor in enumerate(p)])


for avg in avgs:
    print(avg, get_sigma(avg))


xs = list(range(30,120,5))
ys = [get_sigma(x) for x in xs]
plt.plot(xs, ys)
plt.show()


