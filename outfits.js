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

  {
    id: "look-01",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/ee1ee67b6b076a4b62ceca86663dbec1.jpg",
    tag: "LOOK #01",
    title: "Look 01",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #1",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/ee1ee67b6b076a4b62ceca86663dbec1.jpg",
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/ee1ee67b6b076a4b62ceca86663dbec1.jpg",
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/ee1ee67b6b076a4b62ceca86663dbec1.jpg",
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/eccacee3e4312af2ca62887a8953ffcb.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN 01", type: "Accessories", link: "#" },
        { name: "PHỤ KIỆN 02", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-02",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/eccacee3e4312af2ca62887a8953ffcb.jpg",
    tag: "LOOK #02",
    title: "Look 02",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #2",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/eccacee3e4312af2ca62887a8953ffcb.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-03",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/dc85743deb2e3b3f679adf3bc4f6b01a.jpg",
    tag: "LOOK #03",
    title: "Look 03",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #3",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/dc85743deb2e3b3f679adf3bc4f6b01a.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-04",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/daeb0c6ccef2d622c9c101b098161d73.jpg",
    tag: "LOOK #04",
    title: "Look 04",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #4",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/daeb0c6ccef2d622c9c101b098161d73.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-05",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/c34945641cab31289a679b2c6e464a9d.jpg",
    tag: "LOOK #05",
    title: "Look 05",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #5",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/c34945641cab31289a679b2c6e464a9d.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-06",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/553c2ed0cec607f7a0f9da74cadd99a6.jpg",
    tag: "LOOK #06",
    title: "Look 06",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #6",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/553c2ed0cec607f7a0f9da74cadd99a6.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-07",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/93c6f18c5d84d6b0c0e7339e0a255f60.jpg",
    tag: "LOOK #07",
    title: "Look 07",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #7",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/93c6f18c5d84d6b0c0e7339e0a255f60.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-08",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg",
    tag: "LOOK #08",
    title: "Look 08",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #8",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-09",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/eccacee3e4312af2ca62887a8953ffcb.jpg",
    tag: "LOOK #09",
    title: "Look 09",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #9",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/eccacee3e4312af2ca62887a8953ffcb.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-10",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/dc85743deb2e3b3f679adf3bc4f6b01a.jpg",
    tag: "LOOK #10",
    title: "Look 10",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #10",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/dc85743deb2e3b3f679adf3bc4f6b01a.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-11",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/daeb0c6ccef2d622c9c101b098161d73.jpg",
    tag: "LOOK #11",
    title: "Look 11",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #11",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/daeb0c6ccef2d622c9c101b098161d73.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-12",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/c34945641cab31289a679b2c6e464a9d.jpg",
    tag: "LOOK #12",
    title: "Look 12",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #12",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/c34945641cab31289a679b2c6e464a9d.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-13",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/553c2ed0cec607f7a0f9da74cadd99a6.jpg",
    tag: "LOOK #13",
    title: "Look 13",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #13",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/553c2ed0cec607f7a0f9da74cadd99a6.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-14",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/93c6f18c5d84d6b0c0e7339e0a255f60.jpg",
    tag: "LOOK #14",
    title: "Look 14",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #14",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/93c6f18c5d84d6b0c0e7339e0a255f60.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-15",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg",
    tag: "LOOK #15",
    title: "Look 15",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #15",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  {
    id: "look-16",
    img: "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg",
    tag: "LOOK #16",
    title: "Look 16",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #16",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/8e06a9da32cba298045bf6355b390710.jpg"
      ],
      items: [
        { name: "ÁO", type: "Top Item", link: "#" },
        { name: "QUẦN", type: "Bottom Item", link: "#" },
        { name: "GIÀY", type: "Footwear", link: "#" },
        { name: "PHỤ KIỆN", type: "Accessories", link: "#" }
      ]
    }
  },

  // ════════════════════════════════════════════════════════════════
  //  ↓ THÊM OUTFIT MỚI Ở ĐÂY — copy block này, xoá dấu // rồi điền
  // ════════════════════════════════════════════════════════════════
  //
  // {
  //   id: "look-17",
  //   img: "URL_ẢNH_THUMBNAIL",
  //   tag: "LOOK #17",
  //   title: "Look 17",
  //   category: "Dark Feminine",
  //   detail: {
  //     title: "OUTFIT DETAILS #17",
  //     desc: "Mô tả ngắn về look này.",
  //     imgs: [
  //       "URL_ẢNH_1",
  //       "URL_ẢNH_2",
  //     ],
  //     items: [
  //       { name: "ÁO",       type: "Top Item",    link: "LINK_SHOPEE" },
  //       { name: "QUẦN",     type: "Bottom Item", link: "LINK_SHOPEE" },
  //       { name: "GIÀY",     type: "Footwear",    link: "LINK_SHOPEE" },
  //       { name: "PHỤ KIỆN", type: "Accessories", link: "LINK_SHOPEE" },
  //     ]
  //   }
  // },

];
