# Calibration corpus

Real messages, verbatim. When SKILL.md and these disagree, these win — the rules were
derived from the messages, not the other way round.

Read the *shape*, not the content: how a message opens, how much context gets a paren,
where the line breaks fall, how confidence is signalled, how it ends.

---

## 1. Explaining a tool to a non-programmer colleague

> Hi Brian --
>
> I use claude.ai (claude chat) for text based reasoning and research. Claude code (uses
> the same underlying claude's LLM models) is some kind of interface (can be used in
> terminal or other IDE) which is specifically designed to work with coding.
>
> Anyways, I would just put your query in the chat and get some response to it like below
> (uses PubMed connector to get the correct papers):
> However, for multiple query texts, I would use claude code to write a small script which
> loops over all query texts and do its PubMed based research and then finally collect all
> results in some json file or some dictionary (query: results) which can then later be
> used programmatically to do other downstream analysis.
>
> Is this what you had in mind?

**What to take:** "some kind of interface" instead of a precise definition — precision
the reader doesn't need is noise. Heavy parenthetical context. "Anyways" as a real
transition. Ends by handing control back with a question rather than a summary.

---

## 2. Status update, work in progress

> Hi Brian --
>
> Dylan sent me the annotations (he did some re-clustering using leiden and annotated the
> cell types). Looks okay to me (and him as well). I did ask him if he got a chance to show
> this to Paul and is waiting his reply.
>
> My next step is to now add EPAS1 to this and see how that looks. If everything looks okay
> and the proportions align with the expectations, I'll go ahead and re-do the RNA velocity
> and temporal DE analysis later today.
>
> Will update you as it goes and when we meet today.

**What to take:** who did what, then my assessment with its confidence attached ("Looks
okay to me"), then the conditional next step ("If everything looks okay ... I'll go
ahead"), then when. Three short paragraphs, each doing one job.

---

## 3. Logistics / scheduling

> Brian --
>
> I initially schedule a zoom meeting with Dylan (as per his availability) at 3:00pm ET
> today but heard from him that something came up and either he could meet me later after
> 4:15pm today or tomorrow 11:00 am ET onwards.
>
> Therefore I canceled the current zoom meeting. Since I'm not sure when we will meet, I
> might ping you ad-hoc to see if you want to hop-on.

**What to take:** no opener greeting beyond the name. Facts with real times, then the
decision taken and why, then what the reader should expect. No apology ceremony.

---

## 4. Answering a question about a result

> Thanks. Yes, The differences in conditions are minimal because primitive syn cells are
> expected to not change much between the conditions (at least that's what I get from cell
> type compositions) but there would be significant changes in ExM and unknown lineages.
> I'm generating those heatmaps and will share soon.

**What to take:** answers the question in the first four words ("Yes, the differences are
minimal"), then the reason, then the source of the belief in parens, then the contrast
that matters, then what's coming. Four sentences total.

---

## 5. Handing over files

> Hi Gautam -- I just added following files in the shared folder for BXD heritability
>
> 1. `h2_estimates_with_usage_bxd.txt` --> containing h2 estimates (from ANNOVA) and the
>    motif usage for BXD population.
> 2. `h2_estimates_with_usage_jabs1200.txt` --> containing h2 estimates (from GEMMA) and
>    the motif usage for JABS1200 population.
>
> the one that you used earlier was renamed to `h2_estimates_with_usage_combined_OFA.txt`
> which contains h2 estimates (GEMMA) and their motif usage for the combined population.
> The phenotype files remains the same.
>
> The quadrant threshold for both of the population are 0.4 for h^2 and 0.5% (NOTICE THE
> PERCENTAGE) for motif usage.

**What to take:** this is the one case where a numbered list belongs — discrete artifacts
the reader will open. `filename --> what's in it, and which method produced it`. The
rename gets called out because it will otherwise break their script.

NOTE on the caps: "NOTICE THE PERCENTAGE" is a one-off in this corpus, not a habit -- do
not reproduce it. The instinct behind it is right (0.5 vs 0.5% is a 100x error waiting to
happen, so the reader has to see it), but write the warning in plain text instead.

---

## 6. Explaining a subtle technical point

> Let's just meet with together with Vivek.
>
> I think, I now understand the issue. It was basically similar to what you suggested
> yesterday. Kinship measures not similarity of genotype but variation from population
> means of the genotypes (SNPs). So, an inbred strain genotype (0,2) would have high
> deviation from population mean genotype (1) and that would result in a larger self
> kinship.

**What to take:** the model example of the Feynman move. Credit first ("similar to what
you suggested"), the confidence marked ("I think, I now understand"), then the correction
in the form *not X but Y*, then one concrete instance with actual values that makes the
conclusion inevitable. Nothing abstract survives without a number attached to it.

---

## 7. The working register — prompts to Claude, notes to self

> I need a skill who can write it in my style and tone and does not have the typical AI
> slop. I like to write or follow feynman style thinking and reasoning -- meaning
> intuition and simple ideas first and not usign convoluted or jargony language. Here is
> some examples of my slack replies for you to undertsand my tone

> yes this is fine but have a warmer tone and a bit of my thing which is adding some
> additional context in paranthesis. Also, see my prompts with you -- this would also
> give you idea about my style

**What to take:** answer first, qualify second ("yes this is fine but ..."). The
mid-sentence `--` introducing a gloss, and "meaning X" doing the defining. Clauses joined
with "and" rather than split into tidy sentences. Zero preamble and zero sign-off.

**What not to take:** the typos. Those come from typing fast, not from style, and they
shouldn't appear in anything going to a colleague.
