import os, re

body = os.environ.get("ISSUE_BODY", "")

def pick(label, default):
    m = re.search(rf"{label}\s*:\s*([^\n]+)", body)
    return (m.group(1).strip() if m else default)

mode       = pick("モード", "normal")
gold_ovs   = pick("Gold OVS 最小値", "85")
plat_ovs   = pick("Platinum OVS 最小値", "90")
categories = [s.strip() for s in pick("アフィカテゴリ", "tripod,wide_lens,remote,warm_gear").split(",") if s.strip()]

lines = []
lines.append(f"mode: {mode}")
lines.append("thresholds:")
lines.append(f"  gold: {{ovs_min: {gold_ovs}, safety_min: 3}}")
lines.append(f"  platinum: {{ovs_min: {plat_ovs}, safety_min: 4, new_moon_window_days: 3}}")
lines.append("weights: {cloud_cover: -0.45, moon_alt_deg: -0.25, wind_mps: -0.10, humidity: -0.05, light_pollution: -0.10}")
lines.append("affiliates:")
lines.append("  price_caps: {low: 6000, mid: 15000, high: 35000}")
lines.append("  categories:")
for c in categories:
    lines.append(f"    - {c}")

open("rules.yml","w",encoding="utf-8").write("\n".join(lines)+"\n")
print("rules.yml written")
