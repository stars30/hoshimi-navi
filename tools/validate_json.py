# 超簡易バリデータ：requiredキーの存在だけ確認
import json, sys

def main():
    try:
        schema_path = sys.argv[sys.argv.index('--schema') + 1]
        data_path   = sys.argv[sys.argv.index('--data') + 1]
    except Exception:
        print("Usage: python tools/validate_json.py --schema schemas/site_state.schema.json --data public/data/site_state.json")
        raise SystemExit(2)

    schema = json.load(open(schema_path, 'r', encoding='utf-8'))
    data   = json.load(open(data_path,   'r', encoding='utf-8'))

    for k in schema.get("required", []):
        if k not in data:
            raise SystemExit(f"[validate_json] missing required key: {k}")

    print("[validate_json] ok")

if __name__ == "__main__":
    main()
