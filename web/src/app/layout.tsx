import type { Metadata, Viewport } from "next";
import { EB_Garamond, Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";
import { bookMeta } from "@/lib/book-meta";
import { site, keywords } from "@/lib/site";

const ebGaramond = EB_Garamond({
  variable: "--font-eb-garamond",
  subsets: ["latin"],
  display: "swap",
});

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  weight: ["500", "600", "700"],
  subsets: ["latin"],
  display: "swap",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `${bookMeta.title} — ${bookMeta.subtitle}`,
    template: `%s · ${bookMeta.title}`,
  },
  description: bookMeta.tagline,
  applicationName: bookMeta.title,
  authors: [{ name: site.author }],
  creator: site.author,
  publisher: site.author,
  keywords: [...keywords],
  category: "religion",
  alternates: {
    canonical: "/",
  },
  // Google Search Console is already linked; these are picked up from env when
  // set so you can also verify Bing Webmaster Tools (msvalidate.01) without a
  // code change. Unset values are simply omitted.
  verification: {
    google: process.env.NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION,
    other: process.env.NEXT_PUBLIC_BING_SITE_VERIFICATION
      ? { "msvalidate.01": process.env.NEXT_PUBLIC_BING_SITE_VERIFICATION }
      : {},
  },
  openGraph: {
    title: `${bookMeta.title} — ${bookMeta.subtitle}`,
    description: bookMeta.tagline,
    type: "book",
    siteName: bookMeta.title,
    locale: site.locale,
    url: site.url,
  },
  twitter: {
    card: "summary_large_image",
    title: `${bookMeta.title} — ${bookMeta.subtitle}`,
    description: bookMeta.tagline,
  },
};

export const viewport: Viewport = {
  themeColor: "#f7f1e6",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${ebGaramond.variable} ${cormorant.variable} ${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
