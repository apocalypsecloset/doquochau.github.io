const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const model=require('../../assets/js/pod-shop-model.js');
const snapshot=require('./catalog.snapshot.json');
let variants=0;
for(const p of snapshot.products){
  const url='https://apocalypsecloset.com/products/'+p.slug+'/';
  const schema=model.productSchema(p,url);
  assert.equal(schema['@type'],'ProductGroup');
  assert.equal(schema.hasVariant.length,p.variants.length);
  for(const v of schema.hasVariant){
    const actual=p.variants.find(x=>String(x.id)===v.sku);
    assert(actual);assert(v.image.length);
    assert.equal(new URL(v.url).searchParams.get('variant'),String(actual.id));
    assert.equal(v.offers['@type'],'Offer');
    assert.equal(Number(v.offers.price),Number(actual.unitPrice.value));
    assert.equal(v.offers.priceCurrency,actual.unitPrice.currency);
    assert.equal(v.offers.availability,'https://schema.org/InStock');
    variants++;
  }
  const source=fs.readFileSync(path.join(__dirname,'../../products',p.slug,'index.html'),'utf8');
  const staticSchema=JSON.parse(source.match(/id="ac-product-detail-schema"[^>]*>([\s\S]*?)<\/script>/)[1]);
  assert.deepEqual(staticSchema.hasVariant,schema.hasVariant);
  assert(!JSON.stringify(staticSchema).includes('AggregateOffer'));
}
const p=structuredClone(snapshot.products[1]);
p.variants[0].stock.type='SOLD_OUT';
p.variants[1].unitPrice.value=null;
p.variants[2].unitPrice.currency='invalid';
const invalidID=p.variants[1].id,badCurrency=p.variants[2].id;
const schema=model.productSchema(p,'https://apocalypsecloset.com/products/test/');
assert.equal(schema.hasVariant[0].offers.availability,'https://schema.org/OutOfStock');
assert(!schema.hasVariant.some(v=>[invalidID,badCurrency].includes(v.sku)));
console.log('PASS: '+variants+' real variants; static/live schema parity, unique URLs, prices, sold-out and malformed data');
