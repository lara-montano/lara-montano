# Designing heat exchangers under uncertainty — explained for everyone

**ESCAPE 2026 poster** · *Design Optimization of Shell-and-Tube Heat Exchangers under Operational Uncertainty: A Comparative Study Across Three Paradigms*
F. I. Gómez-Castro · S. I. Martínez-Guido · C. Gutiérrez-Antonio · O. D. Lara-Montaño

---

## How to read this document

This text explains the work **from scratch**, taking nothing for granted. It is meant for
someone with no background in chemical engineering, so they can understand **what we did, why
it matters, and what we found**. Every technical word is explained in plain language the first
time it appears, with everyday comparisons. If you only have a minute, read Section 1. If you
want to really understand it, read straight through: each section builds on the one before.

> **The whole idea in one line:** when you design a piece of industrial equipment, the real
> operating conditions are never exactly what you assumed. We compare four ways of accounting
> for that variability, and we show which one is worth using — and which one, surprisingly,
> turns out worse than expected.

---

## 1 · The one-minute version

Imagine you have to design the radiator for a factory: a device that cools down a hot liquid.
The usual approach is to design it assuming **one single fixed set of conditions** (this much
flow, this temperature). But in real life those conditions change all the time. So the device
that looked perfect on paper **fails part of the time** once reality drifts away from what you
assumed.

We took **a realistic case** — cooling hot methanol with seawater — and designed it in **four
different ways**, each with a different philosophy for dealing with that variability. Then we
made all four compete on **the same test**: 2,000 realistic operating situations that none of
them had seen before, with the test rules fixed in advance so no one could cheat.

**Three findings:**

1. **Accounting for uncertainty is almost free.** Three of the four methods cost practically
   the same (within 0.9 % of each other). You don't have to pay extra to design carefully.
2. **There is a clear winner: the "distributional" method (WDRO).** It costs the same as the
   other good ones, but it produces the **most predictable** cost (the one that varies least
   from one situation to the next). In engineering, predictability is worth a lot.
3. **The big surprise: the "worst-case" method (RO) is the worst.** In theory it should be the
   safest, but the way it is usually built it costs **almost 2.5 times more** and is also the
   **least reliable**. Its obsession with protecting against the worst backfires.

**Take-home message:** account for uncertainty (it costs no more), prefer the distributional
method for the final design, and **be skeptical of "worst-case protection" that is really only
approximate**.

---

## 2 · What is a shell-and-tube heat exchanger?

A **heat exchanger** is any device that moves heat from a hot fluid to a cold one **without
letting them mix**. A car radiator and the coil behind a refrigerator are heat exchangers.

The most common type in industry is the **shell-and-tube** heat exchanger (**STHE** for short).
To picture it:

- Take a **large metal cylinder**, like a long barrel lying on its side. That is the **shell**.
- Inside it, place **hundreds or thousands of thin tubes** side by side, like a bundle of
  drinking straws. That bundle is the **tube bundle**.
- One fluid flows **inside the tubes** (the "tube side"). The other fluid flows **outside the
  tubes, but inside the shell** (the "shell side").
- Heat from the hot fluid passes **through the metal wall of the tubes** and into the cold
  fluid. They never touch or mix; they only trade heat through the metal.

So that the shell-side fluid does not just run straight through (which would cool it very
little), we add **plates placed across the flow, called baffles**. They force the fluid to
**zig-zag** and brush past more tubes — just as a river slows down and touches more of its
banks when you drop stones in it. That way more heat is transferred.

### Our specific case

- Through the **shell** flows **hot methanol** (an industrial alcohol). It comes in at **95 °C**
  and must leave at **40 °C**. In other words, it has to be **cooled down**.
- Through the **tubes** flows **cold seawater**, which comes in at **25 °C** and carries the
  heat away.
- The amount of heat the device must remove is about **3.87 megawatts** (MW). To make that
  tangible: it is like the heat of **about 2,600 household electric stoves** running at once. We
  call this required amount of heat the **heat duty**, and we write it **Q**.

