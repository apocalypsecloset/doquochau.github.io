<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Apocalypse Closet</title>
</head>
<body>
    <!-- Nơi dữ liệu sẽ được in ra -->
    <div id="outfit-container"></div>

    <!-- 1. Bắt buộc chèn file data VÀO TRƯỚC -->
    <script src="outfits.js"></script>

    <!-- 2. Viết mã để in ra màn hình VÀO SAU -->
    <script>
        // Vì outfits.js đã tải xong, bạn có thể lấy biến "outfits" ra dùng luôn!
        const container = document.getElementById("outfit-container");

        // Lặp qua danh sách và tạo HTML
        outfits.forEach(outfit => {
            const itemHTML = `
                <div style="border: 1px solid #ccc; margin-bottom: 20px; padding: 10px;">
                    <h3>${outfit.title} (${outfit.category})</h3>
                    <img src="${outfit.img}" alt="${outfit.title}" style="width: 200px; height: auto;">
                    <p>${outfit.detail.desc}</p>
                </div>
            `;
            container.innerHTML += itemHTML;
        });
    </script>
</body>
</html>
