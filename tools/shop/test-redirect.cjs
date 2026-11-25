const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
  const source=fs.readFileSync(path.join(__dirname,'../../cloudflare/site-delivery.js'),'utf8');
  const worker=(await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'))).default;
  const original=global.fetch;let upstreamCalls=0;
  global.fetch=async()=>{upstreamCalls++;return new Response('unchanged',{headers:{'Content-Type':'text/plain'}});};
  try{
    const cases=[
      ['http://www.apocalypsecloset.com/','https://apocalypsecloset.com/'],
      ['http://www.apocalypsecloset.com/en/blog.html?utm_source=test','https://apocalypsecloset.com/en/blog.html?utm_source=test'],
      ['http://apocalypsecloset.com/products/tee/?variant=123','https://apocalypsecloset.com/products/tee/?variant=123'],
      ['https://www.apocalypsecloset.com/index.html?a=1','https://apocalypsecloset.com/?a=1'],
      ['https://apocalypsecloset.com/index.html','https://apocalypsecloset.com/']];
    for(const [from,to] of cases){const r=await worker.fetch(new Request(from));assert.equal(r.status,301);assert.equal(r.headers.get('Location'),to);}
    assert.equal(upstreamCalls,0);
    const canonical=await worker.fetch(new Request('https://apocalypsecloset.com/en/blog.html?x=1'));
    assert.equal(canonical.status,200);assert.equal(await canonical.text(),'unchanged');
    const other=await worker.fetch(new Request('https://example.com/'));
    assert.equal(await other.text(),'unchanged');assert.equal(upstreamCalls,2);
    console.log('PASS: canonical redirect cases preserve path/query, no upstream hop, canonical/other hosts unchanged');
  }finally{global.fetch=original;}
})().catch(e=>{console.error(e);process.exitCode=1;});
