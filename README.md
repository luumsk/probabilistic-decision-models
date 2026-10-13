# Probabilistic Decision Models

Lectures, notebooks, and experiments for learning how models estimate probabilities and turn them into decisions. Topics include calibration, proper scoring rules, cost-aware decisions, and the design of decision workflows. Typed decision APIs such as Jev and OpenAI Decisions appear as optional case studies.

## Structure

```
lectures/      Lecture notes and slides
notebooks/     Runnable notebooks for the lectures
src/pdm/       Shared code: metrics, decision rules, synthetic data
experiments/   One dated folder per experiment (start from _template/)
data/          Synthetic and recorded data
```

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[notebooks,dev]"
```

For live API experiments, also run `uv pip install -e ".[providers]"`, then copy `.env.example` to `.env` and add your keys. Everything else works offline.

## License

[MIT](LICENSE)
