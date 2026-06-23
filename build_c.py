# -*- coding: utf-8 -*-
import re
PATH = "unpacked_final/word/document.xml"
s = open(PATH, encoding="utf-8").read()
LDQ, RDQ, EM = "&#x201C;", "&#x201D;", "—"

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
def note(label, text):
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
def src(text):
    return ('    <w:p>\n      <w:r>\n'
            f'        <w:t xml:space="preserve">{text}</w:t>\n      </w:r>\n    </w:p>\n')

def insert_before_para(marker, block):
    global s
    pos = s.find(marker)
    assert pos != -1, f"marker not found: {marker[:50]!r}"
    assert s.find(marker, pos+1) == -1, f"marker not unique: {marker[:50]!r}"
    p = s.rfind('    <w:p>\n', 0, pos)
    assert p != -1
    s = s[:p] + block + s[p:]

# =====================================================================
# 9) ANTIQUITY subsections (before the Burgon paragraph)
# =====================================================================
antiquity = (
 para("A persistent popular myth holds that the divinity of Christ was invented in the fourth century " + EM + " voted into existence at the Council of Nicaea (325) under the Emperor Constantine, and unknown to the simpler faith of Jesus' first followers. The historical record runs flatly against it. The confession of Jesus as Lord and God is embedded in the very oldest material the New Testament contains, predating Paul's own letters, and it is everywhere assumed by the Christian writers of the century after the apostles. Nicaea did not create the doctrine; it defended one already ancient.")
 + h2("The Earliest Creeds and Hymns")
 + para("Paul's letters " + EM + " our earliest Christian documents, written c. AD 48" + EM + "60 " + EM + " repeatedly quote material older than themselves: confessions, hymns, and creeds already in circulation. The most famous is the Christ-hymn of Philippians 2:6" + EM + "11, widely judged a pre-Pauline composition Paul is citing. It says that Christ, " + LDQ + "being in the form of God (en morphe theou), thought it not robbery to be equal with God," + RDQ + " yet took " + LDQ + "the form of a servant," + RDQ + " and was so exalted that at " + LDQ + "the name of Jesus every knee should bow" + RDQ + " " + EM + " applying to Jesus the very words YHWH speaks in Isaiah 45:23. If Paul is quoting an existing hymn, then the worship of Jesus as the bearer of the divine Name was already being sung in the churches within a few years of the crucifixion.")
 + note("Background", "On a crucifixion date of AD 30" + EM + "33, with Philippians written c. AD 60 quoting an earlier hymn, the high Christology of Philippians 2 traces to within perhaps three to five years of the events " + EM + " far too early to be a slowly evolved legend or a later Hellenistic import. Other pre-Pauline formulae point the same way: the creed Paul says he " + LDQ + "received" + RDQ + " and " + LDQ + "delivered" + RDQ + " in 1 Corinthians 15:3" + EM + "7; the confession " + LDQ + "Jesus is Lord" + RDQ + " (Romans 10:9); and the Aramaic prayer Marana tha, " + LDQ + "Our Lord, come" + RDQ + " (1 Corinthians 16:22) " + EM + " Aramaic-speaking Jewish believers invoking Jesus as Lord at the very fountainhead of the movement.")
 + para("Most striking of all, in 1 Corinthians 8:6 Paul takes the Shema itself " + EM + " Israel's " + LDQ + "the LORD our God, the LORD is one" + RDQ + " " + EM + " and distributes its two terms, " + LDQ + "God" + RDQ + " and " + LDQ + "Lord" + RDQ + " (the Greek Bible's standard rendering of the Name YHWH), across the Father and Jesus: " + LDQ + "to us there is but one God, the Father... and one Lord Jesus Christ, by whom are all things." + RDQ + " He does not set Jesus alongside the one God as a second being; he places Jesus inside the Shema, identifying Him as the " + LDQ + "one Lord" + RDQ + " of Israel's own creed.")
 + h2("Modern Scholarship: The Earliest Christology Was Already High")
 + para("Recent scholarship has largely abandoned the old evolutionary model in which a merely human Jesus was gradually divinized by later Gentile converts. Larry Hurtado documented that the worship of Jesus " + EM + " prayer to Him, hymns about Him, invocation of His name, baptism into Him " + EM + " erupted among Jewish believers within the first years, an unprecedented " + LDQ + "binitarian" + RDQ + " devotion offered to Jesus alongside God. Richard Bauckham reframed the question around divine identity: the New Testament writers include Jesus in the unique identity of the one God " + EM + " as Creator, Ruler of all, bearer of the Name, and recipient of worship " + EM + " using the very markers by which Judaism distinguished its God from everything else. On this reading the highest Christology is also the earliest, and it is thoroughly Jewish, not a Greek corruption of a simpler original.")
 + h2("The Density of Early Citation")
)
insert_before_para("A second, much-cited apologetic statistic records a tally", antiquity)
print("antiquity subsections inserted")

