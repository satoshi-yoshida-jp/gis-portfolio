import json
import math
from pathlib import Path

import pandas as pd

# ファイル保存
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/processed/mesh_analysis_500m.csv"
OUTPUT = ROOT / "outputs/day09"
P75_USED = 4420  # QGISで設定した高人口閾値

df = pd.read_csv(INPUT, dtype=str, encoding="utf-8-sig", keep_default_na=False)
df.columns = df.columns.str.strip()
required = ["mesh_id", "population", "station_dist_m", "boundary_status"]
missing = sorted(set(required) - set(df.columns))

if missing:
    raise ValueError(f"列が不足：{missing} / 実際の列：{df.columns.tolist()}")

df = df[required].copy()
for col in required:
    df[col] = df[col].str.strip()


boundary_map = {
    "inside": "inside",
    "boundary": "boundary",
    "完全市内": "inside",
    "市境": "boundary",
}

unknown = sorted(set(df["boundary_status"]) - set(boundary_map))
if unknown:
    raise ValueError(f"boundary_statusの値を確認しboundary_mapを修正: {unknown}")

if len(df) != 69:
    raise ValueError(f"入力は対象全69メッシュのはずですが、{len(df)}行です。")
if not df["mesh_id"].str.fullmatch(r"\d{9}").all():
    raise ValueError("500mメッシュコードは9桁の文字列で確認してください。")
if df["mesh_id"].duplicated().any():
    raise ValueError("メッシュコードが重複。結合やクリップ後の分割を確認してください。")

for col in ["population", "station_dist_m"]:
    df[col] = pd.to_numeric(df[col], errors="raise")
    if not df[col].map(math.isfinite).all() or (df[col] < 0).any():
        raise ValueError(f"{col}に欠損・無限大・負数があります。")

if (df["population"] % 1 != 0).any():
    raise ValueError("人口に小数があります。元の総人口列を確認してください。")

q3_linear = float(df["population"].quantile(0.75, interpolation="linear"))
if not math.isclose(q3_linear, P75_USED, abs_tol=1e-9, rel_tol=0):
    print(f"注意: pandasのlinear方式のP75={q3_linear:g}、採用値={P75_USED}。")
    print("対象行・欠損・四分位点の計算方法を確認。採用値は自動変更しません。")


df["access_class"] = "inside_800m"
df.loc[df["station_dist_m"] > 800, "access_class"] = "outside_800m"
is_high = df["population"] >= P75_USED
is_outside = df["station_dist_m"] > 800
is_fully_in_city = df["boundary_status"] == "inside"

candidates = df.loc[is_high & is_outside].copy()
candidates["candidate_class"] = candidates["boundary_status"].map(
    {"inside": "main", "boundary": "reference"}
)
candidates = candidates.sort_values("population", ascending=False)
stats = df.groupby("access_class")["population"].agg(
    count="count", mean="mean", median="median", maximum="max"
)

rows = []
for distance in [800, 1000, 1200]:
    selected = is_high & (df["station_dist_m"] > distance)
    rows.append(
        {
            "threshold_m": distance,
            "main_count": int((selected & is_fully_in_city).sum()),
            "reference_count": int((selected & ~is_fully_in_city).sum()),
        }
    )
sensitivity = pd.DataFrame(rows)

OUTPUT.mkdir(parents=True, exist_ok=True)
candidates.to_csv(OUTPUT / "candidates.csv", index=False, encoding="utf-8-sig")
stats.to_csv(OUTPUT / "access_stats.csv", encoding="utf-8-sig")
sensitivity.to_csv(OUTPUT / "threshold_check.csv", index=False, encoding="utf-8-sig")
report = {
    "input": str(INPUT.relative_to(ROOT)),
    "rows": len(df),
    "unique_mesh_ids": int(df["mesh_id"].nunique()),
    "p75_used": P75_USED,
    "p75_linear_check": q3_linear,
    "pandas_version": pd.__version__,
    "main_count": int((candidates["candidate_class"] == "main").sum()),
    "reference_count": int((candidates["candidate_class"] == "reference").sum()),
}
(OUTPUT / "run_info.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("\n候補一覧\n", candidates.to_string(index=False))
print("\nアクセス圏統計\n", stats.round(2).to_string())
print("\n距離閾値の比較\n", sensitivity.to_string(index=False))
print(f"\n保存先: {OUTPUT}")
