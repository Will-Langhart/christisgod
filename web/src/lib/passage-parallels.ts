export type PassageParallel = {
  theme: string;
  oldRef: string;
  oldText: string;
  oldHighlight: string;
  newRef: string;
  newText: string;
  newHighlight: string;
  explanation: string;
};

export const passageParallels: PassageParallel[] = [
  {
    theme: "Whose way is being prepared?",
    oldRef: "Isaiah 40:3",
    oldText: "The voice of him that crieth in the wilderness, Prepare ye the way of the LORD, make straight in the desert a highway for our God.",
    oldHighlight: "Prepare ye the way of the LORD",
    newRef: "Mark 1:2–3",
    newText: "Behold, I send my messenger before thy face, which shall prepare thy way before thee. The voice of one crying in the wilderness, Prepare ye the way of the Lord, make his paths straight.",
    newHighlight: "Prepare ye the way of the Lord",
    explanation: "Isaiah announces the coming of Yahweh. Mark places that prophecy at the opening of his Gospel, where John prepares for the arrival of Jesus.",
  },
  {
    theme: "On whose name must one call?",
    oldRef: "Joel 2:32",
    oldText: "And it shall come to pass, that whosoever shall call on the name of the LORD shall be delivered.",
    oldHighlight: "call on the name of the LORD",
    newRef: "Romans 10:9–13",
    newText: "If thou shalt confess with thy mouth the Lord Jesus… thou shalt be saved. For whosoever shall call upon the name of the Lord shall be saved.",
    newHighlight: "call upon the name of the Lord",
    explanation: "Paul quotes Joel’s promise about calling upon Yahweh immediately after identifying the confessed Lord as Jesus.",
  },
  {
    theme: "Before whom will every knee bow?",
    oldRef: "Isaiah 45:22–23",
    oldText: "I am God, and there is none else… That unto me every knee shall bow, every tongue shall swear.",
    oldHighlight: "unto me every knee shall bow",
    newRef: "Philippians 2:10–11",
    newText: "That at the name of Jesus every knee should bow… And that every tongue should confess that Jesus Christ is Lord.",
    newHighlight: "at the name of Jesus every knee should bow",
    explanation: "Isaiah’s speaker insists he alone is God. Paul applies that speaker’s universal worship to Jesus, to the glory of the Father.",
  },
  {
    theme: "Who founded the earth?",
    oldRef: "Psalm 102:25–27",
    oldText: "Of old hast thou laid the foundation of the earth: and the heavens are the work of thy hands… but thou art the same, and thy years shall have no end.",
    oldHighlight: "laid the foundation of the earth",
    newRef: "Hebrews 1:8, 10–12",
    newText: "But unto the Son he saith… Thou, Lord, in the beginning hast laid the foundation of the earth; and the heavens are the works of thine hands.",
    newHighlight: "unto the Son he saith",
    explanation: "Hebrews introduces the quotation as the Father speaking to the Son, then addresses the Son with a psalm about Yahweh the unchanging Creator.",
  },
  {
    theme: "Who was pierced?",
    oldRef: "Zechariah 12:10",
    oldText: "And they shall look upon me whom they have pierced, and they shall mourn for him, as one mourneth for his only son.",
    oldHighlight: "look upon me whom they have pierced",
    newRef: "John 19:34–37",
    newText: "But one of the soldiers with a spear pierced his side… And again another scripture saith, They shall look on him whom they pierced.",
    newHighlight: "They shall look on him whom they pierced",
    explanation: "Zechariah records Yahweh speaking in the first person. John sees that text fulfilled when the crucified Jesus is pierced.",
  },
];
