# -*- coding: utf-8 -*-
import re
PATH = "unpacked_final/word/document.xml"
s = open(PATH, encoding="utf-8").read()
LDQ, RDQ, EM = "&#x201C;", "&#x201D;", "—"

def need(old, count=1):
    n = s.count(old)
    assert n == count, f"expected {count} got {n}: {old[:60]!r}"

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
# 5) CONTENTS — rewrite the table of contents (16 sections + Sources)
# =====================================================================
contents_titles = [
    "I. Introduction " + EM + " Why the Divinity of Christ Matters",
    "II. The Monotheistic Context " + EM + " Why the Claim Was Radical",
    "III. Romans 9:5 " + EM + " The Anchor Text",
    "IV. " + LDQ + "Jesus Is God" + RDQ + " " + EM + " The Direct Witness of Scripture",
    "V. Old Testament Theophanies " + EM + " The Angel of the LORD",
    "VI. The Divine Works of Christ",
    "VII. The Indirect but Unmistakable Claim",
    "VIII. Worship Given to Christ",
    "IX. The Omnipresence of Christ",
    "X. The Holy Trinity " + EM + " A Comparative Table",
    "XI. How Early Is This Belief? " + EM + " The Antiquity of the Confession",
    "XII. The Manuscript and Textual Witness",
    "XIII. Islam's View of Christ",
    "XIV. Anticipating Objections",
    "XV. A Compact Apologetic Case",
    "XVI. Conclusion " + EM + " From Confession to Worship",
    "Sources Consulted",
]
new_contents = "".join(contents_entry(t) for t in contents_titles)

c_start = '<w:t xml:space="preserve">Contents</w:t>\n      </w:r>\n    </w:p>\n'
intro_anchor = ('    <w:p>\n      <w:pPr>\n        <w:pStyle w:val="Heading1"/>\n        <w:pBdr>\n'
                '          <w:bottom w:val="single" w:color="8B6914" w:sz="8" w:space="4"/>\n        </w:pBdr>\n'
                '        <w:spacing w:after="200" w:before="480"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
                '          <w:color w:val="7A1F1F"/>\n        </w:rPr>\n        <w:t xml:space="preserve">I. Introduction')
i1 = s.find(c_start); assert i1 != -1
i1 += len(c_start)
i2 = s.find(intro_anchor); assert i2 != -1 and i2 > i1
s = s[:i1] + new_contents + s[i2:]
print("contents rewritten")

# =====================================================================
# 6) DELETE the Coptic section (body heading XIII -> just before XIV)
# =====================================================================
del_start = ('    <w:p>\n      <w:pPr>\n        <w:pStyle w:val="Heading1"/>\n        <w:pBdr>\n'
             '          <w:bottom w:val="single" w:color="8B6914" w:sz="8" w:space="4"/>\n        </w:pBdr>\n'
             '        <w:spacing w:after="200" w:before="480"/>\n      </w:pPr>\n      <w:r>\n        <w:rPr>\n'
             '          <w:color w:val="7A1F1F"/>\n        </w:rPr>\n'
             '        <w:t xml:space="preserve">XIII. The Patristic and Liturgical Witness of the Coptic Church</w:t>')
# fall back to plain heading form if needed
if del_start not in s:
    del_start = '<w:t>XIII. The Patristic and Liturgical Witness of the Coptic Church</w:t>'
ds = s.find(del_start); assert ds != -1, "coptic heading not found"
ds = s.rfind('    <w:p>\n', 0, ds)
# end boundary: the Compact Apologetic Case heading
m_compact = s.find('XIV. A Compact Apologetic Case')
assert m_compact != -1
de = s.rfind('    <w:p>\n', 0, m_compact)
assert de > ds
removed = s[ds:de]
assert 'Coptic' in removed and 'Theotokos' in removed and 'Agpeya' in removed, "deletion range looks wrong"
assert 'Compact' not in removed
s = s[:ds] + s[de:]
print("coptic section deleted (", len(removed), "chars )")

