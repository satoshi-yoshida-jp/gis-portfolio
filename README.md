# 東京武蔵野市における公共交通アクセスと都市構造の空間分析

## Overview

## Research Question

人口が多いにもかかわらず、鉄道駅へのアクセス性が低い地域はどこか？

## Data

- 人口データ
- 鉄道駅データ
- 土地利用データ
- 人流データ

## Methods

- Buffer analysis
- Spatial join
- Overlay analysis
- Exploratory statistical analysis

## Results

武蔵野市と交差する69の500m人口メッシュについて、メッシュ中心点から最寄り鉄道駅までの直線距離を算出した。全69メッシュのうち、37メッシュ（53.6%）が最寄り鉄道駅から800m圏外に分類された。圏外メッシュの平均人口と中央値は圏内より低かったが、最大人口は圏内を上回った。P75以上の高人口かつ800m圏外となる候補は6件あり、このうち市境界メッシュを除く主要候補4件はすべて市北部中央に連続して分布し、最寄駅はいずれも三鷹駅だった。この結果から、市北部中央には鉄道駅への空間的近接性が相対的に低い高人口地域が集中している可能性が示された。

## Tools

- QGIS
- Python
- GeoPandas
- pandas
- statsmodels

## Limitations

## Repository Structure
