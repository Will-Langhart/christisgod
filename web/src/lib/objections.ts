export type Objection = {
  question: string;
  shortAnswer: string;
  explanation: string;
  passages: string[];
  href: string;
  linkLabel: string;
};

export const objections: Objection[] = [
  {
    question: "Jesus never said, ‘I am God.’",
    shortAnswer: "He made claims his first hearers understood as divine claims.",
    explanation:
      "Jesus identified himself with the ‘I am,’ claimed authority to forgive sins, placed himself above the Sabbath, and said he would judge the world. At his trial, he joined Daniel’s heavenly Son of Man to the divine cloud-rider—and the council charged him with blasphemy. His claim is larger than one modern formula.",
    passages: ["John 8:58–59", "Mark 2:5–12", "Mark 14:61–64"],
    href: "/read/vii-the-indirect-but-unmistakable-claim",
    linkLabel: "Examine Jesus’ own claims",
  },
  {
    question: "If Jesus is God, why did he pray to God?",
    shortAnswer: "Because the Son is not the Father, and the Son truly became human.",
    explanation:
      "Christian belief is not that Jesus is the Father. The eternal Son relates to the Father personally and, in the incarnation, lives a genuinely human life of trust and obedience. His prayers reveal both that personal distinction and the reality of his humanity; neither requires him to be a creature.",
    passages: ["John 1:1–2", "John 17:1–5", "Philippians 2:5–8"],
    href: "/read/x-the-holy-trinity",
    linkLabel: "Understand the Trinity",
  },
  {
    question: "Didn’t Jesus say, ‘The Father is greater than I’—and call him the only true God?",
    shortAnswer: "Those words describe his incarnate mission, not a lesser divine nature.",
    explanation:
      "The Son willingly takes the servant’s place and is sent by the Father. Yet in the same Gospel he possesses glory with the Father before creation, is called God, and receives Thomas’s confession, ‘My Lord and my God.’ Personal order and willing humility do not amount to inferiority of being.",
    passages: ["John 14:28", "John 17:3–5", "John 20:28"],
    href: "/read/xiv-anticipating-objections",
    linkLabel: "Read the passages in context",
  },
  {
    question: "Does ‘firstborn of creation’ mean Jesus was created?",
    shortAnswer: "In context, ‘firstborn’ names supremacy and inheritance—not first creature.",
    explanation:
      "Paul immediately explains the title: all things were created through Christ and for Christ, and he exists before all things. Scripture can call David ‘firstborn’ while also calling him the youngest son. The title marks the heir and ruler of creation, placing Christ on the Creator side of the Creator–creature distinction.",
    passages: ["Colossians 1:15–17", "Psalm 89:27", "John 1:3"],
    href: "/read/xiv-anticipating-objections",
    linkLabel: "Study the disputed texts",
  },
  {
    question: "Was Jesus made God at the Council of Nicaea?",
    shortAnswer: "No. Christians worshiped Jesus and called him God centuries earlier.",
    explanation:
      "Paul’s letters already contain early hymns and confessions placing Jesus within the identity of Israel’s one God. Ignatius calls Jesus ‘our God’ around AD 110, and Pliny reports Christians singing to Christ as to a god. Nicaea did not create the confession; it defined language to defend it against a new denial.",
    passages: ["Philippians 2:5–11", "1 Corinthians 8:6", "Hebrews 1:8"],
    href: "/history",
    linkLabel: "Explore the visual timeline",
  },
  {
    question: "Could the Bible have been changed to make Jesus divine?",
    shortAnswer: "The case survives across early manuscripts, authors, and textual variants.",
    explanation:
      "Christ’s divinity does not depend on one late or disputed verse. It appears across Paul, John, Hebrews, and the Gospels—in direct titles, worship, divine works, and Old Testament passages applied to Jesus. Even granting the less explicit reading of every notable textual variant leaves the cumulative case intact.",
    passages: ["John 1:1", "Romans 9:5", "Hebrews 1:8", "Titus 2:13"],
    href: "/read/xii-the-manuscript-and-textual-witness",
    linkLabel: "Inspect the manuscript evidence",
  },
];
