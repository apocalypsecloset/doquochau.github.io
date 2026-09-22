 
(() => {
  const header = document.querySelector('.ac-site-header');
  if (!header) return;
  const primaryNav = header.querySelector('.ac-primary-nav');
  if (primaryNav && !primaryNav.querySelector('[data-ac-nav="builder"]')) {
    const link = document.createElement('a');
    link.dataset.acNav = 'builder';
    link.href = '/app-phoi-do.html';
    link.textContent = 'Tạo outfit';
    const blogLink = primaryNav.querySelector('[data-ac-nav="blog"]');
    if (blogLink) primaryNav.insertBefore(link, blogLink); else primaryNav.appendChild(link);
  }
  document.querySelectorAll('.ac-site-footer').forEach(footer => {
    const groups = footer.querySelectorAll('.ac-footer-links');
    const first = groups[0];
    if (first && !first.querySelector('a[href="/app-phoi-do.html"]')) {
      const li = document.createElement('li');
      li.innerHTML = '<a href="/app-phoi-do.html">App phối đồ online</a>';
      first.insertBefore(li, first.firstChild);
    }
  });
  const menuButton = header.querySelector('.ac-menu-toggle');
  const dropdown = header.querySelector('.ac-nav-dropdown');
  const dropdownButton = header.querySelector('.ac-dropdown-toggle');
  const closeMenu = () => {
    header.classList.remove('is-menu-open');
    menuButton?.setAttribute('aria-expanded','false');
    dropdown?.classList.remove('is-open');
    dropdownButton?.setAttribute('aria-expanded','false');
  };
  menuButton?.addEventListener('click', () => {
    const open = !header.classList.contains('is-menu-open');
    header.classList.toggle('is-menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
  });
  const desktopHover = window.matchMedia('(hover: hover) and (min-width: 961px)');
  let dropdownCloseTimer = 0;
  const setDropdownOpen = (open) => {
    if (!dropdown) return;
    window.clearTimeout(dropdownCloseTimer);
    dropdown.classList.toggle('is-open', open);
    dropdownButton?.setAttribute('aria-expanded', String(open));
  };
  dropdownButton?.addEventListener('click', (event) => {
    event.preventDefault();
    setDropdownOpen(!dropdown.classList.contains('is-open'));
  });
  dropdown?.addEventListener('pointerenter', () => {
    if (desktopHover.matches) setDropdownOpen(true);
  });
  dropdown?.addEventListener('pointerleave', () => {
    if (!desktopHover.matches) return;
    window.clearTimeout(dropdownCloseTimer);
    dropdownCloseTimer = window.setTimeout(() => setDropdownOpen(false), 180);
  });
  dropdown?.addEventListener('focusin', () => setDropdownOpen(true));
  dropdown?.addEventListener('focusout', (event) => {
    if (!dropdown.contains(event.relatedTarget)) setDropdownOpen(false);
  });
  document.addEventListener('click', (event) => {
    if (dropdown && !dropdown.contains(event.target)) {
      dropdown.classList.remove('is-open');
      dropdownButton?.setAttribute('aria-expanded','false');
    }
  });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
  header.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    if (window.matchMedia('(max-width: 960px)').matches) closeMenu();
  }));
  const path = (location.pathname || '/').replace(/\/+$/,'') || '/';
  let section = '';
  if (path === '/') section = 'home';
  else if (path === '/app-phoi-do.html') section = 'builder';
  else if (path === '/phoi-do-nu-ca-tinh.html' || path.startsWith('/outfits/')) section = 'outfits';
  else if (path.startsWith('/style/')) section = 'style';
  else if (path === '/blog.html' || path.startsWith('/blog/')) section = 'blog';
  else if (path === '/closet.html' || path === '/login.html') section = 'closet';
  if (section === 'style') dropdownButton?.classList.add('is-active');
  else header.querySelector(`[data-ac-nav="${section}"]`)?.classList.add('is-active');
  header.querySelectorAll('.ac-dropdown-menu a').forEach(link => {
    const href = new URL(link.href, location.origin).pathname.replace(/\/+$/,'');
    if (href === path) link.classList.add('is-active');
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 960) closeMenu(); }, {passive:true});
})();
