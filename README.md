# Crispy Enigma — Praxis Engine

Crispy Enigma is a small workflow engine that powers my personal Praxis system.
The structure is simple:

- A **request** is JSON (`workflow` + `context`)
- The engine (`run.py`) evaluates it
- The output is deterministic JSON (DayScript or ReflectionLog)
- A custom GPT acts as the conversational interface

This repo is the long-term home for all Praxis logic, tooling, and workflows.

---

## 🔧 v1.0 — Deterministic Baseline

The initial implementation used:

- `praxis-spec.yaml` for static structure
- A fixed `run.py` that produced **DayScript** or **ReflectionLog**
- Simple hard-coded logic with no customization

This version established:
- Shape of the JSON outputs  
- Basic inputs  
- Foundation for GPT integration  

Tagged as **v1.0.0**.

---

## 🚧 v1.1 — Context-Aware Engine (Work in Progress)

The current feature branch (`feature/v1.1-lisp-engine`) focuses on:

- Replacing the DSL/Lisp experiment with **clean, readable Python**
- A context-aware engine that:
  - Responds to `energy_score`
  - Derives actions from user-provided commitments
  - Allows overrides for north star, counters, risks, deltas, etc.
  - Computes an alignment score based on completed actions

The v1.1 engine produces the same output structure as v1, but is **smarter and simpler**.

When complete, this will be merged into `main` and tagged as **v1.1.0**.

---

## 📁 Project Structure
```
crispy-enigma/
│
├── run.py # The active engine (context-aware)
├── praxis.lisp # Design sketches (not currently executed)
├── request.morning.json
├── request.evening.json
├── README.md
└── CHANGELOG.md

```


---

## 🧪 Running Locally

Create your virtual environment (done once):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Run any request:

powershell
Copy code
python run.py request.morning.json
python run.py request.evening.json
Or send JSON over stdin:

powershell

echo "{ \"workflow\": \"MorningPraxis\", \"context\": { \"energy_score\": 4 } }" | python run.py
```

## 🔮 Roadmap
Planned directions include:

v1.1: Logging (optional JSONL history)

v1.2: Reflection heuristics (better deltas + future seed logic)

v1.3: Task weighting / friction scoring

v2.0: Optional mini-DSL (only if it proves useful)

The system evolves strictly based on real usage, not ideology.

## 🧠 Philosophy
This repo exists to:

Externalize mental load

Provide structure without constraint

Let GPT act as a natural-language interface

Keep Praxis grounded and forward-moving

It’s intentionally small and pragmatic.


---

# ✅ **CHANGELOG.md (starting version)**

```markdown
# Changelog

All notable changes to this project will be documented here.
This project follows a simple semantic versioning pattern.

---

## [Unreleased]
### Added
- Context-aware engine (v1.1 work in progress)
- Default actions now derive from commitments
- Fallback logic when `energy_score < 3`
- Alignment scoring for EveningPraxis
- README and project documentation updates

### Changed
- Removed DSL/Lisp evaluator (postponed for future exploration)
- Simplified `run.py` for readability and maintainability

---

## [1.0.0] — Baseline Release
### Added
- Deterministic `run.py` engine
- DayScript + ReflectionLog output schema
- Initial project structure```