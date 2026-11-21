// Offline support: keep a copy of the app on the device.
// The page checks online first (a quick check when nothing changed) and uses the saved copy when offline or slow.
const CACHE = "sdle-v33";
const CORE = ["./", "./index.html"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE.map(u => new Request(u, {cache: "reload"})))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const isPage = req.mode === "navigate" || (url.origin === location.origin && url.pathname.endsWith(".html"));
  const isFont = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!isPage && !isFont && url.origin !== location.origin) return;
  e.respondWith(caches.open(CACHE).then(async c => {
    const key = isPage ? "./index.html" : req;
    const hit = await c.match(key);
    const net = fetch(isPage ? new Request(req.url, {cache: "no-cache"}) : req).then(r => { if (r && (r.ok || r.type === "opaque")) c.put(key, r.clone()); return r; }).catch(() => null);
    if (hit && isPage) {
      e.waitUntil(net);
      const quick = await Promise.race([net, new Promise(r => setTimeout(() => r(null), 4000))]);
      return quick || hit;
    }
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response("Offline and not saved yet. Open once while online.", {status: 503});
  }));
});
