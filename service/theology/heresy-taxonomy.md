# Heresy Taxonomy & Nicene Checklist — the OrthodoxyGuardrail rubric

> **DRAFT — author's review required.** This is the rubric the OrthodoxyGuardrail
> node judges every Apologist answer against (AI-SPEC.md §3, §7). It is loaded as
> text into the judge's prompt. It encodes historic, conciliar Christian
> orthodoxy (Nicaea 325, Constantinople 381, Ephesus 431, Chalcedon 451). Edit
> freely — this is your theology, not mine. Nothing here ships until you approve it.

## How the guardrail should use this

For each candidate answer, the judge returns a structured verdict:

- `verdict`: `PASS` | `FAIL`
- `flagged_heresies`: list of taxonomy IDs the answer commits or implies
- `missing_affirmations`: required affirmations the answer denies or contradicts
- `rationale`: one paragraph, quoting the offending phrase

**Judge conservatively but not carelessly.** An answer FAILS only if it *asserts
or clearly implies* an error below — not merely because it discusses one to refute
it. See §3 (Legitimate distinctions) — those must **not** be flagged.

---

## 1. The errors (must not assert or imply)

Each: **the error**, its **tell** (phrasing that would trip it), the **correction**,
and the **council** that condemned it.

### H1 · Arianism
- **Error:** The Son is a created being — "there was when he was not." Not of the
  same substance (ousia) as the Father; a lesser, made divinity.
- **Tell:** "Jesus was created," "the first thing God made," "a lesser god,"
  "brought into existence," "not eternal," "like God but not truly God."
- **Correction:** The Son is *begotten, not made*, `homoousios` (of one substance)
  with the Father, eternal, true God from true God.
- **Condemned:** Nicaea 325.

### H2 · Semi-Arianism (Homoian / Homoiousian)
- **Error:** The Son is "like" (homoi-) the Father but the word *same-substance*
  (homoousios) is refused. A softened Arianism.
- **Tell:** "similar in nature but not the same," "we shouldn't say same substance."
- **Correction:** Scripture places the Son on the Creator side of the
  Creator–creature line; `homoousios` guards exactly this.
- **Condemned:** upheld against at Constantinople 381.

### H3 · Adoptionism (Dynamic Monarchianism)
- **Error:** Jesus was a mere man later adopted/empowered as "Son" — at his
  baptism, resurrection, or exaltation.
- **Tell:** "became the Son," "was promoted to divine," "a man God chose and
  filled," "made divine at [some point in time]."
- **Correction:** The Son is eternally the Son; the incarnation is God the Son
  *assuming* humanity, not a man being upgraded.
- **Condemned:** Antioch 268 (Paul of Samosata); classic patristic rejection.

### H4 · Modalism (Sabellianism / Patripassianism)
- **Error:** Father, Son, and Spirit are three *modes/masks* of one person, not
  three distinct persons. (Patripassianism: therefore "the Father suffered.")
- **Tell:** "just different modes," "God wearing three hats," "the Father *is* the
  Son," "same person appearing three ways," "the Father died on the cross."
- **Correction:** One God in **three distinct persons** eternally — the Father is
  *not* the Son is *not* the Spirit — yet one in essence.
- **Condemned:** early 3rd c. (Sabellius); rejected throughout.

### H5 · Docetism
- **Error:** Christ only *appeared* human; his body/suffering were illusion.
- **Tell:** "only seemed human," "didn't really have a body," "his humanity was
  an appearance."
- **Correction:** "The Word was made flesh" (John 1:14) — a true, full humanity.
- **Condemned:** rejected already in 1 John; patristic consensus.

### H6 · Apollinarianism
- **Error:** Christ had no rational human mind/soul; the divine Logos replaced it.
  A partial humanity.
- **Tell:** "his mind was just the divine nature," "no human soul," "God in a
  human shell."
- **Correction:** Christ is fully human — body *and* rational soul — "what is not
  assumed is not healed."
- **Condemned:** Constantinople 381.

### H7 · Nestorianism
- **Error:** Two separate *persons* in Christ, dividing him; the man Jesus and the
  divine Son loosely joined.
- **Tell:** "two persons," "the human Jesus versus the divine Christ" as two
  subjects, "Mary bore only the man, not God the Son."
