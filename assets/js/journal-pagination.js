/* Static archive pages remain crawlable; the full catalogue loads on demand. */
(() => {
  'use strict';
  const root=document.querySelector('[data-journal-catalog]');
  if(!root)return;
  const en=root.dataset.journalLocale==='en';
  const grid=document.querySelector(en?'#latest .cards':'#post-grid');
  const input=document.getElementById(en?'journal-search':'post-search');
  const count=document.getElementById(en?'journal-count':'results-count');
  const more=document.getElementById(en?'journal-more':'load-more-btn');
  const moreWrap=en?more:document.getElementById('load-more-wrap');
  const reset=document.getElementById('journal-reset');
  const nav=document.querySelector('.journal-pagination');
  const initial=grid.innerHTML;
  const initialCount=grid.children.length;
  const pageSize=30;
  let catalogue,loading,query='',category='all',tag='',limit=pageSize,sequence=0;
  const normalize=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[đĐ]/g,'d').toLocaleLowerCase().trim();
  const normalizeTag=s=>normalize(s).replace(/^#/,'').replace(/[^a-z0-9]+/g,'');
  const params=new URLSearchParams(location.search);
  const filters={
    style:['Aesthetic','Style Guide','Style Audit','Trend Anatomy','Material Ledger','Punk / Grunge','Goth','Dark Feminine','Aesthetic Guide','Dark / Alt','J-Fashion','Subculture / Street','Goth / Cyber','Retro / Subculture','Historical Fashion','Fashion Knowledge','Mainstream Style','J-Fashion / Gyaru','K-Fashion','Tailoring / Workwear','J-Fashion / Retro','Classic / Preppy Adjacent','J-Fashion / Streetwear','J-Fashion / Kawaii','Internet Aesthetic','Y2K / Retro','Contemporary Style'],
    mix:['Fit Lab','Dress Code Desk','Fashion Basics','Office Code','Item Guide'],shopping:['Shopping Guide','Garment Lab','Accessory Guide'],care:['Care Guide','Beauty Guide'],mindset:['Tâm Lý Học'],tips:['Tips']
  };
  const topics={gothic:/\bgoth(?:ic)?\b|whimsigoth/,grunge:/\bgrunge\b/,graphic:/\bgraphic\b|\bt[- ]?shirts?\b|\btees?\b/,styling:/\bstyl(?:e|ing)\b|\boutfits?\b|\blayer(?:ing|s)?\b/};
  function active(){return !!query||category!=='all'||!!tag;}
  function announce(text){if(count)count.textContent=text;}
  function buttons(){
    document.querySelectorAll(en?'.journal-topics [data-topic]':'#filter-bar [data-filter]').forEach(b=>{
      const on=(en?b.dataset.topic:b.dataset.filter)===category;
      b.setAttribute('aria-pressed',String(on));b.classList.toggle('active',on);
    });
    if(reset)reset.hidden=!active();
  }
  async function getCatalogue(){
    if(catalogue)return catalogue;
    if(!loading)loading=fetch(root.dataset.journalCatalog,{credentials:'same-origin'}).then(r=>{
      if(!r.ok)throw new Error('Catalogue unavailable');return r.json();
    }).then(rows=>{
      if(!Array.isArray(rows))throw new Error('Invalid catalogue');
      catalogue=rows.map(r=>({...r,normalized:normalize(r.search)}));return catalogue;
    }).catch(e=>{loading=null;throw e;});
    return loading;
  }
  function showInitial(){
    grid.innerHTML=initial;if(nav)nav.hidden=false;if(moreWrap)moreWrap.hidden=true;
    announce(en?`${initialCount} articles on this page · ${root.dataset.journalTotal} in the archive`:`${initialCount} bài trên trang này · ${root.dataset.journalTotal} bài trong thư viện`);
    buttons();
  }
  async function render(){
    const ticket=++sequence;
    buttons();
    if(!active()){showInitial();return;}
    announce(en?'Searching the archive…':'Đang tìm trong toàn bộ thư viện…');
    try{
      const rows=await getCatalogue();if(ticket!==sequence)return;
      const words=normalize(query).split(/\s+/).filter(Boolean);
      const matches=rows.filter(r=>words.every(w=>r.normalized.includes(w))&&
        (category==='all'||(en?topics[category]?.test(r.normalized):filters[category]?.includes(r.category)))&&
        (!tag||String(r.tags||'').split(/\s+/).some(t=>normalizeTag(t)===tag)));
      grid.innerHTML=matches.slice(0,limit).map(r=>r.html).join('');
      if(nav)nav.hidden=true;if(moreWrap)moreWrap.hidden=matches.length<=limit;
      announce(matches.length?(en?`Showing ${Math.min(limit,matches.length)} of ${matches.length} articles`:`Đang hiển thị ${Math.min(limit,matches.length)}/${matches.length} bài viết`):(en?'No matching articles':'Không có bài viết phù hợp'));
    }catch(_){
      if(ticket!==sequence)return;
      // Keep the already-rendered archive usable, including real page links.
      if(nav)nav.hidden=false;if(moreWrap)moreWrap.hidden=true;
      announce(en?'Search is temporarily unavailable. Browse the archive pages below.':'Tìm kiếm tạm thời chưa tải được. Bạn có thể dùng các trang bên dưới.');
    }
  }
  let timer;
  input?.addEventListener('input',()=>{query=input.value;limit=pageSize;clearTimeout(timer);timer=setTimeout(render,160);});
  document.querySelector(en?'.journal-topics':'#filter-bar')?.addEventListener('click',event=>{
    const b=event.target.closest(en?'[data-topic]':'[data-filter]');if(!b)return;
    category=en?b.dataset.topic:b.dataset.filter;tag='';limit=pageSize;render();
  });
  more?.addEventListener('click',()=>{limit+=pageSize;render();});
  reset?.addEventListener('click',()=>{query='';category='all';tag='';limit=pageSize;if(input)input.value='';render();input?.focus();});
  document.querySelector('.journal-topics')?.removeAttribute('hidden');
  if(en){if(topics[params.get('category')])category=params.get('category');}
  else{if(filters[params.get('category')])category=params.get('category');tag=normalizeTag(params.get('tag'));}
  if(params.get('q')){query=params.get('q');if(input)input.value=query;}
  render();
})();
