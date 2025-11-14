# crispy-enigma

A personal **Praxis Engine** — a deterministic backend for structured self-reflection and daily execution, powered by GPT as a conversational interface.

---

## 🧱 v1.0.0 – Deterministic Baseline
**Released:** 2025-11-14  
**Tag:** `v1.0.0`

### Features
- `run.py` executes fixed deterministic workflows.  
- `praxis-spec.yaml` defines guard conditions and outputs.  
- `schema.json` enforces structural validation.  
- Produces **DayScript** and **ReflectionLog** JSONs.

### Example Run
```bash
python run.py request.morning.json
Output:

json
Copy code
{
  "type": "DayScript",
  "north_star": "Progress pipeline + protect back",
  "actions": [
    "submit documents by 12:00",
    "confirm ID contingency",
    "TRX core circuit"
  ]
}
```

🚧 v1.1.0 – Lisp DSL Engine (in progress)
Branch: feature/v1.1-lisp-engine

Goal
Replace hard-coded logic with a small Lisp interpreter and workflow DSL.

Planned Additions
praxis.lisp defining workflows in S-expression syntax

Mini Lisp evaluator inside run.py

Support for contextual variables (energy, commitments, actions_done)

Deterministic helper functions: (plan), (schedule), (align), etc.

Backward compatibility: same JSON outputs as v1

Example Workflow (MorningPraxis)
```
lisp
Copy code
(workflow MorningPraxis
  (if (>= (get energy_score) 3)
      (output DayScript (map north_star "Progress pipeline + protect back"))
      (output DayScript (map north_star "Recover + one leverage task"))))
```
	  
🗂️ Structure
graphql
Copy code
crispy-enigma/
│
├─ run.py              # Engine entrypoint
├─ praxis-spec.yaml    # v1.0 config
├─ schema.json         # Spec validator
├─ praxis.lisp         # v1.1 DSL workflows
├─ requests/           # Example JSON requests
└─ logs/               # Optional run history
🧭 Usage
```
bash
Copy code
# Activate environment
.\.venv\Scripts\activate

# Run a request
python run.py request.morning.json

# Tag release
git tag -a v1.1.0 -m "Lisp DSL engine"
```

🔮 Roadmap
 Implement (log …) form for journaling

 Add energy-based branching macros

 Integrate GPT interface templates

 Add persistence layer (JSONL log per day)

 Prepare v1.2 with dynamic planning verbs