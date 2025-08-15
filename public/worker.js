const CACHE='hoshimi-v1', ASSETS=['/','/index.html','/app.js','/ui.js','/manifest.webmanifest','/data/site_state.json','/data/affiliates.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));});
self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(res=>{
  const net=fetch(e.request).then(r=>{if(r.ok&&e.request.method==='GET'){const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));}return r;}).catch(()=>res||new Response('offline',{status:503}));
  return res||net;
}));});
