"""Offline integration QA: public catalog snapshots and generated image fixtures only."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,parse_qs,quote
import threading,functools,os,json
from playwright.sync_api import sync_playwright
SITE=Path(__file__).resolve().parents[2]
OUT=SITE.parent/'seo-reports/fixes-20261125';OUT.mkdir(exist_ok=True,parents=True)
os.environ['PLAYWRIGHT_BROWSERS_PATH']=str(SITE.parent/'.runtime/ms-playwright')
products=json.loads(Path(__file__).with_name('catalog.snapshot.json').read_text(encoding='utf-8'))['products']
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(SITE)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)
fixture='<svg xmlns="http://www.w3.org/2000/svg" width="800" height="950"><rect width="800" height="950" fill="#302c2b"/><path d="M240 200L100 320 180 430 240 390 240 790 560 790 560 390 620 430 700 320 560 200Z" fill="#111"/><text x="400" y="470" text-anchor="middle" fill="#ddd" font-size="30">LOCAL QA FIXTURE</text></svg>'
errors=[];writes=[];checks=[];state={'offline':False}
def route(r):
    u=urlsplit(r.request.url)
    if u.hostname in ('127.0.0.1','localhost'):r.continue_();return
    if r.request.method not in ('GET','HEAD'):writes.append(r.request.url);r.abort();return
    if u.hostname=='apocalypse-pod-api.doquochau92.workers.dev':
        if state['offline']:r.fulfill(status=503,json={'error':'Offline fixture'});return
        product=next((p for p in products if u.path.endswith('/products/'+p['slug'])),None)
        if product:r.fulfill(json=product)
        elif '/collections/' in u.path:r.fulfill(json={'results':products})
        else:r.fulfill(status=404,json={'error':'Fixture route not found'})
    elif u.hostname=='imgproxy.fourthwall.dev':r.fulfill(content_type='image/svg+xml',body=fixture)
    else:r.abort()
def decline(page):
    button=page.get_by_role('button',name='Decline analytics',exact=True)
    if button.is_visible():button.click()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(viewport={'width':390,'height':900})
        context.route('**/*',route)
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        for product in products:
            target=base+'/products/'+product['slug']+'/'
            for width in [360,390,430,768,1440]:
                page.set_viewport_size({'width':width,'height':900})
                page.goto(target);page.wait_for_function("document.querySelector('#ac-hero-size').options.length>1")
                decline(page)
                assert page.locator('#ac-photo-thumbnails button').count()==len(product['variants'][0]['images'])
                geometry=page.locator('#ac-main-photo').evaluate('(x)=>({x:x.getBoundingClientRect().x,w:x.getBoundingClientRect().width,v:innerWidth,img:x.querySelector("img").getBoundingClientRect().width,loaded:x.querySelector("img").naturalWidth>0})')
                assert geometry['loaded'] and geometry['x']>=-1 and geometry['x']+geometry['w']<=width+1,geometry
                assert geometry['img']<=geometry['w']+1,geometry
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.locator('#ac-photo-thumbnails button').nth(1).click()
                assert page.locator('#ac-photo-thumbnails button').nth(1).get_attribute('aria-pressed')=='true'
                page.locator('#ac-main-photo').click()
                assert page.locator('#ac-image-lightbox').is_visible()
                page.keyboard.press('Escape')
                if width in (390,1440):
                    page.locator('#ac-photo-thumbnails button').first.click()
                    page.screenshot(path=str(OUT/(product['slug']+'-'+str(width)+'.png')))
                checks.append({'product':product['slug'],'viewport':width,'gallery':geometry})
            for variant in product['variants']:
                page.goto(target+'?variant='+quote(variant['id']))
                page.wait_for_function('id=>document.querySelector("#ac-hero-size").value===id',arg=variant['attributes']['size']['name'])
                assert page.locator('#ac-hero-color').input_value()==variant['attributes']['color']['name']
                assert page.locator('#ac-hero-size').input_value()==variant['attributes']['size']['name']
                assert page.locator('#ac-feature-price').inner_text()=='$'+format(variant['unitPrice']['value'],'.2f')
                assert page.locator('#ac-hero-add').is_enabled()
                schema=json.loads(page.locator('#ac-product-detail-schema').text_content())
                assert schema['@type']=='ProductGroup'
                assert len(schema['hasVariant'])==len(product['variants'])
            checks.append({'product':product['slug'],'variant_urls':len(product['variants']),'passed':True})
        state['offline']=True
        page.goto(base+'/products/'+products[0]['slug']+'/')
        page.wait_for_selector('#ac-product-retry',state='visible')
        assert page.locator('#ac-hero-add').is_disabled()
        assert json.loads(page.locator('#ac-product-detail-schema').text_content())['hasVariant'][0]['offers']['price']=='29.99'
        checks.append({'catalog_outage':'static schema/price preserved; purchase disabled'})
        state['offline']=False
        for width in (390,1440):
            page.set_viewport_size({'width':width,'height':900})
            page.goto(base+'/outfits/look-85-grunge.html')
            assert page.locator('.outfit-styling-notes').count()==1
            assert page.locator('.outfit-info-col').bounding_box()['width']>=300
            assert page.locator('.outfit-info-col .ac-reading-path').count()==1
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('.outfit-styling-notes').scroll_into_view_if_needed()
            page.screenshot(path=str(OUT/f'outfit-85-notes-{width}.png'))
        assert not errors,errors
        assert not writes,writes
        context.close();browser.close()
    (OUT/'browser-verification.json').write_text(json.dumps({'passed':True,'checks':checks,'page_errors':errors,'external_writes':writes,'images':'Synthetic fixtures; no image quality claim'},indent=2),encoding='utf-8')
    print('PASS: 10 gallery viewports, 21 deep-linked variants, API outage, outfit section; no external writes')
finally:server.shutdown();server.server_close()