# =====================================================================
# 10) Patristic confession + Nicaea + NEW Manuscript section (before Islam)
# =====================================================================
preislam = (
 h2("The Fathers' Explicit Confession")
 + para("The same generations that so saturated their writing with the New Testament also confessed its Christology in plain words. Ignatius of Antioch, led to martyrdom around AD 107 " + EM + " within a decade or two of the apostle John " + EM + " writes with no sense of novelty of " + LDQ + "Jesus Christ our God" + RDQ + " (Ephesians, salutation), says that " + LDQ + "our God, Jesus the Christ, was conceived by Mary" + RDQ + " (Ephesians 18:2), and glorifies " + LDQ + "Jesus Christ, the God who has thus given you wisdom" + RDQ + " (Smyrnaeans 1:1). Around AD 112 the pagan governor Pliny the Younger reports to the Emperor Trajan that Christians " + LDQ + "sing a hymn to Christ as to a god" + RDQ + " (carmen Christo quasi deo) " + EM + " a hostile outside witness to the same worship. Justin Martyr (c. 150) calls Christ God and worthy of worship; Irenaeus and Tertullian treat His full deity as settled; and Tertullian (c. 213) gives Latin theology its first vocabulary for the doctrine " + EM + " trinitas, and the formula " + LDQ + "three Persons, one substance." + RDQ + "")
 + note("Greek note", "Ignatius can speak of " + LDQ + "the blood of God" + RDQ + " (en haimati theou, Ephesians 1:1) and bless his readers in " + LDQ + "Jesus Christ our God" + RDQ + " (Iesou Christou tou theou hemon). These are not careful, hedged formulations defended against opponents; they are the casual idiom of a bishop who simply assumes his readers share the confession " + EM + " two full centuries before Nicaea.")
 + h2("Nicaea: Guardrail, Not Invention")
 + para("When the Council of Nicaea met in 325, it did not vote on whether Jesus was divine; that was the shared assumption of the bishops, of the martyrs behind them, and of the liturgies they prayed. The question was how to guard it against Arius, who taught that the Son was the highest of creatures " + EM + " made before time, but still made: " + LDQ + "there was when He was not." + RDQ + " Nicaea answered with one precise word: the Son is homoousios, " + LDQ + "of one essence," + RDQ + " with the Father " + EM + " true God from true God, begotten, not made. The decision was not a hair's-breadth vote brokered by Constantine (a modern fiction); it was overwhelming, and it canonized what Ignatius and the Philippian hymn had already confessed long before.")
 + h1("XII. The Manuscript and Textual Witness")
 + para("A doctrine is only as secure as the text that conveys it, and skeptics sometimes suggest that the deity of Christ hangs on a handful of late or corrupted verses. The opposite is the case. The deity of Christ runs through the best-attested strata of the New Testament, and the manuscript tradition " + EM + " by its antiquity, its sheer abundance, and even one of its most distinctive habits " + EM + " reinforces the confession rather than undermining it.")
 + h2("The Earliest Witnesses")
 + para("The New Testament is, by orders of magnitude, the best-attested text of the ancient world: more than 5,800 Greek manuscripts, with fragments reaching back to within a generation or two of composition. The Rylands fragment (P52) of John's Gospel dates to about AD 125, and the great papyri P66 and P75 (c. 200) preserve the Gospel of John " + EM + " with its " + LDQ + "the Word was God" + RDQ + " (1:1), its " + LDQ + "only-begotten God" + RDQ + " (1:18), and Thomas' " + LDQ + "My Lord and my God" + RDQ + " (20:28) " + EM + " more than a century before Nicaea. The texts on which the case for Christ's deity rests are not late insertions; they are among the very earliest words we possess.")
 + h2("The Disputed Verses, Weighed Honestly")
 + para("A few of the " + LDQ + "God" + RDQ + " texts do carry textual footnotes, and honesty requires naming them. 1 Timothy 3:16 reads " + LDQ + "God was manifest in the flesh" + RDQ + " in the later majority but " + LDQ + "who was manifested" + RDQ + " in the oldest manuscripts " + EM + " a difference of a single stroke between the sacred contraction for " + LDQ + "God" + RDQ + " and the pronoun for " + LDQ + "who," + RDQ + " though on either reading the One manifested, seen, and taken up in glory is plainly divine. Acts 20:28 " + EM + " " + LDQ + "the church of God, which he purchased with his own blood" + RDQ + " " + EM + " has a minority " + LDQ + "church of the Lord," + RDQ + " yet the blood that buys the Church is divine on either reading. John 1:18, as already noted, is in fact stronger in the earliest text (" + LDQ + "God" + RDQ + "), not weaker. The pattern is telling: where the text varies, the deity of Christ survives every viable reading.")
 + note("Textual note", "This is the decisive answer to the " + LDQ + "a few corrupted verses" + RDQ + " objection. Grant the critics every disputed reading at once " + EM + " concede 1 Timothy 3:16, Acts 20:28, even John 1:18 " + EM + " and Romans 9:5, John 1:1, John 20:28, Titus 2:13, Hebrews 1:8, Colossians 2:9, and the entire web of worship and divine-works texts remain untouched. The doctrine is over-determined by the evidence; it never rested on any single contested verse.")
 + h2("The Nomina Sacra " + EM + " Jesus Among the Sacred Names")
 + para("The manuscripts preserve a silent but eloquent testimony in their very ink. From the earliest copies onward, Christian scribes wrote a small set of sacred words not in full but in contracted form, capped with a horizontal line " + EM + " the nomina sacra, the " + LDQ + "sacred names." + RDQ + " The practice is nearly universal in Christian manuscripts and almost unknown outside them. The striking fact is which words were so honored: alongside " + LDQ + "God" + RDQ + " (Theos) and " + LDQ + "Lord" + RDQ + " (Kyrios), the scribes gave identical reverent treatment to " + LDQ + "Jesus" + RDQ + " (Iesous) and " + LDQ + "Christ" + RDQ + " (Christos).")
 + note("Manuscripts", "Of roughly 300 Christian manuscripts predating AD 300, all but a handful use the nomina sacra, and the four oldest and most consistent are exactly Theos, Kyrios, Iesous, and Christos. Larry Hurtado argues the habit is a visual act of devotion. Whatever its precise origin, its theological import is plain: the same copyists who reverently abbreviated the name of God reverently abbreviated the name of Jesus, placing " + LDQ + "Jesus" + RDQ + " in the same sacred class as " + LDQ + "God" + RDQ + " and " + LDQ + "Lord" + RDQ + " " + EM + " not as a debated thesis, but as the unreflective, established convention of the oldest Christian books we have.")
)
insert_before_para(">XI. Islam's View of Christ<", preislam)
print("patristic + Nicaea + manuscript section inserted")

