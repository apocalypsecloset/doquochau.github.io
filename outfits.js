// ═══════════════════════════════════════════════════════════════════
//  APOCALYPSE CLOSET — DATA FILE (SINGLE SOURCE OF TRUTH)
//
//  Chỉ cần sửa file này khi thêm/xoá/chỉnh sửa outfit.
//  Mọi trang (index, style, outfit-detail) đều đọc từ đây.
// ═══════════════════════════════════════════════════════════════════

const outfits = [
  {
    "id": "look-01",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-1-1.png",
    "tag": "LOOK #01",
    "title": "Look 01",
    "category": "E-Girl",
    "detail": {
      "title": "OUTFIT DETAILS #1",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-1-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-02",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-2-1.png",
    "tag": "LOOK #02",
    "title": "Look 02",
    "category": "Baddie Streetwear",
    "detail": {
      "title": "OUTFIT DETAILS #2",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-2-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "https://s.shopee.vn/70GyjqNLNt"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "https://s.shopee.vn/6pxYXXNyis"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "https://s.shopee.vn/7AaOw9Mi2u"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "https://s.shopee.vn/7Ktp8SM4hv"
        }
      ]
    }
  },
  {
    "id": "look-03",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-3-1.png",
    "tag": "LOOK #03",
    "title": "Look 03",
    "category": "Punk",
    "detail": {
      "title": "OUTFIT DETAILS #3",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-3-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-04",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-4-1.png",
    "tag": "LOOK #04",
    "title": "Look 04",
    "category": "Dark Feminine",
    "detail": {
      "title": "OUTFIT DETAILS #4",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-4-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-05",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-5-1.png",
    "tag": "LOOK #05",
    "title": "Look 05",
    "category": "E-Girl",
    "detail": {
      "title": "OUTFIT DETAILS #5",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-5-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-06",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-6-1.png",
    "tag": "LOOK #06",
    "title": "Look 06",
    "category": "Punk",
    "detail": {
      "title": "OUTFIT DETAILS #6",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-6-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-07",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-7-1.png",
    "tag": "LOOK #07",
    "title": "Look 07",
    "category": "Baddie Streetwear",
    "detail": {
      "title": "OUTFIT DETAILS #7",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-7-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-08",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-8-1.png",
    "tag": "LOOK #08",
    "title": "Look 08",
    "category": "E-Girl",
    "detail": {
      "title": "OUTFIT DETAILS #8",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-8-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-09",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-9-1.png",
    "tag": "LOOK #09",
    "title": "Look 09",
    "category": "Goth",
    "detail": {
      "title": "OUTFIT DETAILS #9",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-9-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-10",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-10-1.png",
    "tag": "LOOK #10",
    "title": "Look 10",
    "category": "Punk",
    "detail": {
      "title": "OUTFIT DETAILS #10",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-10-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-11",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-11-1.png",
    "tag": "LOOK #11",
    "title": "Look 11",
    "category": "E-Girl",
    "detail": {
      "title": "OUTFIT DETAILS #11",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-11-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-12",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-12-1.png",
    "tag": "LOOK #12",
    "title": "Look 12",
    "category": "Punk",
    "detail": {
      "title": "OUTFIT DETAILS #12",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-12-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-13",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-13-1.png",
    "tag": "LOOK #13",
    "title": "Look 13",
    "category": "E-Girl",
    "detail": {
      "title": "OUTFIT DETAILS #13",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-13-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-14",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-14-1.png",
    "tag": "LOOK #14",
    "title": "Look 14",
    "category": "Baddie Streetwear",
    "detail": {
      "title": "OUTFIT DETAILS #14",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-14-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-15",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-15-1.png",
    "tag": "LOOK #15",
    "title": "Look 15",
    "category": "Dark Feminine",
    "detail": {
      "title": "OUTFIT DETAILS #15",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-15-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-16",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-16-1.png",
    "tag": "LOOK #16",
    "title": "Look 16",
    "category": "Goth",
    "detail": {
      "title": "OUTFIT DETAILS #16",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-16-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-17",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-17.png",
    "tag": "LOOK #17",
    "title": "Look 17",
    "category": "Baddie Streetwear",
    "detail": {
      "title": "OUTFIT DETAILS #17",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-17.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-18",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-18-1.png",
    "tag": "LOOK #18",
    "title": "Look 18",
    "category": "Dark Feminine",
    "detail": {
      "title": "OUTFIT DETAILS #18",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-18-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-19",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-19-1.png",
    "tag": "LOOK #19",
    "title": "Look 19",
    "category": "Punk",
    "detail": {
      "title": "OUTFIT DETAILS #19",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-19-1.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  },
  {
    "id": "look-20",
    "img": "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-20-2.png",
    "tag": "LOOK #20",
    "title": "Look 20",
    "category": "Baddie Streetwear",
    "detail": {
      "title": "OUTFIT DETAILS #20",
      "desc": "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      "imgs": [
        "https://apocalypsecloset.wordpress.com/wp-content/uploads/2026/05/apocalypse-badgirl-20-2.png"
      ],
      "items": [
        {
          "name": "ÁO",
          "type": "Top Item",
          "link": "#"
        },
        {
          "name": "QUẦN",
          "type": "Bottom Item",
          "link": "#"
        },
        {
          "name": "GIÀY",
          "type": "Footwear",
          "link": "#"
        },
        {
          "name": "PHỤ KIỆN",
          "type": "Accessories",
          "link": "#"
        }
      ]
    }
  }
];
