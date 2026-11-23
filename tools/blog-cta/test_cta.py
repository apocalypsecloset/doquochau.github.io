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

    def test_two_locales_repeat_generation_and_short_article(self):
        for lang in ['en','vi']:
            for sections in [1,6]:
                with self.subTest(lang=lang,sections=sections),tempfile.TemporaryDirectory() as temp:
                    p=Path(temp)/'grunge.html'
                    body=''.join(f'<h2>Section {i}</h2><p>Original advice {i}.</p>' for i in range(sections))
                    p.write_text('<html><head><title>Guide</title></head><body><article><h1>Grunge</h1><p class="intro">Original introduction.</p>'+body+'</article></body></html>',encoding='utf8')
                    first,info=cta.process(p,lang,self.cfg,self.tpl,self.opts)
                    p.write_text(first,encoding='utf8')
                    again,_=cta.process(p,lang,self.cfg,self.tpl,self.opts)
                    self.assertEqual(first,again)
                    self.assertEqual(first.count('<!-- ac-cta:top -->'),1)
                    self.assertEqual(first.count('<!-- ac-cta:end -->'),1)
                    self.assertEqual(bool(info['mid']),sections==6)
                    self.assertIn('href="/#shop"',first)
                    top=re.search(r'<!-- ac-cta:top -->(.*?)<!-- /ac-cta:top -->',first,re.S).group(1)
                    self.assertNotIn('href="/#shop"',top)
                    self.assertIn('utm_medium=cta-top',top)
                    self.assertIn(self.cfg['products']['silent-chaos']['fourthwall'],top)
                    self.assertIn('Mua mẫu áo này' if lang=='vi' else 'Shop this tee',top)
                    self.assertNotIn('/?utm_source',first)
                    self.assertIn('cta-mid' if sections==6 else 'cta-end',first)
                    self.assertIn('Từ $29.99 USD' if lang=='vi' else 'From $29.99 USD',first)
                    self.assertIn('Original advice 0.',first)


if __name__=='__main__':unittest.main()
