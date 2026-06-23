# -*- coding: utf-8 -*-
import re, io

PATH = "unpacked/word/document.xml"
s = open(PATH, encoding="utf-8").read()

LDQ = "&#x201C;"   # left double quote
RDQ = "&#x201D;"   # right double quote
EM  = "—"     # em dash

ops = []  # (label, fn) ; fn returns new string ; we assert via count helpers

def repl(label, old, new, count=1):
    n = s_count(old)
    assert n == count, f"[{label}] expected {count} got {n}"
    return label, old, new

def s_count(sub):
    return s.count(sub)

# ----- XML building helpers (match existing styles) -----
def para(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:spacing w:after="160" w:before="0" w:line="276"/>\n'
            '        <w:jc w:val="both"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:sz w:val="23"/>\n'
            '          <w:szCs w:val="23"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

def h1(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:pStyle w:val="Heading1"/>\n'
            '        <w:pBdr>\n'
            '          <w:bottom w:val="single" w:color="8B6914" w:sz="8" w:space="4"/>\n'
            '        </w:pBdr>\n'
            '        <w:spacing w:after="200" w:before="480"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:color w:val="7A1F1F"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

def h2(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:pStyle w:val="Heading2"/>\n'
            '        <w:spacing w:after="140" w:before="320"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:color w:val="1F2A44"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

def h3(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:pStyle w:val="Heading3"/>\n'
            '        <w:spacing w:after="100" w:before="220"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:i/>\n'
            '          <w:iCs/>\n'
            '          <w:color w:val="8B6914"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

def ref(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:pBdr>\n'
            '          <w:left w:val="single" w:color="8B6914" w:sz="12" w:space="8"/>\n'
            '        </w:pBdr>\n'
            '        <w:spacing w:after="180" w:before="0"/>\n'
            '        <w:ind w:left="360"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:i/>\n'
            '          <w:iCs/>\n'
            '          <w:color w:val="1F2A44"/>\n'
            '          <w:sz w:val="22"/>\n'
            '          <w:szCs w:val="22"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

def contents_entry(text):
    return ('    <w:p>\n'
            '      <w:pPr>\n'
            '        <w:spacing w:after="100"/>\n'
            '      </w:pPr>\n'
            '      <w:r>\n'
            '        <w:rPr>\n'
            '          <w:color w:val="1F2A44"/>\n'
            '          <w:sz w:val="24"/>\n'
            '          <w:szCs w:val="24"/>\n'
            '        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n'
            '      </w:r>\n'
            '    </w:p>\n')

# =====================================================================
# 1) CORRECTIONS & GENERALIZATIONS (regex-based, robust)
# =====================================================================

# Fix garbled Greek in Cyril formula (two occurrences): τοϱ Θεού -> τοῦ Θεοῦ
bad_greek = "τοϱ Θεού"   # τοϱ Θεού
good_greek = "τοῦ Θεοῦ"  # τοῦ Θεοῦ
assert s.count(bad_greek) == 2, s.count(bad_greek)
s = s.replace(bad_greek, good_greek)

# Romans 9:5 — de-reference the slide "arrow" and add transliteration
old = ("The arrow drawn in the notes from this verse to " + LDQ + "Trinity" + RDQ +
       " is therefore well placed: Romans 9:5")
new = ("The link this verse forges between the title " + LDQ + "God" + RDQ +
       " and the incarnate Christ is decisive: Romans 9:5")
assert s.count(old) == 1
s = s.replace(old, new)

old = ("the same union of natures the Coptic Church confesses as μία "
       "φύσις τοῦ Θεοῦ "
       "Λόγου σεσαρκωμένη, "
       + LDQ + "the one incarnate nature of God the Word," + RDQ + " the Cyrilline formula at the heart of our Christology.")
new = ("the same union of natures the Coptic Church confesses as μία "
       "φύσις τοῦ Θεοῦ "
       "Λόγου σεσαρκωμένη "
       "(mia physis tou Theou Logou sesarkomene), " + LDQ + "the one incarnate nature of God the Word," + RDQ +
       " the Cyrilline formula at the heart of her Christology.")
assert s.count(old) == 1, "romans cyril tail"
s = s.replace(old, new)

# 1 Tim 3:16 — remove personal ref + fix nomina sacra detail
old = ("A textual note belongs here, since Lang's interest in canon and text-critical "
       "questions makes it relevant: the earliest")
new = ("A textual note belongs here, and it bears directly on how the verse should be read: the earliest")
assert s.count(old) == 1
s = s.replace(old, new)

# nomina sacra parenthetical (wildcard the abbreviation glyphs)
pat = re.compile(r"differing from θεός by only a single stroke in uncial script \(.*?the nomina sacra\)", re.S)
m = pat.search(s)
assert m, "nomina sacra not found"
new = ("differing from θεός by only a single stroke in uncial script: in the "
       "nomina sacra (the scribal abbreviations of sacred names), " + LDQ + "God" + RDQ +
       " was written ΘС with an overbar, separated from the ordinary relative pronoun "
       "ΟС (" + LDQ + "who" + RDQ + ") only by the cross-stroke inside the theta and the line above")
s = s[:m.start()] + new + s[m.end():]

# Section V intro — remove "in Lang's experience"
old = "A frequent objection " + EM + " raised often, in Lang's experience, by Jehovah's Witnesses"
new = "A frequent objection " + EM + " raised often by Jehovah's Witnesses"
assert s.count(old) == 1
s = s.replace(old, new)

# Section IX (Objections) intro — remove Lang's debates
old = ("it is worth briefly anticipating the texts most often raised in reply, since Lang's "
       "debates with Jehovah's Witnesses and other non-trinitarian interlocutors will almost "
       "certainly bring them forward.")
new = ("it is worth briefly anticipating the texts most often raised in reply by Jehovah's "
       "Witnesses, Unitarians, and other non-trinitarian interlocutors.")
assert s.count(old) == 1
s = s.replace(old, new)

# ---- De-reference physical images / slide (won't exist on the website) ----
old = "The catechism notes place Romans 9:5 at the head of the study, and rightly so:"
new = "This study places Romans 9:5 at its head, and rightly so:"
assert s.count(old) == 1; s = s.replace(old, new)

old = "The catechism notes therefore turn from confession to action:"
new = "The study therefore turns from confession to action:"
assert s.count(old) == 1; s = s.replace(old, new)

old = "a particular divine work that the catechism notes link to creation:"
new = "a particular divine work the prophets link to creation:"
assert s.count(old) == 1; s = s.replace(old, new)

old = "The accompanying catechism slide (reproduced and corrected below in table form) sets out a classic instructional device:"
new = "The table below sets out a classic instructional device:"
assert s.count(old) == 1; s = s.replace(old, new)

old = ("The second image attached to the catechism notes records a well-known apologetic "
       "statistic: a tally of explicit New Testament quotations")
new = ("A second, much-cited apologetic statistic records a tally of explicit New Testament quotations")
assert s.count(old) == 1; s = s.replace(old, new)

old = "the version reflected in the photographed table " + EM
new = "the version reflected in the table below " + EM
assert s.count(old) == 1; s = s.replace(old, new)

# =====================================================================
# 2) DEEPEN EXISTING SECTIONS (verbatim patristic sources)
# =====================================================================

# Tertullian precision in the Fathers section
old = ("Tertullian alone, writing circa 200 A.D., already employs the Latin term trinitas and "
       "treats the full deity of the Son as settled Christian teaching; Origen, writing in the "
       "early third century, comments verse by verse on nearly the whole New Testament, including "
       "its most exalted Christological texts.")
new = ("Tertullian, writing at the turn of the third century, already treats the full deity of the "
       "Son as settled Christian teaching, and in his Against Praxeas (c. 213) supplies Latin "
       "theology its first technical vocabulary for the doctrine " + EM + " trinitas "
       "(" + LDQ + "Trinity" + RDQ + "), and the formula tres personae, una substantia "
       "(" + LDQ + "three Persons, one substance" + RDQ + "). Origen, writing in the early third "
       "century, comments verse by verse on nearly the whole New Testament, including its most "
       "exalted Christological texts.")
assert s.count(old) == 1; s = s.replace(old, new)

# Ignatius — add verbatim quotations with letter citations
old = ("Writing within a decade or two of the death of the last apostle, Ignatius repeatedly and "
       "without apparent controversy speaks of " + LDQ + "our God, Jesus Christ" + RDQ + " in his "
       "letters to Ephesus, Rome, and Smyrna, defends the reality of Christ's flesh against early "
       "docetism, and refers to the Eucharist as the flesh of the Savior " + EM + " testimony that "
       "the divinity, true humanity, and Real Presence at the heart of this study were apostolic-era "
       "convictions, not later philosophical accretions.")
new = ("Writing within a decade or two of the death of the last apostle, on his way to martyrdom in "
       "Rome, Ignatius speaks of the deity of Christ not as a thesis to be argued but as a settled "
       "commonplace of the faith he is about to die for. He greets the Ephesians in the name of "
       + LDQ + "Jesus Christ our God" + RDQ + " (Ephesians, salutation) and tells them that "
       + LDQ + "our God, Jesus the Christ, was conceived by Mary" + RDQ + " (Ephesians 18:2); he "
       "writes that " + LDQ + "our God Jesus Christ is now more manifest" + RDQ + " in the Father "
       "(Romans 3:3); and he opens his letter to Smyrna by glorifying " + LDQ + "Jesus Christ, the "
       "God who has thus given you wisdom" + RDQ + " (Smyrnaeans 1:1). In the same breath he defends "
       "the reality of Christ's flesh against the docetists and calls the Eucharist " + LDQ + "the "
       "flesh of our Savior Jesus Christ" + RDQ + " (Smyrnaeans 7:1) " + EM + " testimony that the "
       "divinity, true humanity, and Real Presence at the heart of this study were apostolic-era "
       "convictions, not later philosophical accretions.")
assert s.count(old) == 1; s = s.replace(old, new)

# Athanasius — add the Greek of the famous formula
old = ("His On the Incarnation remains the classical Alexandrian statement of why Christ's full "
       "divinity is not a peripheral dogma but the condition of human salvation.")
new = ("His On the Incarnation gives the exchange its most quoted form: Αὐτὸς "
       "γὰρ ἐνηνθρώπησεν, "
       "ἵνα ἡμεῖς θεοποιηθῶμεν "
       "(autos gar enenthropesen, hina hemeis theopoiethomen) " + EM + " " + LDQ + "He became man "
       "that we might be made God" + RDQ + " (On the Incarnation 54). The whole treatise remains the "
       "classical Alexandrian statement of why Christ's full divinity is not a peripheral dogma but "
       "the very condition of human salvation.")
assert s.count(old) == 1; s = s.replace(old, new)

# Cyril — fix garbled grammar "Cyril's twenty-fourth Pope of Alexandria's defense"
old = ("Cyril's twenty-fourth Pope of Alexandria's defense of the title Theotokos "
       "(" + LDQ + "God-bearer" + RDQ + ") for the Virgin Mary against Nestorius was, at root,")
new = ("Cyril, twenty-fourth Pope of Alexandria, defended the title Theotokos "
       "(" + LDQ + "God-bearer" + RDQ + ") for the Virgin Mary against Nestorius; this was, at root,")
assert s.count(old) == 1; s = s.replace(old, new)

# Introduction — note the two added witnesses
old = ("Wherever it sharpens the argument, the underlying Greek or Hebrew vocabulary is supplied, "
       "since much of the force of these texts rests on a single verb, a definite article, or a "
       "deliberate echo of the Divine Name.")
new = old + (" To these four lines the present expansion adds two further witnesses the Fathers "
       "prized: the pre-incarnate appearances of the Son under the Old Covenant, and the worship "
       "which Christ " + EM + " alone among all who are not God " + EM + " consistently receives and "
       "never once refuses.")
assert s.count(old) == 1; s = s.replace(old, new)

open(PATH, "w", encoding="utf-8").write(s)
print("PHASE 1-2 OK. Length now:", len(s))
