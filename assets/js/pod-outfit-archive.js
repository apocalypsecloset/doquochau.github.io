/* Reuse Apocalypse Closet original 136 outfit images as a non-affiliate inspiration gallery. */
(function(){
'use strict';
const section=document.querySelector('#outfit-archive');
const grid=document.querySelector('#ac-archive-grid');
const filters=document.querySelector('#ac-archive-filters');
const shuffleBtn=document.querySelector('#ac-archive-shuffle');
const count=document.querySelector('#ac-archive-count');
const dialog=document.querySelector('#ac-archive-lightbox');
const photo=document.querySelector('#ac-archive-lightbox-photo');
const caption=document.querySelector('#ac-archive-dialog-title');
const categoryCaption=document.querySelector('#ac-archive-dialog-category');
if(!section || !grid || !filters || !shuffleBtn || !dialog) return;
const source=Array.isArray(window.outfits) ? window.outfits.filter(x =>
 x && typeof x.img==='string' && /^\/images\/badgirl-outfits\/[\w.-]+\.webp$/i.test(x.img)
 && typeof x.primaryStyle==='string' && typeof x.id==='string') : [];
if(!source.length){
 count.textContent='THE ORIGINAL LOOK ARCHIVE IS TEMPORARILY UNAVAILABLE.';
 const a=document.createElement('a');a.className='ac-btn';a.href='/phoi-do-nu-ca-tinh.html';a.textContent='VIEW STYLE ARCHIVE ↗';grid.append(a);
 return;
}
const queues=new Map();
const size=12;
let active='all';
let previousOpen=null;
function shuffle(array){
 for(let i=array.length-1;i>0;i--){
   const j=Math.floor(Math.random()*(i+1));
   [array[i],array[j]]=[array[j],array[i]];
 }
 return array;
}
function pool(style){return style==='all'?source:source.filter(x=>x.primaryStyle===style);}
function queueFor(style){
 let q=queues.get(style);
 if(!q||!q.length){q=shuffle(pool(style).slice());queues.set(style,q);}
 return q;
}
function draw(style){
 const subset=pool(style);
 if(!subset.length) return [];
 const picked=[];
 const used=new Set();
 let guard=0;
 while(picked.length<Math.min(size,subset.length) && guard<subset.length*4){
   guard++;
   const q=queueFor(style);
   const choice=q.pop();
   if(choice&&!used.has(choice.id)){picked.push(choice);used.add(choice.id);}
 }
 return picked;
}
function photoUrl(look){
 const f=look.img.split('/').pop();
 return {
  full:look.img,
  mobile:'/images-mobile-hd/badgirl-outfits/'+f,
  grid:'/images-grid/badgirl-outfits/'+f
 };
}
function textElement(tag,cls,txt){
 const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;
}
function openPreview(look){
 const urls=photoUrl(look);
 previousOpen=document.activeElement;
 photo.onerror=function(){this.onerror=null;this.src=urls.full;};
 photo.src=urls.full;
 photo.alt=look.title||look.tag;
 caption.textContent=look.tag||'ARCHIVE LOOK';
 categoryCaption.textContent=(look.primaryStyle||'Alternative')+' · ORIGINAL APOCALYPSE CLOSET LOOK';
 if(typeof dialog.showModal==='function')dialog.showModal();
}
function render(){
 const chosen=draw(active);
 const fragment=document.createDocumentFragment();
 chosen.forEach((look)=>{
   const card=textElement('article','ac-archive-card');
   const button=textElement('button','ac-archive-image-button');button.type='button';
   button.setAttribute('aria-label','Preview '+(look.tag||'outfit')+' in '+look.primaryStyle);
   const picture=document.createElement('picture');
   const sourceMobile=document.createElement('source');sourceMobile.media='(max-width:700px)';sourceMobile.srcset=photoUrl(look).mobile;
   const img=document.createElement('img');
   img.loading='lazy';img.decoding='async';img.width=Number(look.width)||768;img.height=Number(look.height)||1024;
   img.src=photoUrl(look).grid;img.alt=(look.tag||'Outfit')+' — '+(look.title||look.primaryStyle);
   img.onerror=function(){this.onerror=null;sourceMobile.remove();this.src=photoUrl(look).full;};
   picture.append(sourceMobile,img);
   button.append(picture,textElement('span','ac-archive-look-number',look.tag||'ORIGINAL LOOK'),
     textElement('span','ac-archive-view','EXPAND ↗'));
   button.addEventListener('click',()=>openPreview(look));
   const body=textElement('div','ac-archive-card-body');
   body.append(textElement('p','ac-archive-card-category',look.primaryStyle));
   body.append(textElement('h3','ac-archive-card-title',look.tag+' / '+look.primaryStyle));
   body.append(textElement('p','ac-archive-card-note','STYLE INSPIRATION / NOT FOR SALE'));
   card.append(button,body);fragment.append(card);
 });
 grid.replaceChildren(fragment);
 count.textContent='SHOWING '+chosen.length+' OF '+pool(active).length+' ARCHIVE LOOKS · '+source.length+' TOTAL · NO AFFILIATE LINKS HERE';
}
filters.addEventListener('click',event=>{
 const button=event.target.closest('button[data-style]');
 if(!button||!filters.contains(button))return;
 const next=button.dataset.style||'all';
 if(next===active) return;
 active=next;
 filters.querySelectorAll('button[data-style]').forEach(b=>{
   const selected=b===button;
   b.classList.toggle('is-active',selected);
   b.setAttribute('aria-pressed',String(selected));
 });
 render();
});
shuffleBtn.addEventListener('click',()=>render());
dialog.querySelector('#ac-archive-lightbox-close')?.addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
dialog.addEventListener('close',()=>{if(previousOpen&&previousOpen.isConnected) previousOpen.focus();});
render();
})();