Some words that will come up later, in plain terms:

| Term | What it is, in simple terms |
|---|---|
| **Tube passes** | How many times the fluid travels the length of the device before leaving (1, 2, or 4 times here). |
| **Pitch** | How far apart the tubes are spaced from each other. |
| **Layout** | The pattern the tubes are arranged in (triangular, square…). |
| **Fouling** | The layer of grime that builds up over time on the walls and blocks the heat, like scale inside a pipe. |

---

## 3 · What does "optimizing the design" mean?

To **design** the exchanger is to decide what it looks like inside: how wide the shell is, which
tubes to use, how many, how to arrange them, how to space the baffles, and so on. In this work
there are **11 design choices** (engineers call them *design variables* and group them into a
list we call **x**).

To **optimize** is to choose those 11 things so the device **costs as little as possible**,
without breaking any engineering rule.

### The cost we want to minimize

We are not just after the cheapest device to buy. We want the cheapest **over its whole working
life**. This is called the **total annualized cost** (**TAC**), and it has two parts:

1. **What the equipment costs** (to buy and build), spread out year by year over the ~20 years
   it will last. It is like the "yearly payment" on a loan.
2. **What the electricity costs** to **pump** the two fluids through the device, every year.
   Pushing liquid through thin tubes uses energy.

Here is the central trade-off, and it is very intuitive:

> A **larger** device lets the fluids through easily (it uses little pumping electricity) **but
> is expensive to buy**. A **more compact** device is cheap to buy **but needs harder pumping**
> (more electricity). The best design is the sweet spot between those two extremes.

### The rules you cannot break (constraints)

A good design is not just cheap: it has to **work**. It must meet these conditions, called
**constraints**, no matter what:

- **Cool enough:** deliver the required heat duty (**Q ≥ 3.87 MW**). If it cools too little, it
  is useless.
- **Don't resist the flow too much:** the "pressure drop" on each side must be **≤ 70 kPa**.
  (The *pressure drop* is how much push is lost moving the fluid through; more drop = more
  electricity and more mechanical strain.)
- **Keep the water speed in a healthy range:** between **0.5 and 3 meters per second**. Too slow
  and it fouls; too fast and it wears the tubes away.
- **Don't be absurdly long:** the device cannot be more than 15 times longer than it is wide
  (**L/D ≤ 15**), for practical installation reasons.

A design that meets **all** the rules is called **feasible**. If it breaks **even one**, it is
**infeasible**.

> *Technical note, for completeness:* the physics of the device is computed with two standard
> engineering methods: **Bell–Delaware** for the shell side and **Sieder–Tate** for the tube
> side. You don't need to understand them to follow along; they are the accepted "calculators"
> that tell you how much heat passes and how much pressure is lost.

---

## 4 · Why does uncertainty matter? (the heart of the work)

This is the single most important idea in the whole poster.

Classic design fixes **one single set of conditions** — the "nominal" ones, the on-paper ones —
and optimizes for them. **The problem is that reality never holds still.** In a real plant:

- the **flow rate** (how much fluid arrives) goes up and down because of what happens upstream;
- the **inlet temperatures** drift a little;
- the **fouling** slowly builds up between cleanings.

We model **6 things we don't control and that vary** (engineers call them *uncertain
parameters* and group them into a list called **ξ**, the Greek letter "xi"): the **2 inlet
temperatures**, the **2 flow rates**, and the **2 fouling resistances** (one on each side).

### The key picture: the cloud of scenarios

Imagine a map. The **nominal point** — the on-paper conditions — is **one single blue dot** that
lands **comfortably inside the safe zone** (the area where the design meets all the rules).

But reality is not that dot: it is **a cloud of dots** around it, because conditions vary. And
here is the punch:

> **About 17 % of that cloud lands outside the safe zone.** In other words, the design that
> looked perfect **fails roughly 1 time out of 6** whenever the plant drifts away from nominal.
> And it fails **silently**: no one notices on paper, only in real operation.

