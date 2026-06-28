// IndexNow submitter — pings Bing / Microsoft Edge (and other participating
// engines) to instantly (re)crawl the site's URLs after a deploy.
//
// Usage:
//   node scripts/indexnow.mjs            # submit every URL in sitemap.xml
//   node scripts/indexnow.mjs <url> ...  # submit only the given URLs
//
// The key below must match the file served at https://<host>/<key>.txt.
// See https://www.indexnow.org/documentation

const HOST = "christisgod.app";
const KEY = "6b066dde377fc1fd276bca71cc216d7d";
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;
const ENDPOINT = "https://api.indexnow.org/indexnow";

async function urlsFromSitemap() {
  const res = await fetch(`https://${HOST}/sitemap.xml`);
  if (!res.ok) throw new Error(`Failed to fetch sitemap: ${res.status}`);
  const xml = await res.text();
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim());
}

async function main() {
  const cliUrls = process.argv.slice(2);
  const urlList = cliUrls.length > 0 ? cliUrls : await urlsFromSitemap();

  if (urlList.length === 0) {
    console.error("No URLs to submit.");
    process.exit(1);
  }

  console.log(`Submitting ${urlList.length} URL(s) to IndexNow…`);
  for (const u of urlList) console.log(`  • ${u}`);

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: HOST, key: KEY, keyLocation: KEY_LOCATION, urlList }),
  });

  const body = await res.text();
  // 200 = accepted, 202 = accepted/validation pending. Anything else is an error.
  if (res.status === 200 || res.status === 202) {
    console.log(`\n✓ IndexNow accepted (HTTP ${res.status}).`);
  } else {
    console.error(`\n✗ IndexNow returned HTTP ${res.status}: ${body}`);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
