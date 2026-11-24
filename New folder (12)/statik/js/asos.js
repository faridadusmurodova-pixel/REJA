// REJA - Frontend JavaScript mantiqi (asos.js)

document.addEventListener('DOMContentLoaded', function () {
    // 1. Bildirishnoma (alert) xabarlarini bir necha soniyadan keyin avtomatik yashirish
    const xabarlar = document.querySelectorAll('.xabar');
    if (xabarlar.length > 0) {
        setTimeout(() => {
            xabarlar.forEach(x => {
                x.style.transition = 'opacity 0.5s ease';
                x.style.opacity = '0';
                setTimeout(() => x.remove(), 500);
            });
        }, 4000);
    }

    // 2. Sahifada tezkor vazifa qidirish (Real-time filter)
    const qidiruvMaydoni = document.getElementById('jonli-qidiruv');
    if (qidiruvMaydoni) {
        qidiruvMaydoni.addEventListener('input', function (e) {
            const matn = e.target.value.toLowerCase().trim();
            const kartalar = document.querySelectorAll('.vazifa-karta');
            kartalar.forEach(karta => {
                const sarlavha = karta.querySelector('.vazifa-nom')?.textContent.toLowerCase() || '';
                const tavsif = karta.querySelector('.vazifa-tavsif')?.textContent.toLowerCase() || '';
                if (sarlavha.includes(matn) || tavsif.includes(matn)) {
                    karta.style.display = 'flex';
                } else {
                    karta.style.display = 'none';
                }
            });
        });
    }

    // 3. Sana maydoniga bugungi sanani avtomatik to'ldirish (agar bo'sh bo'lsa)
    const sanaKiritish = document.querySelector('input[type="date"]');
    if (sanaKiritish && !sanaKiritish.value) {
        const bugun = new Date().toISOString().split('T')[0];
        sanaKiritish.value = bugun;
    }
});
