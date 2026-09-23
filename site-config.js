// 사이트 공통 설정 — 대표전화 등 여러 페이지에서 재사용하는 값.
// 실제 대표번호가 개통되면 phone/phoneTel을 채우고 phoneEnabled를 true로 바꾸는 것만으로
// 헤더·푸터·플로팅 버튼·견적서 출력 등 사이트 전체에 반영된다(지시서 SEO-01 F).
const SITE_CONFIG = {
    phone: "02-1234-5678",
    phoneTel: "tel:02-1234-5678",
    phoneEnabled: false,
    email: "ylwood0009@naver.com"
};

function applySiteConfigContact() {
    document.querySelectorAll(".header-phone-number, .footer-tel span").forEach(el => {
        el.textContent = SITE_CONFIG.phone;
    });
    document.querySelectorAll("a.floating-btn-circle.phone, a[data-phone-cta]").forEach(el => {
        el.setAttribute("href", SITE_CONFIG.phoneTel);
    });

    if (!SITE_CONFIG.phoneEnabled) {
        document.querySelectorAll(".header-phone, .footer-tel, a.floating-btn-circle.phone, a[data-phone-cta]").forEach(el => {
            el.style.display = "none";
        });
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applySiteConfigContact);
} else {
    applySiteConfigContact();
}
