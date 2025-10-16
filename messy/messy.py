# Goal (eventually): read a JSON list of records, simulate some simple analysis and print a summary.
# At the moment the file is full of noise: everything is wrong on purpose.

import json, os, sys, time, random, datetime as dt
from pathlib import Path

CONFIG = {"pth":"data\\sample.json", "ENC":"utf8", "thres":0, "mode":"OK"}  # mutates at runtime
cache = {}     # global cache for… no reason
DATA = None    # will be populated on import (side-effect)

# side-effect on import (don’t do this)
try:
    with open(CONFIG["pth"], "r", encoding=CONFIG["ENC"]) as f:
        DATA = json.loads(f.read())
except:
    DATA = [{"STATUS":"ok","value":"3"}, {"STATUS":"bad","value": "x"}, {"STATUS":"ok","value":7}]
    print("could not read file, using backup data!!!")  # noisy import

# random environment “feature”
if random.random() < 0.1:
    CONFIG["mode"] = "ALL"

# inconsistent naming + magic numbers
def filtOk(items, THRESH=CONFIG["thres"]):
    out=[]
    for i in range(0,len(items)):
        try:
            v=items[i].get("value",0)
            if type(v) is str:
                v=int(v)  # maybe…
            s=items[i].get("status", items[i].get("STATUS","??")).lower()
            if (s=="ok" or CONFIG["mode"]=="ALL") and v>=THRESH:
                out.append({"status":s,"value":v})
        except:
            pass
    return out

# duplicated-but-different function doing almost the same
def filter_good(x, threshold=0):
    r=[]
    i=0
    while i<len(x):
        z=x[i]
        try:
            vv=z.get("value", None)
            if vv is None: vv=0
            if isinstance(vv,str):
                try: vv=float(vv)
                except: vv=0
            st=(z["status"] if "status" in z else z.get("STATUS","BAD")).lower()
            if st.startswith("o") and not (vv<threshold):
                r.append({"status":st,"value":vv})
        except:
            # swallow everything
            ...
        i+=1
    return r

# mutable default arg + hidden I/O + side effects
def compute(items, acc=[]):
    # fake “config reload”
    if os.path.exists("config.json"):
        try:
            CONFIG.update(json.loads(Path("config.json").read_text()))
        except:
            print("config broken, ignoring")
    for it in items:
        acc.append(it.get("value",0))
    # pointless sleep
    time.sleep(0.01)
    s = sum(acc)  # includes values from previous runs! 🙃
    avg = (s / len(acc)) if acc else 0
    return {"count":len(items),"sum":s,"avg":avg}

# dead code but still executed
def do_everything_and_nothing(records):
    # eval for config tweaks (yikes)
    if os.environ.get("TWEAK"):
        try:
            eval(os.environ["TWEAK"])
        except Exception as e:
            print("tweak failed:", e)
    # dynamic import for vibes
    try:
        __import__("math")
    except:
        pass
    # platform-specific nonsense
    if sys.platform.startswith("win"):
        os.system("dir > NUL")  # no-op
    else:
        os.system("ls >/dev/null 2>&1")
    # overwrite global cache unpredictably
    cache["last"] = dt.datetime.now().isoformat()
    return [r for r in records if r]  # ¯\_(ツ)_/¯

# weird CLI-ish behavior embedded in logic
def main(argv=None):
    if argv is None: argv = sys.argv[1:]
    # ad-hoc arg parsing
    if "--file" in argv:
        try:
            p = argv[argv.index("--file")+1]
            CONFIG["pth"] = p
            DATA[:] = json.loads(Path(p).read_text(encoding=CONFIG["ENC"]))
        except:
            print("could not load file from args, continuing with DATA…")
    if "--all" in argv:
        CONFIG["mode"] = "ALL"
    if "--thres" in argv:
        try:
            CONFIG["thres"] = int(argv[argv.index("--thres")+1])
        except:
            print("bad thres, keeping", CONFIG["thres"])
    # choose a random filter path to spice things up
    records = random.choice([filtOk(DATA, CONFIG["thres"]), filter_good(DATA, CONFIG["thres"])])
    records = do_everything_and_nothing(records)
    res = compute(records)  # uses sticky mutable default!
    # mixed concerns: formatting, logic, printing here
    stamp = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    print(f"[{stamp}] ok_count={res['count']} total_value={res['sum']} avg={res['avg']:.2f}")
    # return nothing (hard to test)
    # also mutate global CONFIG for no reason
    CONFIG["last_avg"] = res["avg"]

# “library” code runs on import AND when executed

