# ルールとダミー入力から OVS/Safety を計算して site_state.json を生成
# 依存なし（標準ライブラリのみ）
import sys, json, time, math, os

# rules.yml が無くても動く簡易デフォルト
DEFAULT_RULES = {
  "mode": "normal",
  "thresholds": {"platinum": {"ovs_min": 90, "safety_min": 4}},
  "weights": {
    "cloud_cover": -0.45,
    "moon_alt_deg": -0.25,
    "wind_mps": -0.10,
    "humidity": -0.05,
    "light_pollution": -0.10
  }
}

def load_rules(path):
  # 超簡易YAML→dict（今回のキーだけ想定）。YAMLパーサ非使用でスマホ/Actionsでも動くように。
  # 正式には rules_sync.yml で生成された YAML を使う想定だが、無くてもDEFAULTで動かす。
  if not os.path.exists(path):
    return DEFAULT_RULES
  try:
    # ざっくりパース（:以降をJSON風に整形する簡易手法）
    # 失敗しても DEFAULT_RULES にフォールバック
    text = open(path, 'r', encoding='utf-8').read()
    if not text.strip():
      return DEFAULT_RULES
    # すべてのキーを網羅するのは大変なので、必要部分だけ拾う
    rules = DEFAULT_RULES.copy()
    if "mode:" in text:
      mode_line = [l for l in text.splitlines() if l.strip().startswith("mode:")][0]
      rules["mode"] = mode_line.split(":")[1].strip()
    return rules
  except:
    return DEFAULT_RULES

def f01(x): 
  try:
    return max(0.0, min(1.0, float(x)))
  except:
    return 0.0

def score(inp, w):
  # 0〜100にクリップしたスコア
  return max(0, min(100,
      100
    + w['cloud_cover']     * (-f01(inp.get('cloud_cover_grid', 0)/100))
    + w['moon_alt_deg']    * (-f01(inp.get('moon',{}).get('alt_deg', 0)/90))
    + w['wind_mps']        * (-f01(inp.get('wind_mps', 0)/20))
    + w['humidity']        * (-f01(inp.get('humidity', 0)/100))
    + w['light_pollution'] * (-f01(inp.get('light_pollution', 0)))
  ))

def wind_chill(t_c, v_ms):   # 体感温度（近似）
  v = max(v_ms*3.6, 1.0)
  return 13.12 + 0.6215*t_c - 11.37*(v**0.16) + 0.3965*t_c*(v**0.16)

def heat_index(t_c, rh):     # 暑さ指数（簡易近似）
  tf = t_c*9/5 + 32.0
  hi_f = -42.379 + 2.04901523*tf + 10.14333127*rh - .22475541*tf*rh
  return (hi_f - 32.0)*5/9

def dewpoint(t_c, rh):
  a,b = 17.27, 237.7
  rh = max(1.0, min(100.0, float(rh)))
  alpha = (a*t_c)/(b+t_c) + math.log(rh/100.0)
  return (b*alpha)/(a-alpha)

def safety(inp):
  if inp.get("warnings"):
    return 1
  s = 4
  try:
    t = float(inp.get("temp_c", 10))
    v = float(inp.get("wind_mps", 1))
    rh = float(inp.get("humidity", 40))
    if wind_chill(t, v) < -10: s -= 1
    if heat_index(t, rh) > 31: s -= 1
    if (t - dewpoint(t, rh)) < 2: s -= 1  # 結露注意
  except:
    pass
  return max(1, min(4, s))

def main():
  # 引数処理
  try:
    in_path  = sys.argv[sys.argv.index('--in')  + 1]
  except:
    in_path = 'data/inputs.json'
  try:
    out_path = sys.argv[sys.argv.index('--out') + 1]
  except:
    out_path = 'public/data/site_state.json'
  try:
    rules_path = sys.argv[sys.argv.index('--rules') + 1]
  except:
    rules_path = 'rules.yml'

  rules = load_rules(rules_path)
  inp = json.load(open(in_path, 'r', encoding='utf-8'))

  w = rules.get('weights', DEFAULT_RULES['weights'])
  ovs = round(score(inp, w))
  sft = safety(inp)

  out = {
    "lastmod": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    "mode": rules.get('mode', 'normal'),
    "confidence": 0.92,
    "tonight": {
      "ovs": ovs,
      "safety": sft,
      "moon_pct": inp.get('moon',{}).get('phase_pct', 0.0),
      "iss": inp.get('iss', {})
    },
    "badges": {
      "family_not_recommended": sft < 3,
      "uncertain": False
    },
    "thresholds": rules.get('thresholds', DEFAULT_RULES['thresholds'])
  }

  os.makedirs(os.path.dirname(out_path), exist_ok=True)
  with open(out_path, 'w', encoding='utf-8') as f:
    f.write(json.dumps(out))
  print(f"Wrote site_state to {out_path}")

if __name__ == "__main__":
  main()
