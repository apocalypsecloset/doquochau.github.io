// ═══════════════════════════════════════════════════════════════════
//  APOCALYPSE CLOSET — DATA FILE (SINGLE SOURCE OF TRUTH)
//
//  Chỉ cần sửa file này khi thêm/xoá/chỉnh sửa outfit.
//  Mọi trang (index, style, outfit-detail) đều đọc từ đây.
//
//  CATEGORY hợp lệ:
//    "Dark Feminine" | "E-Girl" | "Goth" | "Baddie Streetwear" | "Punk"
//
//  SLUG: dùng cho URL tĩnh /outfits/{slug}.html
//    Format: look-{XX}-{category-kebab}
// ═══════════════════════════════════════════════════════════════════

const BASE = "/images/badgirl-outfits";
const STYLE_BY_LOOK = { 1: "e-girl", 2: "baddie-streetwear", 3: "punk", 4: "dark-feminine", 5: "e-girl", 6: "punk", 7: "baddie-streetwear", 8: "e-girl", 9: "goth", 10: "punk", 11: "e-girl", 12: "punk", 13: "e-girl", 14: "baddie-streetwear", 15: "dark-feminine", 16: "goth", 17: "baddie-streetwear", 18: "dark-feminine", 19: "punk", 20: "baddie-streetwear", 21: "baddie-streetwear", 22: "dark-feminine", 23: "baddie-streetwear", 24: "goth", 25: "goth", 26: "baddie-streetwear", 27: "baddie-streetwear", 28: "baddie-streetwear", 29: "dark-feminine", 30: "dark-feminine", 31: "e-girl", 32: "goth", 33: "e-girl", 34: "baddie-streetwear", 35: "e-girl", 36: "dark-feminine", 37: "baddie-streetwear", 38: "punk", 39: "baddie-streetwear", 40: "dark-feminine" };
const IMG_PART_BY_INDEX = { 1: "full-outfit", 2: "top", 3: "bottom", 4: "shoes-accessories" };
const G = (look, idx) => `${BASE}/badgirl-${STYLE_BY_LOOK[look]}-look-${String(look).padStart(2, '0')}-${IMG_PART_BY_INDEX[idx]}.webp`;

