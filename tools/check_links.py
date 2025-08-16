# -*- coding: utf-8 -*-
# affiliates.json を“安全に”生成・補完する最小版
# - 既存ファイルを尊重してマージ
# - seeds と bundles から catalog を必ず埋める
# - rules.yml の price_caps で簡易健全性チェック
# 後で実在リンク検査/公式APIに差し替えOK

import json, sys, os, time
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None  # rules.yml 読み取りが無くても動く

def load_json(p):
    try:
        return json.load(open(p, "r", encoding="utf-8"))
    except Exception:
        return None

def dump_json(obj, p):
    Path(os.path.dirname(p)).mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)

def load_rules(rules_path):
    if not rules_path or not os.path.exists(rules_path) or yaml is None:
        return {}
    try:
        return yaml.safe_load(open(rules_path, "r", encoding="utf-8")) or {}
    except Exception:
        return {}

def load_seeds():
    # 任意: tools/seeds/affiliates_seeds.json があれば使う
    p = "tools/seeds/affiliates_seeds.json"
    seeds = load_json(p)
    if seeds:
        return seeds

    # 無ければ最小ダミー（タイトル/URLはプレースホルダ）
    return {
      "tripod-A": {"title": "軽量三脚A", "price": 4980,  "url": "https://example.com/tripod-a"},
      "remote-A": {"title": "スマホレリーズA", "price": 1580, "url": "https://example.com/remote-a"},
      "warm-A":   {"title": "防寒グローブA",   "price": 980,  "url": "https://example.com/warm-a"},
      "tripod-B": {"title": "安定三脚B",   "price": 12800, "url": "https://example.com/tripod-b"},
      "remote-B": {"title": "スマホレリーズB", "price": 2280,  "url": "https://example.com/remote-b"},
      "warm-B":   {"title": "防寒ネックB",   "price": 1680,  "url": "https://example.com/warm-b"}
    }

def main():
    # 引数処理
    argv = sys.argv
    def argval(flag, default=None):
        return argv[argv.index(flag)+1] if flag in argv and (argv.index(flag)+1) < len(argv) else default

    out_path   = argval("--out",   "public/data/affiliates.json")
    rules_path = argval("--config", "rules.yml")

    # 既存 affiliates.json を読み込み（あれば）
    base = {"bundles": [], "catalog": {}}
    existing = load_json(out_path)
    if existing:
        base.update({k: existing.get(k, base[k]) for k in base.keys()})

    # バンドルが空なら初回デフォルトを投入
    if not base.get("bundles"):
        base["bundles"] = [
            {"id":"kit_low","title":"入門セット(低価格)","items":["tripod-A","remote-A","warm-A"],"ok":True},
            {"id":"kit_mid","title":"安定セット(中価格)","items":["tripod-B","remote-B","warm-B"],"ok":True}
        ]

    # ルール（価格上限など）
    rules  = load_rules(rules_path)
    caps   = (rules.get("affiliates") or {}).get("price_caps") or {}
    maxcap = max([v for v in caps.values() if isinstance(v,(int,float))], default=None)

    # シードから商品マスタ
    seeds = load_seeds()

    # catalog を必ず埋める
    catalog = base.get("catalog") or {}
    needed_ids = set()
    for b in base["bundles"]:
        for item_id in b.get("items", []):
            needed_ids.add(item_id)

    for item_id in sorted(needed_ids):
        if item_id in catalog:
            # 既存を整形: okフィールド付与・最低限のキーを保証
            entry = catalog[item_id]
            entry.setdefault("id", item_id)
            entry.setdefault("title", seeds.get(item_id, {}).get("title", item_id))
            entry.setdefault("price", seeds.get(item_id, {}).get("price", 0))
            entry.setdefault("url", seeds.get(item_id, {}).get("url", "https://example.com/placeholder"))
            entry.setdefault("ok", True)
        else:
            seed = seeds.get(item_id, {})
            catalog[item_id] = {
                "id": item_id,
                "title": seed.get("title", item_id),
                "price": seed.get("price", 0),
                "url": seed.get("url", "https://example.com/placeholder"),
                "ok": True
            }

        # 簡易価格ガード：上限を超える場合は ok:false
        price = catalog[item_id].get("price", 0)
        if isinstance(price, (int, float)) and maxcap is not None and price > maxcap:
            catalog[item_id]["ok"] = False

    # 仕上げ
    base["catalog"]   = catalog
    base["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    dump_json(base, out_path)
    print(f"Wrote affiliates to {out_path} (items={len(catalog)})")

if __name__ == "__main__":
    main()
