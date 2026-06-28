// Reusable schema.org / JSON-LD nodes shared across pages. Using stable @id
// values lets Google merge the Organization, WebSite, and Book nodes into one
// connected graph for richer understanding of the site.
import { bookMeta } from "@/lib/book-meta";
import { chapters } from "@/lib/chapters";
import { site } from "@/lib/site";

const ORG_ID = `${site.url}/#organization`;
const WEBSITE_ID = `${site.url}/#website`;
const BOOK_ID = `${site.url}/#book`;
const FULL_TITLE = `${bookMeta.title} — ${bookMeta.subtitle}`;

export const organizationNode = {
  "@type": "Organization",
  "@id": ORG_ID,
  name: site.name,
  url: site.url,
  logo: {
    "@type": "ImageObject",
    url: `${site.url}${site.logo}`,
  },
};

export const websiteNode = {
  "@type": "WebSite",
  "@id": WEBSITE_ID,
  name: FULL_TITLE,
  url: site.url,
  inLanguage: "en",
  publisher: { "@id": ORG_ID },
};

export const bookNode = {
  "@type": "Book",
  "@id": BOOK_ID,
  name: bookMeta.title,
  alternateName: FULL_TITLE,
  description: bookMeta.tagline,
  url: site.url,
  inLanguage: "en",
  bookFormat: "https://schema.org/EBook",
  genre: ["Religion", "Christian apologetics", "Theology"],
  datePublished: bookMeta.year,
  numberOfPages: chapters.length,
  author: { "@type": "Person", name: site.author },
  publisher: { "@id": ORG_ID },
  image: `${site.url}/opengraph-image`,
  hasPart: chapters.map((c) => ({
    "@type": "Chapter",
    name: c.title,
    url: `${site.url}/read/${c.slug}`,
  })),
};

/** The home page graph: organization + website + book, fully linked. */
export const homeGraph = {
  "@context": "https://schema.org",
  "@graph": [organizationNode, websiteNode, bookNode],
};

/** Article + breadcrumb graph for a single chapter page. */
export function chapterGraph({
  title,
  slug,
  description,
  modified,
}: {
  title: string;
  slug: string;
  description: string;
  /** Last-modified time of the chapter's source, for Article dateModified. */
  modified?: Date;
}) {
  const url = `${site.url}/read/${slug}`;
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Article",
        "@id": `${url}#article`,
        headline: title,
        description,
        url,
        inLanguage: "en",
        image: `${url}/opengraph-image`,
        datePublished: bookMeta.year,
        ...(modified ? { dateModified: modified.toISOString() } : {}),
        author: { "@type": "Person", name: site.author },
        publisher: { "@id": ORG_ID },
        mainEntityOfPage: { "@type": "WebPage", "@id": url },
        isPartOf: { "@id": BOOK_ID },
      },
      {
        "@type": "BreadcrumbList",
        "@id": `${url}#breadcrumb`,
        itemListElement: [
          { "@type": "ListItem", position: 1, name: bookMeta.title, item: site.url },
          { "@type": "ListItem", position: 2, name: title, item: url },
        ],
      },
    ],
  };
}
