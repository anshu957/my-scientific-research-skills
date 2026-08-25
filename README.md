# My Scientific Research Skills

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) **Agent Skills** I use for scientific-research work — figure making, experiment scaffolding, project setup, and talk building. Each skill is a self-contained folder with a `SKILL.md` that Claude loads on demand.

## Skills

| Skill | What it does | Last updated |
|-------|--------------|:---:|
| [`figure-hygiene`](skills/figure-hygiene) | Produce clean, publication-quality scientific figures: one title = the key question, only necessary labels, vector PDF into `figures/` with a journal rcParams style and colorblind-safe palette; all detail lives in a synced `figure_captions.md`. | ![](https://img.shields.io/badge/updated-2026--08--21-blue) |
| [`new-experiment`](skills/new-experiment) | Scaffold a self-contained Lab-Standard `experiments/exp-NNNN_slug/` run (config + `run.py` + provenance manifest + MLflow + hypothesis README) and register it in `experiments/INDEX.md`. | ![](https://img.shields.io/badge/updated-2026--07--14-blue) |
| [`new-project`](skills/new-project) | Scaffold a new scientific project from the Lab Standard template (`src/` package, `experiments/`, `notebooks/`, `data/`, `docs/decisions/`, `AGENTS.md`, `justfile`, `environment.yml`, MLflow + provenance helpers). | ![](https://img.shields.io/badge/updated-2026--07--14-blue) |
| [`scientific-talk`](skills/scientific-talk) | Build a figure-forward `.pptx` talk (journal club, lab meeting, conference, thesis committee): one claim per slide, arc-driven, matched to a house style. | ![](https://img.shields.io/badge/updated-2026--08--21-blue) |

Each skill folder also carries a `.last-updated` stamp (ISO date) so the date travels with the skill.

## Install

Clone into your Claude Code skills directory:

```bash
git clone https://github.com/anshu957/my-scientific-research-skills.git
# copy (or symlink) the skills you want into ~/.claude/skills/
cp -r my-scientific-research-skills/skills/* ~/.claude/skills/
```

Restart Claude Code (or start a new session) and the skills become available as `/figure-hygiene`, `/new-experiment`, `/new-project`, `/scientific-talk`.

## License

See each skill folder for any bundled `LICENSE`. Unless otherwise noted, personal research tooling — reuse freely with attribution.
