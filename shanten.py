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
    ret = 0
    for e in hand:
        ret = (ret * 5) + e
    return ret


# int -> hand
def decode(hash):
    ret = np.zeros(9, dtype=int)
    for i in range(9):
        ret[8-i] = hash % 5
        hash //= 5
    return ret


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
def bfs(W):
    dist = {}
    deq = deque()
    for hash, hand in W.items():
        dist[hash] = 0
        deq.append((hash, hand))

    while len(deq) > 0:
        hash, hand = deq.popleft()
        for k in range(9):
            if hand[k] < 4 and sum(hand) < 14:
                hand_add = deepcopy(hand)
                hand_add[k] += 1
                hash_add = encode(hand_add)
                if hash_add not in dist:
                    dist[hash_add] = dist[hash]
                    deq.appendleft((hash_add, hand_add))
            if hand[k] > 0:
                hand_sub = deepcopy(hand)
                hand_sub[k] -= 1
                hash_sub = encode(hand_sub)
                if hash_sub not in dist:
                    dist[hash_sub] = dist[hash] + 1
                    deq.append((hash_sub, hand_sub))

    return dist


def main():
    W = complete_hands()
    shanten = bfs(W)
    assert(len(shanten) == 405350)

    # 計算結果を保存
    with open("shanten.txt", mode='w') as f:
        for hash, shanten in shanten.items():
            hand = decode(hash)
            f.write("{} {} {} {} {} {} {} {} {} {}\n".format(
                hand[0], hand[1], hand[2], hand[3], hand[4],
                hand[5], hand[6], hand[7], hand[8], shanten))


if __name__ == '__main__':
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time: {} [sec]".format(elapsed_time))
