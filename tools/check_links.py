# 最小ダミー：在庫チェックはまだしないで、常に安全なJSONを出力
# 後で公式API(例: Amazon PA-API / 楽天)に置き換え可能
import json, sys, os

def main():
    # 引数
    try:
        out_path = sys.argv[sys.argv.index('--out') + 1]
    except:
        out_path = 'public/data/affiliates.json'

    # 既存ファイルがあれば尊重しつつ最低限の構造を保証
    base = {"bundles": [], "catalog": {}}
    if os.path.exists(out_path):
        try:
            base = json.load(open(out_path, 'r', encoding='utf-8'))
        except:
            pass

    # バンドルが空ならデフォルトを投入（初回表示用）
    if not base.get("bundles"):
        base["bundles"] = [
            {"id":"kit_low","title":"入門セット(低価格)","items":["tripod-A","remote-A","warm-A"],"ok":True},
            {"id":"kit_mid","title":"安定セット(中価格)","items":["tripod-B","remote-B","warm-B"],"ok":True}
        ]

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(base))
    print(f"Wrote affiliates to {out_path}")

if __name__ == "__main__":
    main()
