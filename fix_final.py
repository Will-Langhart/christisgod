# -*- coding: utf-8 -*-
PATH = "unpacked_final/word/document.xml"
s = open(PATH, encoding="utf-8").read()
LDQ, RDQ, EM = "&#x201C;", "&#x201D;", "—"

def sub(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"expected {count} got {n} for: {old[:50]!r}"
    s = s.replace(old, new)

# 1) Garbled Greek  τοϱ Θεού  ->  τοῦ Θεοῦ   (both Cyril-formula occurrences)
sub("τοϱ Θεού",
    "τοῦ Θεοῦ", count=2)

# 2) Romans 9:5 — drop the "arrow drawn in the notes" slide reference
sub("The arrow drawn in the notes from this verse to " + LDQ + "Trinity" + RDQ + " is therefore well placed: Romans 9:5",
    "The link this verse forges between the title " + LDQ + "God" + RDQ + " and the incarnate Christ is decisive: Romans 9:5")

# 2b) Add transliteration of the Cyrilline formula + third-person ("her") — ASCII anchor only
sub(", " + LDQ + "the one incarnate nature of God the Word," + RDQ + " the Cyrilline formula at the heart of our Christology.",
    " (mia physis tou Theou Logou sesarkomene), " + LDQ + "the one incarnate nature of God the Word," + RDQ + " the Cyrilline formula at the heart of her Christology.")

# 3) Romans intro — de-reference the slide
sub("The catechism notes place Romans 9:5 at the head of the study, and rightly so:",
    "This study places Romans 9:5 at its head, and rightly so:")

# 4) Divine Works intro — de-reference the slide
sub("The catechism notes therefore turn from confession to action:",
    "The study therefore turns from confession to action:")

# 5) Creator section — de-reference the slide
sub("a particular divine work that the catechism notes link to creation:",
    "a particular divine work the prophets link to creation:")

# 6) Early Church Fathers — remove "second image attached" + "photographed table"
sub("The second image attached to the catechism notes records a well-known apologetic statistic: a tally of explicit New Testament quotations",
    "A second, much-cited apologetic statistic records a tally of explicit New Testament quotations")
sub("the version reflected in the photographed table " + EM,
    "the version reflected in the table below " + EM)

open(PATH, "w", encoding="utf-8").write(s)
print("All corrections applied. Verification:")
for kw in ["τοϱ", "arrow drawn", "catechism notes", "photographed", "second image attached", "her Christology", "mia physis"]:
    print(f"  {kw!r}: {s.count(kw)}")
