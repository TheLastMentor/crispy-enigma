import sys, json, yaml, pathlib
from jsonschema import validate

ROOT = pathlib.Path(__file__).parent
spec = yaml.safe_load((ROOT/"praxis-spec.yaml").read_text())
schema = json.loads((ROOT/"schema.json").read_text())
validate(spec, schema)

def run(req):
    wf = spec["workflows"][req["workflow"]]
    ctx = req.get("context", {})

    if req["workflow"] == "MorningPraxis":
        # guard / fallback
        if not eval(str(wf.get("guard", "True")), {}, dict(**ctx)):
            fb = wf["fallback"]
            return {
                "type": "DayScript",
                "north_star": fb["north_star"],
                "actions": fb["actions"],
                "counters": ["remove friction", "hydrate", "10m walk"],
                "schedule": [],
                "risks": ["low energy"]
            }
        # minimal deterministic “planner”
        north_star = "Progress pipeline + protect back"
        actions = [
            "submit documents by 12:00",
            "confirm ID contingency",
            "TRX core circuit"
        ]
        counters = ["timer before paperwork", "docs checklist", "light carries only"]
        schedule = [["10:30","paperwork prep"],["13:00","union application"],["18:00","TRX"]]
        risks = ["bureaucratic delay","low_back flare"]
        return {"type":"DayScript","north_star":north_star,"actions":actions,"counters":counters,"schedule":schedule,"risks":risks}

    if req["workflow"] == "EveningPraxis":
        done = ctx.get("actions_done", [])
        align = round(0.3 + 0.4 * min(len(done),3)/3, 2)
        deltas = ["tighten doc-prep window", "pre-pack ID packet"]
        lesson = "Small prep eliminates bureaucratic drag."
        seed = "Protect back + move the pipeline one click."
        return {"type":"ReflectionLog","alignment_score":align,"deltas":deltas,"lesson":lesson,"tomorrow_seed":seed}

    raise SystemExit(f"Unknown workflow: {req['workflow']}")

if __name__ == "__main__":
    # Accept a YAML request file path or read from stdin JSON
    if len(sys.argv) > 1:
        req = yaml.safe_load(pathlib.Path(sys.argv[1]).read_text())
    else:
        req = json.loads(sys.stdin.read())
    out = run(req)
    print(json.dumps(out, indent=2))
