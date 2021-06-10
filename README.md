# Flush Shanten

A python implementation of calculating "shanten number" in Japanese mahjong, only for flush hand

## How To Use

```
git clone --recursive https://github.com/habara-k/flush-shanten.git
cd flush-shanten
mkdir build
cd build
cmake ..
make
python3 ../shanten.py
rustc -C opt-level=3 -C debug_assertions=no ../shanten.rs
./shanten
./verify
```

## Benchmark
Using 3.2GHz CPU and 8GB RAM,
- `shanten.py`: 42±1 sec
- `shanten.rs`: 2.15±0.08 sec

## Description
[清一色のシャンテン数を01BFSで計算する](https://habara-k.hatenadiary.jp/entry/2021/06/09/181140)

## Licence

[MIT](https://github.com/habara-k/flush-shanten/blob/main/LICENSE)

## Author

[habara-k](https://github.com/habara-k)
