from darts.dart import Dart
from darts.logic import *
from darts.sequences import *
from time import sleep


class AbstractPlayer:
    def __init__(self, alias, mode=501):
        self.alias = alias
        self.mode = mode
        self.starts_leg = True

        self.legs = 0
        self.sets = 0

        self.score = self.mode

        self.first_n = 15

        # self.points_total = 0
        # self.darts_thrown = 0

        self.first_n_points_total = 0
        self.first_n_thrown = 0

        # self.current_leg_darts_thrown = 0

        self.checkouts = []
        self.highest_throw = 0
        # self.darts_to_win_leg = []

        self.leg_stats = []

        self.double_attempts = 0

    def on_leg_start(self):
        self.score = self.mode
        # self.current_leg_darts_thrown = 0
        self.leg_stats.append({'points': 0, 'thrown': 0})
        self.starts_leg = not self.starts_leg

    def visit(self):
        print(f'{self.alias} ({self.score}) is throwing...')
        visit_score = 0
        for i in range(3):
            dart = self.throw_dart(visit_score, 3 - i)

            left = self.score - visit_score
            if left == 50 or (left <= 40 and left % 2 == 0):
                self.double_attempts += 1

            visit_score += dart.score()
            left = self.score - visit_score

            if left == 0 and dart.multiplier == 2:
                self.after_visit(visit_score, i + 1, checkout=True)
                print('CHECKOUT!')
                return True  # checkout
            elif left <= 1:
                self.after_visit(0, i + 1, checkout=False)
                print('BUST!')
                return False  # bust

        self.after_visit(visit_score=visit_score, darts_thrown=i+1, checkout=False)
        return False

    def throw_dart(self, visit_score, in_hand):
        raise NotImplementedError("Must override throw_dart")

    def after_visit(self, visit_score: int, darts_thrown: int, checkout: bool):
        self.score -= visit_score

        # self.points_total += visit_score
        # self.darts_thrown += darts_thrown
        self.leg_stats[-1]['points'] += visit_score
        self.leg_stats[-1]['thrown'] += darts_thrown

        # if self.current_leg_darts_thrown < 9:
        if self.leg_stats[-1]['thrown'] < self.first_n:
            self.first_n_points_total += visit_score
            self.first_n_thrown += darts_thrown

        # self.current_leg_darts_thrown += darts_thrown

        if visit_score > self.highest_throw:
            self.highest_throw = visit_score

        if checkout:
            self.after_checkout(visit_score)

    def after_checkout(self, visit_score):
        self.legs += 1

        self.checkouts.append(visit_score)
        # self.darts_to_win_leg.append(self.current_leg_darts_thrown)

    # def reset_before_leg(self):
    #     self.score = self.mode
    #     self.current_leg_darts_thrown = 0
    #     self.starts_leg = not self.starts_leg

    def scoreboard(self):
        return self.alias, self.legs, self.score, self.starts_leg

    def average(self):
        darts_thrown = sum((leg['thrown'] for leg in self.leg_stats))
        return sum((leg['points'] for leg in self.leg_stats)) / darts_thrown * 3 if darts_thrown else 0

    def first_n_average(self):
        return self.first_n_points_total / self.first_n_thrown * 3 if self.first_n_thrown else 0

    def checkout_percentage(self):
        return self.legs / self.double_attempts * 100 if self.double_attempts else 0

    def advanced_stats(self):
        print(f'\nPlayer {self.alias}')
        print(f'Current AVG: {self.average()}')
        print(f'First {self.first_n} AVG: {self.first_n_average()}')
        print(f'Checkouts: {self.legs}/{self.double_attempts} {int(self.checkout_percentage())}%\n')

    def advanced_advanced_stats(self):
        print(f'\nPlayer {self.alias}')
        print(f'Highest score: {self.highest_throw}')
        print(f"Highest checkout: {max(self.checkouts) if self.checkouts else '-'}")
        # print(f"Fastest leg: {min(self.darts_to_win_leg) if self.darts_to_win_leg else '-'}\n")


class PlayerReal(AbstractPlayer):
    def throw_dart(self, visit_score, in_hand):
        while True:
            dart_str = input('Insert your dart:\n')
            try:
                return Dart(dart_str)
            except:
                pass


