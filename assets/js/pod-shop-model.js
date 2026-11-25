/* Pure catalog/cart rules shared by the storefront and its regression checks. */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.ACShopModel=api;
})(typeof window==='object'?window:this,function(){
  'use strict';
  const order=['XXS','XS','S','M','L','XL','2XL','3XL','4XL','5XL'];
  const color=v=>String(v?.attributes?.color?.name||'Default');
  const size=v=>String(v?.attributes?.size?.name||'One size');
  function available(product){
    return (Array.isArray(product?.variants)?product.variants:[]).filter(v=>v?.id&&
      !['UNAVAILABLE','SOLD_OUT'].includes(v.stock?.type)&&v.unitPrice?.value!=null&&
      Number.isFinite(Number(v.unitPrice.value))&&Number(v.unitPrice.value)>=0);
  }
  function photos(value){
    return [...new Set((Array.isArray(value)?value:[]).map(x=>typeof x==='string'?x:x?.url)
      .filter(u=>typeof u==='string'&&/^https:\/\//.test(u)))];
  }
  function colors(product){return [...new Set(available(product).map(color))];}
  function sizes(product,chosenColor){
    return available(product).filter(v=>color(v)===chosenColor).sort((a,b)=>{
      const rank=v=>{const n=order.indexOf(size(v));return n<0?99:n;};
      return rank(a)-rank(b)||size(a).localeCompare(size(b));
    });
  }
  function variant(product,chosenColor,chosenSize){
    return available(product).find(v=>color(v)===chosenColor&&size(v)===chosenSize)||null;
  }
  function colorPhotos(product,chosenColor,chosenVariant){
    const all=Array.isArray(product?.variants)?product.variants:[];
    const same=all.filter(v=>color(v)===chosenColor);
    const specific=chosenVariant&&color(chosenVariant)===chosenColor?photos(chosenVariant.images):[];
    if(specific.length)return specific;
    for(const v of same){const urls=photos(v.images);if(urls.length)return urls;}
    // Product-wide photos are safe only when no other color exists, including sold-out colors.
    return new Set(all.map(color)).size===1?photos(product.images):[];
  }
  function cartItems(cart){return Array.isArray(cart?.items)?cart.items:[];}
  function total(cart){return Math.round(cartItems(cart).reduce((sum,i)=>
    sum+Number(i.quantity||0)*Number(i.variant?.unitPrice?.value||0),0)*100)/100;}
  function ecommerceItem(v,quantity,name){
    return {item_id:String(v.id),item_name:name||v.name||'Apocalypse Closet item',
      item_brand:'Apocalypse Closet',item_variant:[color(v),size(v)].join(' / '),
      price:Number(v.unitPrice.value),quantity:Number(quantity)};
  }
  function eventForVariant(v,quantity,name){
    return {currency:v.unitPrice.currency||'USD',value:Math.round(Number(v.unitPrice.value)*quantity*100)/100,
      items:[ecommerceItem(v,quantity,name)]};
  }
  function productSchema(product,url){
    // Sizes/colors are variants of one design, not offers from multiple sellers.
    // Preserve sold-out variants with truthful availability; never invent identifiers.
    const priced=(Array.isArray(product?.variants)?product.variants:[]).filter(v=>
      v?.id&&v.stock?.type!=='UNAVAILABLE'&&v.unitPrice?.value!=null&&
      Number.isFinite(Number(v.unitPrice.value))&&Number(v.unitPrice.value)>=0&&
      /^[A-Z]{3}$/.test(v.unitPrice.currency||''));
    const result={'@context':'https://schema.org','@type':'ProductGroup','@id':url+'#product-group',
      name:product.name,url,image:photos(product.images),
      brand:{'@type':'Brand',name:'Apocalypse Closet'},
      productGroupID:String(product.id||product.slug),
      variesBy:['https://schema.org/color','https://schema.org/size'],
      hasVariant:priced.map(v=>{
        const target=new URL(url);target.searchParams.set('variant',v.id);
        const ownPhotos=photos(v.images),sameColor=colorPhotos(product,color(v),v);
        return {'@type':'Product','@id':url+'#variant-'+encodeURIComponent(v.id),
          sku:String(v.id),
          name:product.name+' — '+color(v)+' / '+size(v),url:target.href,
          image:(ownPhotos.length?ownPhotos:sameColor).slice(0,1),
          color:color(v),size:size(v),inProductGroupWithID:String(product.id||product.slug),
          offers:{'@type':'Offer',url:target.href,priceCurrency:v.unitPrice.currency,
            price:Number(v.unitPrice.value).toFixed(2),
            availability:'https://schema.org/'+(v.stock?.type==='SOLD_OUT'?'OutOfStock':'InStock')}};
      })};
    return result;
  }
  const expired=error=>[404,410].includes(Number(error?.status));
  return {color,size,available,colors,sizes,variant,photos,colorPhotos,cartItems,total,ecommerceItem,eventForVariant,expired,productSchema};
});
