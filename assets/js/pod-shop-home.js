/* Apocalypse Closet / Fourthwall POD catalog + cart. Public Cloudflare Worker URL only. */
(function(){
'use strict';
const API = String(window.AC_FOURTHWALL && window.AC_FOURTHWALL.apiBase || '').replace(/\/+$/, '');
const SHOP = 'https://apocalypse-closet-shop.fourthwall.com';
const FEATURED_SLUG = 'silent-chaos-gothic-angel-graphic-tee-apocalypse-closet';
const grid = document.querySelector('#ac-product-grid');
const status = document.querySelector('#ac-catalog-status');
const heroVisual = document.querySelector('#ac-store-hero-visual');
const heroPrice = document.querySelector('#ac-feature-price');
const bagButton = document.querySelector('#ac-cart-button');
const dialog = document.querySelector('#ac-cart-dialog');
const cartList = document.querySelector('#ac-cart-items');
const subtotal = document.querySelector('#ac-cart-subtotal');
const checkout = document.querySelector('#ac-checkout-link');
const cartStatus = document.querySelector('#ac-cart-status');
const mobileToggle = document.querySelector('.ac-menu-toggle');
const nav = document.querySelector('#ac-primary-nav');
const lookbook = document.querySelector('#lookbook');
const lookbookGallery = document.querySelector('#ac-lookbook-gallery');
const lightbox = document.querySelector('#ac-image-lightbox');
const lightboxImg = document.querySelector('#ac-lightbox-image');
const lightboxCounter = document.querySelector('#ac-lightbox-count');
let lightboxImages = [];
let lightboxIndex = 0;
const storageKey = 'ac_fourthwall_cart_id';
let cartId = '';
let busy = false;
if(!grid || !dialog || !bagButton || !API) return;
function say(element, value){ if(element) element.textContent=value; }
function money(amount,currency){const n=Number(amount);return Number.isFinite(n) ? new Intl.NumberFormat('en-US',{style:'currency',currency:currency||'USD'}).format(n):'Price at checkout';}
function errorFallback(message){
  say(status,message || 'Products are temporarily unavailable. You can shop securely on Fourthwall.');
  grid.replaceChildren();
  const box=document.createElement('div');box.className='ac-collection-fallback';
  const h=document.createElement('strong');h.textContent='SILENT CHAOS — GOTHIC ANGEL TEE';
  const p=document.createElement('p');p.textContent='Shop the original drop directly on our Fourthwall storefront while our live catalog reconnects.';
  const a=document.createElement('a');a.className='ac-btn';a.href=SHOP+'/products/'+FEATURED_SLUG;a.textContent='VIEW THE DROP ↗';a.rel='noopener noreferrer';
  box.append(h,p,a);grid.appendChild(box);
}
async function api(path, options){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),12000);
  try{
    const response=await fetch(API+'/v1'+path,{...(options||{}),signal:controller.signal});
    if(!response.ok)throw new Error('Request failed: '+response.status);
    return response.json();
  }finally{clearTimeout(timer);}
}
function publicProduct(p){return p && typeof p.slug==='string' && p.state?.type==='AVAILABLE' && p.access?.type==='PUBLIC';}
function variants(p){
  return (Array.isArray(p?.variants)?p.variants:[]).filter(v=>v && v.id && v.stock?.type!=='UNAVAILABLE' && v.stock?.type!=='SOLD_OUT' && Number.isFinite(Number(v.unitPrice?.value)));
}
function lowest(p){
  const arr=variants(p);
  if(!arr.length) return null;
  return arr.reduce((a,b)=>Number(b.unitPrice.value)<Number(a.unitPrice.value)?b:a);
}
function imageUrl(p){
  const value=(p.images||[]).find(i=>i&&typeof i.url==='string'&&/^https:\/\//.test(i.url));
  return value?.url||'';
}
function productPhotos(product){
  return (Array.isArray(product?.images)?product.images:[])
    .filter(im=>im && typeof im.url==='string' && /^https:\/\//.test(im.url))
    .filter((im,i,arr)=>arr.findIndex(other=>other.url===im.url)===i)
    .map(im=>im.url);
}
function showLightbox(index){
  if(!lightbox || !lightboxImages.length) return;
  lightboxIndex = (index + lightboxImages.length) % lightboxImages.length;
  lightboxImg.src = lightboxImages[lightboxIndex];
  lightboxImg.alt = 'Silent Chaos tee: product view ' + (lightboxIndex+1);
  say(lightboxCounter,(lightboxIndex+1)+' / '+lightboxImages.length);
  if(!lightbox.open && typeof lightbox.showModal==='function') lightbox.showModal();
}
function renderLookbook(product){
  if(!lookbook || !lookbookGallery) return;
  const urls=productPhotos(product);
  if(urls.length<2){lookbook.hidden=true;return;}
  // Use distinct images from different positions in the product media sequence.
  // This is one tee, never mislabel these as separate products.
  const preferred=urls.length>=12?[1,4,8,12,16]:urls.length>=7?[1,3,5,6]:[0,1,2,3,4];
  const picks=preferred.filter(i=>i<urls.length).map(i=>urls[i]);
  lightboxImages=picks;
  lookbookGallery.replaceChildren();
  picks.forEach((src,index)=>{
    const button=document.createElement('button');
    button.type='button';button.className='ac-lookbook-shot';
    button.setAttribute('aria-label','Expand Silent Chaos product view '+(index+1));
    const photo=document.createElement('img');
    photo.src=src;
    photo.alt='Silent Chaos Gothic Angel Tee — product photograph '+(index+1);
    photo.loading='lazy';photo.decoding='async';photo.width=560;photo.height=740;
    const label=document.createElement('span');
    label.className='ac-lookbook-shot-label';
    label.textContent='FRAME 0'+(index+1)+' / '+String(picks.length).padStart(2,'0');
    button.append(photo,label);
    button.addEventListener('click',()=>showLightbox(index));
    lookbookGallery.append(button);
  });
  lookbook.hidden=false;
}
lightbox?.querySelector('#ac-lightbox-close')?.addEventListener('click',()=>lightbox.close());
lightbox?.querySelector('#ac-lightbox-prev')?.addEventListener('click',()=>showLightbox(lightboxIndex-1));
lightbox?.querySelector('#ac-lightbox-next')?.addEventListener('click',()=>showLightbox(lightboxIndex+1));
lightbox?.addEventListener('click',event=>{if(event.target===lightbox)lightbox.close();});
lightbox?.addEventListener('keydown',event=>{
  if(event.key==='ArrowRight'){event.preventDefault();showLightbox(lightboxIndex+1);}
  if(event.key==='ArrowLeft'){event.preventDefault();showLightbox(lightboxIndex-1);}
});
function el(tag, cls, txt){
  const e=document.createElement(tag);
  if(cls)e.className=cls;
  if(txt!==undefined)e.textContent=txt;
  return e;
}
function priceOf(v){return money(v.unitPrice?.value,v.unitPrice?.currency);}
function variantLabel(v){
  const col=v.attributes?.color?.name, size=v.attributes?.size?.name;
  return [col,size].filter(Boolean).join(' / ') || v.attributes?.description || v.name || 'One size';
}
function createCard(p,index){
  const card=el('article','ac-product-card');
  const media=el('div','ac-product-media');
  const photo=el('a','ac-product-image');
  photo.href=SHOP+'/products/'+encodeURIComponent(p.slug);
  photo.rel='noopener noreferrer';photo.setAttribute('aria-label','View '+p.name+' on Fourthwall');
  const image=imageUrl(p);
  if(image){
    const img=document.createElement('img');img.src=image;img.alt=p.name;img.loading=index<2?'eager':'lazy';img.decoding='async';img.width=560;img.height=640;photo.append(img);
  }else{
    photo.append(el('span','ac-product-image-placeholder','APOCALYPSE'));
  }
  photo.append(el('span','ac-product-flag',index===0?'DROP 001':'MADE TO ORDER'));
  media.append(photo);
  const galleryUrls=productPhotos(p).slice(0,6);
  if(galleryUrls.length>1 && image){
    const thumbRail=el('div','ac-thumb-rail');
    const mainPhoto=photo.querySelector('img');
    galleryUrls.forEach((src,thumbIndex)=>{
      const thumbnail=el('button','ac-thumb'+(thumbIndex===0?' is-selected':''));
      thumbnail.type='button';
      thumbnail.setAttribute('aria-label','Show product photograph '+(thumbIndex+1));
      thumbnail.setAttribute('aria-pressed',thumbIndex===0?'true':'false');
      const miniature=document.createElement('img');
      miniature.src=src;miniature.alt='';miniature.loading='lazy';miniature.decoding='async';
      thumbnail.append(miniature);
      thumbnail.addEventListener('click',()=>{
        mainPhoto.src=src;
        mainPhoto.alt=p.name+' — view '+(thumbIndex+1);
        thumbRail.querySelectorAll('button').forEach(button=>{
          button.classList.remove('is-selected');button.setAttribute('aria-pressed','false');
        });
        thumbnail.classList.add('is-selected');thumbnail.setAttribute('aria-pressed','true');
      });
      thumbRail.append(thumbnail);
    });
    media.append(thumbRail);
  }
  const body=el('div','ac-product-body');
  body.append(el('p','ac-product-type','APOCALYPSE CLOSET / ORIGINAL'));
  const title=el('h3','ac-product-title');
  const link=el('a','',p.name);link.href=photo.href;title.append(link);
  body.append(title);
  const min=lowest(p);
  const price=el('strong','ac-product-price',min?'FROM '+priceOf(min):'Unavailable');
  body.append(price);
  const purch=el('div','ac-product-purchase');
  const select=el('select','ac-product-size');select.setAttribute('aria-label','Choose size for '+p.name);
  select.add(new Option('CHOOSE SIZE',''));
  const options=variants(p);
  const preferred=['XS','S','M','L','XL','2XL','3XL','4XL','5XL'];
  options.sort((a,b)=>{
    const as=a.attributes?.size?.name||'',bs=b.attributes?.size?.name||'';
    return (preferred.indexOf(as)<0?99:preferred.indexOf(as))-(preferred.indexOf(bs)<0?99:preferred.indexOf(bs));
  });
  options.forEach(v=>select.add(new Option(variantLabel(v)+' · '+priceOf(v),v.id)));
  const buy=el('button','ac-product-add','ADD TO BAG');buy.type='button';
  const note=el('p','ac-product-status','Select your size · Checkout by Fourthwall');
  if(!options.length){select.disabled=true;buy.disabled=true;say(note,'Currently unavailable');}
  select.addEventListener('change',()=>{
    const v=options.find(v=>v.id===select.value);
    say(price,v?priceOf(v):min?'FROM '+priceOf(min):'Unavailable');
  });
  buy.addEventListener('click',async()=>{
    const v=options.find(v=>v.id===select.value);
    if(!v){say(note,'Please select a size first.');select.focus();return;}
    await addToCart(v.id,buy,note);
  });
  purch.append(select,buy);body.append(purch,note);card.append(media,body);return card;
}
function paintHero(product){
  if(!product)return;
  const src=imageUrl(product);
  if(src && heroVisual){
    const img=document.createElement('img');
    img.src=src;img.alt='Silent Chaos gothic angel graphic tee — Apocalypse Closet';img.decoding='async';img.fetchPriority='high';img.width=800;img.height=950;
    heroVisual.querySelector('.ac-visual-placeholder')?.replaceWith(img);
  }
  const v=lowest(product);
  if(v)say(heroPrice,'FROM '+priceOf(v));
}
async function loadCatalog(){
  try{
    const data=await api('/collections/all/products?page=0&size=24');
    const products=Array.isArray(data.results)?data.results.filter(publicProduct):[];
    if(!products.length){
      const fallback=await api('/products/'+encodeURIComponent(FEATURED_SLUG));
      if(!publicProduct(fallback))throw new Error('No public product');
      products.push(fallback);
    }
    grid.replaceChildren(...products.map(createCard));
    grid.classList.toggle('is-single',products.length===1);
    say(status,products.length===1?'DROP 001 · ONE DESIGN · MULTIPLE VIEWS':products.length+' ORIGINAL DROPS');
    const featured=products.find(p=>p.slug===FEATURED_SLUG)||products[0];
    paintHero(featured);
    renderLookbook(featured);
  }catch(e){
    try{const product=await api('/products/'+encodeURIComponent(FEATURED_SLUG));if(!publicProduct(product))throw new Error('Not public');grid.replaceChildren(createCard(product,0));grid.classList.add('is-single');say(status,'DROP 001 · ONE DESIGN · MULTIPLE VIEWS');paintHero(product);renderLookbook(product);}
    catch(_){errorFallback();}
  }
}
function getStoredCart(){
  try{const value=localStorage.getItem(storageKey)||'';return /^[a-zA-Z0-9-]{1,64}$/.test(value)?value:'';}
  catch(_){return '';}
}
function storeCart(value){
  cartId=value;
  try{localStorage.setItem(storageKey,value);}catch(_){}
}
function countItems(cart){return Array.isArray(cart.items)?cart.items.reduce((n,i)=>n+Number(i.quantity||0),0):0;}
function cartTotal(cart){
  return (cart.items||[]).reduce((sum,item)=>sum+Number(item.quantity||0)*Number(item.variant?.unitPrice?.value||0),0);
}
function updateCount(cart){say(bagButton,'BAG ('+countItems(cart)+')');}
function displayCart(cart){
  updateCount(cart);cartList.replaceChildren();
  (cart.items||[]).forEach(item=>{
    const li=el('li','');
    const details=el('div','');
    const product=el('strong','',item.variant?.name||'Apocalypse Closet item');
    const meta=el('div','', 'Qty '+Number(item.quantity||0));meta.style.color='#b8aaa1';
    details.append(product,meta);
    const total=el('span','',money(Number(item.variant?.unitPrice?.value||0)*Number(item.quantity||0),item.variant?.unitPrice?.currency||'USD'));
    li.append(details,total);cartList.append(li);
  });
  say(subtotal,money(cartTotal(cart),'USD'));
  checkout.href=SHOP+'/checkout/?'+new URLSearchParams({cartCurrency:'USD',cartId:cart.id}).toString();
  checkout.hidden=!cart.id||!countItems(cart);
  say(cartStatus,countItems(cart)?'Shipping and any applicable taxes are calculated during secure checkout.':'Your bag is empty.');
}
async function newCartWith(variantId){
  const cart=await api('/carts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{variantId,quantity:1}]})});
  if(!cart?.id)throw new Error('No cart ID');
  storeCart(cart.id);
  return cart;
}
async function addToCart(variantId,button,note){
  if(busy)return;
  busy=true;button.disabled=true;say(note,'ADDING…');
  try{
    let cart;
    const stored=cartId||getStoredCart();
    if(stored){
      try{
        await api('/carts/'+encodeURIComponent(stored)+'/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{variantId,quantity:1}]})});
        cart=await api('/carts/'+encodeURIComponent(stored));
        storeCart(stored);
      }catch(e){
        // Only create a new cart if the old cart is actually expired/missing.
        const code=String(e.message||'');
        if(!/404|410/.test(code))throw e;
        cart=await newCartWith(variantId);
      }
    }else cart=await newCartWith(variantId);
    // A create response may omit full cart items, so fetch the current cart.
    if(!Array.isArray(cart.items))cart=await api('/carts/'+encodeURIComponent(cartId));
    displayCart(cart);say(note,'ADDED TO BAG');if(typeof dialog.showModal==='function')dialog.showModal();
    if(window.gtag)window.gtag('event','add_to_cart',{currency:'USD',value:cartTotal(cart),items:[{item_id:variantId,quantity:1}]});
  }catch(e){say(note,'Could not add item. Please retry or open its Fourthwall page.');}
  finally{busy=false;button.disabled=false;}
}
async function openCart(){
  const stored=cartId||getStoredCart();
  if(!stored){cartList.replaceChildren();say(subtotal,money(0,'USD'));checkout.hidden=true;say(cartStatus,'Your bag is empty.');dialog.showModal();return;}
  try{const cart=await api('/carts/'+encodeURIComponent(stored));storeCart(stored);displayCart(cart);dialog.showModal();}
  catch(_){storeCart('');cartList.replaceChildren();checkout.hidden=true;say(cartStatus,'Your saved cart expired. Add an item to start a new bag.');dialog.showModal();}
}
bagButton.addEventListener('click',openCart);
document.querySelector('#ac-cart-close')?.addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
mobileToggle?.addEventListener('click',()=>{
  const open=nav.classList.toggle('is-open');
  mobileToggle.setAttribute('aria-expanded',String(open));
});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');mobileToggle?.setAttribute('aria-expanded','false');}));
const stored=getStoredCart();
if(stored){
  api('/carts/'+encodeURIComponent(stored)).then(cart=>{storeCart(stored);updateCount(cart);}).catch(()=>storeCart(''));
}
loadCatalog();
})();
