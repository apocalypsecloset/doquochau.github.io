"""Focused regression checks for the shared bilingual blog CTA generator."""
import argparse
import json
import tempfile
import re
import unittest
from pathlib import Path
import inject_cta as cta


class BlogCTA(unittest.TestCase):
    def setUp(self):
        self.cfg=json.loads((cta.HERE/'config.json').read_text(encoding='utf8'))
        self.tpl=cta.load_template()
        self.opts=argparse.Namespace(remove=False,move_vi_link=False,keep_app_box=True)

    def test_style_matching_and_safe_markup(self):
        self.assertEqual(cta.pick_product(self.cfg,'phoi-do-grunge-nu','Phối đồ grunge nữ'),'silent-chaos')
        self.assertEqual(cta.pick_product(self.cfg,'romantic-goth-style-guide','Romantic Goth'),'thorn-heart')
        self.assertFalse(cta.matches_keyword('winter trends','ren'))
        self.assertEqual(cta.fill('{{text}}',{'text':'<script>&"'}),'&lt;script&gt;&amp;&quot;')

    def test_product_and_legacy_modes_keep_product_links_on_main_domain(self):
        for mode in ['product','fourthwall']:
            self.cfg['link_mode']=mode
            for pid, product in self.cfg['products'].items():
                target=cta.url(self.cfg,pid,'mid','example-guide')
                self.assertEqual(target,product['product_url'])
                self.assertTrue(target.startswith('https://apocalypsecloset.com/products/'))
                self.assertNotIn('utm_',target)

    def test_two_locales_repeat_generation_and_short_article(self):
        for lang in ['en','vi']:
            for sections in [1,6]:
                with self.subTest(lang=lang,sections=sections),tempfile.TemporaryDirectory() as temp:
                    p=Path(temp)/'grunge.html'
                    body=''.join(f'<h2>Section {i}</h2><p>Original advice {i}.</p>' for i in range(sections))
                    p.write_text('<html><head><title>Guide</title></head><body><header>Menu</header><main><article><h1>Grunge</h1><p class="intro">Original introduction.</p>'+body+'</article></main></body></html>',encoding='utf8')
                    first,info=cta.process(p,lang,self.cfg,self.tpl,self.opts)
                    p.write_text(first,encoding='utf8')
                    again,_=cta.process(p,lang,self.cfg,self.tpl,self.opts)
                    self.assertEqual(first,again)
                    self.assertEqual(first.count('<!-- ac-cta:top -->'),1)
                    self.assertEqual(first.count('<!-- ac-cta:end -->'),1)
                    self.assertEqual(bool(info['mid']),sections==6)
                    self.assertEqual(first.count('class="ac-bcta__banner-bar"'),3 if sections==6 else 2)
                    self.assertEqual(first.count('ac-bcta--red"'),2 if sections==6 else 1)
                    self.assertIn('href="/#shop"',first)
                    top=re.search(r'<!-- ac-cta:top -->(.*?)<!-- /ac-cta:top -->',first,re.S).group(1)
                    self.assertIn('href="/#shop"',top)
                    self.assertLess(first.index('</header>'),first.index('<!-- ac-cta:top -->'))
                    self.assertLess(first.index('<main>'),first.index('<!-- ac-cta:top -->'))
                    self.assertLess(first.index('<!-- ac-cta:top -->'),first.index('<article>'))
                    self.assertEqual(first.count(cta.FONT_PRELOAD),1)
                    self.assertEqual(first.count('<style id="ac-blog-cta-style"'),1)
                    self.assertNotIn('href="/assets/css/blog-shop-cta.',first)
                    self.assertNotIn('shop.apocalypsecloset.com',first)
                    self.assertNotIn('utm_',first)
                    self.assertIn('Mua mẫu áo này' if lang=='vi' else 'Shop this tee',top)
                    self.assertNotIn('/?utm_source',first)
                    self.assertIn('Từ $29.99 USD' if lang=='vi' else 'From $29.99 USD',first)
                    self.assertIn('Original advice 0.',first)

    def test_existing_middle_survives_a_shorter_article(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'grunge.html'
            body=''.join(f'<h2>Section {i}</h2><p>Original advice {i}.</p>' for i in range(6))
            p.write_text('<html><head></head><body><main><article><h1>Grunge</h1><p class="intro">Intro.</p>'+body+'</article></main></body></html>',encoding='utf8')
            first,_=cta.process(p,'en',self.cfg,self.tpl,self.opts)
            for i in range(2,6):first=first.replace(f'<h2>Section {i}</h2><p>Original advice {i}.</p>','')
            p.write_text(first,encoding='utf8')
            revised,info=cta.process(p,'en',self.cfg,self.tpl,self.opts)
            self.assertTrue(info['mid'])
            self.assertEqual(revised.count('<!-- ac-cta:mid -->'),1)
            self.assertNotIn(cta.MID_POSITION,revised)
            p.write_text(revised,encoding='utf8')
            self.assertEqual(cta.process(p,'en',self.cfg,self.tpl,self.opts)[0],revised)

    def test_remove_clears_inline_style_and_font_preload(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'grunge.html'
            p.write_text('<html><head></head><body><main><article><h1>Grunge</h1><p class="intro">Intro.</p></article></main></body></html>',encoding='utf8')
            rendered,_=cta.process(p,'vi',self.cfg,self.tpl,self.opts)
            p.write_text(rendered,encoding='utf8')
            self.opts.remove=True
            stripped,_=cta.process(p,'vi',self.cfg,self.tpl,self.opts)
            self.assertNotIn('ac-cta:',stripped)
            self.assertNotIn('ac-blog-cta-style',stripped)
            self.assertNotIn(cta.FONT_HREF,stripped)


if __name__=='__main__':unittest.main()
