# GapWatch‑AI

One‑click reproducibility tracking **and** energy‑usage auditing for any ML or LLM project.  
Built for async agents like **Google Jules** but works in plain GitHub Actions.

---

## ✨ Features
- **Deterministic replays** – container + seed lockfile (`gapwatch.jsonld`)
- **Live GreenMeter** – kWh, CO₂, & watt‑hours / output‑token
- **EdgeGuard** – verifies post‑quantization accuracy on test sets
- **CI / Jules integration** – adds status checks & PR comments
- **Zero‑config dashboard** – `npm run dev` spins up a SvelteKit UI

---

## 🏗 Architecture
```

repo/
├─ gapwatch/          # Python core
│   ├─ replay.py      # build & data lock
│   ├─ energy.py      # power probes via NVML / intel\_rapl
│   └─ edgeguard.py   # PTQ & eval harness
├─ web/               # Svelte frontend
├─ .github/
│   └─ workflows/ci.yml
└─ README.md

````

---

## 🚀 Quick Start

```bash
pip install gapwatch-ai
gapwatch init            # creates lockfile
gapwatch train scripts/train_bert.py --epochs 3
gapwatch replay <run_id> # deterministic rerun
````

Add to CI:

```yaml
- name: GapWatch
  run: gapwatch ci --quantize int8 --notify
```

---

## 📊 Dashboard Preview

```bash
npm install && npm run dev
# http://localhost:5173
```

Displays **energy / step**, accuracy deltas, and a “replay” button.

---

## 🗺 Roadmap

* [ ] EU AI‑Act audit report export (XAI tags)
* [ ] ARM & Apple‑Silicon energy probes
* [ ] Agentic‑safety fuzz tests plug‑in
* [ ] Multi‑modal dataset hashing

---

## 🤝 Contributing

1. Fork → feature branch → PR.
2. All code must pass `ruff` + `pytest`.
3. New features require a demo in `/examples`.

---

## 📄 License

Apache‑2.0
