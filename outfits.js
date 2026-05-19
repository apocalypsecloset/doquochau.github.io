// ═══════════════════════════════════════════════════════════════════
//  APOCALYPSE CLOSET — DATA FILE (SINGLE SOURCE OF TRUTH)
//
//  Chỉ cần sửa file này khi thêm/xoá/chỉnh sửa outfit.
//  Mọi trang (index, style, outfit-detail) đều đọc từ đây.
//
//  CATEGORY hợp lệ:
//    "Dark Feminine" | "E-Girl" | "Goth" | "Baddie Streetwear" | "Punk"
// ═══════════════════════════════════════════════════════════════════

const BASE = "/image";
const G = (look, idx) => `${BASE}/apocalypse-badgirl-${look}-${idx}_result.webp`;

const outfits = [

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-01",
    img: G(1, 1),
    tag: "LOOK #01",
    title: "Look 01",
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
    img: G(2, 1),
    tag: "LOOK #02",
    title: "Look 02",
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
    img: G(3, 1),
    tag: "LOOK #03",
    title: "Look 03",
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
    img: G(4, 1),
    tag: "LOOK #04",
    title: "Look 04",
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
    img: G(5, 1),
    tag: "LOOK #05",
    title: "Look 05",
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
    img: G(6, 1),
    tag: "LOOK #06",
    title: "Look 06",
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
    img: G(7, 1),
    tag: "LOOK #07",
    title: "Look 07",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #7",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [ G(7,1), G(7,2), G(7,3), G(7,4) ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-08",
    img: G(8, 1),
    tag: "LOOK #08",
    title: "Look 08",
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
    img: G(9, 1),
    tag: "LOOK #09",
    title: "Look 09",
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
    img: G(10, 1),
    tag: "LOOK #10",
    title: "Look 10",
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
    img: G(11, 1),
    tag: "LOOK #11",
    title: "Look 11",
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
    img: G(12, 1),
    tag: "LOOK #12",
    title: "Look 12",
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
    img: G(13, 1),
    tag: "LOOK #13",
    title: "Look 13",
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
    img: G(14, 1),
    tag: "LOOK #14",
    title: "Look 14",
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
    img: G(15, 1),
    tag: "LOOK #15",
    title: "Look 15",
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
    img: G(16, 1),
    tag: "LOOK #16",
    title: "Look 16",
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
    img: G(17, 1),
    tag: "LOOK #17",
    title: "Look 17",
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
    img: G(18, 1),
    tag: "LOOK #18",
    title: "Look 18",
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
    img: G(19, 1),
    tag: "LOOK #19",
    title: "Look 19",
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
    img: G(20, 1),
    tag: "LOOK #20",
    title: "Look 20",
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

  // ════════════════════════════════════════════════════════════════
  //  ↓ THÊM OUTFIT MỚI Ở ĐÂY — copy block này, xoá dấu // rồi điền
  // ════════════════════════════════════════════════════════════════
  //
  // {
  //   id: "look-21",
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
