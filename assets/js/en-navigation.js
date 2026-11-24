/* One English shell controller; commerce/cart logic remains in its own module. */
(()=>{
 'use strict';
 const header=document.querySelector('.en-shell-header');if(!header)return;
 const menu=header.querySelector('.en-shell-nav'),toggle=header.querySelector('.en-shell-toggle');
 const dropdowns=[...header.querySelectorAll('.en-shell-dropdown')];
 function closeDropdowns(except){dropdowns.forEach(d=>{if(d===except)return;d.classList.remove('is-open');d.querySelector('button')?.setAttribute('aria-expanded','false');});}
 function closeMenu(){header.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');closeDropdowns();}
 toggle.addEventListener('click',()=>{const open=!header.classList.contains('is-open');closeMenu();header.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',String(open));});
 dropdowns.forEach(d=>{
   const button=d.querySelector('button');
   button.addEventListener('click',()=>{const open=!d.classList.contains('is-open');closeDropdowns(d);d.classList.toggle('is-open',open);button.setAttribute('aria-expanded',String(open));});
   d.addEventListener('focusout',event=>{if(!d.contains(event.relatedTarget)){d.classList.remove('is-open');button.setAttribute('aria-expanded','false');}});
 });
 document.addEventListener('click',event=>{if(!header.contains(event.target))closeMenu();});
 document.addEventListener('keydown',event=>{
   if(event.key!=='Escape')return;
   const openDropdown=dropdowns.find(d=>d.classList.contains('is-open'));
   if(openDropdown){closeDropdowns();openDropdown.querySelector('button').focus();return;}
   if(header.classList.contains('is-open')){closeMenu();toggle.focus();}
 });
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
 window.matchMedia('(min-width:1280px)').addEventListener('change',closeMenu);
 const path=location.pathname.replace(/\/+$/,'')||'/';
 menu.querySelectorAll('a').forEach(a=>{
   const url=new URL(a.href,location.href);
   if(url.origin===location.origin&&!url.hash&&(url.pathname===path||(url.pathname==='/en/blog.html'&&path.startsWith('/en/blog/'))))a.setAttribute('aria-current','page');
 });
})();