# =====================================================================
# 11) RENUMBER body H1 headings (>old< -> >new<)
# =====================================================================
renum = [
 ("II. Romans 9:5 " + EM + " The Anchor Text", "III. Romans 9:5 " + EM + " The Anchor Text"),
 ("III. " + LDQ + "Jesus Is God" + RDQ + " " + EM + " The Direct Witness of Scripture", "IV. " + LDQ + "Jesus Is God" + RDQ + " " + EM + " The Direct Witness of Scripture"),
 ("IV. Old Testament Theophanies " + EM + " The Angel of the LORD", "V. Old Testament Theophanies " + EM + " The Angel of the LORD"),
 ("V. The Divine Works of Christ", "VI. The Divine Works of Christ"),
 ("VI. The Indirect but Unmistakable Claim", "VII. The Indirect but Unmistakable Claim"),
 ("VII. Worship Given to Christ", "VIII. Worship Given to Christ"),
 ("VIII. The Omnipresence of Christ", "IX. The Omnipresence of Christ"),
 ("IX. The Holy Trinity " + EM + " A Comparative Table", "X. The Holy Trinity " + EM + " A Comparative Table"),
 ("X. The Witness of the Early Church Fathers", "XI. How Early Is This Belief? " + EM + " The Antiquity of the Confession"),
 ("XI. Islam's View of Christ", "XIII. Islam's View of Christ"),
 ("XII. Anticipating Objections", "XIV. Anticipating Objections"),
 ("XIV. A Compact Apologetic Case", "XV. A Compact Apologetic Case"),
 ("XV. Conclusion " + EM + " From Confession to Communion", "XVI. Conclusion " + EM + " From Confession to Worship"),
]
for old, new in renum:
    o = ">" + old + "<"
    n = ">" + new + "<"
    c = s.count(o)
    assert c == 1, f"renumber expected 1 got {c}: {old!r}"
    s = s.replace(o, n)
