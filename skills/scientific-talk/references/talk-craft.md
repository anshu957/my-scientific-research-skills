# Talk craft: the review checklist and the delivery plan

Read this when planning the arc (phase 2) and again before calling a deck done
(phase 6). It is the accumulated review of real decks, not general advice.

## Contents

1. Arc — does it build or does it list?
2. Assertion–evidence — does the figure show the claim?
3. Slide economy — what earns its place
4. Figure treatment — journal panel vs slide panel
5. Speaker notes — the shape that survives contact with a room
6. Delivery plan — time budget, pauses, framing someone else's work
7. The pass/fail questions

---

## 1. Arc — does it build or does it list?

The commonest structural failure is that the deck's order is the *paper's figure
order*. Figures 1–6 become six sections, each individually true, none of them
owed to the previous one. Symptoms and fixes:

| symptom | fix |
|---|---|
| nothing is promised in the first two minutes | state the punchline on slide 2, out loud, and say the methods are how they earned it |
| the closing slide's headline is the word "Summary" | make it the assertion the talk earned |
| consecutive headlines could be swapped | the middle is a list; find the question each section answers and let the previous one raise it |
| the audience learns the main result at minute 40 | keep the result there, but plant it at minute 2 |
| attention sags in the methods | give the methods a job: they are the audience's audit of a claim they already know is coming |

Read the headlines in order with nothing else. That list is the talk. If it does
not narrate, no amount of slide polish will fix it.

## 2. Assertion–evidence — does the figure show the claim?

Every slide is one claim plus the evidence for it. Go slide by slide and ask:
does the figure on *this* slide demonstrate *this* headline?

Typical mismatches, all seen in real decks:

- The headline claims a negative control ("not body size") whose panel is not on
  the slide — only an annotation states it. **Fix**: crop the panel in, or weaken
  the claim to what is shown.
- The headline claims a property the panel cannot resolve at slide scale
  ("blocky, not jittery" over a sparse dot raster). **Fix**: zoom the panel to a
  window where the property is visible, or state what the panel does show and say
  the rest out loud, flagged as not visible here.
- The headline claims a negative ("aging is not smooth") from evidence that only
  establishes the positive (a stage model was fit). **Fix**: add the panel that
  contrasts the two models, or split the claim across two slides.

An audience that catches one of these stops trusting the others.

## 3. Slide economy — what earns its place

- **Cut**: any slide making a claim an earlier slide already made; any panel
  making a second claim the headline does not make (it shrinks the first);
  supplementary insets rendered so small their axis text is illegible.
- **Keep even under time pressure**: the slide that shows the method *failing*
  (it buys credibility for the ones where it works); the one slide where the
  audience sees the phenomenon with their own eyes before any model touches it —
  it does emotional work, and a talk with none is a report.
- **Move to backup** rather than cutting: model-selection curves, robustness
  checks, regime details, full ROC families. A backup slide is the right answer
  to "why 100 states?" and costs nothing until asked.
- **Add if the audience is specialist**: how this method compares with the ones
  *they* use. If they benchmark the alternatives, they will ask; being the person
  who can answer it turns a report into a contribution.

## 4. Figure treatment — journal panel vs slide panel

A journal panel is for a reader with unlimited time; a slide panel gets ~30–90
seconds and no zoom. Interventions, cheapest first:

1. **Crop tighter** — drop the across-life half of a panel when the claim is
   "at 100 days".
2. **Shorten the headline to one line** — buys ~28 pt of figure height, which is
   ~12% of the figure area on a 16:9 slide.
3. **Zoom then texture** — one readable row/unit of a dense panel, then the full
   panel with a different claim ("they do not all behave the same way").
4. **Build** — reveal panels one click at a time from crops of identical
   geometry. Mandatory for the payoff slide; valuable wherever a busy panel hides
   the thing being pointed at.
5. **Annotate** — ≤ 2 short accent-coloured labels, no arrows, in the free
   gutter. Never an annotation that restates a label the panel already prints.
6. **Redraw** — legitimate when you are choosing a visual encoding suited to 30
   seconds (two mean ± SEM traces instead of two heatmaps). Not legitimate if you
   do not have the underlying data: annotate instead of inventing.

Also: put a **slide number** on every slide. In a discussion format people need
to be able to say "go back to fourteen". Cheapest high-value change there is.

## 5. Speaker notes — the shape that survives contact with a room

Accurate prose paragraphs are unusable under pressure: the speaker either reads
them aloud (fatal) or ignores them (wasteful). Give each slide five short fields,
≤ 90 words total:

```
CLAIM    — one sentence, spoken as the slide appears; paraphrases the headline
POINT    — where the cursor goes, numbered, physical instructions only
SAY      — the numbers you will actually pronounce, as fragments
MY READ  — your interpretation, with the verbal marker attached
PAUSE / IF SHORT — the planned question, or how to cut this slide to 20 seconds
```

Two rules that make it work: `SAY` holds only numbers you will speak (everything
else belongs on a backup slide), and every slide has an `IF SHORT` — even if it
is "never cut this one". You will need those decisions at minute 40, not at
minute 5 when you were still on schedule.

## 6. Delivery plan

**Time budget.** ~1.5–2 min per content slide. For a discussion format target
~45 min of material in a 60-min slot; the remainder gets taken by interruption
whether or not you plan for it. Write the budget per section, and name the
slides you will cut if you are behind at the halfway mark — decided in advance,
not in the moment.

**Planned pauses.** Three or four, placed where the audience's own prediction is
worth eliciting *before* you show the answer:

- After the first slide that makes the audience feel the phenomenon: ask what
  they would measure. Take two answers, resolve neither, promise it comes back.
- After the first real result: ask what would convince them it is not circular —
  the next section is your answer, and they now want it.
- After the weakest evidence: ask "do you buy it?" and let it run. Better at
  minute 38 than at minute 58.
- Not at the payoff. Deliver that one fast and inevitable, then move.

**Framing someone else's work** (journal club):

- Open with why you chose it, tied to this lab's work in one sentence. That makes
  you a participant, not a narrator.
- Use three registers and keep them audible: *"the paper reports…"* (fact),
  *"they argue…"* (the authors' interpretation), *"my read is…"* (yours).
- Give a finding its best version before you critique it. A room that hears the
  flaw first stops listening to the result.
- Park objections: "hold that — it's on my last slide." Keep a limitations slide
  as the parking lot, and make its last line the question *this* room should argue
  about.
- Do not defend the authors; you are the room's reader, not their advocate.
- "I don't know, that's not in the supplement" is the correct answer to several
  questions you will get. Guessing about someone else's methods costs the room.

## 7. The pass/fail questions

Before shipping:

1. Read the headlines in order. Do they narrate the argument?
2. Is the payoff promised in the first 90 seconds?
3. For each slide: does the figure demonstrate the headline?
4. Is any figure smaller than the slide allows?
5. Can the claim be read in three seconds from the back?
6. Do the notes tell the speaker what to point at, what to say, and what to cut?
7. Is there a slide number on every slide, and a backup section?
8. Does the last slide state the assertion the talk earned?
