# My Scientific Research Skills

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) **Agent Skills** I use for scientific-research work — figure making, experiment scaffolding, project setup, and talk building. Each skill is a self-contained folder with a `SKILL.md` that Claude loads on demand.

## Skills

| Skill | What it does | Last updated |
|-------|--------------|:---:|
| [`figure-hygiene`](skills/figure-hygiene) | Make one clean scientific figure per question, for screen: the plot form is reasoned from the data, the question is the bold title, only necessary labels, Arial, colorblind-safe palette, vector PDF into `figures/`; all detail lives in a synced `figure_captions.md`. Works from a bare "here's my data, make a figure" prompt. | ![](https://img.shields.io/badge/updated-2026--10--30-blue) |
| [`new-experiment`](skills/new-experiment) | Scaffold a self-contained Lab-Standard `experiments/exp-NNNN_slug/` run (config + `run.py` + provenance manifest + MLflow + hypothesis README) and register it in `experiments/INDEX.md`. | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`new-project`](skills/new-project) | Scaffold a new scientific project from the Lab Standard template (`src/` package, `experiments/`, `notebooks/`, `data/`, `docs/decisions/`, `AGENTS.md`, `justfile`, `environment.yml`, MLflow + provenance helpers). | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`scientific-talk`](skills/scientific-talk) | Build a figure-forward `.pptx` talk (journal club, lab meeting, conference, thesis committee): one claim per slide, arc-driven, matched to a house style. | ![](https://img.shields.io/badge/updated-2026--08--25-blue) |
| [`write-like-me`](skills/write-like-me) | Write anything in Anshul's own voice — plain, Feynman-style, intuition-first, zero AI slop: Slack replies, emails, WORKLOG/README prose, captions, abstracts, PR descriptions. De-slops and tone-matches existing drafts too. | ![](https://img.shields.io/badge/updated-2026--09--18-blue) |

Each skill folder also carries a `.last-updated` stamp (ISO date) so the date travels with the skill.

## Install

Skills are independent — install only the ones you want.

### One skill (Claude Code)

Set `SKILL` to any folder name from the table above:

```bash
SKILL=figure-hygiene
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/anshu957/my-scientific-research-skills.git /tmp/research-skills
git -C /tmp/research-skills sparse-checkout set "skills/$SKILL"
mkdir -p ~/.claude/skills
cp -r "/tmp/research-skills/skills/$SKILL" ~/.claude/skills/
rm -rf /tmp/research-skills
```

This downloads only that skill. To install it for one project instead of for you,
copy it into `<project>/.claude/skills/` and commit it there.

### All skills (Claude Code)

```bash
git clone https://github.com/anshu957/my-scientific-research-skills.git
mkdir -p ~/.claude/skills
cp -r my-scientific-research-skills/skills/* ~/.claude/skills/
```

### Claude.ai / Claude desktop

Zip the skill folder (the zip must contain the folder, e.g. `figure-hygiene/SKILL.md`)
and upload it under **Settings → Capabilities → Skills**.

### Use

Start a new Claude Code session. Claude loads a skill automatically when your request
matches it (e.g. "here's my data, make a figure"), or call it directly as
`/figure-hygiene`, `/new-experiment`, … .

### Update

Re-run the same install commands; `cp -r` overwrites the old copy.

### Requirements

- `figure-hygiene`: Python with matplotlib (+ seaborn for heatmaps), the Arial font, and
  PyMuPDF (`pip install pymupdf`) or poppler for its `qa.py` check.
- `new-experiment`, `new-project`: designed for the [Lab Standard](https://github.com/anshu957/lab-standard) layout.

## License

See each skill folder for any bundled `LICENSE`. Unless otherwise noted, personal research tooling — reuse freely with attribution.
