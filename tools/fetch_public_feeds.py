# 最小ダミー版：まずは動作確認用。後で実データ取得に差し替えます。
import json, sys

out = {
  "cloud_cover_grid": 20,      # 雲量（%相当のダミー）
  "warnings": None,            # 気象警報なし
  "temp_c": 10,
  "wind_mps": 2,
  "humidity": 40,
  "moon": {"phase_pct": 2.1, "alt_deg": 10},
  "iss": {"visible": True, "dur_sec": 210},
  "light_pollution": 0.3
}

# 使い方: python tools/fetch_public_feeds.py --out data/inputs.json
out_path = None
if '--out' in sys.argv:
  out_path = sys.argv[sys.argv.index('--out') + 1]
else:
  out_path = 'data/inputs.json'

# data/ フォルダはActions上で自動生成される想定（無ければ同階層に吐きます）
with open(out_path, 'w') as f:
  f.write(json.dumps(out))
print(f"Wrote dummy inputs to {out_path}")
