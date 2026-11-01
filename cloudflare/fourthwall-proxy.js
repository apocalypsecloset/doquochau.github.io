/**
 * Fourthwall Storefront API reverse proxy for Apocalypse Closet.
 * Deploy to Cloudflare Workers, add secret FOURTHWALL_STOREFRONT_TOKEN.
 * Never commit that token, Open API credentials, or Stripe secrets to GitHub.
 */
const BASE = "https://storefront-api.fourthwall.com";
const ALLOWED_ORIGINS = new Set([
  "https://apocalypsecloset.com",
  "https://www.apocalypsecloset.com",
  "https://doquochau-github-io.pages.dev",
  "http://localhost:8000"
]);
function validPath(path, method) {
  if (method === "GET") return /^\/v1\/(?:shop|products\/[a-z0-9-]+|collections(?:\/[a-z0-9-]+(?:\/products)?)?|carts\/[a-zA-Z0-9-]{1,64})$/.test(path);
  if (method === "POST") return path === "/v1/carts" || /^\/v1\/carts\/[a-zA-Z0-9-]{1,64}\/(?:add|change|remove)$/.test(path);
  return false;
}
export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin");
    const allowed = origin && ALLOWED_ORIGINS.has(origin);
    const cors = {
      "Access-Control-Allow-Origin": allowed ? origin : "https://apocalypsecloset.com",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin",
      "Cache-Control": "no-store"
    };
    const respond = (data, status) => new Response(JSON.stringify(data), {
      status, headers: { ...cors, "Content-Type": "application/json; charset=utf-8" }
    });
    if (request.method === "OPTIONS") {
      return allowed ? new Response(null, { status: 204, headers: cors }) : respond({error:"Forbidden origin"},403);
    }
    if (origin && !allowed) return respond({error:"Forbidden origin"},403);
    const url = new URL(request.url);
    if (!validPath(url.pathname,request.method)) return respond({error:"Route or method not allowed"},404);
    if (!env.FOURTHWALL_STOREFRONT_TOKEN) return respond({error:"Missing Worker secret"},503);
    const upstream = new URL(BASE + url.pathname);
    upstream.searchParams.set("storefront_token", env.FOURTHWALL_STOREFRONT_TOKEN);
    for (const param of ["page","size"]) {
      const value = url.searchParams.get(param);
      if (value && /^\d{1,3}$/.test(value)) upstream.searchParams.set(param,value);
    }
    try {
      let body;
      if (request.method === "POST") {
        const length = Number(request.headers.get("content-length") || 0);
        if (length > 4096) return respond({error:"Body too large"},413);
        body = await request.text();
        if (body.length > 4096) return respond({error:"Body too large"},413);
        JSON.parse(body);
      }
      const upstreamResponse = await fetch(upstream.toString(), {
        method: request.method,
        headers: request.method === "POST" ? { "Content-Type": "application/json" } : {},
        body
      });
      return new Response(upstreamResponse.body, {
        status: upstreamResponse.status,
        headers: { ...cors, "Content-Type": upstreamResponse.headers.get("Content-Type") || "application/json; charset=utf-8" }
      });
    } catch (error) {
      return respond({error:"Fourthwall upstream request failed"},502);
    }
  }
};
