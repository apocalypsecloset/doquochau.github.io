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
test('Vietnamese journal reconstructs every original search string and retains load more and reset',()=>{
 const {execFileSync}=require('node:child_process');
 const old=new JSDOM(execFileSync('git',['show','22b72f2:blog.html'],{cwd:root,encoding:'utf8',maxBuffer:2e6}));
 const expected=new Map([...old.window.document.querySelectorAll('#post-grid a.post-card')].map(c=>[c.getAttribute('href'),c.dataset.search]));
 const dom=new JSDOM(fs.readFileSync(path.join(root,'blog.html'),'utf8'),{url:'https://apocalypsecloset.com/blog.html',runScripts:'outside-only'});
 try{
  const w=dom.window,d=w.document;w.scrollTo=()=>{};
  const code=[...d.querySelectorAll('script:not([src])')].find(s=>s.textContent.includes('const BATCH = 12;')).textContent;
  w.eval(code);const cards=[...d.querySelectorAll('#post-grid a.post-card')];assert.equal(cards.length,expected.size);
  assert.ok(cards.every(c=>c.dataset.search===expected.get(c.getAttribute('href'))));
  const visible=()=>cards.filter(c=>!c.hidden);assert.equal(visible().length,12);d.getElementById('load-more-btn').click();assert.equal(visible().length,18);
  const input=d.getElementById('post-search');input.value='polyester';input.dispatchEvent(new w.Event('input'));assert.ok(visible().length>0);assert.ok(visible().every(c=>c.dataset.search.includes('polyester')));
  input.value='';input.dispatchEvent(new w.Event('input'));assert.equal(visible().length,12);
 }finally{dom.window.close();old.window.close();}
});
