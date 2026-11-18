const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..');
// The exact E2 successor adds four dated collections; all functional checks use the real 442-card DOM.
const englishRelease=JSON.parse(fs.readFileSync(path.join(root,'docs/link-fix-2026-11-17/batch40-release.json'),'utf8'));
const journalBytes=fs.readFileSync(path.join(root,'en/blog.html'));
const journalHash=require('node:crypto').createHash('sha256').update(journalBytes).digest('hex');
const journalLFHash=require('node:crypto').createHash('sha256').update(journalBytes.toString('utf8').replace(/\r\n/g,'\n')).digest('hex');
const journalPin=englishRelease.files['en/blog.html'];
let historicalJournalHash=journalHash;
let imageJournalHash=journalLFHash;
const metadataReleasePath=path.join(root,'data/search-metadata-2026-11-18/release.json');
if(fs.existsSync(metadataReleasePath)){
 const metadataPin=JSON.parse(fs.readFileSync(metadataReleasePath,'utf8')).files['en/blog.html'];
 assert.equal(journalLFHash,metadataPin.after,'Only the exact search metadata successor is accepted');
 imageJournalHash=metadataPin.before;
}
const imageReleasePath=path.join(root,'data/blog-image-seo-2026-11-18/html-changes.json');
if(fs.existsSync(imageReleasePath)){
 const imagePin=JSON.parse(fs.readFileSync(imageReleasePath,'utf8')).files['en/blog.html'];
 assert.equal(imageJournalHash,imagePin.after,'Only the exact image release successor is accepted');
 historicalJournalHash=imagePin.before;
}
assert.ok([journalPin.after_sha256,journalPin.after_crlf_sha256].includes(historicalJournalHash));
const englishExpected=englishRelease.english_journal;
assert.equal(englishExpected.count,442);assert.equal(englishExpected.old_count,438);

test('every English catalogue and featured card has a responsive thumbnail without JavaScript',()=>{
 const dom=new JSDOM(journalBytes.toString('utf8'));
 try{
  const cards=[...dom.window.document.querySelectorAll('#latest .cards a.card,.journal-featured-card')];
  assert.equal(cards.length,445);
  for(const card of cards){
   const images=card.querySelectorAll('img');assert.equal(images.length,1);
   const image=images[0];assert.ok(image.alt.trim());
   assert.ok(Number(image.width)>0&&Number(image.height)>0);
   assert.ok(image.getAttribute('srcset').split(',').length>=2);
   assert.ok(fs.existsSync(path.join(root,image.getAttribute('src'))));
  }
 }finally{dom.window.close();}
});
test('journal exposes every article without JavaScript and supports pagination, search and reset',()=>{
 const dom=new JSDOM(fs.readFileSync(path.join(root,'en/blog.html'),'utf8'),{runScripts:'outside-only'});
 try {
  const w=dom.window,d=w.document,cards=[...d.querySelectorAll('#latest .cards a.card')];
  assert.equal(cards.length,englishExpected.count);assert.equal(new Set(cards.map(x=>x.getAttribute('href'))).size,englishExpected.count);
  assert.ok(cards.every(x=>!x.hidden));
  const dates=cards.map(x=>x.getAttribute('data-published'));
  assert.ok(dates.every(x=>x!==null));assert.deepEqual(dates,[...dates].sort().reverse());
  assert.equal(dates[0],englishExpected.latest_date);
  assert.equal(cards[0].getAttribute('href'),englishExpected.first_url);
  w.eval(fs.readFileSync(path.join(root,'assets/js/journal-discovery.js'),'utf8'));
  const visible=()=>cards.filter(x=>!x.hidden),input=d.getElementById('journal-search'),more=d.getElementById('journal-more');
  assert.equal(visible().length,24);more.click();assert.equal(visible().length,48);
  const search=value=>{input.value=value;input.dispatchEvent(new w.Event('input'));};
  search('goth');assert.ok(visible().length>0);assert.ok(visible().every(x=>x.textContent.toLowerCase().includes('goth')));
  search('zzzz-no-article-matches-zzzz');assert.equal(visible().length,0);assert.equal(more.hidden,true);assert.equal(d.getElementById('journal-count').textContent,'No matching articles');
  search('');assert.equal(visible().length,24);assert.equal(more.hidden,false);
  while(!more.hidden)more.click();assert.equal(visible().length,englishExpected.count);
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
  w.eval(code);const cards=[...d.querySelectorAll('#post-grid a.post-card')];
  const added=['/blog/phoi-mau-quan-ao-nu.html','/blog/chon-trang-phuc-nu-theo-dia-diem-va-dip.html','/blog/cach-cham-soc-do-nu.html','/blog/chon-toc-va-makeup-theo-trang-phuc.html'];
  assert.equal(expected.size,423);assert.equal(cards.length,427);
  assert.deepEqual(cards.filter(c=>!expected.has(c.getAttribute('href'))).map(c=>c.getAttribute('href')).sort(),[...added].sort());
  const originalCards=cards.filter(c=>expected.has(c.getAttribute('href')));assert.equal(originalCards.length,expected.size);
  assert.equal(new Set(cards.map(c=>c.getAttribute('href'))).size,427);
  assert.ok(originalCards.every(c=>c.dataset.search===expected.get(c.getAttribute('href'))));
  const visible=()=>cards.filter(c=>!c.hidden);assert.equal(visible().length,12);d.getElementById('load-more-btn').click();assert.equal(visible().length,18);
  const input=d.getElementById('post-search');input.value='polyester';input.dispatchEvent(new w.Event('input'));assert.ok(visible().length>0);assert.ok(visible().every(c=>c.dataset.search.includes('polyester')));
  input.value='';input.dispatchEvent(new w.Event('input'));assert.equal(visible().length,12);
 }finally{dom.window.close();old.window.close();}
});

test('topic shortcuts combine with search, reset, pagination and retained article URLs',()=>{
 const dom=new JSDOM(fs.readFileSync(path.join(root,'en/blog.html'),'utf8'),{runScripts:'outside-only'});
 try{
  const w=dom.window,d=w.document,cards=[...d.querySelectorAll('#latest .cards a.card')];
  const urls=cards.map(c=>c.getAttribute('href'));
  w.eval(fs.readFileSync(path.join(root,'assets/js/journal-discovery.js'),'utf8'));
  const visible=()=>cards.filter(c=>!c.hidden);
  d.querySelector('[data-topic=gothic]').click();
  assert.ok(visible().length>0);assert.ok(visible().every(c=>/goth|whimsigoth/i.test(c.textContent)));
  assert.equal(d.querySelector('[data-topic=gothic]').getAttribute('aria-pressed'),'true');
  const input=d.querySelector('#journal-search');input.value='romantic';input.dispatchEvent(new w.Event('input'));
  assert.ok(visible().length>0);assert.ok(visible().every(c=>/romantic/i.test(c.textContent)));
  d.querySelector('#journal-reset').click();assert.equal(visible().length,24);assert.equal(input.value,'');
  assert.equal(d.querySelector('[data-topic=all]').getAttribute('aria-pressed'),'true');
  assert.deepEqual(cards.map(c=>c.getAttribute('href')),urls);
 }finally{dom.window.close();}
});
