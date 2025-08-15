# site_state.json の健全性をざっくり点検し、ダメなら前回成功分に戻す
import json, sys, os, shutil

def ok(state):
    try:
        t = state["tonight"]
        return (0 <= int(t["ovs"]) <= 100) and (1 <= int(t["safety"]) <= 4)
    except Exception:
        return False

def main():
    try:
        state_path = sys.argv[sys.argv.index('--state') + 1]
    except:
        state_path = 'public/data/site_state.json'
    try:
        prev_path  = sys.argv[sys.argv.index('--prev') + 1]
    except:
        prev_path = 'public/data/site_state_prev.json'

    try:
        state = json.load(open(state_path, 'r', encoding='utf-8'))
    except Exception:
        state = None

    if not state or not ok(state):
        if os.path.exists(prev_path):
            shutil.copyfile(prev_path, state_path)
            print('Health guard: rollback to previous success.')
        else:
            print('Health guard: no previous file; keeping current (may be bad).')
    else:
        print('Health guard: state looks OK.')

if __name__ == "__main__":
    main()