class PlayerBot(AbstractPlayer):
    # def __init__(self, alias, mode, sigma, fast=True):
    #     super().__init__(alias, mode)
    #     self.sigma = sigma
    #     self.fast = fast
    #
    def __init__(self, mode, fast=False, alias='', **kwargs):
        self.fast = fast

        if 'avg' in kwargs.keys():
            avg = kwargs['avg']
            self.sigma = self.get_sigma(avg)
            if not alias:
                alias = f'BOT{avg}'
        elif 'sigma' in kwargs.keys():
            self.sigma = kwargs['sigma']
            if not alias:
                alias = f'BOT{self.sigma}'
        else:
            raise AttributeError('Not enough arguments.')
        super().__init__(alias, mode)

    def get_sigma(self, avg):
        p = [1.92314465e-14, -1.35162454e-11,  4.10492848e-09, -7.04580034e-07, 7.49280566e-05,
             -5.07404082e-03,  2.15083489e-01, -5.30500833e+00, 6.22105228e+01]
        len_p = len(p)
        return sum([factor * avg ** (len_p - i - 1) for i, factor in enumerate(p)])

    def throw_dart(self, visit_score: int, in_hand: int) -> Dart:
        left = self.score - visit_score
        if in_hand == 1 and left <= 5 and left % 2 == 1 and self.score in (40, 32, 16, 12):
            target = Dart(20, 1)
            print('Trying to bust...')
        else:
            target = get_target(self.score-visit_score, in_hand)
        print(f'{self.score - visit_score} left. Wants {str(target)}...', end=' ')
        if not self.fast:
            sleep(2.0)
        result = simulate_throw(target, self.sigma)
        print(f'Got {str(result)}')
        return result


class Game:
    def __init__(self, players, first_to, mode=100):
        self.FIRST_TO = first_to
        self.MODE = mode

        assert len(players) <= 2
        self.players = players

    def current_result(self):
        second_player = False
        for player in self.players:
            alias, legs, score, starts_leg = player.scoreboard()
            if second_player:
                print(f"- {score} ({legs}) {'*' if starts_leg else ''} {alias}\n")
            else:
                print(f"\n{alias} {'*' if starts_leg else ''} ({legs}) {score}", end=' ')
                second_player = True

    def on_leg_end_info(self, winner):
        print(f"{winner.alias} won the leg in {winner.leg_stats[-1]['thrown']} darts!")
        self.current_result()

    def average_by_leg_comparison(self):
        def average(data):
            return data['points'] / data['thrown'] * 3
        if len(self.players) == 2:
            print('        ', '{:10s}'.format(self.players[0].alias), '{:10s}'.format(self.players[1].alias))
            print('-' * 30)
            for i, (p1, p2) in enumerate(zip(self.players[0].leg_stats, self.players[1].leg_stats)):
                print('{:8s} {:<10.2f} {:<10.2f}'.format(f'Leg {i + 1}', average(p1), average(p2)))

    def start(self):
        if len(self.players) == 2:
            self.players[0].starts_leg = False

        for p in self.players:
            p.on_leg_start()

        while True:
            for player in self.players if self.players[0].starts_leg else reversed(self.players):
                if player.visit():
                    self.on_leg_end_info(player)
                    self.average_by_leg_comparison()
                    for p in self.players:
                        p.advanced_stats()
                        p.on_leg_start()
                    break
                self.current_result()
            for player in self.players:
                if player.legs == self.FIRST_TO:
                    print(f'{player.alias} is the winner!')
                    for player in self.players:
                        player.advanced_advanced_stats()
                    return


if __name__ == '__main__':

    # Example of a correct setup. You need to set the starting points (usually 501 or 301)
    # and how many legs to win.

    MODE = 501
    FIRST_TO = 4

    # Initialize one or two players.
    # For a bot player you need to set the avg variable. The bot's 3-dart average score will converge to this number.
    # If you set fast to False, there will be delay between each throw
    # to simulate as if the player actually threw darts in real time.

    p1 = PlayerReal(alias='Player', mode=MODE)
    p2 = PlayerBot(mode=MODE, avg=50, fast=False)

    game = Game([p1, p2], first_to=FIRST_TO)
    game.start()
