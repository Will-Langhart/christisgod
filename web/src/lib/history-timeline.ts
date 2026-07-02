export type TimelineEvent = {
  date: string;
  era: "New Testament" | "Early Church" | "Council";
  title: string;
  witness: string;
  significance: string;
  source?: string;
};

export const timelineEvents: TimelineEvent[] = [
  {
    date: "c. AD 50–60",
    era: "New Testament",
    title: "An early hymn gives Jesus Yahweh’s worship",
    witness: "Philippians 2:6–11 applies Isaiah 45’s universal bowing and confession to Jesus Christ as Lord.",
    significance: "Paul treats this confession as received Christian worship, not a new theory he needs to defend.",
  },
  {
    date: "c. AD 53–55",
    era: "New Testament",
    title: "Paul includes Jesus in Israel’s confession of one God",
    witness: "1 Corinthians 8:6 names ‘one God, the Father’ and ‘one Lord Jesus Christ,’ through whom all things exist.",
    significance: "The language of the Shema is expanded around the Father and Son without introducing two gods.",
  },
  {
    date: "c. AD 90–100",
    era: "New Testament",
    title: "John calls the Word God",
    witness: "John 1:1 identifies the eternal Word as God; John 20:28 records Thomas addressing the risen Jesus as ‘my Lord and my God.’",
    significance: "Divine identity frames the Gospel from its opening sentence to its climactic confession.",
  },
  {
    date: "c. AD 107–110",
    era: "Early Church",
    title: "Ignatius speaks naturally of ‘Jesus Christ our God’",
    witness: "On his way to martyrdom, the bishop of Antioch repeatedly uses divine language for Christ in pastoral letters.",
    significance: "The phrase appears as the shared vocabulary of geographically separated churches, not as a disputed innovation.",
    source: "https://www.newadvent.org/fathers/0107.htm",
  },
  {
    date: "c. AD 112",
    era: "Early Church",
    title: "A Roman governor observes worship of Christ",
    witness: "Pliny the Younger reports that Christians met before dawn and sang responsively to Christ ‘as to a god.’",
    significance: "An unsympathetic outsider confirms that worship of Christ was established in Bithynia more than two centuries before Nicaea.",
    source: "https://sourcebooks.fordham.edu/source/pliny1.asp",
  },
  {
    date: "c. AD 150–160",
    era: "Early Church",
    title: "Justin describes Christian worship to the emperor",
    witness: "Justin’s First Apology publicly explains Christian devotion to the Father, the Son, and the prophetic Spirit.",
    significance: "The basic pattern later guarded by creedal language was already public Christian teaching in the second century.",
    source: "https://www.newadvent.org/fathers/0126.htm",
  },
  {
    date: "c. AD 200",
    era: "Early Church",
    title: "Tertullian uses the word Trinity",
    witness: "Writing against modalism, Tertullian distinguishes Father, Son, and Spirit while defending one divine substance.",
    significance: "Technical vocabulary develops because Christians are clarifying an inherited belief, not creating Christ’s divinity from nothing.",
    source: "https://www.newadvent.org/fathers/0317.htm",
  },
  {
    date: "AD 325",
    era: "Council",
    title: "Nicaea defines—not invents—the confession",
    witness: "The creed calls the Son ‘true God from true God,’ begotten rather than made, and of one substance with the Father.",
    significance: "The council answers Arius’s claim that the Son was a creature. The historical record already stretches back to Christianity’s earliest sources.",
    source: "https://www.newadvent.org/fathers/3801.htm",
  },
];
