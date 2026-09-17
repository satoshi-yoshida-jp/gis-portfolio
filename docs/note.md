# QGIS基礎

## データ構造

### vector

- point（駅、バス停、事故地点）
- line（鉄道路線、道路、河川）
- polygon（行政区域、土地利用区域、建物、公園）

### raster

以下のような格子
┌──┬──┬──┬──┐
│12│15│24│31│
├──┼──┼──┼──┤
│10│17│29│40│
├──┼──┼──┼──┤
│ 5│12│22│35│
└──┴──┴──┴──┘

各セルが値を持っている
標高データならpixel => 標高

## CSR : Coordinate Reference System

座標参照系

「座標の数字が実際に地球上のどの位置を表すのか」を定義するルール

座標値（ex 139.6917, 38.3255）
＋　基準となる地球モデル
＋　座標の表現方法
＋　必要なら地図投影法

これらが定義されて初めて地球上の位置として解釈できる

### 地球　→　地図への変換

球体の地球を平面の地図にCSRを用いて変換が必要

※ 球面を完全に歪みなく平面にすることはできない

### CRSの種類

1. Geographic CRS : 地理座標系
   代表例　EPSG:4326 / WGS 84
   位置を緯度と経度で表す
   Longtitude: 139.xxx
   Latitude: 35.xxx
   → 距離を測るのは向かない

2. Projected CRS : 投影座標系
   地球上の位置を平面に投影
   X = xxx m
   Y = xxx m
   というm単位の座標で表す
   → 距離や面積の計算ができる

### EPSGとは？

CRSを識別する番号

- EPSG:4326　→　WGS84という地理座標系

- EPSG:6677 → JGD2011/Japan Plane Rectangular CS IX
  日本の平面直角座標系IX系
  東京周辺で距離・面積を扱う場合に使える投影座標系

### Reproject（再投影・座標変換）

地理座標系と投影座標系をそれぞれCRS情報だけ書き換えてはいけない
EPSG:4326で作成されたデータをEPSG:6677に変換はNG（データは変換されない）

中身のデータ変換まで完全に変換する場合は**Reproject**が必要

### プロジェクトCRSもある

異なる複数のCRSのデータが混在する場合がある
QGISではこれらをOn-the-flyで変換し、同じ地図上で重ねて表示できる
各レイヤーのCRS情報を確認する癖をつける

## GeoPackageでレイヤーの作成

Shapefileも有名。gpkgファイルなら１ファイルの中に複数のレイヤーを持てる

setagaya.gpkg

- stations
- railways
- population
- landuse

# Buffer, Clip, Spatial join

## Summary

- Created 400 m and 800 m buffers
- Practiced Clip operations
- Learned Spatial Join using location relationships
- Practiced Select by Location
- Reviewed CRS requirements for distance-based analysis

## Buffer処理

すでに作ってあるpointレイヤーを元に一定距離のPolygonレイヤーを新たに作成する

pointの半径〜mの円（polygon geometry）が表示される

この場合は距離を扱うためCRSは東京の場合EPSG:6677を使用。大事なのはEPSG:4326の地理座標系(Geographic CRS)は座標（degree）なので距離計算には適さない。

800m bufferとは中心からの直線距離800m圏内を表す

## Clip -> Spatial join -> Select by Location

### Clip

あるpolygonの範囲内だけを切り出す処理
（Geometryそのものを切る）

QGISではvector overlay -> clip

## Spatial Join

位置関係をキーにjoinする
（通常のデータ分析はidのような共通キーを使う）

### join attributes by location

predicate

- within : pointがpolygonの中にある
  　point within polygon

- contains : polygonがpointを内包している
  polygon contains point

- intersects : Geometry同士が少しでも接触している、重なってる

### select by location

位置条件に合うFeatureを選択（ハイライト）する処理

## 確認

1. Buffer
   point, line, polygonなどの入力geometryから、指定距離の領域をpolygonとして生成する処理
2. Clip
   Input layerは切られる側、overlay layerは切り抜き範囲を定義するpolygon
