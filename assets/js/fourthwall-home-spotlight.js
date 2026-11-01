/* Public Fourthwall Storefront API integration. Never use Stripe keys or Open API passwords here. */
(function () {
  'use strict';
  var root = document.getElementById('ac-pod-spotlight');
  if (!root) return;
  var cfg = window.AC_FOURTHWALL || {};
  var token = String(cfg.storefrontToken || '').trim();
  var apiEnabled = /^ptkn_[a-zA-Z0-9_-]+$/.test(token);
  var slug = 'silent-chaos-gothic-angel-graphic-tee-apocalypse-closet';
  var shopHost = 'apocalypse-closet-shop.fourthwall.com';
  var productUrl = 'https://' + shopHost + '/products/' + slug;
  var apiBase = 'https://storefront-api.fourthwall.com/v1';
  var priceEl = root.querySelector('#ac-pod-price');
  var artEl = root.querySelector('#ac-pod-art');
  var selectEl = root.querySelector('#ac-pod-size');
  var addEl = root.querySelector('#ac-pod-add');
  var linkEl = root.querySelector('#ac-pod-direct');
  var statusEl = root.querySelector('#ac-pod-status');
  var bagEl = root.querySelector('#ac-pod-bag');
  var dialogEl = document.querySelector('#ac-pod-cart-dialog');
  var detailEl = document.querySelector('#ac-pod-cart-detail');
  var checkoutEl = document.querySelector('#ac-pod-checkout');
  var cartId = '';
  var selected = {};
  var state = 'fallback';
  linkEl.href = productUrl;
  function message(text) { statusEl.textContent = text; }
  function money(v, c) { return new Intl.NumberFormat('en-US', { style: 'currency', currency: c || 'USD' }).format(Number(v)); }
  function endpoint(path, opts) {
    return fetch(apiBase + path + (path.includes('?') ? '&' : '?') + 'storefront_token=' + encodeURIComponent(token), opts).then(function (response) {
      if (!response.ok) throw new Error('Fourthwall returned ' + response.status);
      return response.json();
    });
  }
  function label(variant) {
    var a = variant.attributes || {};
    return [a.color && a.color.name, a.size && a.size.name].filter(Boolean).join(' / ') || variant.name || 'One size';
  }
  function variantOK(v) {
    return Boolean(v && v.id && v.stock && v.stock.type !== 'SOLD_OUT' && v.stock.type !== 'UNAVAILABLE');
  }
  function populate(product) {
    var variants = Array.isArray(product.variants) ? product.variants.filter(variantOK) : [];
    if (!variants.length) throw new Error('No available size');
    var image = (Array.isArray(product.images) && product.images.find(function (x) { return x && x.url; })) || null;
    if (image) {
      var img = document.createElement('img');
      img.src = image.url;
      img.alt = product.name || 'Silent Chaos Gothic Angel Graphic Tee';
      img.loading = 'lazy';
      img.decoding = 'async';
      artEl.querySelector('.ac-pod-art-placeholder').replaceWith(img);
    }
    selectEl.replaceChildren(new Option('Choose size', ''));
    variants.filter(function (v) {
      var color = v.attributes && v.attributes.color && v.attributes.color.name;
      return !color || color.toLowerCase() === 'black';
    }).forEach(function (v) {
      selected[v.id] = v;
      selectEl.add(new Option(label(v) + ' – ' + money(v.unitPrice && v.unitPrice.value || 0, v.unitPrice && v.unitPrice.currency || 'USD'), v.id));
    });
    if (selectEl.options.length === 1) {
      variants.forEach(function (v) {
        selected[v.id] = v;
        selectEl.add(new Option(label(v), v.id));
      });
    }
    selectEl.disabled = false;
    selectEl.hidden = false;
    linkEl.hidden = true;
    addEl.hidden = false;
    bagEl.hidden = false;
    state = 'live';
    message('Select your size. Shipping is calculated at checkout.');
  }
  function currentPrice() {
    var v = selected[selectEl.value];
    priceEl.textContent = v ? money(v.unitPrice && v.unitPrice.value || 0, v.unitPrice && v.unitPrice.currency || 'USD') : 'From $29.99';
  }
  async function ensureCart() {
    var old = '';
    try { old = localStorage.getItem('ac_fourthwall_cart_id') || ''; } catch (e) {}
    if (old) {
      try { await endpoint('/carts/' + encodeURIComponent(old)); return old; }
      catch (e) {}
    }
    var cart = await endpoint('/carts', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({currency:'USD'}) });
    if (!cart.id) throw new Error('Cart creation failed');
    try { localStorage.setItem('ac_fourthwall_cart_id', cart.id); } catch (e) {}
    return cart.id;
  }
  async function fetchCart() {
    if (!cartId) return null;
    return endpoint('/carts/' + encodeURIComponent(cartId));
  }
  async function addToCart() {
    var variantId = selectEl.value;
    if (!variantId || !selected[variantId]) { message('Please choose a size first.'); selectEl.focus(); return; }
    addEl.disabled = true;
    addEl.textContent = 'ADDING…';
    try {
      cartId = await ensureCart();
      await endpoint('/carts/' + encodeURIComponent(cartId) + '/add', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({items:[{variantId:variantId,quantity:1}]}) });
      var cart = await fetchCart();
      var count = (cart && Array.isArray(cart.items) ? cart.items : []).reduce(function (s, x) { return s + Number(x.quantity || 0); }, 0);
      bagEl.textContent = 'BAG (' + count + ')';
      detailEl.textContent = count + ' item(s) in your bag. Shipping and taxes are calculated by Fourthwall at checkout.';
      var params = new URLSearchParams({ cartCurrency:'USD', cartId:cartId });
      checkoutEl.href = 'https://' + shopHost + '/checkout/?' + params.toString();
      if (dialogEl.showModal) dialogEl.showModal();
      message('Added to your bag.');
    } catch (err) {
      message('Could not add to bag. Please retry or use the Fourthwall product page.');
      linkEl.hidden = false;
    } finally {
      addEl.disabled = false;
      addEl.textContent = 'ADD TO BAG';
    }
  }
  function openExistingCart() {
    if (!cartId) { message('Choose a size and add an item first.'); return; }
    fetchCart().then(function (cart) {
      var count = (cart && Array.isArray(cart.items) ? cart.items : []).reduce(function (s, x) { return s + Number(x.quantity || 0); }, 0);
      detailEl.textContent = count + ' item(s) in your bag.';
      checkoutEl.href = 'https://' + shopHost + '/checkout/?' + new URLSearchParams({cartCurrency:'USD',cartId:cartId}).toString();
      dialogEl.showModal();
    }).catch(function () { message('Could not load cart. Please add your item again.'); });
  }
  selectEl.addEventListener('change', currentPrice);
  addEl.addEventListener('click', addToCart);
  bagEl.addEventListener('click', openExistingCart);
  dialogEl.querySelector('[data-ac-pod-close]').addEventListener('click', function () { dialogEl.close(); });
  if (!apiEnabled) { message('Made to order. Choose size and checkout securely on Fourthwall.'); return; }
  message('Loading live product information…');
  endpoint('/products/' + encodeURIComponent(slug)).then(populate).catch(function () {
    state = 'fallback';
    message('Live sizes are unavailable here. View the product on Fourthwall.');
    linkEl.hidden = false;
    addEl.hidden = true;
    bagEl.hidden = true;
    selectEl.hidden = true;
  });
})();
