import json
h = open('page.html').read()
logo = open('logo.b64').read().strip()
assert len(logo) > 1000, "logo missing"
h = h.replace('%%LOGO%%', logo)
js = (
    'const html = ' + json.dumps(h) + ';\n'
    'const logoB64 = ' + json.dumps(logo) + ';\n'
    'function b64ToBytes(b64){const bin=atob(b64);const bytes=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);return bytes}\n\n'
    'export default {\n'
    '  async fetch(request, env) {\n'
    '    const url = new URL(request.url);\n'
    '    if (url.pathname === "/og.png") {\n'
    '      return new Response(b64ToBytes(logoB64), { headers: { "content-type": "image/png", "cache-control": "public, max-age=3600" } });\n'
    '    }\n'
    'if (url.pathname.startsWith("/images/")) {\n'
    '  const key = url.pathname.slice("/images/".length);\n'
    '  if (!env.IMAGES) return new Response("Not found", { status: 404 });\n'
    '  const obj = await env.IMAGES.get(key);\n'
    '  if (!obj) return new Response("Not found", { status: 404 });\n'
    '  return new Response(obj.body, { headers: { "content-type": "image/jpeg", "cache-control": "max-age=86400" } });\n'
    '}\n'
    '    return new Response(html, { headers: { "content-type": "text/html;charset=UTF-8", "cache-control": "no-cache" } });\n'
    '  }\n'
    '};\n'
)
open('worker.js', 'w').write(js)
print('built', len(js), 'bytes')
