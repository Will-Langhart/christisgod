# -*- coding: utf-8 -*-
import re
PATH = "unpacked_final/word/document.xml"
s = open(PATH, encoding="utf-8").read()
LDQ, RDQ, EM = "&#x201C;", "&#x201D;", "—"

def need(old, count=1):
    n = s.count(old)
    assert n == count, f"expected {count} got {n}: {old[:60]!r}"

def sub(old, new, count=1):
    global s
    need(old, count)
    s = s.replace(old, new)

# ---------- XML builders (match existing styles) ----------
def para(text):
    return ('    <w:p>\n      <w:pPr>\n        <w:spacing w:after="160" w:before="0" w:line="276"/>\n'
            '        <w:jc w:val="both"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
            '          <w:sz w:val="23"/>\n          <w:szCs w:val="23"/>\n        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def h1(text):
    return ('    <w:p>\n      <w:pPr>\n        <w:pStyle w:val="Heading1"/>\n        <w:pBdr>\n'
            '          <w:bottom w:val="single" w:color="8B6914" w:sz="8" w:space="4"/>\n        </w:pBdr>\n'
            '        <w:spacing w:after="200" w:before="480"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
            '          <w:color w:val="7A1F1F"/>\n        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def h2(text):
    return ('    <w:p>\n      <w:pPr>\n        <w:pStyle w:val="Heading2"/>\n'
            '        <w:spacing w:after="140" w:before="320"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
            '          <w:color w:val="1F2A44"/>\n        </w:rPr>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def ref(text):
    return ('    <w:p>\n      <w:pPr>\n        <w:pBdr>\n'
            '          <w:left w:val="single" w:color="8B6914" w:sz="12" w:space="8"/>\n        </w:pBdr>\n'
            '        <w:spacing w:after="180" w:before="0"/>\n        <w:ind w:left="360"/>\n      </w:pPr>\n'
            '      <w:r>\n        <w:rPr>\n          <w:i/>\n          <w:iCs/>\n'
            '          <w:color w:val="1F2A44"/>\n          <w:sz w:val="22"/>\n          <w:szCs w:val="22"/>\n'
            f'        </w:rPr>\n        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def note(label, text):
    # Two-layer "technical note": shaded, bordered box with a small-caps red label
    return ('    <w:p>\n      <w:pPr>\n        <w:pBdr>\n'
            '          <w:top w:val="single" w:color="D8CBA0" w:sz="4" w:space="6"/>\n'
            '          <w:left w:val="single" w:color="D8CBA0" w:sz="4" w:space="6"/>\n'
            '          <w:bottom w:val="single" w:color="D8CBA0" w:sz="4" w:space="6"/>\n'
            '          <w:right w:val="single" w:color="D8CBA0" w:sz="4" w:space="6"/>\n        </w:pBdr>\n'
            '        <w:shd w:val="clear" w:color="auto" w:fill="F6F1E3"/>\n'
            '        <w:spacing w:after="180" w:before="80" w:line="264"/>\n'
            '        <w:ind w:left="200" w:right="200"/>\n        <w:jc w:val="both"/>\n      </w:pPr>\n'
            '      <w:r>\n        <w:rPr>\n          <w:b/>\n          <w:bCs/>\n          <w:caps/>\n'
            '          <w:color w:val="7A1F1F"/>\n          <w:sz w:val="18"/>\n          <w:szCs w:val="18"/>\n'
            f'        </w:rPr>\n        <w:t xml:space="preserve">{label}  </w:t>\n      </w:r>\n'
            '      <w:r>\n        <w:rPr>\n          <w:sz w:val="21"/>\n          <w:szCs w:val="21"/>\n'
            f'        </w:rPr>\n        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def contents_entry(text):
    return ('    <w:p>\n      <w:pPr>\n        <w:spacing w:after="80"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
            '          <w:color w:val="1F2A44"/>\n          <w:sz w:val="22"/>\n          <w:szCs w:val="22"/>\n'
            f'        </w:rPr>\n        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def insert_before_para(marker, block):
    global s
    pos = s.find(marker)
    assert pos != -1, f"marker not found: {marker[:50]!r}"
    assert s.find(marker, pos+1) == -1, f"marker not unique: {marker[:50]!r}"
    p = s.rfind('    <w:p>\n', 0, pos)
    assert p != -1
    s = s[:p] + block + s[p:]

# =====================================================================
# 1) TITLE BLOCK
# =====================================================================
sub("<w:t xml:space=\"preserve\">Catechetical Notes Expanded for Study, Devotion, and Apologetics</w:t>",
    "<w:t xml:space=\"preserve\">A Scriptural, Historical, and Grammatical Case for the Deity of Jesus Christ</w:t>")

# Drop the "Coptic Orthodox Catechism" line (whole paragraph)
coptic_subtitle = ('    <w:p>\n      <w:pPr>\n        <w:spacing w:after="40"/>\n        <w:jc w:val="center"/>\n      </w:pPr>\n'
                   '      <w:r>\n        <w:rPr>\n          <w:i/>\n          <w:iCs/>\n          <w:color w:val="595959"/>\n'
                   '          <w:sz w:val="22"/>\n          <w:szCs w:val="22"/>\n        </w:rPr>\n'
                   '        <w:t xml:space="preserve">Coptic Orthodox Catechism</w:t>\n      </w:r>\n    </w:p>\n')
sub(coptic_subtitle, "")

sub("<w:t xml:space=\"preserve\">Notes dated 20 June 2026</w:t>",
    "<w:t xml:space=\"preserve\">2026</w:t>")

# Swap the theosis-flavored Athanasius epigraph for Colossians 2:9
sub("<w:t xml:space=\"preserve\">The Word became flesh, that we might learn from a man how a man may become God.</w:t>",
    "<w:t xml:space=\"preserve\">For in him dwelleth all the fulness of the Godhead bodily.</w:t>")
sub("<w:t xml:space=\"preserve\">  " + EM + " St. Athanasius the Apostolic, On the Incarnation</w:t>",
    "<w:t xml:space=\"preserve\">  " + EM + " Colossians 2:9</w:t>")

# =====================================================================
# 2) INTRODUCTION — rewrite the three Coptic/theosis paragraphs
# =====================================================================
intro1_old = "The confession that Jesus Christ is true God is not a peripheral doctrine"
need(intro1_old)  # sanity
sub("The confession that Jesus Christ is true God is not a peripheral doctrine that can be softened for the sake of comfort or rationalist convenience. It is the hinge on which the entire economy of salvation turns. If the Word who became flesh (John 1:14) is anything less than fully and unreservedly God, then the Cross saves no one, the Eucharist communicates nothing divine, and the goal of the Christian life " + EM + " theosis, our being conformed to the divine nature by grace (2 Peter 1:4) " + EM + " collapses into mere moral self-improvement. St. Athanasius the Apostolic, the great defender of Nicene faith and twentieth Pope of Alexandria, stated the logic of the Incarnation with the precision for which the Alexandrian school is famous: God became what we are, so that we might become what He is. This exchange only holds if the One who assumed our nature is Himself the uncreated, eternal God; otherwise human nature is not healed, but merely instructed by a very holy creature.",
    "The claim that Jesus of Nazareth is God is the most consequential assertion in the New Testament, and the one on which everything else depends. If it is false, then Christianity rests on a catastrophic misunderstanding: its earliest worshippers committed idolatry, and the Cross is merely the execution of a deluded teacher. If it is true, then in Jesus the eternal Creator entered His own creation, and every other question " + EM + " about salvation, prayer, worship, and the meaning of a human life " + EM + " is reframed around Him. There is no neutral middle ground on which He is merely a great moral teacher; a man who was not God but accepted worship, forgave sins against God, and claimed the Divine Name was not merely mistaken but blasphemous. The texts force a verdict. This study makes the case, from Scripture first and read in its original languages and its first-century setting, that the verdict the earliest Christians reached " + EM + " " + LDQ + "My Lord and my God" + RDQ + " (John 20:28) " + EM + " is the one the evidence compels.")

sub("These notes gather and expand a catechetical study on the Divinity of Christ along four converging lines of evidence that the Church has always set before doubters and seekers alike: first, the direct ascription of the title " + LDQ + "God" + RDQ + " to Jesus in the New Testament; second, His exercise of works and prerogatives that belong to God alone; third, His indirect but unmistakable self-disclosure, especially the " + LDQ + "I AM" + RDQ + " sayings, understood against the backdrop of first-century Jewish blasphemy law; and fourth, the witness of the early Church " + EM + " both in the sheer density of its earliest citations of the New Testament and in its mature articulation of Trinitarian theology. Wherever it sharpens the argument, the underlying Greek or Hebrew vocabulary is supplied, since much of the force of these texts rests on a single verb, a definite article, or a deliberate echo of the Divine Name.",
    "The argument proceeds along several converging lines, no one of which need stand alone but which together form a rope that cannot be cut by reinterpreting any single strand. We begin with the fierce monotheism of the world into which the claim was first spoken, for only against Israel's confession of one God does calling a man " + LDQ + "God" + RDQ + " register as either blasphemy or revelation. We then assemble the direct ascriptions of the title " + LDQ + "God" + RDQ + " to Jesus; the divine works and prerogatives He exercises in His own name; His pre-incarnate appearances in the Old Testament; His indirect but unmistakable self-disclosure, above all the " + LDQ + "I AM" + RDQ + " sayings; the worship He receives and never refuses; and the divine attributes " + EM + " omnipresence, eternity, the power to create and to judge " + EM + " that Scripture predicates of Him. We then show how early this confession is: not a fourth-century invention but the content of the first creeds and hymns the apostles already quote, confirmed by the manuscripts themselves and by the unbroken testimony of the earliest Church. Finally we answer the texts most often raised against the doctrine, and the most significant modern denial of it.")

sub("This is not an academic exercise conducted at arm's length from the soul. The Fathers insisted that correct confession of Christ (orthodoxia) and the path of repentance and ascetic struggle toward union with God (theosis) are inseparable; one cannot be united to a Christ one has misidentified. The data assembled below, therefore, serves a pastoral and doxological end as much as an apologetic one.",
    "Wherever the force of an argument rests on a single verb, a definite article, a grammatical construction, or a deliberate echo of the Divine Name, the underlying Greek or Hebrew is supplied. To keep the main argument readable, these technical observations are set apart in shaded notes: a reader can follow the case without them, or pause on them for the detail that makes the case airtight.")

# =====================================================================
# 3) ROMANS 9:5 — trim the Coptic miaphysite formula
# =====================================================================
s = re.sub(
    r"" + EM + " the same union of natures the Coptic Church confesses as .*?her Christology\\.",
    EM + " so that the one Christ is at once the man descended from Israel according to the flesh and the God who is over all.",
    s, count=1)
assert "Coptic Church confesses" not in s

# =====================================================================
# 4) CONCLUSION — rewrite the Coptic/sacramental close
# =====================================================================
sub("The data assembled here " + EM + " direct ascription, divine works, indirect-but-unmistakable self-disclosure, and the converging witness of the earliest Church " + EM + " does not exist to win debates for their own sake, although it is more than sufficient for that purpose. It exists because the identity of Jesus Christ determines whether the Christian life is, at its root, a moral philosophy offered by an exceptional teacher or an actual union with the living God, accomplished by God Himself taking flesh, suffering, dying, and rising in that same flesh. St. Paul's confession in Romans 9:5, with which this study began, and St. Thomas's confession in John 20:28, with which the Gospel of John brings its witness to its climax, are not merely correct propositions to be defended in argument. They are doorways into worship " + EM + " " + LDQ + "My Lord and my God" + RDQ + " " + EM + " and worship, sustained through the sacramental life of the Church, is the path along which " + LDQ + "we all, with open face beholding as in a glass the glory of the Lord, are changed into the same image from glory to glory, even as by the Spirit of the Lord" + RDQ + " (2 Corinthians 3:18). The confession that Christ is God is, finally, in service of the confession's own deepest purpose: that those who believe it might be united to the One they confess, and by grace become partakers of the divine nature He alone, as true God, was able to bestow.",
    "The evidence assembled here " + EM + " the monotheism the claim defied, the direct ascriptions of the title " + LDQ + "God" + RDQ + ", the divine works done in His own name, the appearances of the Son under the Old Covenant, the unmistakable self-disclosure, the worship He received and never refused, the divine attributes He bears, the antiquity of the confession, and the manuscripts that carry it " + EM + " converges on a single conclusion that no one strand could bear alone but that all of them together make inescapable: the man Jesus of Nazareth is the one God of Israel, come in the flesh. This is not, in the end, a proposition to be filed away once it has won an argument. The same Gospel that opens by calling the Word " + LDQ + "God" + RDQ + " (John 1:1) closes with a doubter on his knees before the risen Christ, saying the only thing left to say " + EM + " " + LDQ + "My Lord and my God" + RDQ + " (John 20:28) " + EM + " and hearing Jesus pronounce blessed all who would believe the same without having seen. The case for the deity of Christ exists to bring its reader to that same confession, and to the worship that is its only fitting response. For if Jesus is God, then He is not merely to be studied or admired, but adored.")

# Compact Case — drop the lone Coptic-leaning "Cyril" name
sub("Ignatius, Justin, Irenaeus, Tertullian, Athanasius, Cyril, and the Nicene fathers do not create a new Jesus.",
    "Ignatius, Justin, Irenaeus, Tertullian, Athanasius, and the Nicene fathers do not create a new Jesus.")

print("STAGE A (edits) OK; length:", len(s))
open(PATH, "w", encoding="utf-8").write(s)