3. Spatial join
   通常は共通のidなどを使用してjoinするが、spatial joinはwithinやintersectsなど空間的位置関係を結合条件に使う
4. within / contains
   withinは含まれる側から見た関係、containsは含んでいる側から見た関係を表す
   point within polygon
   polygon contains point
5. intersects
   2つのGeometryが１点でも共通部分を持つ場合にTrueとなる判定条件。
6. Select by location / Clip
   Select by Locationは既存Featureを選択状態（ハイライト）にする。ClipはGeometryを実際に切って新しいレイヤーを作る

# 実データ取得とプロジェクト設計

## 目標

武蔵野市の行政区域・鉄道・人口メッシュをQGISに読み込み、分析用CRSへ整理し、 「何をどのデータで分析するか」を確定する。

## 対象地域：東京都武蔵野市

よく知っているエリアのため。市域が比較的小さいため、鉄道・駅データの抽出には市境から1.5km外側までを分析対象範囲とする。

## 行政区域データ：武蔵野市を作る

公式ページ： 国土数値情報 行政区域データ　を使用

shpデータをqgisで読み込み
gpkgとして保存
→この時EPSG:6677へ再投影（元のCRS情報は書き換えない）

属性テーブルの式で選択で武蔵野市を選択（地図上で武蔵野市がハイライトされる）し、新レイヤーとして保存

### 分析範囲を広げる場合

武蔵野市レイヤーを元に1500m bufferを作成する

## 鉄道データ取得

公式ページ： 国土数値情報 鉄道データ

### 駅は最初からPointとは限らない

現在のN02では駅も鉄道路線の一部分として線形状で整備されている。
この後必要に応じて代表Pointへ変換する。

### 鉄道データ（駅と路線）を読み込み

extract by locationで分析範囲の1500m buffer内の駅と路線を抽出
EOSG:6677へ再投影して保存

## 500m人口メッシュ取得

e-Statの2020年国勢調査「人口及び世帯」の4次メッシュ（500mメッシュ）を使用

公式ページ： e-Stat 統計地理情報システム

政府統計 国勢調査
調査年 2020年
集計単位 4次メッシュ（500m）
統計表 人口及び世帯
地域 東京都

以下の二つのデータを使用

- 統計データ（CSV） — 人口・世帯数 (CSV)
- 境界データ — 500mメッシュPolygon (世界測地系平面直角座標系 M5339 shapefile)

## 確認

- なぜ武蔵野市境界だけでなく、1.5km外側まで分析範囲を広げるのか?
  武蔵野市は市域が比較的小さく、市境付近の住民が市外の駅を利用する可能性があるため。行政境界だけで鉄道駅を抽出すると、実際には利用可能な周辺駅を除外してしまうため、1.5kmのバッファを設けて分析対象範囲を広げた。
- raw/とprocessed/を分ける理由は何か?
  raw/には取得した元データを変更せず保存し、processed/にはClip、再投影、Joinなどの加工後データを保存する。元データを保持することで、処理をやり直したり分析過程を再現しやすくなる。
- 行政区域データをEPSG:6677へ再投影する理由は何か?
  元データが別のCRSであるため、東京周辺で距離・面積をメートル単位で扱いやすいEPSG:6677に再投影する。今後のBufferや距離計算を一貫した座標系で行うためでもある。
- 人口CSV単体では地図上にPolygonとして表示できないのはなぜか?
  人口CSVには人口や世帯数などの属性値とメッシュコードはあるが、Polygon Geometryそのものを持っていないため。地図上で面として表示するには、同じメッシュコードを持つ500mメッシュ境界データとJoinする必要がある。
- 人口統計CSVと500mメッシュ境界を結合するには、何が必要か?
  両方のデータに共通するメッシュコードが必要で、境界データ側ではKEY_CODEをJoin Keyとして利用する。
