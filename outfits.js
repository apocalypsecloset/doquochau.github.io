// ═══════════════════════════════════════════════════════════════════
//  APOCALYPSE CLOSET — DATA FILE (SINGLE SOURCE OF TRUTH)
//
//  Chỉ cần sửa file này khi thêm/xoá/chỉnh sửa outfit.
//  Mọi trang (index, style, outfit-detail) đều đọc từ đây.
//
//  CATEGORY hợp lệ:
//    "Dark Feminine" | "E-Girl" | "Goth" | "Baddie Streetwear" | "Punk"
// ═══════════════════════════════════════════════════════════════════

const outfits = [

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-01",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-1-1.png",
    tag: "LOOK #01",
    title: "Look 01",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #1",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-1-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-2-1.png",
    tag: "LOOK #02",
    title: "Look 02",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #2",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-2-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-3-1.png",
    tag: "LOOK #03",
    title: "Look 03",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #3",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-3-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-4-1.png",
    tag: "LOOK #04",
    title: "Look 04",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #4",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-4-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-5-1.png",
    tag: "LOOK #05",
    title: "Look 05",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #5",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-5-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-6-1.png",
    tag: "LOOK #06",
    title: "Look 06",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #6",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-6-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-7-1.png",
    tag: "LOOK #07",
    title: "Look 07",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #7",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-7-1.png"
      ],
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
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-8-1.png",
    tag: "LOOK #08",
    title: "Look 08",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #8",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-8-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── GOTH ──────────────────────────────────────────────────────
  {
    id: "look-09",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-9-1.png",
    tag: "LOOK #09",
    title: "Look 09",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #9",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-9-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-10",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-10-1.png",
    tag: "LOOK #10",
    title: "Look 10",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #10",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-10-1.png"
      ],
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
    id: "look-11",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-11-1.png",
    tag: "LOOK #11",
    title: "Look 11",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #11",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-11-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-12",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-12-1.png",
    tag: "LOOK #12",
    title: "Look 12",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #12",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-12-1.png"
      ],
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
    id: "look-13",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-13-1.png",
    tag: "LOOK #13",
    title: "Look 13",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #13",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-13-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-14",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-14-1.png",
    tag: "LOOK #14",
    title: "Look 14",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #14",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-14-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-15",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-15-1.png",
    tag: "LOOK #15",
    title: "Look 15",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #15",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-15-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── GOTH ──────────────────────────────────────────────────────
  {
    id: "look-16",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-16-1.png",
    tag: "LOOK #16",
    title: "Look 16",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #16",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-16-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-17",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-17.png",
    tag: "LOOK #17",
    title: "Look 17",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #17",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-17.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── DARK FEMININE ─────────────────────────────────────────────
  {
    id: "look-18",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-18-1.png",
    tag: "LOOK #18",
    title: "Look 18",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #18",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-18-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── PUNK ──────────────────────────────────────────────────────
  {
    id: "look-19",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-19-1.png",
    tag: "LOOK #19",
    title: "Look 19",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #19",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-19-1.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ── BADDIE STREETWEAR ─────────────────────────────────────────
  {
    id: "look-20",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-20-2.png",
    tag: "LOOK #20",
    title: "Look 20",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #20",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-20-2.png"
      ],
      items: [
        { name: "ÁO",       type: "Top Item",    link: "#" },
        { name: "QUẦN",     type: "Bottom Item", link: "#" },
        { name: "GIÀY",     type: "Footwear",    link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ════════════════════════════════════════════════════════════════
  //  ↓ THÊM OUTFIT MỚI Ở ĐÂY — copy block này, xoá dấu // rồi điền
  // ════════════════════════════════════════════════════════════════
  //
  // {
  //   id: "look-21",
  //   img: "URL_ẢNH_THUMBNAIL",
  //   tag: "LOOK #21",
  //   title: "Look 21",
  //   category: "Dark Feminine",
  //   detail: {
  //     title: "OUTFIT DETAILS #21",
  //     desc: "Mô tả ngắn về look này.",
  //     imgs: [ "URL_ẢNH_1" ],
  //     items: [
  //       { name: "ÁO",       type: "Top Item",    link: "LINK_SHOPEE" },
  //       { name: "QUẦN",     type: "Bottom Item", link: "LINK_SHOPEE" },
  //       { name: "GIÀY",     type: "Footwear",    link: "LINK_SHOPEE" },
  //       { name: "PHỤ KIỆN", type: "Accessories", link: "LINK_SHOPEE" },
  //     ]
  //   }
  // },

];