The traditional "fix" is to **oversize just in case**: make the device bigger "to be safe,"
using a **safety factor** picked by gut feeling. It half-works, but it **spends extra money**
without really knowing how much margin you need.

**The question of the work is:** is there a *principled* way — not a gut-feeling way — to design
while accounting for that variability? And if there are several, **which one is worth using?**

---

## 5 · The four ways to design (with luggage analogies)

There are **three big families** of methods for making decisions when the future is uncertain.
We tested all three (the first one in two versions, giving **four methods** in total). The best
way to understand them is an analogy: **packing a suitcase for a trip without knowing exactly
what the weather will be.**

### DET — Deterministic (the baseline)
**What it does:** designs only for the nominal point, as if the future were known for sure.
**Analogy:** you pack assuming the weather will be **exactly** the average forecast. If you're
right, great; if not, you get wet.
**What it's for:** it's the reference, what almost everyone does today. Very fast, but **no
guarantees** when reality changes.

### SAA — Sample-average approximation (family: stochastic programming)
**What it does:** instead of a single point, it takes **many possible scenarios** with their
probabilities, and picks the design that costs the least **on average** across all of them.
**Analogy:** you look at the weather over **many typical days** and pack so you do well **on
average**.
**What it's for:** the sensible, cheap everyday option. It only needs a representative sample of
how things vary.

### RO — "Box" robust optimization (family: robust / worst-case optimization)
**What it does:** it **ignores probabilities entirely.** It draws a **box** with the limits of
each parameter and protects against **the worst imaginable corner** of that box.
**Analogy:** you pack for **the worst possible weather** within reason: coat, umbrella,
sunscreen, boots… everything at once, just in case.
**The problem:** it sounds safe, but it can lead to **massive oversizing** — lugging a huge
suitcase you don't need. (We'll see that here, on top of that, its "worst case" is only
*approximate*, and that ruins it.)

### WDRO — Wasserstein distributionally robust (family: DRO)
**What it does:** the elegant middle ground. It **trusts the data**, but recognizes that your
record of the past **is good but not perfect**. It allows the "truth" to be anywhere **within a
margin** around what you observed, and protects against **the worst possibility inside that
margin** — without going to RO's paranoid extreme.
**Analogy:** you know your record of past weather is reliable but not flawless, so you cover
yourself against **plausible** variations of that record, without packing for the apocalypse.
**What it's for:** when the data are limited or the future may "move," and you want a
**predictable cost**.

> **The trick that makes WDRO computable:** in practice, WDRO boils down to a simple calculation:
> minimize **the average cost + a penalty for how much the cost varies**. That penalty is tuned
> with a number, **ρ = 0.72**, that acts like a dial: higher means more cautious. It's the
> tractable way of saying "I want it to cost little *and* be stable."

---

## 6 · How did we compare them fairly? (the test)

There's no point in declaring a winner if the test is rigged. The credibility of the work rests
**entirely here**. We set the rules **before seeing a single result**, so we couldn't pick and
choose what looked good.

1. **We generate scenarios with good sampling.** We use *Latin hypercube sampling* (LHS), a
   technique that **covers the range of possibilities evenly**, instead of leaving gaps the way
   pure chance would. (Imagine spreading 500 points across a field so they cover it uniformly,
   instead of tossing them in the air and letting them clump.)

2. **We split the data into three piles**, as in any serious exam:
   - **Training (500 scenarios):** these are used to *tune* each method. They are the "study
     material."
   - **Test (2,000 new scenarios):** these are used to *grade*. They were never seen before — it
     is the real exam. This is called evaluating **out-of-sample**, and it avoids the
     self-deception of grading yourself with your own notes.
   - **Stress (10 extreme scenarios):** the harshest conditions imaginable, to see who holds up
     under the hard hits.