- データ年度が異なる場合、分析上どのような注意が必要か?
  人口、鉄道、土地利用などのデータ年度が異なると、駅の新設・廃止、人口変化、土地利用変化などが反映される時点が異なるため、同一時点の都市構造を厳密に比較しているとは言えない。したがって結果の解釈時に年度差をLimitationsとして明示する必要がある。

# 500m人口メッシュの結合と人口分布可視化

## 使用するデータ

- e-Stat 人口CSV 人口・世帯などの統計属性 メッシュコード、人口列
- 500mメッシュ境界 Polygon Geometry KEY_CODE
- musashino_boundary 武蔵野市行政境界 Geometry
- musashino_study_area_1500m 周辺分析範囲 Geometry

## key_codeでCSVと境界データのjoin

key_codeを各メッシュの一意な識別子としてjoinする
key_codeは識別子なので文字列として扱う方が安全
→ csvのkey_codeは数値だったためto_stringで文字列に変換

## 武蔵野市ポリゴンへClip

## 人口総数列を数値型に変換して新しい列を作成

## コロプレスマップを作る

分類法を検討

- Natural Breaks (Jenks)：データ分布の切れ目を利用。人口分布の自然な差を見る
- Quantile：各階級のFeature数をほぼ同数にする。相対的な地域比較
- Equal Interval：値域を等間隔に分ける。直感的だが偏った分布では弱い

→ 今回をNatural Breaksを5階級程で表示

## 武蔵野市メッシュ内の記述統計量について確認

Count 69
Sum 251085　
※ 市境を跨ぐメッシュに関しては人口値を面積按分していないため、メッシュ全体の単純合計値であり、武蔵野市の正式な総人口としては扱わない
Mean 3638.91
Median 3627
St dev (pop) 1235.35
St dev (sample) 1244.4
Minimum 1130
Maximum 6853
Range 5723
Minority 1130
Majority 3627
Variety 68
Q1 2755
Q3 4420
IQR 1665
Missing (null) values 0

## Map 1を作成

Project
→ New Print Layout
含めるもの：

タイトル
地図本体
凡例
スケールバー
North Arrow
データ出典
対象年：2020年国勢調査

## 確認

- なぜ人口CSVだけではコロプレスマップを作れないのか。
  人口CSVは人口値の統計表データであり、polygonなどgeometryを持たないため、そのままでは地図上の面として描画できない。境界メッシュデータと結合してコロプレスマップを作成する。
- JoinでKEY_CODEを使う理由は何か。
  人口CSVと境界メッシュデータの両データで同一の500mメッシュを一意に識別する共通キーのため
- Join Keyの型が異なると何が起こり得るか。
  joinする際に型が異なると認識されず正常にjoinできない可能性があるため
- Join結果をGeoPackageへExportする理由は何か。
  Join設定はプロジェクト上の一時的な関連付けのため、人口属性付きPolygonとして後続処理に安定して使用できるようGeoPackageへ保存する。
- ClipとJoinは、それぞれ何を変える処理か。
  ClipはポリゴンなどGeometryの対象範囲を切り取る処理。
  joinは別のデータの属性を対象Featureに追加する処理
- Natural BreaksとQuantileの違いは何か。
  Natural Brreaksはクラス内のデータのばらつきを小さくし、クラス間の差が大きくなるように境界を決める。そのため自然なデータの偏りを可視化できる。
  Quantileは各等級のデータ数が均等になるように割り振るため、上位〜％など均等な割合の統計値などを把握しやすい。
- 平均人口と中央値人口の両方を見る理由は何か。
  極端な大きさのデータがある場合平均値が外れ値側に移動するため正しい説明ができない。
  中央値はデータの幅によらず中央に位置する値を見るため極端な値の影響を受けづらい。
- 人口分布と駅位置が近く見えても、なぜ因果関係とは断定できないのか。
  人口分布には駅までの距離のほか、様々な居住環境（家、学校、病院、公共施設、交通手段など）の影響を受けるため、直接的に駅が近いから人口が多いとは断定できない。人口分布と駅位置に相関関係がある可能性は考えられる。また人口集積が鉄道整備を促したという逆因果の可能性も考えられる。
