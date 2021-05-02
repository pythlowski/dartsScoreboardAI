from darts.dart import Dart


# Here is all the logic required to set the optimal goals for a given score left and given number of darts in hand.

# For scores in range(60, 159), the target scores are hardcoded
# to reduce redundant calculations and ensure optimal targets.

def hardcoded_dart(score):
    assert score in range(60, 159)

    if score in [72, 76, 84, 88, 92, 96] + list(range(98, 125)) + list(range(127, 159)):
        return Dart(20, 3)
    elif score in (69, 73, 89, 93, 95, 97, 126):
        return Dart(19, 3)
    elif score in (70, 86, 90, 94):
        return Dart(18, 3)
    elif score in (67, 75, 83, 87, 91):
        return Dart(17, 3)
    elif score in (64, 68, 80, ):
        return Dart(16, 3)
    elif score in (61, 77, 81, 85):
        return Dart(15, 3)
    elif score in (74, 78, 82):
        return Dart(14, 3)
    elif score in (63, 71, 79):
        return Dart(13, 3)
    elif score in (62, 66):
        return Dart(10, 3)
    elif score in (65, 125):
        return Dart(25, 1)


def below_40(score):
    assert score <= 40

    if score % 2 == 0:
        return Dart(int(score/2), 2)
    targets = [20, 16, 8, 18, 12, 4, 2, 1]
    for dart in targets:
        single = score - dart * 2
        if single > 0:
            return Dart(single, 1)
    return None


sequences = {
    (1, 40): lambda x: below_40(x),
    (40, 60): lambda x: Dart(x-40, 1),
    (60, 158): lambda x: hardcoded_dart(x),
    (158, 501): lambda x: Dart(20, 3)
}


def get_target(score, in_hand):
    assert score >= 2

    if in_hand == 1:
        if score == 50: return Dart(25, 2)
        elif score in (182, 185, 188): return Dart(18, 3)
        elif score in (183, 186, 189): return Dart(19, 3)
    elif in_hand == 2:
        if score in range(61, 71): return Dart(score-50, 3)
        elif score in (101, 104, 107, 110): return Dart(int((score-50)/3), 3)

    for score_range, algorithm in sequences.items():
        if score_range[0] < score <= score_range[1]:
            return algorithm(score)


def get_sequence(score):
    sequence = []
    value = 0
    for in_hand in range(3, 0, -1):
        dart = get_target(score - value, in_hand)
        sequence.append(dart)
        value += dart.score()
        if value == score: break
    return sequence


# This is the final function to get optimal checkout for given score

def get_checkout(score):
    if score <= 158 or score in (160, 161, 164, 167, 170):
        return get_sequence(score)
    return None


if __name__ == '__main__':

    for i in range(2, 171):
        if sequence := get_checkout(i):
            print(i, [str(dart) for dart in sequence])
        else:
            print(i)



