# human-0 — what I'm about to do, explained simply

Imagine 87 science‑fair projects, each with a poster that says "we found X". Nobody has checked whether the posters are true. My job is to redo the experiments on your one graphics card and keep a scorecard: did it install, did it run, did it get the number on the poster?

So far the scorecard has two lines. Project 2 (AntiPaSTO) ran perfectly and got a totally different number from its poster. Project 3 (the "noise reveals sandbagging" one) got the same answer as its poster, more clearly than the original author did.

Tonight I'm doing two things:

**1. Project 1 (the "different models don't secretly think alike" one).** It needs six language models downloaded first (about 22 GB — that's the slow part, an hour or so, and it doesn't use the graphics card). Then the actual experiment is short: for each pair of models, feed them the same 10,000 sentences, record what's happening inside at nine depths, and measure how similar the two sets of internal patterns are. The poster says: two models from the same family look very similar (0.9 on a 0–1 scale), two models from different families barely at all (about 0.2). I'll check both numbers. There's a nice trap built in: if even the "same family" pair comes out dissimilar, my pipeline is broken, not the poster.

**2. Then the quick ones.** There are 31 projects that each take minutes rather than hours. Each folder has a little script that clones the code, installs it in its own sandbox, and runs it with a time limit. I'm lining all 31 up so the graphics card is never idle — one at a time, like a bakery oven. When each one comes out I look at it, write down what happened on the scorecard, and leave two notes: a technical one for future‑me (`handoff-N.md`) and one like this for you (`human-N.md`).

**What can go wrong:** downloads stall (happened once already — I now use a slower but reliable path); a project's code needs a library version that no longer exists; a project secretly needs a paid API, which I'm not allowed to use. Those aren't failures of the plan — writing down *why* something didn't run is exactly the point of the scorecard.

**What I won't do:** change what any experiment measures to make it "work". Only the environment gets fixed.