print("headings renumbered")

# =====================================================================
# 12) SOURCES — trim Coptic clause, add new references
# =====================================================================
s = s.replace(
 "St. Athanasius, On the Incarnation of the Word (https://www.newadvent.org/fathers/2802.htm); conciliar and Cyrilline material surrounding Ephesus and the title Theotokos (https://www.newadvent.org/fathers/3810.htm).",
 "St. Athanasius, On the Incarnation of the Word (https://www.newadvent.org/fathers/2802.htm).")

new_sources = (
 src("Grammar and text-critical references: Daniel B. Wallace, Granville Sharp's Canon and Its Kin and Greek Grammar Beyond the Basics, on the article-noun-and-noun construction in Titus 2:13 and 2 Peter 1:1; Bruce M. Metzger, A Textual Commentary on the Greek New Testament, on John 1:18 (monogenes theos), 1 Timothy 3:16, and Acts 20:28; the nomina sacra discussion in Larry W. Hurtado, The Earliest Christian Artifacts (2006).")
 + src("Early Christology and Second Temple background: Richard Bauckham, Jesus and the God of Israel; Larry W. Hurtado, Lord Jesus Christ and One God, One Lord; Alan F. Segal, Two Powers in Heaven; N. T. Wright on 1 Corinthians 8:6 as a christological reworking of the Shema; Philo of Alexandria's Logos and the Targumic Memra as Second Temple categories of divine agency.")
 + src("Pliny the Younger, Letters 10.96, on Christians who " + LDQ + "sang a hymn to Christ as to a god" + RDQ + " (carmen Christo quasi deo), Fordham Internet History Sourcebook (https://sourcebooks.fordham.edu/source/pliny1.asp).")
)
cross = ('    <w:p>\n      <w:pPr>\n        <w:spacing w:after="300" w:before="60"/>\n        <w:jc w:val="center"/>\n      </w:pPr>\n'
         '      <w:r>\n        <w:rPr>\n          <w:color w:val="8B6914"/>\n          <w:sz w:val="26"/>\n          <w:szCs w:val="26"/>\n'
         '        </w:rPr>\n        <w:t xml:space="preserve">✠</w:t>')
ci = s.find(cross); assert ci != -1, "final cross not found"
cp = s.rfind('    <w:p>\n', 0, ci)
s = s[:cp] + new_sources + s[cp:]
print("sources expanded")

open(PATH, "w", encoding="utf-8").write(s)
print("STAGE C OK; length:", len(s))
