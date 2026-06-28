// Canonical site configuration used for metadata, OG images, sitemap, and JSON-LD.
export const site = {
  url: "https://christisgod.app",
  name: "Christ Is God",
  author: "Will Langhart",
  locale: "en_US",
  // Served from /public — used for JSON-LD publisher logo and the web manifest.
  logo: "/christisgod-logo.png",
} as const;

// Topical keywords. Google largely ignores these, but Bing still gives them
// light weight, and they document the site's subject for other consumers.
export const keywords = [
  "divinity of Christ",
  "deity of Jesus",
  "Jesus is God",
  "Christian apologetics",
  "is Jesus God",
  "Romans 9:5",
  "the Holy Trinity",
  "Christology",
  "biblical apologetics",
  "King James Version",
] as const;