3. **We test what happens if reality "moves."** With a dial called **drift (κ)** — from 0 to 1 —
   we deliberately push the test conditions away from the training ones (higher flows, lower
   temperatures, etc.). This measures how well each method holds up **when the world changes**
   after you have designed.

4. **We compare with honest statistics.** To say "this method is better than that one" we use
   **paired statistical tests** (each design is judged on **the same** 2,000 scenarios, so the
   comparison is clean): the **Wilcoxon** test for cost and the **McNemar** test for whether it
   meets the rules. And because we make **6 comparisons**, we apply the **Holm correction**,
   which prevents claiming false victories from running many tests at once.

---

## 7 · What we found (the results)

### The table, in plain terms

| Method | Cost ($/year) | Cost variability (CV) | Reliability (% that meets the rules) | Compute time |
|---|---|---|---|---|
| **DET** (deterministic) | 14,306 | 1.49 % | 82.8 % | 0.1 s |
| **SAA** (average) | 14,357 | 1.52 % | 82.8 % | 3.6 s |
| **WDRO** (distributional) | **14,240** | **0.90 %** | **83.1 %** | ~7,920 s* |
| **RO** (worst-case) | **35,546** | 2.49 % | **79.0 %** | 14.8 s |

\* WDRO's time is highly variable: typically ~36 minutes, but 3 out of 10 runs took more than
**4 hours**. The average is reported.

**How to read the columns:**
- **Cost:** lower is better.
- **Cost variability (CV, the *coefficient of variation*):** measures **how predictable** the
  cost is. It's the "swing" of the cost relative to its size. **Lower = more predictable.** A low
  CV means you know fairly well how much you'll spend.
- **Reliability (feasibility):** out of the 2,000 test scenarios, in **what percentage** the
  design met all the rules. Higher is better.

### The three big takeaways

1. **DET, SAA, and WDRO cost almost the same** (within **0.9 %**). Translation: **accounting for
   uncertainty does not cost you more money.** Doing it properly is essentially free.

2. **WDRO is the best overall.** It has the **lowest average cost** *and* the **lowest
   variability** (CV 0.90 %, versus ~1.5 % for the others). Same price, but **much more
   predictable**. For a design you build once and run for 20 years, that predictability is
   insurance worth having.

3. **RO is the big letdown.** It costs **148 % more** (more than double) and, on top of that, is
   the **least reliable** (only 79 % compliance, versus ~83 % for the others). The method that
   **should** be the safest turned out worst on both counts.

### Why does anything fail, and why does RO fail so badly?

- **Where the 17 % of failures comes from (common to all):** it is almost always **one single
  rule**, the one about cooling enough (the heat duty). The design just barely meets it at
  nominal conditions, so any bad combination — low flow, harsh temperatures, heavy fouling —
  leaves it **a bit short**. This is not a flaw of the methods; it's the price of designing right
  at the nominal limit on purpose (to compare fairly).

- **Why RO sinks:** its "worst case" **is not a true worst case, but an approximate one** (it
  only checks the 64 corners of the box, not the whole interior). That logic pushed it to make
  **the shell as large as possible** and the **tubes extremely long**. The paradoxical result:
  the giant device **transfers heat worse** (its heat-transfer efficiency collapses) and, because
  of the very long tubes, **breaks the pressure limit** on the tube side. Its attempt to armor
  itself backfired.

> **The deeper lesson, and it matters:** "worst-case" protection that is only *approximate*
> **guarantees you nothing**. It can give you a **false sense** of safety while actually handing
> you the most expensive and least reliable design. It is not enough to *say* you protect against
> the worst: you have to **solve that worst case correctly**, and that is mathematically hard.

### One honest statistical subtlety

Among the three good designs (DET, SAA, WDRO), the cost differences are **tiny (under 0.8 %)**,
but **extremely consistent**: WDRO is almost always the cheapest, scenario by scenario. And on
reliability, those three are statistically **tied**: we do **not** claim WDRO is more reliable
than the deterministic one. The only firm reliability result is that **RO is clearly worse than
the other three**. We say exactly what the data support, no more and no less.

