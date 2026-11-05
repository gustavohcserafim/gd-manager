// GD Manager - Service Worker
const CACHE_NAME = "gd-manager-v1";

const STATIC_ASSETS = [
  "/",
  "/static/index.html",
  "/static/manifest.json",
  "/static/icons/icon.svg",
  "/static/css/app.css",
  "/static/js/app.js",
  "/static/js/api.js",
  "/static/js/auth.js",
  "/static/js/members.js",
  "/static/js/history.js"
];

// Install: Pre-cache core shell assets
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn("Service Worker pre-cache partial warning:", err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Purge previous version caches and take control
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Strategy depending on request type
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 1. API Requests
  if (url.pathname.startsWith("/api/")) {
    if (request.method === "GET") {
      // Network-First for GET requests, falling back to cache
      event.respondWith(
        fetch(request)
          .then((response) => {
            if (response && response.status === 200) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseClone);
              });
            }
            return response;
          })
          .catch(async () => {
            const cachedResponse = await caches.match(request);
            if (cachedResponse) {
              return cachedResponse;
            }
            return new Response(
              JSON.stringify({
                error: "offline",
                message: "Dispositivo offline. Conexão indisponível."
              }),
              {
                status: 503,
                headers: { "Content-Type": "application/json" }
              }
            );
          })
      );
    }
    // For non-GET mutations (POST, PUT, DELETE), let them hit network directly
    return;
  }

  // 2. Navigation & Static Asset Requests: Cache-First with Network fallback
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Fetch in background to update cache for next time
        fetch(request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, networkResponse);
              });
            }
          })
          .catch(() => {
            /* ignore background fetch failures */
          });
        return cachedResponse;
      }

      return fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && request.method === "GET") {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, clone);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // If navigation fails, fallback to root / index.html
          if (request.mode === "navigate") {
            return caches.match("/");
          }
        });
    })
  );
});
