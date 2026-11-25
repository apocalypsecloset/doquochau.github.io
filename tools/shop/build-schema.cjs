/* Refresh from the public read-only proxy, then bake the same schema used at runtime. */
const fs=require('node:fs');
const path=require('node:path');
const model=require('../../assets/js/pod-shop-model.js');
const root=path.resolve(__dirname,'../..');
const snapshotFile=path.join(__dirname,'catalog.snapshot.json');
const slugs=['silent-chaos-gothic-angel-graphic-tee-apocalypse-closet','thorn-heart-gothic-graphic-tee-apocalypse-closet'];
function publicSnapshot(p){
  return {id:p.id,slug:p.slug,name:p.name,state:{type:p.state?.type},access:{type:p.access?.type},
    images:model.photos(p.images),additionalInformation:p.additionalInformation||[],
    variants:(p.variants||[]).map(v=>({id:v.id,name:v.name,stock:{type:v.stock?.type},
      unitPrice:v.unitPrice,attributes:{color:{name:model.color(v)},size:{name:model.size(v)}},images:model.photos(v.images)}))};
}
async function main(){
  let snapshot=JSON.parse(fs.readFileSync(snapshotFile,'utf8'));
  if(process.argv.includes('--refresh')){
    const products=[];
    for(const slug of slugs){
      const response=await fetch('https://apocalypse-pod-api.doquochau92.workers.dev/v1/products/'+slug,{signal:AbortSignal.timeout(30000)});
      if(!response.ok)throw new Error('Catalog HTTP '+response.status);
      const product=await response.json();
      if(product.slug!==slug||product.state?.type!=='AVAILABLE'||product.access?.type!=='PUBLIC'||!product.variants?.length)throw new Error('Unexpected public product: '+slug);
      products.push(publicSnapshot(product));
    }
    snapshot={checkedAt:new Date().toISOString(),products};
    fs.writeFileSync(snapshotFile,JSON.stringify(snapshot,null,2)+'\n');
  }
  for(const slug of slugs){
    const product=snapshot.products.find(p=>p.slug===slug);
    if(!product)throw new Error('Missing snapshot: '+slug);
    const file=path.join(root,'products',slug,'index.html');
    const source=fs.readFileSync(file,'utf8');
    const pattern=/(<script id="ac-product-detail-schema" type="application\/ld\+json">)([\s\S]*?)(<\/script>)/;
    const match=source.match(pattern);if(!match)throw new Error('Missing schema block');
    const previous=JSON.parse(match[2]);
    const schema={...model.productSchema(product,'https://apocalypsecloset.com/products/'+slug+'/'),description:previous.description};
    if(!schema.hasVariant.length||schema.hasVariant.some(v=>!v.image.length))throw new Error('Missing priced variants/photos');
    // No HTML execution from API text, including a literal closing script tag.
    const json=JSON.stringify(schema).replace(/</g,'\\u003c');
    let updated=source.replace(pattern,(_,open,old,close)=>open+json+close);
    const available=model.available(product);
    if(available.length){
      const lowest=available.reduce((a,b)=>Number(a.unitPrice.value)<=Number(b.unitPrice.value)?a:b);
      const label='FROM '+new Intl.NumberFormat('en-US',{style:'currency',currency:lowest.unitPrice.currency}).format(lowest.unitPrice.value);
      updated=updated.replace(/(<strong id="ac-feature-price">)[\s\S]*?(<\/strong>)/,(_,a,b)=>a+label+b);
    }
    if(process.argv.includes('--check')){
      if(source!==updated)throw new Error('Static schema/price needs refresh: '+slug);
    }else fs.writeFileSync(file,updated);
  }
  console.log('Verified/built schema for '+slugs.length+' products; snapshot '+snapshot.checkedAt);
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
