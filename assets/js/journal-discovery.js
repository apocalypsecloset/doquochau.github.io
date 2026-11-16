/* Every article remains a real HTML anchor; filters progressively enhance discovery. */
(() => {
  const input=document.getElementById('journal-search');
  const more=document.getElementById('journal-more');
  const count=document.getElementById('journal-count');
  const reset=document.getElementById('journal-reset');
  const topics=document.querySelector('.journal-topics');
  const cards=[...document.querySelectorAll('#latest .cards a.card')];
  if(!input||!more||!count||!cards.length)return;
  const batch=24;
  let limit=batch,topic='all';
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('en').trim();
  const terms=cards.map(card=>normalize(card.textContent));
  const patterns={gothic:/\bgoth(?:ic)?\b|whimsigoth/,grunge:/\bgrunge\b/,graphic:/\bgraphic\b|\bt[- ]?shirts?\b|\btees?\b/,styling:/\bstyl(?:e|ing)\b|\boutfits?\b|\blayer(?:ing|s)?\b/};
  function render(){
    const words=normalize(input.value).split(/\s+/).filter(Boolean);
    const matches=cards.filter((card,i)=>words.every(word=>terms[i].includes(word))&&(topic==='all'||patterns[topic].test(terms[i])));
    const shown=new Set(matches.slice(0,limit));
    cards.forEach(card=>{card.hidden=!shown.has(card);});
    more.hidden=matches.length<=limit;
    count.textContent=matches.length?`Showing ${Math.min(limit,matches.length)} of ${matches.length} articles`:'No matching articles';
    if(reset)reset.hidden=topic==='all'&&!words.length;
    topics?.querySelectorAll('[data-topic]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.topic===topic)));
  }
  input.addEventListener('input',()=>{limit=batch;render();});
  more.addEventListener('click',()=>{const next=cards.filter(c=>!c.hidden).length;limit+=batch;render();cards.filter(c=>!c.hidden)[next]?.focus();});
  topics?.addEventListener('click',event=>{const b=event.target.closest('[data-topic]');if(!b)return;topic=b.dataset.topic;limit=batch;render();});
  reset?.addEventListener('click',()=>{topic='all';input.value='';limit=batch;render();input.focus();});
  if(topics)topics.hidden=false;
  render();
})();
