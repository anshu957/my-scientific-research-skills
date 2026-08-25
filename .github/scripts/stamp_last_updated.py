#!/usr/bin/env python3
"""Refresh each skill's last-updated date from git history.

For every folder under skills/, find the date of the most recent commit that
changed a *real* file in it (ignoring the .last-updated stamp itself), then:
  1. write that date into skills/<name>/.last-updated
  2. update the "updated-YYYY--MM--DD" badge on that skill's README table row

Run by the GitHub Action in .github/workflows/stamp-last-updated.yml.
"""
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"


def last_commit_date(name: str) -> str:
    """ISO date (YYYY-MM-DD) of the newest commit touching skills/<name>,
    excluding the auto-written .last-updated stamp."""
    out = subprocess.check_output(
        ["git", "log", "-1", "--format=%cs", "--",
         f"skills/{name}", f":(exclude)skills/{name}/.last-updated"],
        cwd=ROOT, text=True,
    ).strip()
    return out


def main() -> None:
    readme = README.read_text().splitlines()
    for skill in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        name = skill.name
        date = last_commit_date(name)
        if not date:
            continue

        stamp = skill / ".last-updated"
        if not stamp.exists() or stamp.read_text().strip() != date:
            stamp.write_text(date + "\n")

        badge_date = date.replace("-", "--")  # shields.io escapes dashes
        for i, line in enumerate(readme):
            if f"skills/{name})" in line:  # the table row linking to this skill
                readme[i] = re.sub(r"updated-\d{4}--\d{2}--\d{2}-blue",
                                   f"updated-{badge_date}-blue", line)

    README.write_text("\n".join(readme) + "\n")


if __name__ == "__main__":
    main()
