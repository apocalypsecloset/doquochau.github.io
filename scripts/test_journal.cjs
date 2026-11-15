const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..');
test('journal exposes every article without JavaScript and supports pagination, search and reset',()=>{
 const dom=new JSDOM(fs.readFileSync(path.join(root,'en/blog.html'),'utf8'),{runScripts:'outside-only'});
 try {
  const w=dom.window,d=w.document,cards=[...d.querySelectorAll('#latest .cards a.card')];
  assert.equal(cards.length,438);assert.equal(new Set(cards.map(x=>x.getAttribute('href'))).size,438);
  assert.ok(cards.every(x=>!x.hidden));
  const dates=cards.map(x=>x.getAttribute('data-published'));
  assert.ok(dates.every(x=>x!==null));assert.deepEqual(dates,[...dates].sort().reverse());
  assert.equal(dates[0],'2026-11-15');
  assert.equal(cards[0].getAttribute('href'),'/en/blog/1920s-fashion.html');
  w.eval(fs.readFileSync(path.join(root,'assets/js/journal-discovery.js'),'utf8'));
  const visible=()=>cards.filter(x=>!x.hidden),input=d.getElementById('journal-search'),more=d.getElementById('journal-more');
  assert.equal(visible().length,24);more.click();assert.equal(visible().length,48);
  const search=value=>{input.value=value;input.dispatchEvent(new w.Event('input'));};
  search('goth');assert.ok(visible().length>0);assert.ok(visible().every(x=>x.textContent.toLowerCase().includes('goth')));
  search('zzzz-no-article-matches-zzzz');assert.equal(visible().length,0);assert.equal(more.hidden,true);assert.equal(d.getElementById('journal-count').textContent,'No matching articles');
  search('');assert.equal(visible().length,24);assert.equal(more.hidden,false);
  while(!more.hidden)more.click();assert.equal(visible().length,438);
 } finally {dom.window.close();}
});