# =====================================================================
# 7) NEW SECTION II — The Monotheistic Context
# =====================================================================
sec2 = (
 h1("II. The Monotheistic Context " + EM + " Why the Claim Was Radical")
 + para("To grasp the magnitude of the claim that Jesus is God, one must first hear it as a first-century Jew would have heard it. Israel's defining confession was the Shema: " + LDQ + "Hear, O Israel: The LORD our God is one LORD" + RDQ + " (Deuteronomy 6:4). To this one God alone belonged worship, sacrifice, and the unspeakable Name YHWH; to give them to any other was the gravest of sins, punishable by death (Exodus 20:3" + EM + "5; Deuteronomy 6:13). This was not a vague theism but a jealous, boundaried monotheism for which Jews had died under Antiochus and would die again under Rome. It is into this world " + EM + " not the casual polytheism of Greece, where one more god was no scandal " + EM + " that the first Christians, themselves observant Jews, began to worship a crucified Galilean as Lord and God.")
 + h2("Mediators of the One God")
 + para("Second Temple Judaism did possess a rich vocabulary for God's self-expression and agency " + EM + " figures who stood close to God without being separate gods. The personified Wisdom of Proverbs 8 is " + LDQ + "with" + RDQ + " God at creation; the Word by which the heavens were made (Psalm 33:6) is so exalted in Philo of Alexandria that he can call it a " + LDQ + "second God" + RDQ + " and God's instrument in creating the world; the Aramaic Targums repeatedly put the Memra (" + LDQ + "Word" + RDQ + ") of the LORD where the Hebrew has God Himself acting; and apocalyptic literature exalts a " + LDQ + "Son of Man" + RDQ + " who is brought before the Ancient of Days and given everlasting, universal dominion (Daniel 7:13" + EM + "14). These categories gave the first Christians a ready vocabulary " + EM + " but, as the next paragraph shows, the use they made of it shattered the mold.")
 + note("Background", "Alan F. Segal's landmark study Two Powers in Heaven (1977) traced a Jewish " + LDQ + "two powers" + RDQ + " tradition with roots around 200 BCE, in which a second figure bears the divine Name and glory " + EM + " for example the Angel of the LORD of whom God says " + LDQ + "My name is in him" + RDQ + " (Exodus 23:21). Philo's Logos as a " + LDQ + "second God" + RDQ + " (deuteros theos) and the Targumic Memra show that first-century Judaism already had room for a divine mediator who was neither a creature nor a rival deity. The rabbis only branded the " + LDQ + "two powers" + RDQ + " idea heretical in the second century " + EM + " precisely as Christians were applying it to Jesus.")
 + h2("The Line the Son of Man Crossed")
 + para("Yet there was one line these exalted figures never crossed: not one of them was worshipped. Wisdom, the Logos, the Memra, the highest angels " + EM + " however near to God " + EM + " never received the cultic devotion reserved for YHWH alone; in the visions, the greatest angels expressly refuse it. This is the force of Richard Bauckham's analysis: Second Temple Jews defined their one God not chiefly by an abstract substance but by a unique identity " + EM + " the only Creator of all things, the only sovereign Ruler over all things, the sole bearer of the Name YHWH, and the only rightful recipient of worship. To include Jesus within that identity " + EM + " to confess Him as Creator, Lord of all, bearer of the Name, and recipient of worship " + EM + " was therefore not to add a second god to a pantheon. It was to identify Jesus with the one God of Israel. That is exactly what the New Testament does, deliberately, and from the earliest layer of evidence we can reach.")
)
insert_before_para('>II. Romans 9:5 ' + EM + ' The Anchor Text<', sec2)
print("section II inserted")

