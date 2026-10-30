# My Scientific Research Skills

Agent skills for scientific research. Each skill is one self-contained folder with a `SKILL.md`.

## Skills

| Skill | What it does | Last updated |
|-------|--------------|:---:|
| [`figure-hygiene`](skills/figure-hygiene) | One clean figure per question, from just "here's my data, make a figure": the plot form is reasoned from the data, the question is the title, the details go in a caption file. | ![](https://img.shields.io/badge/updated-2026--10--30-blue) |
| [`new-experiment`](skills/new-experiment) | Scaffold a self-contained Lab-Standard `experiments/exp-NNNN_slug/` run (config + `run.py` + provenance manifest + MLflow + hypothesis README) and register it in `experiments/INDEX.md`. | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`new-project`](skills/new-project) | Scaffold a new scientific project from the Lab Standard template (`src/` package, `experiments/`, `notebooks/`, `data/`, `docs/decisions/`, `AGENTS.md`, `justfile`, `environment.yml`, MLflow + provenance helpers). | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`scientific-talk`](skills/scientific-talk) | Build a figure-forward `.pptx` talk (journal club, lab meeting, conference, thesis committee): one claim per slide, arc-driven, matched to a house style. | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`write-like-me`](skills/write-like-me) | Write anything in Anshul's own voice — plain, Feynman-style, intuition-first, zero AI slop: Slack replies, emails, WORKLOG/README prose, captions, abstracts, PR descriptions. De-slops and tone-matches existing drafts too. | ![](https://img.shields.io/badge/updated-2026--09--18-blue) |

## Install one skill

Put the skill's folder where your tool looks for skills. For example, `figure-hygiene` into Claude Code:

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills
curl -L https://github.com/anshu957/my-scientific-research-skills/archive/main.tar.gz \
  | tar -xz --strip-components=2 my-scientific-research-skills-main/skills/figure-hygiene
```

For another skill, replace `figure-hygiene` with its name. Run the same command again to update.

| Tool | Where the folder goes |
|------|-----------------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Claude.ai / desktop | Zip the folder, then upload it under Settings → Capabilities → Skills |
| Any other LLM | Attach the folder's files and say "follow SKILL.md" |

## License

Personal research tooling. Reuse freely with attribution.
