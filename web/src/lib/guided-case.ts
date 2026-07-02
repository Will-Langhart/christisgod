export type CaseStep = {
  eyebrow: string;
  title: string;
  thesis: string;
  quotation: string;
  reference: string;
  explanation: string;
  supporting: string[];
};

export const guidedCaseSteps: CaseStep[] = [
  {
    eyebrow: "Begin with the setting",
    title: "The first Christians believed in one God.",
    thesis: "Calling Jesus divine was not casual language in a culture crowded with interchangeable gods.",
    quotation: "Hear, O Israel: The LORD our God is one LORD.",
    reference: "Deuteronomy 6:4",
    explanation:
      "Jesus and his earliest followers stood inside Israel’s uncompromising monotheism. The question is therefore not whether they abandoned belief in one God, but why they came to include Jesus within that one God’s identity.",
    supporting: ["Isaiah 45:5", "Mark 12:29", "1 Corinthians 8:4"],
  },
  {
    eyebrow: "The direct witness",
    title: "The New Testament calls Jesus God.",
    thesis: "The claim is not built only from inference; it is stated across several New Testament authors.",
    quotation: "And Thomas answered and said unto him, My Lord and my God.",
    reference: "John 20:28",
    explanation:
      "John opens by saying the Word was God and closes his resurrection narrative with Thomas addressing Jesus as ‘my God.’ Paul, Hebrews, and Peter use the same divine title in distinct settings. The testimony is distributed, not confined to one isolated verse.",
    supporting: ["John 1:1", "Romans 9:5", "Titus 2:13", "Hebrews 1:8"],
  },
  {
    eyebrow: "The Creator’s side of the line",
    title: "Jesus does what only God does.",
    thesis: "Creation, the forgiveness of sins, final judgment, and the giving of life are attributed to him.",
    quotation: "All things were made by him; and without him was not any thing made that was made.",
    reference: "John 1:3",
    explanation:
      "Everything that came into being came through the Word. That leaves no room to place him among created things. In the Gospels, Jesus also forgives sins by his own authority and claims the Father’s work of giving life and judging the world.",
    supporting: ["Mark 2:5–12", "John 5:21–23", "Colossians 1:16–17"],
  },
  {
    eyebrow: "The honor due to God",
    title: "Jesus receives worship.",
    thesis: "The worship of Jesus is deliberate, repeated, and joined to the worship of the Father.",
    quotation: "Worthy is the Lamb that was slain to receive power, and riches, and wisdom, and strength, and honour, and glory, and blessing.",
    reference: "Revelation 5:12",
    explanation:
      "Biblical angels refuse worship, but Jesus receives it. Revelation’s heavenly court gives the Lamb the same unending blessing and honor given to the One seated on the throne. This is far more than a solitary gesture of respect.",
    supporting: ["Matthew 14:33", "John 9:38", "Hebrews 1:6", "Revelation 5:13–14"],
  },
  {
    eyebrow: "Israel’s Scriptures reread",
    title: "Words about Yahweh are applied to Jesus.",
    thesis: "The apostles repeatedly identify Jesus with the Lord revealed in Israel’s Scriptures.",
    quotation: "Prepare ye the way of the LORD, make straight in the desert a highway for our God.",
    reference: "Isaiah 40:3",
    explanation:
      "All four Gospels use Isaiah’s command to prepare Yahweh’s way for John the Baptist preparing the way for Jesus. Paul likewise takes Joel’s promise that everyone calling on Yahweh will be saved and applies it to calling on Jesus as Lord.",
    supporting: ["Mark 1:2–3", "Joel 2:32", "Romans 10:9–13", "Hebrews 1:10–12"],
  },
  {
    eyebrow: "Earlier than the councils",
    title: "The confession began at Christianity’s beginning.",
    thesis: "Jesus was worshiped within the earliest recoverable layers of Christian belief.",
    quotation: "That at the name of Jesus every knee should bow… and that every tongue should confess that Jesus Christ is Lord.",
    reference: "Philippians 2:10–11",
    explanation:
      "Paul quotes an early Christian hymn that applies Isaiah’s vision of universal worship before Yahweh to Jesus. This material predates the fourth-century councils by generations. Nicaea supplied a guardrail for an existing confession; it did not manufacture a new one.",
    supporting: ["Isaiah 45:23", "1 Corinthians 8:6", "Pliny, c. AD 112", "Ignatius, c. AD 110"],
  },
  {
    eyebrow: "The cumulative conclusion",
    title: "Which explanation fits the whole portrait?",
    thesis: "Jesus is distinct from the Father, truly human—and fully included in the identity of the one God.",
    quotation: "For in him dwelleth all the fulness of the Godhead bodily.",
    reference: "Colossians 2:9",
    explanation:
      "Any adequate conclusion must account for all the evidence at once: divine names, works, worship, identity, and the earliest confession, alongside Jesus’ genuine humanity and relationship with the Father. Historic Christian belief gives that synthesis a name: the incarnation of the eternal Son.",
    supporting: ["John 1:14", "Matthew 28:19", "Philippians 2:6–8", "Colossians 2:9"],
  },
];