---

## 8 · The practical recommendations (which method to use)

Summarized in four cards, depending on what you need it for:

- **DET (deterministic):** use it to **explore fast** and make prototypes. It gives results in
  under a second, but it **guarantees nothing** when conditions change.
- **SAA (average):** the sensible **default** for everyday work. Cheap, fast, and principled; it
  only needs a representative sample of how conditions vary.
- **WDRO (distributional):** the **choice for the final design**, especially when data are
  limited, the future may change, or reliability is required. It gives the most predictable cost.
  Its only downside: **it is slow and its time is unpredictable** (minutes to hours).
- **RO (worst-case, approximate):** **not recommended here.** The "worst-case" paradigm is still
  appealing in theory for critical equipment, but **only if you solve the worst case in a
  certified way**, not an approximate one. Without that, it can perform worse than the other
  options.

---

## 9 · Being honest about the study's limits

A good piece of work also states what it does **not** prove:

- **It is a single case study** (one methanol cooler). The ordering of the results — especially
  WDRO beating RO — **might not repeat** with other fluids or conditions. The solid contribution
  is the **fair, reproducible way of comparing**, not a universal law.
- **RO and WDRO were solved approximately** (heuristically), not in a certified way. So RO's bad
  result is **a property of *this* approximate implementation**, not a verdict against the
  worst-case paradigm itself.
- **The stress set is small** (10 scenarios), so those figures are **indicative**.

**What comes next (future work):** (1) a **certified** version of RO — one that solves its worst
case for real — to see if it can be rehabilitated; and (2) a **second case study**, with other
fluids, to see how far these conclusions travel.

---

## 10 · Mini-glossary (one line each)

| Term | In plain words |
|---|---|
| **STHE** | Shell-and-tube heat exchanger: the device that cools one fluid with another without mixing them. |
| **Shell / tubes** | The outer cylinder and the bundle of thin inner tubes; each fluid flows on one side. |
| **Baffles** | Plates that make the fluid zig-zag so it cools better. |
| **Heat duty (Q)** | The heat the device is required to remove (here, 3.87 MW). |
| **Fouling** | Grime that builds up and blocks the heat, like scale in a pipe. |
| **Pressure drop** | The push lost while moving the fluid through; more drop = more pumping electricity. |
| **TAC** | Total annualized cost = price of the equipment (spread per year) + pumping electricity. This is what we minimize. |
| **Design variable (x)** | What the engineer **decides** (the 11 geometry choices). |
| **Uncertain parameter (ξ)** | What the engineer **doesn't control** and that varies (the 6: 2 temperatures, 2 flows, 2 fouling resistances). |
| **Feasible / infeasible** | A design either meets (feasible) or breaks (infeasible) the rules in a given scenario. |
| **Scenario** | One concrete combination of the 6 uncertain parameters: one possible operating situation. |
| **DET** | Designs for a single fixed point. Fast, no guarantees. |
| **SAA** | Designs for the **average** of many scenarios. Sensible and cheap. |
| **RO** | Designs for the **worst case** of a box, ignoring probabilities. Here, approximate, and that's why it fails. |
| **WDRO** | Designs trusting the data but covering against a plausible **margin** of error. The winner. |
| **CV (coefficient of variation)** | How much the cost varies relative to its size. Lower = more predictable. |
| **Out-of-sample** | Grading with new scenarios, never used to design. Avoids self-deception. |
| **LHS** | Sampling that covers the possibilities evenly, leaving no gaps. |
| **Drift (κ)** | A dial that deliberately pushes reality away from what was trained, to test resilience. |
| **Wilcoxon / McNemar / Holm** | Statistical tests to compare cost and rule-compliance honestly. |

---

*Plain-language explainer based on the ESCAPE 2026 poster and paper. The figures match the
study's results table (evaluation over 2,000 out-of-sample scenarios).*