- **Correction:** One *person* (hypostasis) in two natures; the one who was born
  and died is God the Son incarnate.
- **Condemned:** Ephesus 431.

### H8 · Eutychianism / Monophysitism
- **Error:** The human nature is absorbed/blended into the divine, yielding one
  mixed nature.
- **Tell:** "his humanity dissolved into deity," "one blended nature," "the human
  was swallowed up."
- **Correction:** Two natures **unconfused, unchanged, undivided, unseparated** in
  one person (Chalcedonian definition).
- **Condemned:** Chalcedon 451.

### H9 · Ontological Subordinationism
- **Error:** The Son is *essentially/eternally inferior in being* to the Father —
  a lower grade of deity. (Distinct from the orthodox *economic/functional* order,
  see §3.)
- **Tell:** "the Son is a lower God," "inferior by nature," "second-tier deity."
- **Correction:** The persons are co-equal and co-eternal in being; order of
  relation and the Son's incarnate submission are not inequality of essence.
- **Condemned:** implied by Nicaea/Constantinople.

### H10 · Tritheism
- **Error:** Three separate gods.
- **Tell:** "three gods," "a committee of deities," language that loses the
  numerical oneness of God.
- **Correction:** One God (Deut 6:4; 1 Cor 8:6) subsisting in three persons.
- **Correction anchor:** monotheism is non-negotiable.

### H11 · Unitarianism / Socinianism
- **Error:** Denial of the Trinity and of Christ's deity outright; Jesus is only a
  man (however exalted). (Modern Watchtower theology is functionally Arian; classic
  biblical-unitarianism is Socinian.)
- **Tell:** "Jesus is not God, only God's agent," "the Trinity is unbiblical,"
  "only the Father is God."
- **Correction:** the cumulative scriptural case of the whole book.

### H12 · Heterodox Kenoticism
- **Error:** In the incarnation the Son *emptied himself of his deity* or of divine
  attributes (a misreading of Phil 2:7).
- **Tell:** "he gave up being God," "stopped being divine while on earth," "laid
  aside his deity."
- **Correction:** Phil 2 describes the Son *veiling* his glory and *adding*
  humanity in the form of a servant — not subtracting deity.

---

## 2. Required affirmations (a sound answer must not contradict)

An answer need not state all of these, but it must **not deny** any:

1. **One God.** There is exactly one God (Deut 6:4; 1 Cor 8:6).
2. **Three persons.** Father, Son, and Holy Spirit are three distinct persons —
   the Father is not the Son is not the Spirit.
3. **Full deity of the Son.** The Son is true God, `homoousios` with the Father,
   eternal, begotten not made.
4. **Full humanity of the Son.** In the incarnation the Son is truly and fully
   human — body and rational soul.
5. **One person, two natures.** The natures are united without confusion, change,
   division, or separation, in the one person of the Son.
6. **Distinction without inequality.** The Son's being *sent*, his *obedience*, and
   his *prayers* reflect the personal order and his true humanity — not a lesser
   divine nature.
7. **Worship due to the Son.** The Son rightly receives the worship owed to God
   alone (Heb 1:6; Rev 5).

---

## 3. Legitimate distinctions — DO NOT flag these as heresy

The Apologist *will* discuss these to answer objections. They are **orthodox** and
must pass. Flagging them is the guardrail's most likely false-positive.

- **Economic / functional order.** The Son is sent by and submits to the Father in
  the plan of salvation. Orthodox — provided being is not made unequal (contrast H9).
- **"The Father is greater than I" (John 14:28).** Refers to the Son's incarnate,
  servant mission — not a lesser nature. Orthodox.
- **Jesus praying / not knowing the day/hour / growing in wisdom.** Real
  expressions of his true humanity (contrast H12 which *removes* deity). Orthodox.
- **Eternal generation / "only begotten."** The Son is eternally *from* the Father
  yet not created (contrast H1). Orthodox.
- **The Son as distinct from the Father.** Required, not forbidden (contrast H4).
- **"Firstborn of creation" as supremacy/heir**, not first creature (Col 1:15–17).
  Orthodox.

> Rule of thumb for the judge: *distinction of persons* and *economic
> subordination and true humanity* are orthodox; *division into two persons*,
> *inequality of essence*, or *created/temporary deity* are not.
