use std::collections::{VecDeque, BTreeSet, BTreeMap};
use std::fs;
use std::io::Write;
use std::time::Instant;

fn complete_hands() -> BTreeSet<Vec<i32>> {
    let sets = vec![
        vec![1, 1, 1, 0, 0, 0, 0, 0, 0],
        vec![0, 1, 1, 1, 0, 0, 0, 0, 0],
        vec![0, 0, 1, 1, 1, 0, 0, 0, 0],
        vec![0, 0, 0, 1, 1, 1, 0, 0, 0],
        vec![0, 0, 0, 0, 1, 1, 1, 0, 0],
        vec![0, 0, 0, 0, 0, 1, 1, 1, 0],
        vec![0, 0, 0, 0, 0, 0, 1, 1, 1],
        vec![3, 0, 0, 0, 0, 0, 0, 0, 0],
        vec![0, 3, 0, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 3, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 3, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 3, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 3, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 0, 3, 0, 0],
        vec![0, 0, 0, 0, 0, 0, 0, 3, 0],
        vec![0, 0, 0, 0, 0, 0, 0, 0, 3],
    ];
    let heads = vec![
        vec![2, 0, 0, 0, 0, 0, 0, 0, 0],
        vec![0, 2, 0, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 2, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 2, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 2, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 2, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 0, 2, 0, 0],
        vec![0, 0, 0, 0, 0, 0, 0, 2, 0],
        vec![0, 0, 0, 0, 0, 0, 0, 0, 2],
    ];

    let mut ret: BTreeSet<Vec<i32>> = BTreeSet::new();
    
    for s1 in sets.iter() {
        for s2 in sets.iter() {
            for s3 in sets.iter() {
                for s4 in sets.iter() {
                    for head in heads.iter() {
                        let hand: Vec<i32> = (0..9).map(|i| {
                            s1[i] + s2[i] + s3[i] + s4[i] + head[i]
                        }).collect();
                        if hand.iter().all(|&h| h <= 4) {
                            ret.insert(hand);
                        }
                    }
                }
            }
        }
    }

    ret
}

fn bfs(ws: BTreeSet<Vec<i32>>) -> BTreeMap<Vec<i32>, i32> {
    let mut dist: BTreeMap<Vec<i32>, i32> = BTreeMap::new();
    let mut deq: VecDeque<Vec<i32>> = VecDeque::new();

    for hand in ws {
        dist.insert(hand.clone(), 0);
        deq.push_back(hand);
    }

    while !deq.is_empty() {
        let hand = deq.pop_front().unwrap();
        let sum: i32 = hand.iter().sum();
        for k in 0..9 {
            if hand[k] < 4 && sum < 14 {
                let mut hand_add = hand.clone();
                hand_add[k] += 1;
                if !dist.contains_key(&hand_add) {
                    dist.insert(hand_add.clone(), dist[&hand]);
                    deq.push_front(hand_add);
                }
            }
            if hand[k] > 0 {
                let mut hand_sub = hand.clone();
                hand_sub[k] -= 1;
                if !dist.contains_key(&hand_sub) {
                    dist.insert(hand_sub.clone(), dist[&hand] + 1);
                    deq.push_back(hand_sub);
                }
            }
        }
    }

    dist
}

macro_rules! time {
    ($x:expr) => {{
        let start = Instant::now();
        $x;
        let end = start.elapsed();
        end.as_nanos() as f64 / 1_000_000_000 as f64
    }};
}

fn main() {
    let elapsed_time = time!({
        let ws = complete_hands();
        let shanten = bfs(ws);
        assert_eq!(shanten.len(), 405350);

        // 計算結果を保存
        let mut f = fs::File::create("shanten-rs.txt").unwrap();
        for (hand, sh) in shanten {
            f.write_all(format!("{} {} {} {} {} {} {} {} {} {}\n",
                hand[0], hand[1], hand[2], hand[3], hand[4],
                hand[5], hand[6], hand[7], hand[8], sh).as_bytes()).unwrap();
        }
    });
    println!("elapsed_time: {} [sec]", elapsed_time);
}