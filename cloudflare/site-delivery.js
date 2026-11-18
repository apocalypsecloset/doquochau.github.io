/* Optional edge route for GitHub Pages origins. Images/API routes stay separate. */
const ALT_TARGET='https://apocalypsecloset.com/blog/alt-fashion-la-gi-va-tai-sao-no-quan-trong.html';
const ALT_PATHS=new Set([
  '/blog/alt-fashion-la-gi-va-tai-saon-quan-trong.html',
  '/blog/alt-style-la-gi-va-tai-sao-no-quan-important.html',
  '/blog/alt-fashion-la-gi-va-tai-sao-no-quan-torn.html',
  '/blog/alt-fashion-la-gi-va-tai-sao-no-quan-important.html',
  '/blog/alt-style-la-gi-va-tai-sao-no-quan-trong.html',
  '/blog/alt-fashion-la-gi-va-tai-saonquan-trong.html',
  '/blog/alt-fashion-la-gi-va-tai-sao-no-quan-tight.html',
  '/blog/alt-fashion-la-gi-va-tai-no-quan-trong.html',
  '/blog/alt-fashion-la-gi-va-tai-y-no-quan-tro-ng.html'
]);
export default {
  async fetch(request){
    const url=new URL(request.url);
    if(!['apocalypsecloset.com','www.apocalypsecloset.com'].includes(url.hostname))return fetch(request);
    const path=url.pathname;
    let destination=ALT_PATHS.has(path)?ALT_TARGET:['/en','/en/','/en/index.html','/index.html'].includes(path)?'https://apocalypsecloset.com/':null;
    if(destination){const target=new URL(destination);target.search=url.search;return new Response(null,{status:301,headers:{Location:target.href,'Cache-Control':'public, max-age=3600'}});}
    const upstream=await fetch(request);
    const response=new Response(upstream.body,upstream);
    const type=response.headers.get('Content-Type')||'';
    if(type.includes('text/html')){
      response.headers.set('Strict-Transport-Security','max-age=31536000');
      response.headers.set('X-Content-Type-Options','nosniff');
      response.headers.set('X-Frame-Options','SAMEORIGIN');
      response.headers.set('Content-Security-Policy',"frame-ancestors 'self'; object-src 'none'; base-uri 'self'");
      response.headers.set('Referrer-Policy','strict-origin-when-cross-origin');
      response.headers.set('Permissions-Policy','camera=(), microphone=(), geolocation=()');
    }
    const policy=response.headers.get('Cache-Control')||'';
    if(request.method==='GET'&&upstream.status===200&&!/private|no-store/i.test(policy)&&!response.headers.has('Set-Cookie')){
      if(/^\/assets\/journal\/[^/]+-[a-f0-9]{16}\.json$/.test(path)||(/^\/assets\/(?:js|css)\//.test(path)&&url.searchParams.has('v'))||/^\/assets\/css\/compiled\//.test(path))response.headers.set('Cache-Control','public, max-age=31536000, immutable');
      else if(/\.(?:js|css)$/.test(path))response.headers.set('Cache-Control','public, max-age=3600, stale-while-revalidate=86400');
      else if(/\.woff2$/.test(path))response.headers.set('Cache-Control','public, max-age=86400, stale-while-revalidate=604800');
    }
    return response;
  }
};