# =====================================================================
# 8) DIRECT-WITNESS EXPANSION (appended to Section III, before Theophanies)
# =====================================================================
expand3 = (
 h2("Titus 2:13 and 2 Peter 1:1 " + EM + " The Granville Sharp Rule")
 + ref("Titus 2:13; 2 Peter 1:1")
 + para("Two apostolic greetings call Jesus " + LDQ + "God" + RDQ + " not by a disputed word but by a rule of Greek grammar. Titus 2:13 awaits " + LDQ + "the glorious appearing of the great God and our Saviour Jesus Christ" + RDQ + "; 2 Peter 1:1 is addressed to those who have obtained faith " + LDQ + "through the righteousness of our God and Saviour Jesus Christ." + RDQ + " In each, a single Greek article governs two singular nouns " + EM + " " + LDQ + "God" + RDQ + " and " + LDQ + "Saviour" + RDQ + " " + EM + " joined by " + LDQ + "and," + RDQ + " a construction that points to one and the same person.")
 + note("Grammar note", "Granville Sharp's rule: when one article governs two singular, personal, common (non-proper) nouns joined by " + LDQ + "and" + RDQ + " (the article" + EM + "noun" + EM + "kai" + EM + "noun construction), both nouns denote the same person. Daniel B. Wallace's exhaustive survey of every such construction in the New Testament and thousands of Hellenistic papyri found no clear exception once plurals, proper names, and impersonal nouns are set aside. In Titus 2:13 (tou megalou Theou kai soteros hemon Iesou Christou) and 2 Peter 1:1, the rule makes " + LDQ + "God" + RDQ + " and " + LDQ + "Saviour" + RDQ + " one referent: Jesus Christ. The same writers use the identical construction elsewhere for plainly single referents, so an exception here would be special pleading.")
 + h2("John 1:18 " + EM + " The Only-Begotten God")
 + ref("John 1:18")
 + para("John's prologue closes its opening movement by declaring that no one has ever seen God; the Son " + LDQ + "hath declared him." + RDQ + " In the earliest manuscripts the key word is not " + LDQ + "Son" + RDQ + " but " + LDQ + "God" + RDQ + ": " + LDQ + "the only begotten God, which is in the bosom of the Father, he hath declared him." + RDQ + " The reading forms a deliberate bracket with John 1:1 (" + LDQ + "the Word was God" + RDQ + "), enclosing the whole prologue between two affirmations of the Word's deity.")
 + note("Textual note", "The reading monogenes theos (" + LDQ + "only-begotten God" + RDQ + ") is supported by the oldest and best witnesses " + EM + " the papyri P66 and P75 (c. 200) and the great fourth-century codices Sinaiticus, Vaticanus, and Ephraemi. The later majority reading monogenes huios (" + LDQ + "only-begotten Son" + RDQ + ") is itself orthodox, but it is the easier, more familiar phrase " + EM + " which is exactly why a scribe was far likelier to soften " + LDQ + "God" + RDQ + " to " + LDQ + "Son" + RDQ + " than the reverse. Modern critical editions print " + LDQ + "God." + RDQ + "")
 + h2("Colossians 2:9 " + EM + " The Fulness of the Godhead Bodily")
 + ref("Colossians 2:9; cf. 1:19")
 + para("Against teachers who would dilute Christ with a hierarchy of angelic mediators, Paul writes that " + LDQ + "in him dwelleth all the fulness of the Godhead bodily." + RDQ + " The Greek noun is theotes " + EM + " not merely " + LDQ + "divine quality" + RDQ + " but Deity itself, the very state of being God " + EM + " and " + LDQ + "all the fulness" + RDQ + " of it dwells (present tense, permanently) and " + LDQ + "bodily" + RDQ + " in the incarnate Christ. Whatever it is to be God, Paul says, resides wholly and personally in Jesus of Nazareth.")
 + h2("1 John 5:20 " + EM + " This Is the True God")
 + ref("1 John 5:20")
 + para("John's first epistle ends: " + LDQ + "we are in him that is true, even in his Son Jesus Christ. This is the true God, and eternal life." + RDQ + " The nearest antecedent of " + LDQ + "this" + RDQ + " (houtos) is " + LDQ + "Jesus Christ," + RDQ + " just named; and " + LDQ + "eternal life" + RDQ + " is a title John has already given the Son (" + LDQ + "that eternal life, which was with the Father," + RDQ + " 1 John 1:2). The apostle therefore closes by calling Jesus " + LDQ + "the true God" + RDQ + " " + EM + " the very phrase the Old Testament reserves for YHWH over against all idols (Jeremiah 10:10).")
 + h2("Further Ascriptions and Applied YHWH-Texts")
 + para("The pattern recurs across the New Testament. 2 Thessalonians 1:12 speaks of " + LDQ + "the grace of our God and the Lord Jesus Christ" + RDQ + " (again a Granville Sharp construction on a natural reading). 1 Corinthians 2:8 calls the crucified " + LDQ + "the Lord of glory," + RDQ + " a divine title (Psalm 24:7" + EM + "10). Most pointedly, Philippians 2:10" + EM + "11 and Romans 14:11 take Isaiah 45:23 " + EM + " where YHWH swears " + LDQ + "unto me every knee shall bow" + RDQ + " and insists He will share His glory with no other " + EM + " and fulfil it in the universal confession of Jesus as Lord. And Hebrews 1:10" + EM + "12 has the Father address the Son in the words of Psalm 102, a hymn to YHWH the Creator: " + LDQ + "Thou, Lord, in the beginning hast laid the foundation of the earth." + RDQ + " Texts spoken of YHWH alone are, without apology, spoken of Jesus.")
)
insert_before_para('>IV. Old Testament Theophanies ' + EM + ' The Angel of the LORD<', expand3)
print("section III expansion inserted")

open(PATH, "w", encoding="utf-8").write(s)
print("STAGE B-1 OK; length:", len(s))
