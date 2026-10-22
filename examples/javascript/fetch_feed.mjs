// Fetch one league feed with the built-in fetch (Node 18+). Usage: node fetch_feed.mjs nba
const league = process.argv[2] ?? "nba";
const res = await fetch(`https://betbetter.world/${league}/picks?format=json`);
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const feed = await res.json();
console.log(`${feed.sport} - ${feed.count} selections (updated ${feed.updatedUtc})`);
for (const pick of feed.picks ?? []) console.log(pick);
