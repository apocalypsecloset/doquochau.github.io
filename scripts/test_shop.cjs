/* Run with Node and jsdom available via NODE_PATH; no live API/cart is used. */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..');
const model=require('../assets/js/pod-shop-model.js');
function v(id,color,size,price,images,stock='UNLIMITED'){
 return {id,name:'Test tee - '+color+', '+size,attributes:{color:{name:color},size:{name:size}},unitPrice:{value:price,currency:'USD'},images:images.map(url=>({url})),stock:{type:stock}};
}
const black='https://images.example/black.webp',white='https://images.example/white.webp';
function product(){return {id:'product',name:'Test tee',slug:'silent-chaos-gothic-angel-graphic-tee-apocalypse-closet',state:{type:'AVAILABLE'},access:{type:'PUBLIC'},images:[{url:black}],variants:[v('black-s','Black','S',29.99,[black]),v('white-s','White','S',29.99,[white]),v('white-xl','White','XL',31.99,[white]),v('black-xl','Black','XL',31.99,[black],'SOLD_OUT')]};}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
async function boot(stored){
 const dom=new JSDOM(fs.readFileSync(path.join(root,'index.html'),'utf8'),{url:'https://apocalypsecloset.com/',runScripts:'outside-only'});
 const w=dom.window,events=[],calls=[];let cart={id:'test-cart',items:[]},failure=null;
 if(stored)w.localStorage.setItem('ac_fourthwall_cart_id',stored);
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
 w.AC_FOURTHWALL={apiBase:'https://api.example'};w.acTrack=(name,data)=>events.push({name,data});
 w.fetch=async(url,options={})=>{
  const pathname=new URL(url).pathname;calls.push({pathname,body:options.body&&JSON.parse(options.body)});
  if(pathname.includes('/products/')||pathname.includes('/collections/'))return {ok:true,json:async()=>pathname.includes('/collections/')?{results:[product()]}:product()};
  if(failure&&(!options.method||options.method==='GET'))return {ok:false,status:failure};
  const body=options.body?JSON.parse(options.body):{};
  if(pathname==='/v1/carts'||pathname.endsWith('/add')){
   for(const it of body.items||[]){const old=cart.items.find(i=>i.variant.id===it.variantId);if(old)old.quantity+=it.quantity;else cart.items.push({quantity:it.quantity,variant:product().variants.find(v=>v.id===it.variantId)});}
  }
  if(pathname.endsWith('/change'))for(const it of body.items)cart.items.find(i=>i.variant.id===it.variantId).quantity=it.quantity;
  if(pathname.endsWith('/remove'))for(const it of body.items){const old=cart.items.find(i=>i.variant.id===it.variantId);old.quantity-=it.quantity;cart.items=cart.items.filter(i=>i.quantity>0);}
  return {ok:true,json:async()=>JSON.parse(JSON.stringify(cart))};
 };
 w.eval(fs.readFileSync(path.join(root,'assets/js/pod-shop-model.js'),'utf8'));w.eval(fs.readFileSync(path.join(root,'assets/js/pod-shop-home.js'),'utf8'));await tick();await tick();
 return {w,dom,events,calls,setFailure:x=>failure=x,cart:()=>cart};
}
test('color/size uses actual stock and never borrows another color photo',()=>{
 const p=product();assert.equal(model.variant(p,'Black','XL'),null);assert.equal(model.variant(p,'White','XL').id,'white-xl');
 assert.deepEqual(model.colorPhotos(p,'White'),[white]);p.variants.filter(v=>model.color(v)==='White').forEach(v=>v.images=[]);
 assert.deepEqual(model.colorPhotos(p,'White'),[]);p.variants=p.variants.filter(v=>model.color(v)==='White');assert.deepEqual(model.colorPhotos(p,'White'),[black]);
});
test('added value belongs to the added item, not the pre-existing bag',()=>{
 const p=product();assert.equal(model.eventForVariant(p.variants[2],1,p.name).value,31.99);
 assert.equal(model.total({items:[{variant:p.variants[0],quantity:1},{variant:p.variants[2],quantity:1}]}),61.98);
 assert.equal(model.expired({status:503}),false);assert.equal(model.expired({status:404}),true);
});
test('render color-specific photos, add exact variant, edit quantity and remove',async()=>{
 const h=await boot();try{
  const d=h.w.document,c=d.querySelector('.ac-product-color'),s=d.querySelector('.ac-product-size');
  c.value='White';c.dispatchEvent(new h.w.Event('change'));s.value='XL';s.dispatchEvent(new h.w.Event('change'));
  assert.equal(d.querySelector('.ac-product-image img').getAttribute('src'),white);
  d.querySelector('.ac-product-add').click();await tick();await tick();assert.equal(h.cart().items[0].variant.id,'white-xl');assert.equal(d.querySelector('#ac-cart-subtotal').textContent,'$31.99');
  assert.equal(h.events.find(x=>x.name==='add_to_cart').data.value,31.99);
  const qty=d.querySelector('.ac-cart-quantity input');qty.value='2';d.querySelector('.ac-cart-quantity button').click();await tick();await tick();assert.equal(h.cart().items[0].quantity,2);assert.equal(d.querySelector('#ac-cart-subtotal').textContent,'$63.98');
  assert.match(d.querySelector('#ac-checkout-link').href,/cartCurrency=USD&cartId=test-cart/);
  [...d.querySelectorAll('.ac-cart-quantity button')].find(b=>b.textContent==='REMOVE').click();await tick();await tick();assert.equal(h.cart().items.length,0);assert.equal(d.querySelector('#ac-cart-button').textContent,'BAG (0)');assert.equal(d.querySelector('#ac-checkout-link').hidden,true);
  assert.deepEqual(h.calls.find(c=>c.pathname.endsWith('/remove')).body,{items:[{variantId:'white-xl',quantity:2}]});
 }finally{h.dom.window.close();}
});
test('transient saved-cart failure preserves the ID, expiry clears it',async()=>{
 const h=await boot('saved-cart');try{
  h.setFailure(503);h.w.document.querySelector('#ac-cart-button').click();await tick();await tick();
  assert.equal(h.w.localStorage.getItem('ac_fourthwall_cart_id'),'saved-cart');assert.equal(h.w.document.querySelector('#ac-cart-retry').hidden,false);
  h.setFailure(410);h.w.document.querySelector('#ac-cart-retry').click();await tick();await tick();assert.equal(h.w.localStorage.getItem('ac_fourthwall_cart_id'),'');
 }finally{h.dom.window.close();}
});
