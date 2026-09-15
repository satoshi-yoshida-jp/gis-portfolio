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
