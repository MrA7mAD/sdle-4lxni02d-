// Offline support: keep a copy of the app on the device.
// Opens instantly from the saved copy, then quietly checks for a newer version online.
const CACHE = "sdle-v1";
const CORE = ["./", "./index.html"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
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
    const net = fetch(req).then(r => { if (r && (r.ok || r.type === "opaque")) c.put(key, r.clone()); return r; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response("Offline and not saved yet. Open once while online.", {status: 503});
  }));
});
