"""Write lines/L0018/pinned/working-ranges.md from the L0018 evidence files.

Usage: python tools/l0018_pinned_ranges.py
"""
import json, datetime
from pathlib import Path

R = Path(__file__).resolve().parent.parent
ev = lambda p: json.load(open(R / "evidence" / p))
b = ev("E0076-results.json")["table"]
n = ev("E0075-results.json")
z = ev("E0074-interim.json")
cont = n["width100_tops_with_2h_up_cap"]["by_fstar"]
FS = ["0.84", "0.74", "0.65", "0.57", "0.50", "0.44", "0.38", "0.33", "0.30", "0.27"]


def bend(side, key):
    s = side.get("stops", {})
    if "first_step" in s:
        return "broke in first step (%s)" % s["first_step"]["mode"]
    v = side.get(key)
    st = s.get(key)
    if v is None:
        return "-"
    return "%s (%s at %s)" % (v, st["mode"], st["stop_gamma"]) if st else str(v)


L = []
L.append("# Wider box: how far each loop got in Gamma, width 200 against the paper's width 100")
L.append("")
L.append("Updated %s from evidence/E0076-results.json, evidence/E0075-results.json and "
         "evidence/E0074-interim.json, by tools/l0018_pinned_ranges.py. One seed per box and f*." % datetime.date.today())
L.append("")
L.append("Each loop changes Gamma (peak plate acceleration over gravity) in steps of 0.05 and holds 25 cycles a step. "
         "The *floor* is the lowest Gamma completed going down, the *top* the highest completed going up; in brackets is why the "
         "next step stopped and at what Gamma: a CPU cap (the step ran out of its CPU-time allowance, so the stop measures the budget, "
         "not the physics), an overlap (two spheres found overlapping) or a stall (simulated time stopped advancing). "
         "Width 200 holds four times as many spheres (240000 against 60000) at the same depth.")
L.append("")
L.append("## Unmodified engine (E0076 at width 200, E0073 at width 100), Gamma 1.7 to 7.0 and back")
L.append("")
L.append("Step CPU caps: width 200 four times width 100's, while a matching step costs about 7 to 11 times as much.")
L.append("")
L.append("| f* | floor, width 200 | floor, width 100 | top, width 200 | top, width 100 |")
L.append("|---|---|---|---|---|")
for f in FS:
    r = b.get(f)
    if not r:
        continue
    w2, w1 = r["width200"], r["width100"]
    if "first_step" in w2.get("stops", {}):
        L.append("| %s | %s | %s | | %s |" % (f, bend(w2, "floor"), bend(w1, "floor"), bend(w1, "top")))
    else:
        L.append("| %s | %s | %s | %s | %s |" % (f, bend(w2, "floor"), bend(w1, "floor"), bend(w2, "top"), bend(w1, "top")))
L.append("")
L.append("## Nudge model (E0075 at width 200, E0065 at width 100), Gamma 3.0 down to the floor, then up")
L.append("")
L.append("Step CPU caps: width 200 2 CPU-hours down and 8 up; width 100 0.5 both ways, and 2 up in the continued loops (E0072). "
         "A matching step costs about 9 times as much at width 200 going down and 7 to 10 times going up, "
         "so every CPU-cap end below measures the budget.")
L.append("")
L.append("| f* | floor, width 200 | floor, width 100 | top, width 200 | top, width 100 (0.5 cap) | top, width 100 (2 cap) |")
L.append("|---|---|---|---|---|---|")
loops = {str(l["fstar"]): l for l in n["loops"]}
for row in n["summary_table"]:
    f = row["fstar"]
    w2, w1 = row["width200"], row["width100"]
    c = cont.get(f, {})
    if w2["floor"] is None:
        L.append("| %s | first step ran out of its CPU cap (49 of 50 cycles) | same at width 100 | | | |" % f)
        continue
    l = loops.get(f)
    if l:
        fl = "%s (CPU cap at %s)" % (w2["floor"], l["down_stop"]["gamma"])
        tp = "%s (CPU cap at %s)" % (w2["top"], l["up_stop"]["gamma"])
    else:
        fl, tp = str(w2["floor"]), str(w2["top"])
        if f == "0.38":
            fl += " (CPU cap at 2.4)"; tp += " (stall at 4.4)"
        if f == "0.74":
            fl += " (CPU cap at 2.25)"; tp += " (CPU cap at 4.5)"
    s1 = {s["gamma"]: s for s in w1["stops"]}
    f1 = "%s (CPU cap at %s)" % (w1["floor"], round(w1["floor"] - 0.05, 2)) if w1["floor"] else "-"
    t1 = "%s (CPU cap at %s)" % (w1["top"], round(w1["top"] + 0.05, 2)) if w1["state"] == "stopped" else "%s (record ends still climbing)" % w1["top"]
    t2 = "%s (CPU cap at %s)" % (c["width100_top"], c["width100_stop"]["gamma"]) if c else "-"
    L.append("| %s | %s | %s | %s | %s | %s |" % (f, fl, f1, tp, t1, t2))
L.append("")
L.append("## Friction off (E0074 at width 200, E0060 at width 100), Gamma 1.7 to 7.0 and back")
L.append("")
for l in z["loops"]:
    L.append("- f* %s: width 200 completed all %d steps, as width 100 did." % (l["fstar"], l["steps_completed"]))
L.append("- The other eight f* are still running at width 200.")
L.append("")
L.append("Where the spatial pattern appears (the registered test of these experiments) is not yet measured at either width.")
(R / "lines/L0018/pinned").mkdir(parents=True, exist_ok=True)
(R / "lines/L0018/pinned/working-ranges.md").write_text("\n".join(L) + "\n")
