// 사이트 공통 설정 — 대표전화 등 여러 페이지에서 재사용하는 값.
// 실제 대표번호가 개통되면 phone/phoneTel을 채우고 phoneEnabled를 true로 바꾸는 것만으로
// 헤더·푸터·플로팅 버튼·견적서 출력 등 사이트 전체에 반영된다(지시서 SEO-01 F).
//
// 지시서 SEO-02 A: 번호 텍스트/tel: 링크는 HTML 원문에 두지 않는다(빈 자리표시 요소만 존재).
// phoneEnabled가 false면 JS도 아무 값을 채우지 않는다 — 검색엔진이 원문을 읽어도
// 번호가 전혀 존재하지 않는 상태를 유지하기 위함. true일 때만 채워 넣는다.
const SITE_CONFIG = {
    phone: "010-5250-0019",
    phoneTel: "tel:010-5250-0019",
    phoneEnabled: true,
    email: "ylwood0009@naver.com"
};

function applySiteConfigContact() {
    if (SITE_CONFIG.phoneEnabled) {
        document.querySelectorAll(".header-phone-number, .footer-tel span").forEach(el => {
            el.textContent = SITE_CONFIG.phone;
        });
        document.querySelectorAll("a.floating-btn-circle.phone, a[data-phone-cta]").forEach(el => {
            el.setAttribute("href", SITE_CONFIG.phoneTel);
        });
    } else {
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
