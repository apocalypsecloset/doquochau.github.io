// ═══════════════════════════════════════════════════════════════════
//  APOCALYPSE CLOSET — DATA FILE (SINGLE SOURCE OF TRUTH)
//
//  Chỉ cần sửa file này khi thêm/xoá/chỉnh sửa outfit.
//  Mọi trang (index, style, outfit-detail) đều đọc từ đây.
//
//  CATEGORY hợp lệ:
//    "Dark Feminine" | "E-Girl" | "Goth" | "Baddie Streetwear" | "Punk"
// ═══════════════════════════════════════════════════════════════════

const D = id => `https://drive.google.com/uc?export=view&id=${id}`;

const outfits = [

  // ── E-GIRL ────────────────────────────────────────────────────
  {
    id: "look-01",
    img: D("1VXZnkNvF-KdVU2YKctOJjQZeQ3VIKP-A"),
    tag: "LOOK #01",
    title: "Look 01",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #1",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1VXZnkNvF-KdVU2YKctOJjQZeQ3VIKP-A"),
        D("1zfZUBGBxPvFq6HNAw-W2eGgtjGyVDOh7"),
        D("1Rv3Bk4zIPy6RBftYpEnhYZAwB3mURJGg"),
        D("1-7W-0nQ-vYIFmF8cUcefxEO2vVMTVwuX")
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
    img: D("1iVEb6hWXHFWs9WsJidwNBXxt4orojgHf"),
    tag: "LOOK #02",
    title: "Look 02",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #2",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1iVEb6hWXHFWs9WsJidwNBXxt4orojgHf"),
        D("13s84Sy1Ef9IAnUD9sflabYcYOw_nMeOV"),
        D("1Sh3RuTQ71gIoSi7--njBkPyDXqCxm8od"),
        D("1gUxUf_W2T7stRPJ3-IxRP2LvleW6eLEc")
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
    img: D("18tRZdre37xEmngFQZgjZy8fC0csEsx0t"),
    tag: "LOOK #03",
    title: "Look 03",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #3",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("18tRZdre37xEmngFQZgjZy8fC0csEsx0t"),
        D("1Te0nMItA5SYzbPv_lIgyF7_oJexBVF4a"),
        D("1U-kHYIjFoKt8YnZXZ2gcrM6UUTdK1Dt0"),
        D("1F98wClLv8KaBkAZebPlFrp-E3z6SkweC")
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
    img: D("1l1UCbDPOxVWZP3ydWuxVD_v_ylP2JbZ7"),
    tag: "LOOK #04",
    title: "Look 04",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #4",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1l1UCbDPOxVWZP3ydWuxVD_v_ylP2JbZ7"),
        D("102VP9aer6qL_E0SzQEvqHoBMIqo7jRI6"),
        D("1SQQoLFL0nsKMZ9RTPtmpbh20EIGLt4fR"),
        D("10QucbEcjYq98KDOYJITi-3WHk2w2y094")
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
    img: D("1h6I1TJeGjkvlp6mBlmvl3mANvq_lAoyJ"),
    tag: "LOOK #05",
    title: "Look 05",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #5",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1h6I1TJeGjkvlp6mBlmvl3mANvq_lAoyJ"),
        D("1GHwrmpd2kmYGTHD_33f_F1GUNViG7rnM"),
        D("12TOTlY1evbwJO-Ij6upX-Y7-TLFqDu-e"),
        D("12VvSDmEFBXHJWlFUQAWGQyVgBGVmpsu8")
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
    img: D("1oxhK1lwPgwZEiM8H1RUdWPbHGjFiOCy7"),
    tag: "LOOK #06",
    title: "Look 06",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #6",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1oxhK1lwPgwZEiM8H1RUdWPbHGjFiOCy7"),
        D("1XhjkH4WRkYtKJ6FezbVf2r129Hom6htC"),
        D("17jGmBvFRtNAgPcoOoFBSnX7PPka_NGij"),
        D("1-dtQtHDJyEQC8bhp5TI4fWUVq9lmivf8")
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
    img: D("1eAllGjhtT1oWjcMbCNRB7wzq4IYXPbsg"),
    tag: "LOOK #07",
    title: "Look 07",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #7",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1eAllGjhtT1oWjcMbCNRB7wzq4IYXPbsg"),
        D("1fRCSMCOH55AhVQRNkGpEN8KCb-KFuwLP"),
        D("1C71baizq_3LrQrBBuTlUvz5DUPY9omf4"),
        D("1oF3fjvXP5G2yrsm2nJrdxyOXRAE9YYRm")
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
    img: D("1OntvFsJaXfLQAViBzPNmn0pVHrAPEEUy"),
    tag: "LOOK #08",
    title: "Look 08",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #8",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1OntvFsJaXfLQAViBzPNmn0pVHrAPEEUy"),
        D("1gX9Jri4Q_KUkJNlvO8m6pK8OMgz1LuUn"),
        D("1_4v3xttmVbUimN2nX_dmU0w-HxRvx9o8"),
        D("1ZcH06A757H2mrUhw8tUYxAYraQcDbNmm")
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
    img: D("1Gok8shepkrD3-8EzsgtZN3YQqd8L2W1x"),
    tag: "LOOK #09",
    title: "Look 09",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #9",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1Gok8shepkrD3-8EzsgtZN3YQqd8L2W1x"),
        D("1eNkGZNvnB0mncHKl3mR8a11XlrngRrB-"),
        D("114VH3kmZgz_RNi9fmY2_ndW7byOTc0Y3"),
        D("1PcxAd-gUJDkhGKTjdJJMPBgwwsDzOZlr")
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
    img: D("19QZyj4KTU8dopI4e5o5PSSTX7eIs0Oc9"),
    tag: "LOOK #10",
    title: "Look 10",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #10",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("19QZyj4KTU8dopI4e5o5PSSTX7eIs0Oc9"),
        D("1CFYTOgSVBBawCsPFQebZ38nQXEUHeo9t"),
        D("1DmqwkQ-i5tuH4WEWDMa1ZU0EM9QW8ttC"),
        D("1NFVW4xd4hTmLolPTAhS3KZm5Xj9CCHSA")
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
    img: D("1hsk7NQ-WasvzIXEhQnu29n4erM-NFchA"),
    tag: "LOOK #11",
    title: "Look 11",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #11",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1hsk7NQ-WasvzIXEhQnu29n4erM-NFchA"),
        D("1OWJ0QdLUyrEb-ighut0yiJSRe2i_yRFV"),
        D("12xXKSyJRBeeCY9vsNy7LdNdw7E9pC0q9"),
        D("15nP2Ruh0GOeydiek8PIlR16_OMMdYc5R")
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
    img: D("1HlOXX_SBHLuB8oq4vGYHmSR_jIH4qGMC"),
    tag: "LOOK #12",
    title: "Look 12",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #12",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1HlOXX_SBHLuB8oq4vGYHmSR_jIH4qGMC"),
        D("1FlnrQDFg7umFBGGn-6nHrvDhHicqQaZW"),
        D("1pMLHzHmLlos6hKUDzhTHS3Hz5nbMgBLj"),
        D("1YuLRfCleRdi7xnedZU5vteR2nMBE3nFx")
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
    img: D("1IHiRBwNNkAzJmwEu4IKec6eiNG6WcPdE"),
    tag: "LOOK #13",
    title: "Look 13",
    category: "E-Girl",
    detail: {
      title: "OUTFIT DETAILS #13",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1IHiRBwNNkAzJmwEu4IKec6eiNG6WcPdE"),
        D("1FDHLgrG61D5MUgB10Q0H29LgGIW8rJ2n"),
        D("10U0NYErg6Pbjwero3VcgBwIUPbRUVD4I"),
        D("1Pohze_RqnPHKZ_tVmzCbE5zsU-GJKHXz")
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
    img: D("1b7HT8CDUTEVDclc_qP-uXR9TPRWF7dT4"),
    tag: "LOOK #14",
    title: "Look 14",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #14",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1b7HT8CDUTEVDclc_qP-uXR9TPRWF7dT4"),
        D("1lWdvK0r8YQBFdzFkJI9hGCqh_e66_pyr"),
        D("1lgdM8zF38YzVg7yqmbBIba_vHmbUP1O6"),
        D("1zQcHpD7tWacO_ASZZbcfL1HzDYWHH384")
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
    img: D("1Xkqu_9icd4OklZxoo2IlVqt75xSfduqx"),
    tag: "LOOK #15",
    title: "Look 15",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #15",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1Xkqu_9icd4OklZxoo2IlVqt75xSfduqx"),
        D("1-wwYBKrm1qYptQXK4IGklNQ6-CfAm2SF"),
        D("1CXTVOGCTOPc6xoEPc4kg2u-WG2um51R5"),
        D("1WJSgO7F3kSRzXnipVbNhOnzefxHIgCRX")
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
    img: D("17HTIykvB7PrDmrv6kvH3ym26RTpZAWdO"),
    tag: "LOOK #16",
    title: "Look 16",
    category: "Goth",
    detail: {
      title: "OUTFIT DETAILS #16",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("17HTIykvB7PrDmrv6kvH3ym26RTpZAWdO"),
        D("1KwcG-YWAceLN6xV1JhDciIGhDkLEyUya"),
        D("1pgMA9q3YhhIvUREDZGsCLqA8Ma_6O6c9"),
        D("1cXPPzbSQ0p2cChCh7u5pPYCTGNL-DwYJ")
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
    img: D("1gmAcIyTismktmzOX7C6VDu63m9eHTn3z"),
    tag: "LOOK #17",
    title: "Look 17",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #17",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1gmAcIyTismktmzOX7C6VDu63m9eHTn3z"),
        D("11Ht1gFTE3Bx5RSrk1UiHT5VLQPi2hWfU"),
        D("1uqbrGPFThnpTJiiUXqtMQBbvJDIOqooE"),
        D("152Uav02TavoRCHNLpsOBIYH1Yw0IYsoA")
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
    img: D("1xVWjPXJzEfhbPn0jJjepPpUnP8v4Iw3Z"),
    tag: "LOOK #18",
    title: "Look 18",
    category: "Dark Feminine",
    detail: {
      title: "OUTFIT DETAILS #18",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1xVWjPXJzEfhbPn0jJjepPpUnP8v4Iw3Z"),
        D("1HtP5rX_yxzuW3RR9Z5n7ilub6-hvnh_C"),
        D("1KgoXLZoOaLa2w9FEdq-3datLvBK3Vtkb"),
        D("1-BTRuOfzHDBiRl_eL2oMD8C18khJ6qev")
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
    img: D("1j45obshhk1CrjC7B7S2V3NCcWg5yRkfy"),
    tag: "LOOK #19",
    title: "Look 19",
    category: "Punk",
    detail: {
      title: "OUTFIT DETAILS #19",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1j45obshhk1CrjC7B7S2V3NCcWg5yRkfy"),
        D("1sZJR__nqhwhTbHntdycuLMBHlMd1tLxB"),
        D("1b1n3MYSMVcXn8I2ZOIS6WmwDJMCBFfpI"),
        D("1QmW-wYJYIAI4RThs957KUCrzqbWDPHx9")
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
    img: D("1PAeRcBHPstJiO0hk3X62Kb-vp7IO_UTx"),
    tag: "LOOK #20",
    title: "Look 20",
    category: "Baddie Streetwear",
    detail: {
      title: "OUTFIT DETAILS #20",
      desc: "Nhấn vào từng mục để xem chi tiết sản phẩm.",
      imgs: [
        D("1PAeRcBHPstJiO0hk3X62Kb-vp7IO_UTx"),
        D("1j_DGX1u9hf2FfRwG8OoiTcQSYf9U0Rdn"),
        D("14OKpkwMcwJttz7lTZD5HyvqO1uci-AVh"),
        D("1dZB3_jQ-Lw1DQ4pB_joFVJO4c_3cDiiZ")
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
  //   img: D("FILE_ID_CUA_ANH_1"),
  //   tag: "LOOK #21",
  //   title: "Look 21",
  //   category: "Dark Feminine",
  //   detail: {
  //     title: "OUTFIT DETAILS #21",
  //     desc: "Mô tả ngắn về look này.",
  //     imgs: [ D("ID_1"), D("ID_2"), D("ID_3"), D("ID_4") ],
  //     items: [
  //       { name: "ÁO",       type: "Top Item",    link: "LINK_SHOPEE" },
  //       { name: "QUẦN",     type: "Bottom Item", link: "LINK_SHOPEE" },
  //       { name: "GIÀY",     type: "Footwear",    link: "LINK_SHOPEE" },
  //       { name: "PHỤ KIỆN", type: "Accessories", link: "LINK_SHOPEE" },
  //     ]
  //   }
  // },

];
