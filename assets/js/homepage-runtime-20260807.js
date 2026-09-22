function getUser() {
      try { return JSON.parse(localStorage.getItem('ac_user')); } catch { return null; }
    }

    function getSafeSavedIds() {
      if (window.getSavedIds && typeof window.getSavedIds === 'function') return window.getSavedIds();
      return new Set();
    }

    window.showToast = function(msg) {
      let t = document.getElementById('ac-toast');
      if (!t) {
        t = document.createElement('div');
        t.id = 'ac-toast';
        t.style.cssText = 'position:fixed;bottom:32px;left:50%;transform:translateX(-50%) translateY(20px);background:#111;border:1px solid #333;color:#f0ece4;font-family:Space Mono,monospace;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;padding:12px 24px;opacity:0;transition:opacity 0.3s,transform 0.3s;pointer-events:none;white-space:nowrap;z-index:9998;';
        document.body.appendChild(t);
      }
      t.textContent = msg;
      t.style.opacity = '1';
      t.style.transform = 'translateX(-50%) translateY(0)';
      clearTimeout(t._t);
      t._t = setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(-50%) translateY(20px)'; }, 2200);
    }

    function getPriorityCount() {
      return 0;
    }

    function bindSaveButton(btn, outfit, savedIds) {
      const isSaved = savedIds.has(outfit.id);
      btn.type = 'button';
      btn.dataset.outfitId = outfit.id;
      btn.dataset.outfitTag = outfit.tag;
      btn.className = 'btn-save-card' + (isSaved ? ' saved' : '');
      btn.innerHTML = isSaved ? '♥' : '♡';
      btn.setAttribute('aria-label', isSaved ? `Bỏ lưu ${outfit.tag} khỏi Closet` : `Lưu ${outfit.tag} vào Closet`);
      btn.onclick = (e) => {
        e.stopPropagation();
        if (window.toggleSave) window.toggleSave(outfit, btn);
      };
    }

    function updateGridCopy() {
      const counterEl = document.getElementById('counter');
      if (counterEl) {
        const counterText = '';
        counterEl.textContent = counterText;
        counterEl.setAttribute('data-text', counterText);
      }

      const feedCopy = document.getElementById('feed-end-copy');
      if (feedCopy) feedCopy.textContent = 'Bạn đã xem hết outfit của lượt này.';
    }

    function getThumbDimensions(outfit) {
      return { width: Number(outfit.width) || 720, height: Number(outfit.height) || 1280 };
    }

    function getThumbUrls(outfit) {
      const name = String(outfit.img || '').split('/').pop();
      return {
        mobile: `/images-mobile/badgirl-outfits/${name}`,
        mobileHd: `/images-mobile-hd/badgirl-outfits/${name}`,
        grid: `/images-grid/badgirl-outfits/${name}`
      };
    }

    function buildCard(outfit, i, savedIds, isPriority = false, isHighest = false) {
      const dims = getThumbDimensions(outfit);
      const urls = getThumbUrls(outfit);
      const ratio = `${dims.width} / ${dims.height}`;
      const card = document.createElement('article');
      card.className = 'outfit-card';
      card.dataset.outfitId = outfit.id;
      card.style.aspectRatio = ratio;

      const link = document.createElement('a');
      link.className = 'outfit-card-link';
      link.href = `/outfits/${outfit.slug}.html`;
      link.setAttribute('aria-label', `Xem chi tiết ${outfit.tag}: ${outfit.title}`);
      link.style.aspectRatio = ratio;

      const picture = document.createElement('picture');
      picture.style.aspectRatio = ratio;
      const mobileSource = document.createElement('source');
      const img = document.createElement('img');
      img.alt = `Badgirl outfit ${outfit.tag} — ${outfit.title} (${outfit.category})`;
      img.width = dims.width;
      img.height = dims.height;
      img.style.aspectRatio = ratio;
      if (typeof window.acConfigureOutfitImage === 'function') {
        window.acConfigureOutfitImage(mobileSource, img, urls, dims, isPriority, isHighest);
      } else {
        mobileSource.media = '(max-width: 768px)';
        mobileSource.srcset = `${urls.mobile} 240w, ${urls.mobileHd} 480w`;
        mobileSource.sizes = 'calc((100vw - 6px) / 2)';
        img.src = urls.grid;
        img.srcset = `${urls.mobile} 240w, ${urls.mobileHd} 480w, ${urls.grid} ${dims.width}w`;
        img.sizes = '25vw';
        img.loading = isPriority ? 'eager' : 'lazy';
        img.decoding = isHighest && window.matchMedia('(max-width: 768px)').matches ? 'sync' : 'async';
        if (isHighest) img.fetchPriority = 'high';
        else if (!isPriority) img.fetchPriority = 'low';
      }
      picture.appendChild(mobileSource);
      picture.appendChild(img);

      const overlay = document.createElement('div');
      overlay.className = 'outfit-overlay';
      overlay.innerHTML = `<span class="outfit-tag">XEM OUTFIT</span><div class="outfit-num">${outfit.tag}</div>`;
      link.appendChild(picture);
      link.appendChild(overlay);

      const saveBtn = document.createElement('button');
      card.appendChild(link);
      bindSaveButton(saveBtn, outfit, savedIds);
      card.appendChild(saveBtn);
      return { card, ratioValue: dims.height / dims.width };
    }

    window.renderAll = function(data = outfits) {
      const grid = document.getElementById('outfit-grid');
      if (window.__acMobileLazyObserver) {
        window.__acMobileLazyObserver.disconnect();
        window.__acMobileLazyObserver = null;
      }
      const savedIds = getSafeSavedIds();
      updateGridCopy();
      window.__acCurrentRenderedData = Array.isArray(data) ? data.slice() : [];

      if (!data.length) {
        grid.innerHTML = `<div style="grid-column:1/-1;padding:60px 20px;text-align:center;color:var(--muted);font-size:11px;letter-spacing:0.1em;text-transform:uppercase;">Không tìm thấy outfit nào phù hợp.</div>`;
        return;
      }

      const columnCount = window.matchMedia('(max-width: 768px)').matches ? 2 : 4;
      const columns = Array.from({ length: columnCount }, () => {
        const column = document.createElement('div');
        column.className = 'ac-masonry-column';
        return column;
      });
      const heights = Array(columnCount).fill(0);
      const priorityPerColumn = window.matchMedia('(max-width: 768px)').matches ? 1 : 2;

      data.forEach((outfit, i) => {
        const target = i < columnCount ? i : heights.indexOf(Math.min(...heights));
        const priority = columns[target].childElementCount < priorityPerColumn;
        const built = buildCard(outfit, i, savedIds, priority, i === 0);
        columns[target].appendChild(built.card);
        heights[target] += built.ratioValue + 0.002;
      });
      grid.replaceChildren(...columns);
      grid.setAttribute('aria-busy', 'false');
    };


    window.updateSaveButtons = function() {
      const savedIds = getSafeSavedIds();
      document.querySelectorAll('.btn-save-card').forEach(btn => {
        const id = btn.dataset.outfitId;
        if (!id) return;
        const saved = savedIds.has(id);
        btn.innerHTML = saved ? '♥' : '♡';
        btn.className = 'btn-save-card' + (saved ? ' saved' : '');
        const look = btn.dataset.outfitTag || id;
        btn.setAttribute('aria-label', saved ? `Bỏ lưu ${look} khỏi Closet` : `Lưu ${look} vào Closet`);
      });
    };

    function getPageSize() {
      return Math.min(32, Array.isArray(outfits) ? outfits.length : 32);
    }

    function syncOutfitPoolVersion() {
      const signature = `home32-stable-v6|${outfits.map(outfit => outfit.id).join('|')}`;
      try {
        if (sessionStorage.getItem('ac_outfit_signature') !== signature) {
          sessionStorage.removeItem('ac_pool');
          sessionStorage.removeItem('ac_last_batch');
          sessionStorage.removeItem('savedOutfitOrder');
          sessionStorage.setItem('ac_outfit_signature', signature);
        }
      } catch {}
    }

    function shuffle(ids) {
      const result = [...ids];
      for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
      }
      return result;
    }

    function restoreScrollPosition(x, y) {
      const restore = () => window.scrollTo({ left: x, top: y, behavior: 'auto' });
      restore();
      requestAnimationFrame(() => {
        restore();
        requestAnimationFrame(restore);
      });
    }

    function randomize(shouldScroll = false) {
      const PAGE_SIZE = getPageSize();
      const allIds = outfits.map(o => o.id);
      const scrollX = window.scrollX;
      const scrollY = window.scrollY;

      let pool;
      let lastBatch;
      try {
        pool = JSON.parse(sessionStorage.getItem('ac_pool') || '[]');
        lastBatch = JSON.parse(sessionStorage.getItem('ac_last_batch') || '[]');
      } catch {
        pool = [];
        lastBatch = [];
      }
      pool = Array.isArray(pool) ? pool.filter(id => allIds.includes(id)) : [];
      lastBatch = Array.isArray(lastBatch) ? lastBatch.filter(id => allIds.includes(id)) : [];
      if (pool.length === 0) {
        const fresh = allIds.filter(id => !lastBatch.includes(id));
        pool = shuffle(fresh.length >= PAGE_SIZE ? fresh : allIds);
      }

      const batch = [];
      while (batch.length < PAGE_SIZE && allIds.length > 0) {
        if (pool.length === 0) {
          let candidates = allIds.filter(id => !batch.includes(id) && !lastBatch.includes(id));
          if (candidates.length < PAGE_SIZE - batch.length) {
            candidates = allIds.filter(id => !batch.includes(id));
          }
          pool = shuffle(candidates);
          if (pool.length === 0) break;
        }
        const nextId = pool.shift();
        if (allIds.includes(nextId) && !batch.includes(nextId)) batch.push(nextId);
      }

      sessionStorage.setItem('ac_pool', JSON.stringify(pool));
      sessionStorage.setItem('ac_last_batch', JSON.stringify(batch));
      sessionStorage.setItem('savedOutfitOrder', JSON.stringify(batch));

      const batchOutfits = batch.map(id => outfits.find(o => o.id === id)).filter(Boolean);
      renderAll(batchOutfits);

      if (shouldScroll) {
        requestAnimationFrame(() => {
          document.querySelector('#outfit-grid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      } else {
        restoreScrollPosition(scrollX, scrollY);
      }
    }

    function renderFirstVisit() {
      const PAGE_SIZE = getPageSize();
      const allIds = outfits.map(outfit => outfit.id);
      const pool = shuffle(allIds);
      const batch = pool.splice(0, PAGE_SIZE);

      sessionStorage.setItem('ac_pool', JSON.stringify(pool));
      sessionStorage.setItem('ac_last_batch', JSON.stringify(batch));
      sessionStorage.setItem('savedOutfitOrder', JSON.stringify(batch));

      const batchOutfits = batch.map(id => outfits.find(outfit => outfit.id === id)).filter(Boolean);
      window.renderAll(batchOutfits);
    }

    function initGrid() {
      if (window.__acInitialGridRendered && Array.isArray(window.__acInitialBatch)) {
        window.__acCurrentRenderedData = window.__acInitialBatch.slice();
        updateGridCopy();
        return;
      }
      syncOutfitPoolVersion();
      renderFirstVisit();
    }

    function toggleSearch() {
      const bar = document.getElementById('search-bar');
      const input = document.getElementById('search-input');

      if (bar.style.display === 'block') {
        if (input.value.trim()) {
          bar.requestSubmit();
          return;
        }
        bar.style.display = 'none';
        return;
      }

      bar.style.display = 'block';
      input.focus();
    }

    const audio = document.getElementById('apocalypse-audio');
    const rec   = document.getElementById('record-icon');
    document.getElementById('music-player').addEventListener('click', () => {
      if (audio.paused) { audio.play(); rec.classList.add('playing'); }
      else              { audio.pause(); rec.classList.remove('playing'); }
    });

    
    
    

    document.getElementById('search-bar').addEventListener('submit', function(e) {
      const q = document.getElementById('search-input').value.trim();
      if (!q) e.preventDefault();
    });

    const cachedUser = getUser();
    if (cachedUser) {
      const navBtn = document.getElementById('nav-closet-btn');
      if (navBtn) {
        navBtn.href = 'closet.html';
        document.getElementById('nav-closet-icon').innerHTML = '♥';
        navBtn.style.color = '#e05444';
        navBtn.style.borderColor = '#c0392b';
      }
    }

    const acGridMedia = window.matchMedia('(max-width: 768px)');
    acGridMedia.addEventListener?.('change', () => {
      if (Array.isArray(window.__acCurrentRenderedData) && window.__acCurrentRenderedData.length) {
        window.renderAll(window.__acCurrentRenderedData);
      }
    });

    window._renderAllReady = true;
    if (typeof outfits !== 'undefined') {
      initGrid();
    } else {
      document.addEventListener('DOMContentLoaded', () => {
        if (typeof outfits !== 'undefined') initGrid();
        else {
          const grid = document.getElementById('outfit-grid');
          if (grid) grid.innerHTML = '<div style="grid-column:1/-1;padding:60px 20px;text-align:center;color:var(--muted);font-size:11px;letter-spacing:0.1em;text-transform:uppercase;">Không tải được dữ liệu outfit. Vui lòng refresh lại trang.</div>';
        }
      }, { once: true });
    }

(function(){
    let activeFilterCount = 0;
    let activeMatches = [];
    const originalRandomize = window.randomize;
    function shuffleFiltered(list){
      const copy=[...list];
      for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]];}
      return copy;
    }
    window.acApplyOutfitFilters = function(_state, matched, count){
      const wasActive = activeFilterCount > 0;
      activeFilterCount = count || 0;
      activeMatches = Array.isArray(matched) ? matched : [];
      if(activeFilterCount){
        window.renderAll(activeMatches);
        if(!activeMatches.length){const grid=document.getElementById('outfit-grid');if(grid)grid.innerHTML='<p class="ac-filter-empty">Không có outfit khớp tất cả bộ lọc. Hãy bỏ bớt một lựa chọn.</p>';}
        const counter=document.getElementById('counter');
        if(counter){const text=`${activeMatches.length} LOOK PHÙ HỢP`;counter.textContent=text;counter.setAttribute('data-text',text);}
        const feed=document.getElementById('feed-end-copy');if(feed)feed.textContent=`Đã hiển thị ${activeMatches.length} outfit phù hợp.`;
      }else if(wasActive && typeof originalRandomize==='function'){
        originalRandomize(false);
      }
    };
    let lastFilteredOrder = [];
    window.randomize = function(shouldScroll=false){
      if(!activeFilterCount) return originalRandomize(shouldScroll);
      const scrollX=window.scrollX,scrollY=window.scrollY;
      let shuffled=shuffleFiltered(activeMatches);
      const previousOrder=lastFilteredOrder.length
        ? lastFilteredOrder
        : (Array.isArray(window.__acCurrentRenderedData) ? window.__acCurrentRenderedData.map(item=>item.id) : []);
      if(shuffled.length>1 && previousOrder.length===shuffled.length){
        const same=shuffled.every((item,index)=>item.id===previousOrder[index]);
        if(same) shuffled=[...shuffled.slice(1),shuffled[0]];
      }
      lastFilteredOrder=shuffled.map(item=>item.id);
      window.renderAll(shuffled);
      const counter=document.getElementById('counter');
      if(counter){const text=`${activeMatches.length} LOOK PHÙ HỢP`;counter.textContent=text;counter.setAttribute('data-text',text);}
      if(shouldScroll){
        requestAnimationFrame(()=>document.querySelector('#outfit-grid')?.scrollIntoView({behavior:'smooth',block:'start'}));
      }else{
        const restore=()=>window.scrollTo({left:scrollX,top:scrollY,behavior:'auto'});
        restore();requestAnimationFrame(()=>{restore();requestAnimationFrame(restore);});
      }
    };
    window.acHeaderReload=function(button){
      if(button){
        button.classList.remove('is-reloading');
        void button.offsetWidth;
        button.classList.add('is-reloading');
        window.setTimeout(()=>button.classList.remove('is-reloading'),420);
      }
      window.randomize(false);
    };
  })();
