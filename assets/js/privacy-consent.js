(function () {
  'use strict';
  if (window.ACPrivacy) return;
  var KEY='ac_cookie_consent_v1', AGE=180*24*60*60*1000, GA='G-452MPHT894';
  var production=/^(www\.)?apocalypsecloset\.com$/.test(location.hostname);
  var en=document.documentElement.lang.indexOf('en')===0;
  var signal=navigator.globalPrivacyControl===true;
  var saved=null, loaded=false, banner, dialog, toggle, opener;
  function read(){try{var x=JSON.parse(localStorage.getItem(KEY));return x&&x.v===1&&typeof x.analytics==='boolean'&&Number.isFinite(x.at)&&x.at<=Date.now()&&Date.now()-x.at<AGE?x:null;}catch(_){return null;}}
  saved=read();
  function allowed(){return !signal&&!!(saved&&saved.analytics&&Date.now()-saved.at<AGE);}
  window.dataLayer=window.dataLayer||[];
  function raw(){window.dataLayer.push(arguments);}
  var denied={analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'};
  if(!window.__acConsentDefault)raw('consent','default',denied);window.__acConsentDefault=true;
  window['ga-disable-'+GA]=!allowed();
  // Legacy callers cannot queue analytics before consent, including shop/login events.
  window.gtag=function(){if(arguments[0]==='consent'||(production&&allowed()))raw.apply(null,arguments);};
  function clearCookies(){
    document.cookie.split(';').forEach(function(part){var name=part.split('=')[0].trim();if(!/^(_ga(?:_|$)|_gid$|_gat(?:_|$))/.test(name))return;
      ['',location.hostname,'.'+location.hostname,'apocalypsecloset.com','.apocalypsecloset.com'].forEach(function(domain){document.cookie=name+'=; Max-Age=0; Path=/'+(domain?'; Domain='+domain:'')+'; SameSite=Lax';});
    });
  }
  function changed(){window.dispatchEvent(new CustomEvent('ac:consentchange',{detail:{analytics:allowed()}}));}
  function choose(analytics){
    var was=allowed();saved={v:1,analytics:!!analytics&&!signal,at:Date.now()};
    try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(_){}
    window['ga-disable-'+GA]=!allowed();
    if(!allowed())clearCookies();
    if(banner)banner.hidden=true;
    if(dialog&&dialog.open)dialog.close();
    if(toggle)toggle.checked=allowed();
    changed();
    // Unload the previously accepted Google library as well as disabling it.
    // The next document queues only default-denied and never loads Google tags.
    if(was&&!allowed()&&loaded)location.reload();
  }
  window.ACPrivacy={analyticsAllowed:allowed,choose:choose,openSettings:function(){if(dialog){toggle.checked=allowed();opener=document.activeElement;dialog.showModal();}},markAnalyticsLoaded:function(){loaded=true;},grantGoogleConsent:function(){if(production&&allowed())raw('consent','update',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});}};
  if(!allowed())clearCookies();
  window.addEventListener('storage',function(e){if(e.key!==KEY&&e.key!==null)return;var was=allowed();saved=read();window['ga-disable-'+GA]=!allowed();if(!allowed())clearCookies();if(banner)banner.hidden=!!saved||signal;if(toggle)toggle.checked=allowed();changed();if(was&&!allowed()&&loaded)location.reload();});
  // Re-check expiry when a long-lived tab is revisited.
  document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'&&saved&&Date.now()-saved.at>=AGE){saved=null;window['ga-disable-'+GA]=true;clearCookies();changed();if(loaded)location.reload();else if(banner)banner.hidden=false;}});
  var words=en?{
    title:'Your cookie choices',text:'Necessary storage supports sign-in, saved outfits, your bag and this choice. Optional Google Analytics measures visits and interactions only if you allow it. Declining does not prevent shopping.',reject:'Necessary only',accept:'Allow analytics',settings:'Cookie settings',save:'Save choices',analytics:'Allow Google Analytics',detail:'Optional. Advertising storage, ad user data and ad personalization remain denied. You can withdraw consent here at any time; a loaded page will reload to stop analytics.',signal:'Your browser privacy signal keeps analytics off.',privacy:'Privacy policy',close:'Close settings'
  }:{title:'Lựa chọn cookie',text:'Lưu trữ cần thiết phục vụ đăng nhập, tủ đồ, giỏ hàng và lựa chọn này. Google Analytics chỉ đo lượt truy cập và tương tác khi bạn cho phép. Từ chối không cản trở mua hàng.',reject:'Chỉ cần thiết',accept:'Cho phép phân tích',settings:'Cài đặt cookie',save:'Lưu lựa chọn',analytics:'Cho phép Google Analytics',detail:'Không bắt buộc. Lưu trữ quảng cáo, dữ liệu người dùng cho quảng cáo và cá nhân hóa quảng cáo luôn bị từ chối. Bạn có thể rút lại đồng ý tại đây; trang đã tải analytics sẽ tải lại để dừng đo lường.',signal:'Tín hiệu riêng tư của trình duyệt đang giữ analytics tắt.',privacy:'Quyền riêng tư',close:'Đóng cài đặt'};
  function el(tag,text){var e=document.createElement(tag);if(text)e.textContent=text;return e;}
  function button(text,action){var e=el('button',text);e.type='button';e.onclick=action;return e;}
  function ui(){
    var css=el('link');css.rel='stylesheet';css.href='/assets/css/privacy-consent.css?v=20261116a';document.head.appendChild(css);
    banner=el('section');banner.id='ac-cookie-banner';banner.className='ac-cookie-banner';banner.setAttribute('aria-label',words.title);banner.hidden=!!saved||signal;
    var title=el('h2',words.title);banner.append(title,el('p',words.text));
    var actions=el('div');actions.className='ac-cookie-actions';actions.append(button(words.reject,function(){choose(false);}),button(words.accept,function(){choose(true);}),button(words.settings,window.ACPrivacy.openSettings));banner.append(actions);
    var privacy=el('a',words.privacy);privacy.href=en?'/en/privacy.html':'/privacy.html';banner.append(privacy);document.body.appendChild(banner);
    dialog=el('dialog');dialog.id='ac-cookie-dialog';dialog.className='ac-cookie-dialog';dialog.setAttribute('aria-labelledby','ac-cookie-title');
    title=el('h2',words.settings);title.id='ac-cookie-title';dialog.append(title,el('p',words.text));
    var label=el('label');toggle=el('input');toggle.type='checkbox';toggle.checked=allowed();toggle.disabled=signal;label.append(toggle,document.createTextNode(words.analytics));dialog.append(label,el('p',words.detail));if(signal)dialog.append(el('p',words.signal));
    actions=el('div');actions.className='ac-cookie-actions';actions.append(button(words.reject,function(){choose(false);}),button(words.save,function(){choose(toggle.checked);}),button(words.close,function(){dialog.close();}));dialog.append(actions);dialog.addEventListener('close',function(){if(opener&&opener.isConnected)opener.focus();});document.body.appendChild(dialog);
    var footer=el('div');footer.className='ac-policy-access';footer.append(button(words.settings,window.ACPrivacy.openSettings));
    [['terms',en?'Terms':'Điều khoản'],['shipping',en?'Shipping':'Giao hàng'],['returns',en?'Returns & refunds':'Đổi trả & hoàn tiền']].forEach(function(pair){var a=el('a',pair[1]);a.href=(en?'/en/':'/')+pair[0]+'.html';footer.append(a);});
    (document.querySelector('footer')||document.body).appendChild(footer);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ui,{once:true});else ui();
}());
