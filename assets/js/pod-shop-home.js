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
const heroSize = document.querySelector('#ac-hero-size');
const heroAdd = document.querySelector('#ac-hero-add');
const heroStatus = document.querySelector('#ac-hero-buy-status');
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
/* Color/size selection is keyed by the actual Fourthwall variant ID.
   Variant.images are authoritative for each color. Never infer colors from filenames. */
function colorOf(v){return String(v?.attributes?.color?.name||'Standard').trim();}
function colorKey(name){return String(name||'').trim().toLowerCase();}
function sizeOf(v){return String(v?.attributes?.size?.name||'One Size').trim();}
const sizeOrder=['XS','S','M','L','XL','2XL','3XL','4XL','5XL'];
function variantSort(a,b){
 const ia=sizeOrder.indexOf(sizeOf(a).toUpperCase()),ib=sizeOrder.indexOf(sizeOf(b).toUpperCase());
 return (ia<0?99:ia)-(ib<0?99:ib);
}
function colorGroups(options){
 const map=new Map();
 for(const v of options){
   const name=colorOf(v),key=colorKey(name);
   if(!map.has(key))map.set(key,{key,name,swatch:v.attributes?.color?.swatch||'',options:[]});
   map.get(key).options.push(v);
 }
 return [...map.values()];
}
function uniquePhotoUrls(items){
 return (Array.isArray(items)?items:[])
   .filter(x=>x && typeof x.url==='string' && /^https:\/\//.test(x.url))
   .map(x=>x.url)
   .filter((url,i,arr)=>arr.indexOf(url)===i);
}
function photosForColor(product,key){
 const groups=colorGroups(variants(product));
 const match=groups.find(g=>g.key===key)||groups[0];
 if(!match)return productPhotos(product);
 // Single-color catalog photo galleries are safe for the only available color.
 if(groups.length===1){
   const general=productPhotos(product),specific=uniquePhotoUrls(match.options.flatMap(v=>v.images||[]));
   return general.length>=specific.length ? general : specific;
 }
 // Multicolor: only use Fourthwall images attached to the selected variant.
 return uniquePhotoUrls(match.options.flatMap(v=>v.images||[]));
}
function showColorImage(img,placeholder,urls,color,notice){
 const source=urls[0]||'';
 if(source){
   if(img){img.src=source;img.hidden=false;img.alt='Apocalypse Closet apparel in '+color;}
   if(placeholder)placeholder.hidden=true;
   if(notice){notice.hidden=true;say(notice,'');}
 }else{
   if(img){img.hidden=true;img.removeAttribute('src');}
   if(placeholder){placeholder.hidden=false;say(placeholder,'PHOTO PENDING');}
   if(notice){notice.hidden=false;say(notice,'Color-specific image is not available through the catalog yet. Verify the selected color on Fourthwall before ordering.');}
 }
}
function renderPhotoRail(container,urls,onSelect,caption){
 if(!container)return;
 container.replaceChildren();
 urls.slice(0,6).forEach((src,i)=>{
   const b=el('button','ac-thumb'+(i===0?' is-selected':''));
   b.type='button';b.setAttribute('aria-label',(caption||'Product')+' photo '+(i+1));
   b.setAttribute('aria-pressed',i===0?'true':'false');
   const img=document.createElement('img');img.src=src;img.alt='';img.loading='lazy';img.decoding='async';
   b.append(img);b.addEventListener('click',()=>{
     onSelect(src,i);
     container.querySelectorAll('button').forEach(t=>{t.classList.remove('is-selected');t.setAttribute('aria-pressed','false');});
     b.classList.add('is-selected');b.setAttribute('aria-pressed','true');
   });
   container.append(b);
 });
}

function showLightbox(index){
  if(!lightbox || !lightboxImages.length) return;
  lightboxIndex = (index + lightboxImages.length) % lightboxImages.length;
  lightboxImg.src = lightboxImages[lightboxIndex];
  lightboxImg.alt = 'Silent Chaos tee: product view ' + (lightboxIndex+1);
  say(lightboxCounter,(lightboxIndex+1)+' / '+lightboxImages.length);
  if(!lightbox.open && typeof lightbox.showModal==='function') lightbox.showModal();
}
function renderLookbook(product,selectedColor){
  if(!lookbook || !lookbookGallery)return;
  const urls=photosForColor(product,selectedColor || colorGroups(variants(product))[0]?.key);
  if(urls.length<2){lookbook.hidden=true;lookbookGallery.replaceChildren();lightboxImages=[];return;}
  const preferred=urls.length>=12?[1,4,8,12,16]:urls.length>=7?[1,3,5,6]:[0,1,2,3,4];
  const picks=preferred.filter(i=>i<urls.length).map(i=>urls[i]);
  lightboxImages=picks;
  lookbookGallery.replaceChildren();
  picks.forEach((src,index)=>{
    const button=document.createElement('button');
    button.type='button';button.className='ac-lookbook-shot';
    button.setAttribute('aria-label','Expand selected-color product view '+(index+1));
    const photo=document.createElement('img');
    photo.src=src;photo.alt='Apocalypse Closet '+product.name+' — selected-color photo '+(index+1);
    photo.loading='lazy';photo.decoding='async';photo.width=560;photo.height=740;
    const label=document.createElement('span');label.className='ac-lookbook-shot-label';
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
  const imageEl=document.createElement('img');imageEl.alt=p.name;imageEl.loading=index<2?'eager':'lazy';
  imageEl.decoding='async';imageEl.width=560;imageEl.height=640;
  const placeholder=el('span','ac-product-image-placeholder','PHOTO PENDING');
  photo.append(imageEl,placeholder,el('span','ac-product-flag',index===0?'DROP 001':'MADE TO ORDER'));
  media.append(photo);
  const rail=el('div','ac-thumb-rail');media.append(rail);
  const body=el('div','ac-product-body');
  body.append(el('p','ac-product-type','APOCALYPSE CLOSET / ORIGINAL'));
  const title=el('h3','ac-product-title'),link=el('a','',p.name);
  link.href=photo.href;title.append(link);body.append(title);
  const price=el('strong','ac-product-price','Price at checkout');body.append(price);
  const purch=el('div','ac-product-purchase');
  const options=variants(p),groups=colorGroups(options);
  const colorSelect=el('select','ac-product-color');colorSelect.setAttribute('aria-label','Choose color for '+p.name);
  const sizeSelect=el('select','ac-product-size');sizeSelect.setAttribute('aria-label','Choose size for '+p.name);
  groups.forEach(g=>colorSelect.add(new Option(g.name,g.key)));
  if(!groups.length){colorSelect.add(new Option('Unavailable',''));colorSelect.disabled=true;}
  const note=el('p','ac-product-status','Choose color and size · Secure Fourthwall checkout');
  const imageNote=el('p','ac-product-image-notice');imageNote.hidden=true;
  const buy=el('button','ac-product-add','ADD TO BAG');buy.type='button';
  function refreshSize(){
    const selected=groups.find(g=>g.key===colorSelect.value);
    sizeSelect.replaceChildren(new Option('CHOOSE SIZE',''));
    (selected?.options||[]).slice().sort(variantSort).forEach(v=>{
      sizeSelect.add(new Option(sizeOf(v)+' · '+priceOf(v),v.id));
    });
    sizeSelect.disabled=!selected?.options.length;
    buy.disabled=!selected?.options.length;
    const min=(selected?.options||[]).reduce((a,v)=>!a||Number(v.unitPrice.value)<Number(a.unitPrice.value)?v:a,null);
    say(price,min?'FROM '+priceOf(min):'Unavailable');
    const urls=photosForColor(p,colorSelect.value);
    showColorImage(imageEl,placeholder,urls,selected?.name||'selected color',imageNote);
    renderPhotoRail(rail,urls,(src,i)=>{
      imageEl.src=src;imageEl.alt=p.name+' in '+(selected?.name||'selected color')+' — photo '+(i+1);
    },p.name);
  }
  colorSelect.addEventListener('change',refreshSize);
  sizeSelect.addEventListener('change',()=>{
    const v=options.find(v=>v.id===sizeSelect.value && colorKey(colorOf(v))===colorSelect.value);
    say(price,v?priceOf(v):'Choose a size');
  });
  buy.addEventListener('click',async()=>{
    const v=options.find(v=>v.id===sizeSelect.value && colorKey(colorOf(v))===colorSelect.value);
    if(!v){say(note,'Please choose a size first.');sizeSelect.focus();return;}
    await addToCart(v.id,buy,note);
  });
  purch.append(colorSelect,sizeSelect,buy);
  body.append(purch,note,imageNote);
  card.append(media,body);
  refreshSize();
  return card;
}
/**
 * Preview-only grid slots: 5 additional visual cards built from the existing
 * Silent Chaos images. Never invent inventory, prices, variant IDs or checkout.
 * These placeholders disappear on production and as real catalog items arrive.
 */
function isLayoutPreview(){
  return location.hostname.endsWith('.pages.dev') || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
}
function createDemoCard(product,slot){
  const card=el('article','ac-product-card ac-product-card--demo');
  card.setAttribute('data-layout-preview','true');
  const media=el('div','ac-product-media');
  const imageBox=el('div','ac-product-image');
  const images=productPhotos(product);
  const photoIndex=images.length ? [1,4,7,10,13][(slot-1)%5] % images.length : -1;
  if(photoIndex>=0){
    const photo=document.createElement('img');
    photo.src=images[photoIndex]; photo.loading='lazy';photo.decoding='async';
    photo.alt='Alternate mockup view of the existing Silent Chaos tee — layout demo '+slot;
    photo.width=560;photo.height=640;
    imageBox.append(photo);
  }else imageBox.append(el('span','ac-product-image-placeholder','SILENT CHAOS'));
  imageBox.append(el('span','ac-product-flag ac-product-flag--demo','LAYOUT DEMO'));
  media.append(imageBox);
  const body=el('div','ac-product-body');
  body.append(el('p','ac-product-type','DESIGN SLOT '+String(slot+1).padStart(2,'0')+' / PREVIEW'));
  const title=el('h3','ac-product-title','SILENT CHAOS / MOCKUP '+String(slot).padStart(2,'0'));
  body.append(title,el('strong','ac-product-price ac-demo-price','COMING SOON'));
  const purchase=el('div','ac-product-purchase');
  const button=el('button','ac-product-add ac-demo-button','PREVIEW ONLY');
  button.type='button';button.disabled=true;
  button.title='Layout demonstration. This is not a separately purchasable product.';
  purchase.append(button);
  body.append(purchase,el('p','ac-product-status','Same shirt, another photo · Not for sale'));
  card.append(media,body);
  return card;
}
function paintCatalog(products, featured){
  const showDemo = isLayoutPreview() && products.length < 6;
  const fillers=showDemo
    ? Array.from({length:6-products.length},(_,i)=>createDemoCard(featured,i+1))
    : [];
  grid.replaceChildren(...products.map((p,i)=>createCard(p.slug===featured.slug?featured:p,i)),...fillers);
  grid.classList.toggle('is-single',products.length===1&&!showDemo);
  grid.classList.toggle('is-demo',showDemo);
  say(status,showDemo
    ? products.length+' LIVE DESIGN'+(products.length>1?'S':'')+' · '+fillers.length+' DEMO SLOTS · PREVIEW ONLY'
    : products.length+' LIVE DROPS');
  const notice=document.querySelector('#ac-demo-note');
  if(notice) notice.hidden=!showDemo;
}
function paintHero(product){
  if(!product || !heroSize || !heroAdd)return;
  const opts=variants(product), groups=colorGroups(opts);
  const colorSel=document.querySelector('#ac-hero-color');
  const heroRail=document.querySelector('#ac-hero-gallery');
  const imageNote=document.querySelector('#ac-hero-image-note');
  const colorLine=document.querySelector('#ac-feature-color-line');
  if(!colorSel)return;
  const oldColor=colorSel.value;
  colorSel.replaceChildren();
  groups.forEach(g=>colorSel.add(new Option(g.name,g.key)));
  if(!groups.length){colorSel.add(new Option('Unavailable',''));colorSel.disabled=true;}
  else colorSel.disabled=groups.length<2;
  colorSel.value=groups.some(g=>g.key===oldColor)?oldColor:groups[0]?.key||'';
  let img=heroVisual?.querySelector('img');
  const placeholder=heroVisual?.querySelector('.ac-visual-placeholder');
  if(!img && heroVisual){
    img=document.createElement('img');
    img.decoding='async';img.fetchPriority='high';img.width=800;img.height=950;
    heroVisual.append(img);
  }
  function refreshHero(){
    const group=groups.find(g=>g.key===colorSel.value);
    const current=group?.options||[];
    heroSize.replaceChildren(new Option('CHOOSE SIZE',''));
    current.slice().sort(variantSort).forEach(v=>heroSize.add(new Option(sizeOf(v)+' · '+priceOf(v),v.id)));
    heroSize.disabled=!current.length;heroAdd.disabled=!current.length;
    const min=current.reduce((a,v)=>!a||Number(v.unitPrice.value)<Number(a.unitPrice.value)?v:a,null);
    say(heroPrice,min?'FROM '+priceOf(min):'Unavailable');
    say(colorLine,group?.name ? 'USD · '+group.name.toUpperCase()+' · SELECT YOUR SIZE':'USD · COLOR UNAVAILABLE');
    say(heroStatus,current.length?'Choose your size to add the selected color to your bag.':'No available sizes for the selected color.');
    const urls=photosForColor(product,colorSel.value);
    showColorImage(img,placeholder,urls,group?.name||'selected color',imageNote);
    renderPhotoRail(heroRail,urls,(src,i)=>{
      img.src=src;
      img.alt=product.name+' in '+group.name+' — photo '+(i+1);
    },product.name);
    renderLookbook(product,colorSel.value);
  }
  colorSel.onchange=refreshHero;
  heroSize.onchange=()=>{
    const group=groups.find(g=>g.key===colorSel.value);
    const v=(group?.options||[]).find(v=>v.id===heroSize.value);
    say(heroPrice,v?priceOf(v):'Choose a size');
  };
  heroAdd.onclick=async()=>{
    const group=groups.find(g=>g.key===colorSel.value);
    const v=(group?.options||[]).find(v=>v.id===heroSize.value);
    if(!v){say(heroStatus,'Please choose a size first.');heroSize.focus();return;}
    await addToCart(v.id,heroAdd,heroStatus);
  };
  refreshHero();
}

async function loadCatalog(){
  // Load the featured product immediately: buyers should see real size/price
  // before the rest of the catalog has finished loading.
  const featuredPromise=api('/products/'+encodeURIComponent(FEATURED_SLUG))
    .then(p=>{if(publicProduct(p)){paintHero(p);}return p;})
    .catch(()=>null);
  try{
    const data=await api('/collections/all/products?page=0&size=24');
    const products=Array.isArray(data.results)?data.results.filter(publicProduct):[];
    let featured=await featuredPromise;
    if(!products.length){
      if(!publicProduct(featured))throw new Error('No public product');
      products.push(featured);
    }
    const head=products.find(p=>p.slug===FEATURED_SLUG)||products[0];
    // Prefer the original first tee even if a collection returns products in a new order.
    if(!publicProduct(featured) || featured.slug!==head.slug){
      try{featured=await api('/products/'+encodeURIComponent(head.slug));}
      catch(_){featured=head;}
    }
    paintCatalog(products,featured);
    paintHero(featured);
  }catch(e){
    const featured=await featuredPromise;
    if(publicProduct(featured)){
      paintCatalog([featured],featured);
      paintHero(featured);
      renderLookbook(featured);
    }else{
      errorFallback();
      say(heroStatus,'Live sizes are unavailable. View the product on Fourthwall.');
    }
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