const outfits = [

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-01",
    slug: "look-01-egirl",
    img: G(1, 1),
    tag: "LOOK #01",
    title: "E-Girl Badgirl Look #01",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #1",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(1,1), G(1,2), G(1,3), G(1,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/5L8kqv2cYU" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/7KtpB6lXBE" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/1qYsgUvT14" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/3Vh6fZe3wj" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-02",
    slug: "look-02-baddie-streetwear",
    img: G(2, 1),
    tag: "LOOK #02",
    title: "Baddie Streetwear Badgirl Look #02",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #2",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(2,1), G(2,2), G(2,3), G(2,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/70GyjqNLNt" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/6pxYXXNyis" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/7AaOw9Mi2u" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/7Ktp8SM4hv" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-03",
    slug: "look-03-punk",
    img: G(3, 1),
    tag: "LOOK #03",
    title: "Punk Badgirl Look #03",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #3",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(3,1), G(3,2), G(3,3), G(3,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/8V5mcrsUPh?lp=aff" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/3Vh6fgqDnP" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/8KmMQaKM7U" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/60OReIw2jE" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-04",
    slug: "look-04-dark-feminine",
    img: G(4, 1),
    tag: "LOOK #04",
    title: "Dark Feminine Badgirl Look #04",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #4",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(4,1), G(4,2), G(4,3), G(4,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/8V5mcw7r05" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2g7zgEMETK" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/9023DsWZ05" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/8fPCpH1o0K" }
      ]
    }
  },

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-05",
    slug: "look-05-egirl",
    img: G(5, 1),
    tag: "LOOK #05",
    title: "E-Girl Badgirl Look #05",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #5",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(5,1), G(5,2), G(5,3), G(5,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/7pq5pkwORf" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2g7zgHJmcL" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/9zuaPkE8Ab" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/9UyJoqOZEZ" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-06",
    slug: "look-06-punk",
    img: G(6, 1),
    tag: "LOOK #06",
    title: "Punk Badgirl Look #06",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #6",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(6,1), G(6,2), G(6,3), G(6,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/70GysF5r8y" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/BQehiyWob" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/8fPCpKtS82" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/6VKiFMzZvL" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-07",
    slug: "look-07-baddie-streetwear",
    img: G(7, 1),
    tag: "LOOK #07",
    title: "Baddie Streetwear Badgirl Look #07",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #7",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(7,1), G(7,2), G(7,3), G(7,4) ],
      items: [
        
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/20sdZXBm96" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2BC3lqB8o9" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/2LVTy9AVTC" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/2VouAS9s8F" }
      
      ]
    }
  },

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-08",
    slug: "look-08-egirl",
    img: G(8, 1),
    tag: "LOOK #08",
    title: "E-Girl Badgirl Look #08",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #8",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(8,1), G(8,2), G(8,3), G(8,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/7AaU1mc6qg" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/70H3pTckBf" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/7VDKQOaqAm" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/7KtuE5bTVl" }
      ]
    }
  },

  // ── GOTH ──────────────────────────────────────────────────────
  {
    id: "look-09",
    slug: "look-09-goth",
    img: G(9, 1),
    tag: "LOOK #09",
    title: "Goth Badgirl Look #09",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #9",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(9,1), G(9,2), G(9,3), G(9,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/7pqAp0ZZUs" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/7fWkchaCpr" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/8AT1DcYIoy" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/809b1JYw9x" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-10",
    slug: "look-10-punk",
    img: G(10, 1),
    tag: "LOOK #10",
    title: "Punk Badgirl Look #10",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #10",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(10,1), G(10,2), G(10,3), G(10,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/8V5rcEX294" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/8KmRPvXfU3" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/8pii0qVlTA" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/8fPHoXWOo9" }
      ]
    }
  },

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-11",
    slug: "look-11-egirl",
    img: G(11, 1),
    tag: "LOOK #11",
    title: "E-Girl Badgirl Look #11",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #11",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(11,1), G(11,2), G(11,3), G(11,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/9ALYPSUUnG" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/9028D9V88F" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/9UyOo4TE7M" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/9KeyblTrSL" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-12",
    slug: "look-12-punk",
    img: G(12, 1),
    tag: "LOOK #12",
    title: "Punk Badgirl Look #12",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #12",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(12,1), G(12,2), G(12,3), G(12,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/9pbFCgRxRS" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/9fHp0NSamR" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/AAE5bIQglY" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/9zufOzRK6X" }
      ]
    }
  },

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-13",
    slug: "look-13-egirl",
    img: G(13, 1),
    tag: "LOOK #13",
    title: "E-Girl Badgirl Look #13",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #13",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(13,1), G(13,2), G(13,3), G(13,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/AUqvzuPQ5e" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/AKXVnbQ3Qd" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/BQjgv2l3g" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/17JUc3OOf" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-14",
    slug: "look-14-baddie-streetwear",
    img: G(14, 1),
    tag: "LOOK #14",
    title: "Baddie Streetwear Badgirl Look #14",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #14",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(14,1), G(14,2), G(14,3), G(14,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/W3a5X1UNm" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/Lk9tE27il" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/qgQU90Dhs" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/gN0Hq0r2r" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-15",
    slug: "look-15-dark-feminine",
    img: G(15, 1),
    tag: "LOOK #15",
    title: "Dark Feminine Badgirl Look #15",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #15",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(15,1), G(15,2), G(15,3), G(15,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/1BJGskyx1y" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/10zqgRzaMx" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/1Vw7HMxgM4" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/1Lch53yJh3" }
      ]
    }
  },

  // ── GOTH ──────────────────────────────────────────────────────
  {
    id: "look-16",
    slug: "look-16-goth",
    img: G(16, 1),
    tag: "LOOK #16",
    title: "Goth Badgirl Look #16",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #16",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(16,1), G(16,2), G(16,3), G(16,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/1qYxfywPgA" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/1gFXTfx319" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/2BBo4av90G" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/20sNsHvmLF" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-17",
    slug: "look-17-baddie-streetwear",
    img: G(17, 1),
    tag: "LOOK #17",
    title: "Baddie Streetwear Badgirl Look #17",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #17",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(17,1), G(17,2), G(17,3), G(17,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/2VoeTCtsKM" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2LVEGtuVfL" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/2qRUrosbeS" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/2g84fVtEzR" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-18",
    slug: "look-18-dark-feminine",
    img: G(18, 1),
    tag: "LOOK #18",
    title: "Dark Feminine Badgirl Look #18",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #18",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(18,1), G(18,2), G(18,3), G(18,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/3B4LGQrKyY" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/30kv47ryJX" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/3VhBf2q4Ie" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/3LNlSjqhdd" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-19",
    slug: "look-19-punk",
    img: G(19, 1),
    tag: "LOOK #19",
    title: "Punk Badgirl Look #19",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #19",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(19,1), G(19,2), G(19,3), G(19,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/3qK23eonck" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/3g0brLpQxj" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/4AwsSGnWwq" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/40dSFxoAHp" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-20",
    slug: "look-20-baddie-streetwear",
    img: G(20, 1),
    tag: "LOOK #20",
    title: "Baddie Streetwear Badgirl Look #20",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #20",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(20,1), G(20,2), G(20,3), G(20,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/4VZiqsmGGw" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/4LGIeZmtbv" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/4qCZFUkzb2" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/4ft93Blcw1" }
      ]
    }
  },


  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-21",
    slug: "look-21-baddie-streetwear",
    img: G(21, 1),
    tag: "LOOK #21",
    title: "Baddie Streetwear Badgirl Look #21",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #21",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(21,1), G(21,2), G(21,3), G(21,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/20sdZXBm96" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2BC3lqB8o9" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/2LVTy9AVTC" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/6VL2vnue1P" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-22",
    slug: "look-22-dark-feminine",
    img: G(22, 1),
    tag: "LOOK #22",
    title: "Dark Feminine Badgirl Look #22",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #22",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(22,1), G(22,2), G(22,3), G(22,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/2g8KMl9EnI" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2qRkZ48bSL" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/30lAlN7y7O" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/3B4axg7KmR" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-23",
    slug: "look-23-baddie-streetwear",
    img: G(23, 1),
    tag: "LOOK #23",
    title: "Baddie Streetwear Badgirl Look #23",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #23",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(23,1), G(23,2), G(23,3), G(23,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/3LO19z6hRU" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/3VhRMI646X" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/3g0rYb5Qla" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/3qKHku4nQd" }
      ]
    }
  },

  // ── GOTH ─────────────────────────────────────────────
  {
    id: "look-24",
    slug: "look-24-goth",
    img: G(24, 1),
    tag: "LOOK #24",
    title: "Goth Badgirl Look #24",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #24",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(24,1), G(24,2), G(24,3), G(24,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/40dhxD4A5g" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/4Ax89W3Wkj" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/4LGYLp2tPm" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/4VZyY82G4p" }
      ]
    }
  },

  // ── GOTH ─────────────────────────────────────────────
  {
    id: "look-25",
    slug: "look-25-goth",
    img: G(25, 1),
    tag: "LOOK #25",
    title: "Goth Badgirl Look #25",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #25",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(25,1), G(25,2), G(25,3), G(25,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/4ftOkR1cjs" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/4qCowk0zOv" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/50WF930M3y" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/5ApfLLzij1" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-26",
    slug: "look-26-baddie-streetwear",
    img: G(26, 1),
    tag: "LOOK #26",
    title: "Baddie Streetwear Badgirl Look #26",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #26",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(26,1), G(26,2), G(26,3), G(26,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/5L95Xez5O4" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/5VSVjxyS37" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/5flvwGxoiA" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/5q5M8ZxBND" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-27",
    slug: "look-27-baddie-streetwear",
    img: G(27, 1),
    tag: "LOOK #27",
    title: "Baddie Streetwear Badgirl Look #27",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #27",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(27,1), G(27,2), G(27,3), G(27,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/60OmKswY2G" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/6AiCXBvuhJ" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/6L1cjUvHMM" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/6VL2vnue1P" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-28",
    slug: "look-28-baddie-streetwear",
    img: G(28, 1),
    tag: "LOOK #28",
    title: "Baddie Streetwear Badgirl Look #28",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #28",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(28,1), G(28,2), G(28,3), G(28,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/6feT86u0gS" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/6pxtKPtNLV" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/70HJWisk0Y" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/7Aajj1s6fb" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-29",
    slug: "look-29-dark-feminine",
    img: G(29, 1),
    tag: "LOOK #29",
    title: "Dark Feminine Badgirl Look #29",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #29",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(29,1), G(29,2), G(29,3), G(29,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/7Ku9vKrTKe" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/7VDa7dqpzh" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/7fX0JwqCek" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/7pqQWFpZJn" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-30",
    slug: "look-30-dark-feminine",
    img: G(30, 1),
    tag: "LOOK #30",
    title: "Dark Feminine Badgirl Look #30",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #30",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(30,1), G(30,2), G(30,3), G(30,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/809qiYovyq" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/8ATGuroIdt" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/8Kmh7AnfIw" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/8V67JTn1xz" }
      ]
    }
  },

  // ── E-GIRL ─────────────────────────────────────────────
  {
    id: "look-31",
    slug: "look-31-egirl",
    img: G(31, 1),
    tag: "LOOK #31",
    title: "E-Girl Badgirl Look #31",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #31",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(31,1), G(31,2), G(31,3), G(31,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/8fPXVmmOd2" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/8pixi5llI5" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/902NuOl7x8" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/9ALo6hkUcB" }
      ]
    }
  },

  // ── GOTH ─────────────────────────────────────────────
  {
    id: "look-32",
    slug: "look-32-goth",
    img: G(32, 1),
    tag: "LOOK #32",
    title: "Goth Badgirl Look #32",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #32",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(32,1), G(32,2), G(32,3), G(32,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/9KfEJ0jrHE" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/9UyeVJjDwH" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/9fI4hciabK" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/9pbUtvhxGN" }
      ]
    }
  },

  // ── E-GIRL ─────────────────────────────────────────────
  {
    id: "look-33",
    slug: "look-33-egirl",
    img: G(33, 1),
    tag: "LOOK #33",
    title: "E-Girl Badgirl Look #33",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #33",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(33,1), G(33,2), G(33,3), G(33,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/9zuv6EhJvQ" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/AAELIXggaT" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/AKXlUqg3FW" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/AUrBh9fPuZ" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-34",
    slug: "look-34-baddie-streetwear",
    img: G(34, 1),
    tag: "LOOK #34",
    title: "Baddie Streetwear Badgirl Look #34",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #34",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(34,1), G(34,2), G(34,3), G(34,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/BQzOAIksa" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/17ZBrJODZ" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/W3pmmHUCg" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/LkPaTI7Xf" }
      ]
    }
  },

  // ── E-GIRL ─────────────────────────────────────────────
  {
    id: "look-35",
    slug: "look-35-egirl",
    img: G(35, 1),
    tag: "LOOK #35",
    title: "E-Girl Badgirl Look #35",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #35",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(35,1), G(35,2), G(35,3), G(35,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/qggBOGDWm" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/gNFz5Gqrl" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/1BJWa0Ewqs" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/1106NhFaBr" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-36",
    slug: "look-36-dark-feminine",
    img: G(36, 1),
    tag: "LOOK #36",
    title: "Dark Feminine Badgirl Look #36",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #36",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(36,1), G(36,2), G(36,3), G(36,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/1VwMycDgAy" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/1LcwmJEJVx" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/1qZDNECPV4" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/1gFnAvD2q3" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-37",
    slug: "look-37-baddie-streetwear",
    img: G(37, 1),
    tag: "LOOK #37",
    title: "Baddie Streetwear Badgirl Look #37",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #37",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(37,1), G(37,2), G(37,3), G(37,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/2BC3lqB8pA" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/20sdZXBmA9" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/2VouAS9s9G" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/2LVTy9AVUF" }
      ]
    }
  },

  // ── PUNK ─────────────────────────────────────────────
  {
    id: "look-38",
    slug: "look-38-punk",
    img: G(38, 1),
    tag: "LOOK #38",
    title: "Punk Badgirl Look #38",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #38",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(38,1), G(38,2), G(38,3), G(38,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/2qRkZ48bTM" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/2g8KMl9EoL" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/3B4axg7KnS" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/30lAlN7y8R" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────────
  {
    id: "look-39",
    slug: "look-39-baddie-streetwear",
    img: G(39, 1),
    tag: "LOOK #39",
    title: "Baddie Streetwear Badgirl Look #39",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #39",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(39,1), G(39,2), G(39,3), G(39,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/3VhRMI647Y" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/3LO19z6hSX" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/3qKHku4nRe" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/3g0rYb5Qmd" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-40",
    slug: "look-40-dark-feminine",
    img: G(40, 1),
    tag: "LOOK #40",
    title: "Dark Feminine Badgirl Look #40",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #40",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(40,1), G(40,2), G(40,3), G(40,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "https://s.shopee.vn/4Ax89W3Wlk" },
        { name: "QUẦN",     type: "Bottom Item", link: "https://s.shopee.vn/40dhxD4A6j" },
        { name: "GIÀY",     type: "Footwear",    link: "https://s.shopee.vn/4VZyY82G5q" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "https://s.shopee.vn/4LGYLp2tQp" }
      ]
    }
  },

  // ════════════════════════════════════════════════════════════════
  //  ↓ THÊM OUTFIT MỚI Ở ĐÂY — copy block này, xoá dấu // rồi điền
  // ════════════════════════════════════════════════════════════════
  //
  // {
  //   id: "look-21",
  //   slug: "look-21-dark-feminine",       // ← thêm dòng này
  //   img: G(21, 1),
  //   tag: "LOOK #21",
  //   title: "Look 21",
  //   category: "Dark Feminine",
  //   detail: {
  //     title: "OUTFIT DETAILS #21",
  //     desc: "Mô tả ngắn về look này.",
  //     imgs: [ G(21,1), G(21,2), G(21,3), G(21,4) ],
  //     items: [
  //       { name: "ÁO",       type: "Top Item",    link: "LINK_SHOPEE" },
  //       { name: "QUẦN",     type: "Bottom Item", link: "LINK_SHOPEE" },
  //       { name: "GIÀY",     type: "Footwear",    link: "LINK_SHOPEE" },
  //       { name: "PHỤ KIỆN", type: "Accessories", link: "LINK_SHOPEE" },
  //     ]
  //   }
  // },

];
