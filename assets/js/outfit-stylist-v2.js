(() => {
  'use strict';
  const data = Array.isArray(window.AC_BUILDER_OUTFITS) ? window.AC_BUILDER_OUTFITS : [];
  if (!data.length) return;

  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => Array.from(root.querySelectorAll(s));
  const STYLES = ['Dark Feminine','Baddie Streetwear','Goth','E-Girl','Punk / Grunge'];
  const DNA_KEY = 'ac_style_dna_v1';
  const QUIZ_ROUNDS = 8;
  const adjacency = {
    'Dark Feminine': {'Goth':1.15,'Baddie Streetwear':.95,'Punk / Grunge':.35},
    'Baddie Streetwear': {'Dark Feminine':.95,'E-Girl':.75,'Punk / Grunge':.45},
    'Goth': {'Dark Feminine':1.05,'Punk / Grunge':.95,'E-Girl':.3},
    'E-Girl': {'Punk / Grunge':.85,'Baddie Streetwear':.75,'Goth':.25},
    'Punk / Grunge': {'Goth':.9,'E-Girl':.7,'Baddie Streetwear':.4}
  };
  const moodMap = {
    'Dark Feminine':['Dark','Confident','Feminine'],
    'Baddie Streetwear':['Bold','Confident','Street'],
    'Goth':['Dark','Mysterious','Dramatic'],
    'E-Girl':['Alt','Playful','Cute'],
    'Punk / Grunge':['Rebellious','Raw','Layered']
  };

  let quizRound = 0;
  let quizScores = Object.fromEntries(STYLES.map(s=>[s,0]));
  let pickedLooks = [];
  let shownIds = [];
  let currentPair = [];
  let dna = loadDNA();
  let lastRanked = [];

  const track = (name, params={}) => {
    try {
      if (typeof window.acTrack === 'function') window.acTrack(name, params);
      else if (typeof window.gtag === 'function') window.gtag('event', name, params);
      else { window.dataLayer = window.dataLayer || []; window.dataLayer.push({event:name, ...params}); }
    } catch (_) {}
  };

  function loadDNA(){
    try {
      const v=JSON.parse(localStorage.getItem(DNA_KEY)||'null');
      if(v && v.percentages && STYLES.every(s=>Number.isFinite(v.percentages[s]))) return v;
    } catch(_){}
    return null;
  }
  function saveDNA(v){ try{localStorage.setItem(DNA_KEY,JSON.stringify(v));}catch(_){} }
  function shuffle(arr){
    const a=[...arr];
    for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
    return a;
  }
  function imageUrls(o){
    const name=String(o.img||'').split('/').pop();
    return {mobile:`/images-mobile/badgirl-outfits/${name}`, mobileHd:`/images-mobile-hd/badgirl-outfits/${name}`, grid:`/images-grid/badgirl-outfits/${name}`, full:`/images/badgirl-outfits/${name}`};
  }
  function titleShort(o){ return String(o.title||o.tag).replace(/^Look #\d+\s*/i,'').replace(/^[-–—:]\s*/,''); }
  function styleLabel(s){ return s==='Baddie Streetwear'?'Baddie':s; }
  function pickFromStyle(style, exclude=[]){
    const pool=data.filter(o=>o.primaryStyle===style && !exclude.includes(o.id));
    return pool[Math.floor(Math.random()*pool.length)] || data[Math.floor(Math.random()*data.length)];
  }
  function nextPair(){
    const schedule=[
      ['Dark Feminine','Baddie Streetwear'],
      ['Goth','E-Girl'],
      ['Punk / Grunge','Dark Feminine'],
      ['Baddie Streetwear','Goth'],
      ['E-Girl','Dark Feminine'],
      ['Punk / Grunge','Baddie Streetwear'],
      ['Goth','Punk / Grunge'],
      ['E-Girl','Baddie Streetwear']
    ];
    const pairStyles=schedule[quizRound % schedule.length];
    const used=[...shownIds];
    currentPair=shuffle([pickFromStyle(pairStyles[0],used),pickFromStyle(pairStyles[1],used)]);
    shownIds.push(...currentPair.map(x=>x.id));
    renderPair();
  }
  function renderPair(){
    const pair=$('#sty-quiz-pair'); if(!pair) return;
    pair.innerHTML='';
    currentPair.forEach((o,idx)=>{
      if(idx===1){const vs=document.createElement('div');vs.className='sty-vs';vs.textContent='VS';pair.appendChild(vs);}
      const btn=document.createElement('button');btn.type='button';btn.className='sty-choice';btn.dataset.choice=o.id;
      const u=imageUrls(o);
      btn.innerHTML=`<img src="${u.mobileHd}" srcset="${u.mobile} 240w, ${u.mobileHd} 480w, ${u.grid} ${o.width||720}w" sizes="(max-width:620px) 42vw, 320px" width="${o.width||720}" height="${o.height||1280}" alt="${o.tag} ${styleLabel(o.primaryStyle)}" decoding="async"><span class="sty-choice-meta"><b>${o.tag}</b>${styleLabel(o.primaryStyle)}</span>`;
      btn.addEventListener('click',()=>choose(o));
      pair.appendChild(btn);
    });
    const progress=$('#sty-quiz-progress span'); if(progress) progress.style.width=`${Math.round((quizRound/QUIZ_ROUNDS)*100)}%`;
    const label=$('#sty-quiz-label'); if(label) label.innerHTML=`<span>Chọn outfit đúng gu bạn hơn</span><span>${quizRound+1}/${QUIZ_ROUNDS}</span>`;
  }
  function choose(o){
    pickedLooks.push(o);
    quizScores[o.primaryStyle]=(quizScores[o.primaryStyle]||0)+4;
    Object.entries(adjacency[o.primaryStyle]||{}).forEach(([s,w])=>{quizScores[s]=(quizScores[s]||0)+w;});
    quizRound++;
    track('style_discovery_choice',{round:quizRound,outfit_id:o.id,style:o.primaryStyle});
    if(quizRound>=QUIZ_ROUNDS) finishQuiz(); else nextPair();
  }
  function buildDNA(){
    const max=Math.max(...STYLES.map(s=>quizScores[s]),1);
    const percentages={};
    STYLES.forEach(s=>{percentages[s]=Math.max(18,Math.min(94,Math.round(18+(quizScores[s]/max)*76)));});
    const sorted=[...STYLES].sort((a,b)=>percentages[b]-percentages[a]);
    const moods=[]; sorted.slice(0,3).forEach(s=>(moodMap[s]||[]).forEach(m=>{if(!moods.includes(m))moods.push(m);}));
    const colorCount={}; const fitCount={}; const footwearCount={};
    pickedLooks.forEach(o=>{
      const c=o.filters?.color; if(c) colorCount[c]=(colorCount[c]||0)+1;
      (o.filters?.fit||[]).forEach(f=>fitCount[f]=(fitCount[f]||0)+1);
      const fw=o.filters?.footwear;if(fw)footwearCount[fw]=(footwearCount[fw]||0)+1;
    });
    const topKeys=(obj,n)=>Object.keys(obj).sort((a,b)=>obj[b]-obj[a]).slice(0,n);
    return {percentages,topStyles:sorted,moods:moods.slice(0,3),colors:topKeys(colorCount,3),fits:topKeys(fitCount,2),footwear:topKeys(footwearCount,2),pickedIds:pickedLooks.map(o=>o.id),updatedAt:Date.now()};
  }
  function finishQuiz(){
    dna=buildDNA(); saveDNA(dna); renderDNA();
    track('complete_style_discovery',{top_style:dna.topStyles[0],top_score:dna.percentages[dna.topStyles[0]],rounds:QUIZ_ROUNDS});
  }
  function renderDNA(){
    if(!dna) return;
    const quiz=$('#sty-quiz'); const box=$('#sty-dna'); if(quiz) quiz.classList.add('is-hidden'); if(box) box.classList.add('is-active');
    const top=$('#sty-dna-top'); if(top) top.textContent=styleLabel(dna.topStyles[0]);
    const bars=$('#sty-dna-bars'); if(bars){
      bars.innerHTML=dna.topStyles.map(s=>`<div class="sty-dna-row"><span>${styleLabel(s)}</span><div class="sty-dna-bar"><i style="width:${dna.percentages[s]}%"></i></div><b>${dna.percentages[s]}%</b></div>`).join('');
    }
    const mood=$('#sty-dna-mood'); if(mood) mood.textContent=(dna.moods||[]).join(' · ') || 'Dark · Confident · Alt';
    const colors=$('#sty-dna-colors'); if(colors) colors.textContent=(dna.colors||[]).join(' · ') || 'Đen · Xám / Bạc';
    const helper=$('#sty-today-helper'); if(helper) helper.innerHTML=`Style DNA đang được dùng để xếp hạng Look. Gu mạnh nhất của bạn: <strong>${styleLabel(dna.topStyles[0])} ${dna.percentages[dna.topStyles[0]]}%</strong>.`;
  }
  function resetQuiz(){
    quizRound=0;quizScores=Object.fromEntries(STYLES.map(s=>[s,0]));pickedLooks=[];shownIds=[];currentPair=[];dna=null;
    try{localStorage.removeItem(DNA_KEY);}catch(_){}
    $('#sty-quiz')?.classList.remove('is-hidden');$('#sty-dna')?.classList.remove('is-active');
    nextPair();track('restart_style_discovery',{source_page:'app_phoi_do'});
  }

  function selectedValue(group){ return $(`.sty-chip.is-active[data-group="${group}"]`)?.dataset.value || ''; }
  function bindChips(){
    $$('.sty-chip').forEach(btn=>btn.addEventListener('click',()=>{
      const group=btn.dataset.group; $$(`.sty-chip[data-group="${group}"]`).forEach(x=>x.classList.remove('is-active')); btn.classList.add('is-active');
    }));
  }
  function recommendationState(){return {occasion:selectedValue('occasion'),bottom:selectedValue('bottom'),footwear:selectedValue('footwear'),complexity:selectedValue('complexity')};}
  function scoreOutfit(o,s){
    let got=0,possible=0;const reasons=[];
    if(dna){
      possible+=60;const p=dna.percentages[o.primaryStyle]||18;got+=60*(p/100);
      if(p>=75) reasons.push(`${styleLabel(o.primaryStyle)} ${p}% DNA`); else if(p>=55) reasons.push(`Hợp gu ${styleLabel(o.primaryStyle)}`);
    }
    if(s.occasion){possible+=20;if((o.filters?.occasions||[]).includes(s.occasion)){got+=20;reasons.push(s.occasion);}}
    if(s.bottom){possible+=8;if(o.filters?.bottom===s.bottom){got+=8;reasons.push(s.bottom);}}
    if(s.footwear){possible+=8;if(o.filters?.footwear===s.footwear){got+=8;reasons.push(s.footwear);}}
    if(s.complexity){possible+=4;if(o.filters?.complexity===s.complexity){got+=4;reasons.push(s.complexity);}}
    if(!possible){possible=1;got=.72;}
    let pct=Math.round((got/possible)*100);
    if(dna || Object.values(s).some(Boolean)) pct=Math.max(32,Math.min(98,pct));
    else pct=0;
    return {pct,reasons};
  }
  function rank(s){
    return data.map(o=>({o,...scoreOutfit(o,s),tie:Math.random()})).sort((a,b)=>b.pct-a.pct || b.reasons.length-a.reasons.length || a.tie-b.tie);
  }
  function renderResults(scroll=true){
    const s=recommendationState(); lastRanked=rank(s); const list=lastRanked.slice(0,3); const root=$('#sty-results'); if(!root)return;
    root.innerHTML='';
    list.forEach((r,index)=>{
      const o=r.o,u=imageUrls(o),card=document.createElement('article');card.className='sty-result-card';
      const badge=r.pct?`<span class="sty-match"><b>${r.pct}%</b>match</span>`:`<span class="sty-match"><b>NEW</b>discover</span>`;
      const reasons=(r.reasons.length?r.reasons:[(o.filters?.occasions||[])[0],o.filters?.color]).filter(Boolean).slice(0,3);
      card.innerHTML=`<a class="sty-result-media" href="/outfits/${o.slug}.html" data-track-look="${o.id}">${badge}<img src="${u.grid}" srcset="${u.mobile} 240w, ${u.mobileHd} 480w, ${u.grid} ${o.width||720}w" sizes="(max-width:620px) 92vw, (max-width:960px) 46vw, 31vw" width="${o.width||720}" height="${o.height||1280}" loading="lazy" decoding="async" alt="${o.tag} ${styleLabel(o.primaryStyle)}"></a><div class="sty-result-body"><div class="sty-result-top"><b>${o.tag}</b><span>${styleLabel(o.primaryStyle)}</span></div><p>${titleShort(o)}</p><div class="sty-reasons">${reasons.map(x=>`<span>${x}</span>`).join('')}</div><div class="sty-result-actions"><a href="/outfits/${o.slug}.html" data-track-look="${o.id}">Xem Look</a><button type="button" data-quick="${o.id}">Xem nhanh</button></div></div>`;
      root.appendChild(card);
    });
    const head=$('#sty-results-copy'); if(head){
      const signals=[dna?`Style DNA: ${styleLabel(dna.topStyles[0])}`:'',s.occasion,s.bottom,s.footwear,s.complexity].filter(Boolean);
      head.textContent=signals.length?`Xếp hạng theo ${signals.join(' · ')}.`:'Chọn nhu cầu hoặc khám phá Style DNA để cá nhân hóa Match %.';
    }
    track('complete_outfit_recommender',{top_outfit:list[0]?.o.id||'',top_match:list[0]?.pct||0,occasion:s.occasion||'all',bottom:s.bottom||'all',footwear:s.footwear||'all',complexity:s.complexity||'all',has_style_dna:!!dna});
    if(scroll) $('#sty-results-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});
  }

  function openDrawer(id){
    const r=lastRanked.find(x=>x.o.id===id) || {o:data.find(x=>x.id===id),...scoreOutfit(data.find(x=>x.id===id),recommendationState())}; if(!r.o)return;
    const o=r.o,u=imageUrls(o),shell=$('#sty-drawer-shell'),content=$('#sty-drawer-content'); if(!shell||!content)return;
    const reasons=(r.reasons||[]).slice(0,4);
    content.innerHTML=`<div class="sty-drawer-match">${r.pct?`${r.pct}% MATCH VỚI LỰA CHỌN CỦA BẠN`:'GỢI Ý KHÁM PHÁ'}</div><h3>${o.tag}</h3><div class="sty-drawer-meta">${styleLabel(o.primaryStyle)} · ${(o.filters?.occasions||[]).join(' · ')} · ${o.filters?.color||''}</div><img src="${u.grid}" srcset="${u.mobileHd} 480w, ${u.grid} ${o.width||720}w, ${u.full} ${o.fullWidth||1080}w" sizes="min(440px,92vw)" width="${o.width||720}" height="${o.height||1280}" alt="${o.tag} ${styleLabel(o.primaryStyle)}"><ul class="sty-drawer-list">${(o.coreItems||[]).map(i=>`<li><b>${i.label}</b><span>${i.name}</span></li>`).join('')}</ul><div class="sty-drawer-why"><strong>Vì sao Look này được chọn?</strong><br>${reasons.length?reasons.join(' · '):'Look này đang nằm trong nhóm khám phá từ 136 outfit hiện có.'}</div><div class="sty-drawer-actions"><a href="/outfits/${o.slug}.html" data-track-look="${o.id}">XEM CHI TIẾT LOOK →</a><a href="/outfits/${o.slug}.html#shop-items" data-track-look="${o.id}">XEM CÁC MÓN PHỐI ĐỒ</a><a href="/?utm_source=outfits&utm_medium=shop-link#shop">XEM ÁO APOCALYPSE CLOSET</a></div>`;
    shell.hidden=false;document.body.style.overflow='hidden';$('#sty-drawer-close')?.focus();
    track('open_stylist_look',{outfit_id:o.id,match:r.pct||0});
  }
  function closeDrawer(){const shell=$('#sty-drawer-shell');if(shell)shell.hidden=true;document.body.style.overflow='';}
  function toast(msg){let t=$('#sty-toast');if(!t)return;t.textContent=msg;t.classList.add('is-show');clearTimeout(t._timer);t._timer=setTimeout(()=>t.classList.remove('is-show'),2000);}

  function init(){
    bindChips();
    $('#sty-reset-dna')?.addEventListener('click',resetQuiz);
    $('#sty-use-dna')?.addEventListener('click',()=>{renderResults(true);toast('Đã dùng Style DNA để phối Look');});
    $('#sty-today-submit')?.addEventListener('click',()=>renderResults(true));
    $('#sty-hero-discover')?.addEventListener('click',()=>{$('#sty-discovery')?.scrollIntoView({behavior:'smooth',block:'start'});});
    $('#sty-hero-recommend')?.addEventListener('click',()=>{$('#sty-today')?.scrollIntoView({behavior:'smooth',block:'start'});});
    $('#sty-results')?.addEventListener('click',e=>{const q=e.target.closest('[data-quick]');if(q){e.preventDefault();openDrawer(q.dataset.quick);return;}const a=e.target.closest('a[data-track-look]');if(a)track('click_builder_outfit',{outfit_id:a.dataset.trackLook,source_page:'app_phoi_do_v2'});});
    $('#sty-drawer-shell')?.addEventListener('click',e=>{if(e.target.matches('[data-close-drawer]'))closeDrawer();const a=e.target.closest('a[data-track-look]');if(a)track('click_builder_outfit',{outfit_id:a.dataset.trackLook,source_page:'stylist_drawer'});});
    document.addEventListener('keydown',e=>{if(e.key==='Escape' && !$('#sty-drawer-shell')?.hidden) closeDrawer();});
    if(dna) renderDNA(); else nextPair();
    renderResults(false);
    track('view_style_discovery',{source_page:'app_phoi_do'});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
