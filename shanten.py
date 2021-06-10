import numpy as np
from collections import deque
from copy import deepcopy
import time


# 面子のリスト
sets = [
    np.array([1, 1, 1, 0, 0, 0, 0, 0, 0]),
    np.array([0, 1, 1, 1, 0, 0, 0, 0, 0]),
    np.array([0, 0, 1, 1, 1, 0, 0, 0, 0]),
    np.array([0, 0, 0, 1, 1, 1, 0, 0, 0]),
    np.array([0, 0, 0, 0, 1, 1, 1, 0, 0]),
    np.array([0, 0, 0, 0, 0, 1, 1, 1, 0]),
    np.array([0, 0, 0, 0, 0, 0, 1, 1, 1]),
    np.array([3, 0, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 3, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 3, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 3, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 3, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 3, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 3, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 3, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 3]),
]

# 雀頭のリスト
heads = [
    np.array([2, 0, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 2, 0, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 2, 0, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 2, 0, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 2, 0, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 2, 0, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 2, 0, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 2, 0]),
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 2]),
]


# hand -> int (5進数とみなす)
def encode(hand):
    code = 0
    for h in hand:
        code = (code * 5) + h
    return code


# int -> hand
def decode(code):
    hand = np.zeros(9, dtype=int)
    for i in range(9):
        hand[8-i] = code % 5
        code //= 5
    return hand


# 4面子1雀頭の形を列挙
def complete_hands():
    ret = {}
    for s1 in sets:
        for s2 in sets:
            for s3 in sets:
                for s4 in sets:
                    for head in heads:
                        hand = s1 + s2 + s3 + s4 + head
                        if (hand <= 4).all():
                            ret[encode(hand)] = hand
    return ret


# 01BFSを用いてシャンテン数を計算
def bfs(ws):
    dist = {}
    deq = deque()
    for code, hand in ws.items():
        dist[code] = 0
        deq.append((code, hand))

    while len(deq) > 0:
        code, hand = deq.popleft()
        for k in range(9):
            if hand[k] < 4 and sum(hand) < 14:
                hand_add = deepcopy(hand)
                hand_add[k] += 1
                code_add = encode(hand_add)
                if code_add not in dist:
                    dist[code_add] = dist[code]
                    deq.appendleft((code_add, hand_add))
            if hand[k] > 0:
                hand_sub = deepcopy(hand)
                hand_sub[k] -= 1
                code_sub = encode(hand_sub)
                if code_sub not in dist:
                    dist[code_sub] = dist[code] + 1
                    deq.append((code_sub, hand_sub))

    return dist


def main():
    ws = complete_hands()
    print("len(ws):", len(ws))
    shanten = bfs(ws)
    assert(len(shanten) == 405350)

    # 計算結果を保存
    with open("shanten.txt", mode='w') as f:
        for code, shanten in shanten.items():
            hand = decode(code)
            f.write("{} {} {} {} {} {} {} {} {} {}\n".format(
                hand[0], hand[1], hand[2], hand[3], hand[4],
                hand[5], hand[6], hand[7], hand[8], shanten))


if __name__ == '__main__':
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time: {} [sec]".format(elapsed_time))
