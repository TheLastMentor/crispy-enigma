import sys
import json
import yaml
import pathlib
from jsonschema import validate

ROOT = pathlib.Path(__file__).parent

# -----------------------
# Optional: spec/schema validation (v1.0 compatibility)
# -----------------------

def _load_and_validate_spec():
    """
    Try to load praxis-spec.(yaml|yml) and schema.json.
    If they exist, validate once at startup.
    If they don't, just skip quietly.
    """
    # find spec
    spec_path = ROOT / "praxis-spec.yaml"
    if not spec_path.exists():
        alt = ROOT / "praxis-spec.yml"
        if alt.exists():
            spec_path = alt
        else:
            return None

    schema_path = ROOT / "schema.json"
    if not schema_path.exists():
        return None

    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(spec, schema)
    return spec

SPEC = _load_and_validate_spec()

# -----------------------
# Helpers
# -----------------------

def _derive_schedule(commitments):
    """
    Take a list of strings like:
      "13:00 union application"
      "18:00 TRX"
    and turn them into [["13:00","union application"], ...].
    If no time prefix, time is "".
    """
    schedule = []
    for c in commitments or []:
        text = str(c)
        parts = text.split(" ", 1)
        if len(parts) == 2 and len(parts[0]) in (4, 5) and ":" in parts[0]:
            # crude HH:MM detection
            schedule.append([parts[0], parts[1]])
        else:
            schedule.append(["", text])
    return schedule


def _derive_actions(ctx, max_actions=3):
    """
    Use ctx['actions'] if provided.
    Else derive from commitments or fall back to default list.
    """
    actions = ctx.get("actions")
    if actions:
        return list(actions)[:max_actions]

    commits = ctx.get("commitments") or []
    if commits:
        derived = [f"advance: {str(c).split(' ', 1)[-1]}" for c in commits]
    else:
        derived = ["one leverage task", "admin pass", "body maintenance"]

    return derived[:max_actions]


def _compute_alignment(actions_done):
    """
    Tiny heuristic: 0.3 base + up to 0.4 for first 3 actions completed.
    """
    done = actions_done or []
    base = 0.3
    inc = min(len(done), 3) * (0.4 / 3.0)
    return round(base + inc, 2)


# -----------------------
# Workflows
# -----------------------

def _run_morning(ctx):
    """
    MorningPraxis:
    - If energy_score < 3 → fallback DayScript.
    - Else → build DayScript from context, with defaults.
    """
    energy = ctx.get("energy_score", 3)

    # Fallback path
    if energy < 3:
        return {
            "type": "DayScript",
            "north_star": "Recover + one leverage task",
            "actions": ["Do one small thing"],
            "counters": ["remove friction", "hydrate", "10m walk"],
            "schedule": [],
            "risks": ["low energy"]
        }

    # Normal path
    north_star = ctx.get("north_star", "Progress pipeline + protect back")
    actions = _derive_actions(ctx, max_actions=3)
    counters = ctx.get("counters") or [
        "timer before paperwork",
        "docs checklist",
        "light carries only"
    ]
    schedule = _derive_schedule(ctx.get("commitments"))
    risks = ctx.get("risks") or ["bureaucratic delay", "low_back flare"]

    return {
        "type": "DayScript",
        "north_star": north_star,
        "actions": actions,
        "counters": counters,
        "schedule": schedule,
        "risks": risks,
    }


def _run_evening(ctx):
    """
    EveningPraxis:
    - Compute alignment from actions_done.
    - Allow overrides for deltas/lesson/tomorrow_seed via context.
    """
    actions_done = ctx.get("actions_done") or []
    intention = ctx.get("intention")  # not used yet, but kept for future logic

    alignment_score = _compute_alignment(actions_done)

    deltas = ctx.get("deltas") or [
        "tighten doc-prep window",
        "pre-pack ID packet",
    ]

    lesson = ctx.get("lesson") or "Small prep eliminates bureaucratic drag."

    tomorrow_seed = ctx.get("tomorrow_seed") or \
        "Protect back + move the pipeline one click."

    return {
        "type": "ReflectionLog",
        "alignment_score": alignment_score,
        "deltas": deltas,
        "lesson": lesson,
        "tomorrow_seed": tomorrow_seed,
    }


# -----------------------
# Public API
# -----------------------

def run(req: dict):
    """
    req = {
      "workflow": "MorningPraxis" | "EveningPraxis",
      "context": { ... }
    }
    """
    workflow = req.get("workflow")
    ctx = req.get("context", {}) or {}

    if workflow == "MorningPraxis":
        return _run_morning(ctx)
    elif workflow == "EveningPraxis":
        return _run_evening(ctx)
    else:
        raise SystemExit(f"Unknown workflow: {workflow!r}")


# -----------------------
# CLI entrypoint
# -----------------------

if __name__ == "__main__":
    # If given a filename, treat it as JSON request.
    if len(sys.argv) > 1:
        path = pathlib.Path(sys.argv[1])
        req = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = sys.stdin.read()
        if data.strip():
            req = json.loads(data)
        else:
            # Default: simple MorningPraxis with empty context
            req = {"workflow": "MorningPraxis", "context": {}}

    out = run(req)
    print(json.dumps(out, indent=2))
