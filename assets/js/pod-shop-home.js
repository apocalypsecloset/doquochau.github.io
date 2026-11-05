/* Apocalypse Closet / Fourthwall POD catalog + cart. Public Cloudflare Worker URL only. */
(function(){
'use strict';
const API = String(window.AC_FOURTHWALL && window.AC_FOURTHWALL.apiBase || '').replace(/\/+$/, '');
const model = window.ACShopModel;
const SHOP = 'https://apocalypse-closet-shop.fourthwall.com';
const FEATURED_SLUG = 'silent-chaos-gothic-angel-graphic-tee-apocalypse-closet';
const grid = document.querySelector('#ac-product-grid');
const status = document.querySelector('#ac-catalog-status');
const heroVisual = document.querySelector('#ac-store-hero-visual');
const heroPrice = document.querySelector('#ac-feature-price');
const heroSize = document.querySelector('#ac-hero-size');
const heroColor = document.querySelector('#ac-hero-color');
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
let currentCart = null;
let cartNeedsRefresh = false;
let featuredProduct = null;
const variantNames = new Map();
const viewedProducts = new Set();
if(!grid || !dialog || !bagButton || !API || !model) return;
function track(name,payload){
  if(!['apocalypsecloset.com','www.apocalypsecloset.com'].includes(location.hostname))return;
  if(window.acTrack)window.acTrack(name,payload);
  else if(window.gtag)window.gtag('event',name,payload);
}
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
    if(!response.ok){const error=new Error('Request failed: '+response.status);error.status=response.status;throw error;}
    return response.json();
  }finally{clearTimeout(timer);}
}
function publicProduct(p){return p && typeof p.slug==='string' && p.state?.type==='AVAILABLE' && p.access?.type==='PUBLIC';}
function variants(p){
  return model.available(p);
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
function renderLookbook(product,chosenColor,chosenVariant){
  if(!lookbook || !lookbookGallery) return;
  const urls=model.colorPhotos(product,chosenColor||model.colors(product)[0],chosenVariant);
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
function fillSizes(select,product,color,preserve){
  const options=model.sizes(product,color);
  const previous=preserve||'';
  select.replaceChildren(new Option('CHOOSE SIZE',''));
  options.forEach(v=>select.add(new Option(model.size(v)+' · '+priceOf(v),model.size(v))));
  if(options.some(v=>model.size(v)===previous))select.value=previous;
  select.disabled=!options.length;
}
function fillColors(select,product){
  select.replaceChildren();
  model.colors(product).forEach(c=>select.add(new Option(c,c)));
  select.disabled=!select.options.length;
}
function paintCardPhotos(media,product,color,variant){
  const photo=media.querySelector('.ac-product-image');
  photo.replaceChildren();
  media.querySelector('.ac-thumb-rail')?.remove();
  const urls=model.colorPhotos(product,color,variant);
  if(!urls.length){photo.append(el('span','ac-product-image-placeholder','PHOTO PENDING — '+color));return;}
  const img=el('img');img.src=urls[0];img.alt=product.name+' — '+color;img.width=560;img.height=640;img.loading='lazy';img.decoding='async';photo.append(img);
  const rail=el('div','ac-thumb-rail');
  urls.slice(0,6).forEach((src,i)=>{
    const b=el('button','ac-thumb'+(i===0?' is-selected':''));b.type='button';
    b.setAttribute('aria-label','Show '+color+' product photograph '+(i+1));b.setAttribute('aria-pressed',String(i===0));
    const mini=el('img');mini.src=src;mini.alt='';mini.width=90;mini.height=100;mini.loading='lazy';mini.decoding='async';b.append(mini);
    b.addEventListener('click',()=>{img.src=src;img.alt=product.name+' — '+color+' view '+(i+1);rail.querySelectorAll('button').forEach(x=>{x.classList.remove('is-selected');x.setAttribute('aria-pressed','false');});b.classList.add('is-selected');b.setAttribute('aria-pressed','true');});rail.append(b);
  });
  if(urls.length>1)media.append(rail);
}
function variantLabel(v){
  const col=v.attributes?.color?.name, size=v.attributes?.size?.name;
  return [col,size].filter(Boolean).join(' / ') || v.attributes?.description || v.name || 'One size';
}
function createCard(p,index){
  variants(p).forEach(v=>variantNames.set(v.id,p.name));
  const card=el('article','ac-product-card');
  const media=el('div','ac-product-media');
  const photo=el('a','ac-product-image');
  photo.href=SHOP+'/products/'+encodeURIComponent(p.slug);
  photo.rel='noopener noreferrer';photo.setAttribute('aria-label','View '+p.name+' on Fourthwall');media.append(photo);
  const body=el('div','ac-product-body');
  body.append(el('p','ac-product-type','APOCALYPSE CLOSET / ORIGINAL'));
  const title=el('h3','ac-product-title');const link=el('a','',p.name);link.href=photo.href;title.append(link);body.append(title);
  const min=lowest(p),price=el('strong','ac-product-price',min?'FROM '+priceOf(min):'Unavailable');body.append(price);
  const controls=el('div','ac-variant-controls');
  const colorLabel=el('label','ac-variant-field','COLOR');
  const color=el('select','ac-product-color');color.setAttribute('aria-label','Choose color for '+p.name);colorLabel.append(color);
  const sizeLabel=el('label','ac-variant-field','SIZE');
  const size=el('select','ac-product-size');size.setAttribute('aria-label','Choose size for '+p.name);sizeLabel.append(size);
  controls.append(colorLabel,sizeLabel);body.append(controls);
  const buy=el('button','ac-product-add','ADD TO BAG');buy.type='button';
  const note=el('p','ac-product-status','Choose color and size · Checkout by Fourthwall');note.setAttribute('role','status');
  fillColors(color,p);fillSizes(size,p,color.value);
  function refresh(colorChanged){
    if(colorChanged)fillSizes(size,p,color.value,size.value);
    const v=model.variant(p,color.value,size.value);
    say(price,v?priceOf(v):min?'FROM '+priceOf(min):'Unavailable');
    buy.disabled=!v;
    paintCardPhotos(media,p,color.value,v);
    say(note,!color.options.length?'Currently unavailable':v?'Selected '+color.value+' / '+model.size(v):'Choose a size for '+color.value+'.');
  }
  color.addEventListener('change',()=>refresh(true));
  size.addEventListener('change',()=>refresh(false));
  buy.addEventListener('click',async()=>{
    const v=model.variant(p,color.value,size.value);
    if(!v){say(note,'Please choose color and size.');size.focus();return;}
    await addToCart(v,buy,note,p.name);
  });
  body.append(buy,note);card.append(media,body);refresh(false);return card;
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
  grid.replaceChildren(...products.map(createCard),...fillers);
  grid.classList.toggle('is-single',products.length===1&&!showDemo);
  grid.classList.toggle('is-demo',showDemo);
  say(status,showDemo
    ? products.length+' LIVE DESIGN'+(products.length>1?'S':'')+' · '+fillers.length+' DEMO SLOTS · PREVIEW ONLY'
    : products.length+' LIVE DROPS');
  const notice=document.querySelector('#ac-demo-note');
  if(notice) notice.hidden=!showDemo;
  const items=products.map(p=>{const v=lowest(p);return v?model.ecommerceItem(v,1,p.name):null;}).filter(Boolean);
  if(items.length)track('view_item_list',{item_list_id:'home_catalog',item_list_name:'Home catalog',items});
}
function paintHero(product){
  if(!product || !heroSize || !heroColor || !heroAdd)return;
  featuredProduct=product;
  const information=document.querySelector('#ac-product-information');
  if(information){
    information.replaceChildren();
    (Array.isArray(product.additionalInformation)?product.additionalInformation:[]).forEach(info=>{
      const panel=el('div','ac-product-information-panel');panel.append(el('h3','',info.title||'Product details'));
      // Keep upstream text while never attaching upstream HTML or its attributes.
      const parsed=new DOMParser().parseFromString(String(info.bodyHtml||''),'text/html');
      parsed.querySelectorAll('script,style,iframe,object').forEach(n=>n.remove());
      const items=parsed.querySelectorAll('li');
      if(items.length){const list=el('ul');items.forEach(item=>list.append(el('li','',item.textContent)));panel.append(list);}
      else panel.append(el('p','',parsed.body.textContent));
      information.append(panel);
    });
  }
  variants(product).forEach(v=>variantNames.set(v.id,product.name));
  if(!viewedProducts.has(product.id||product.slug)){
    const first=lowest(product);
    if(first){viewedProducts.add(product.id||product.slug);track('view_item',model.eventForVariant(first,1,product.name));}
  }
  const previousColor=heroColor.value,previousSize=heroSize.value;
  fillColors(heroColor,product);
  if(model.colors(product).includes(previousColor))heroColor.value=previousColor;
  fillSizes(heroSize,product,heroColor.value,previousSize);
  const min=lowest(product);
  function refresh(colorChanged){
    if(colorChanged)fillSizes(heroSize,product,heroColor.value,heroSize.value);
    const v=model.variant(product,heroColor.value,heroSize.value);
    const urls=model.colorPhotos(product,heroColor.value,v);
    heroVisual.querySelectorAll('img,.ac-visual-placeholder').forEach(n=>n.remove());
    if(urls.length){
      const img=el('img');img.src=urls[0];img.alt=product.name+' — '+heroColor.value;
      img.decoding='async';img.fetchPriority='high';img.width=800;img.height=950;heroVisual.append(img);
    }else heroVisual.append(el('div','ac-visual-placeholder','PHOTO PENDING — '+heroColor.value));
    heroAdd.disabled=!v;
    say(heroPrice,v?priceOf(v):min?'FROM '+priceOf(min):'Unavailable');
    say(heroStatus,!heroColor.options.length?'Currently unavailable. View the product on Fourthwall.':v?'Selected '+heroColor.value+' / '+model.size(v):'Choose your size for '+heroColor.value+'.');
    renderLookbook(product,heroColor.value,v);
  }
  heroColor.onchange=()=>refresh(true);heroSize.onchange=()=>refresh(false);
  heroAdd.onclick=async()=>{
    const v=model.variant(product,heroColor.value,heroSize.value);
    if(!v){say(heroStatus,'Please choose color and size.');heroSize.focus();return;}
    await addToCart(v,heroAdd,heroStatus,product.name);
  };
  refresh(false);
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
function cartTotal(cart){return model.total(cart);}
function updateCount(cart){say(bagButton,'BAG ('+countItems(cart)+')');}
function showBag(){if(!dialog.open&&typeof dialog.showModal==='function')dialog.showModal();}
function retryVisible(visible){const b=document.querySelector('#ac-cart-retry');if(b)b.hidden=!visible;}
function displayCart(cart){
  currentCart=cart;
  cartNeedsRefresh=false;
  retryVisible(false);updateCount(cart);cartList.replaceChildren();
  model.cartItems(cart).forEach(item=>{
    const v=item.variant,q=Number(item.quantity||0);if(!v)return;
    const li=el('li','');const details=el('div','');
    const name=variantNames.get(v.id)||v.name||'Apocalypse Closet item';
    details.append(el('strong','',name),el('div','ac-cart-variant',[model.color(v),model.size(v)].join(' / ')));
    const controls=el('div','ac-cart-quantity');
    const label=el('label','','QUANTITY');
    const input=el('input');input.type='number';input.min='1';input.max='99';input.step='1';input.value=String(q);
    input.setAttribute('aria-label','Quantity for '+name+' '+model.color(v)+' '+model.size(v));label.append(input);
    const update=el('button','','UPDATE');update.type='button';
    const remove=el('button','','REMOVE');remove.type='button';remove.setAttribute('aria-label','Remove '+name+' '+model.color(v)+' '+model.size(v));
    update.addEventListener('click',()=>{
      const n=Number(input.value);
      if(!Number.isInteger(n)||n<1||n>99){input.reportValidity();say(cartStatus,'Choose a whole quantity from 1 to 99.');return;}
      changeCart(item,n);
    });
    remove.addEventListener('click',()=>changeCart(item,0));controls.append(label,update,remove);details.append(controls);
    li.append(details,el('span','',money(Number(v.unitPrice?.value||0)*q,v.unitPrice?.currency||'USD')));cartList.append(li);
  });
  say(subtotal,money(cartTotal(cart),'USD'));
  checkout.href=SHOP+'/checkout/?'+new URLSearchParams({cartCurrency:'USD',cartId:cart.id||''}).toString();
  checkout.hidden=!cart.id||!countItems(cart);
  say(cartStatus,countItems(cart)?'Shipping and any applicable taxes are calculated during secure checkout.':'Your bag is empty.');
}
async function changeCart(item,quantity){
  if(busy)return;const id=cartId||getStoredCart();if(!id)return;
  busy=true;checkout.setAttribute('aria-disabled','true');cartList.querySelectorAll('button,input').forEach(n=>n.disabled=true);say(cartStatus,'UPDATING BAG…');
  try{
    const action=quantity===0?'remove':'change';
    const payload={items:[{variantId:item.variant.id,quantity:quantity===0?Number(item.quantity):quantity}]};
    await api('/carts/'+encodeURIComponent(id)+'/'+action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const cart=await api('/carts/'+encodeURIComponent(id));displayCart(cart);
    const delta=quantity-Number(item.quantity||0);
    if(delta)track(delta>0?'add_to_cart':'remove_from_cart',model.eventForVariant(item.variant,Math.abs(delta),variantNames.get(item.variant.id)));
  }catch(e){
    if(model.expired(e)){storeCart('');displayCart({items:[]});say(cartStatus,'This bag expired. Add an item to start again.');}
    else{cartNeedsRefresh=true;checkout.hidden=true;retryVisible(true);say(cartStatus,'Could not confirm the update. Your saved bag is kept. Retry loading before making another change.');}
  }finally{busy=false;checkout.removeAttribute('aria-disabled');cartList.querySelectorAll('button,input').forEach(n=>n.disabled=cartNeedsRefresh);}
}
async function newCartWith(variantId){
  const cart=await api('/carts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({currency:'USD',items:[{variantId,quantity:1}]})});
  if(!cart?.id)throw new Error('No cart ID');
  storeCart(cart.id);
  return cart;
}
async function addToCart(variant,button,note,productName){
  const variantId=variant.id;
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
        if(!model.expired(e))throw e;
        cart=await newCartWith(variantId);
      }
    }else cart=await newCartWith(variantId);
    // A create response may omit full cart items, so fetch the current cart.
    if(!Array.isArray(cart.items))cart=await api('/carts/'+encodeURIComponent(cartId));
    displayCart(cart);say(note,'ADDED TO BAG');showBag();
    track('add_to_cart',model.eventForVariant(variant,1,productName));
  }catch(e){say(note,'Could not add item. Please retry or open its Fourthwall page.');}
  finally{busy=false;button.disabled=false;}
}
async function openCart(){
  if(busy)return;
  const stored=cartId||getStoredCart();showBag();
  if(!stored){displayCart({items:[]});return;}
  busy=true;checkout.hidden=true;retryVisible(false);say(cartStatus,'LOADING BAG…');
  try{const cart=await api('/carts/'+encodeURIComponent(stored));storeCart(stored);displayCart(cart);}
  catch(e){
    if(model.expired(e)){storeCart('');displayCart({items:[]});say(cartStatus,'Your saved bag expired. Add an item to start again.');}
    else{retryVisible(true);say(cartStatus,'Connection unavailable. Your saved bag is kept. Retry to load its latest contents.');}
  }finally{busy=false;}
}
bagButton.addEventListener('click',openCart);
document.querySelector('#ac-cart-retry')?.addEventListener('click',openCart);
checkout.addEventListener('click',event=>{
  if(busy||checkout.getAttribute('aria-disabled')==='true'||!currentCart?.id||!countItems(currentCart)){event.preventDefault();return;}
  track('begin_checkout',{currency:'USD',value:cartTotal(currentCart),items:model.cartItems(currentCart).filter(i=>i.variant).map(i=>model.ecommerceItem(i.variant,i.quantity,variantNames.get(i.variant.id)))});
});
document.querySelector('#ac-cart-close')?.addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
mobileToggle?.addEventListener('click',()=>{
  const open=nav.classList.toggle('is-open');
  mobileToggle.setAttribute('aria-expanded',String(open));
});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');mobileToggle?.setAttribute('aria-expanded','false');}));
const stored=getStoredCart();
if(stored){
  api('/carts/'+encodeURIComponent(stored)).then(cart=>{storeCart(stored);updateCount(cart);}).catch(e=>{if(model.expired(e))storeCart('');});
}
loadCatalog();
})();
