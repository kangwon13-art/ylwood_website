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

// 지시서 #14: 문의 전환 계측(전화·카톡 클릭 → GA4 이벤트).
// 이벤트 이름·파라미터를 바꾸면 GA4 누적 데이터가 끊기므로 변경 시 docs/context.md 4번 섹션 표도 함께 갱신할 것.
function getPageType() {
    const path = location.pathname;
    if (path.indexOf("/groups/") !== -1) return "group";
    if (path.indexOf("calculator") !== -1) return "calculator";
    if (path.indexOf("molding") !== -1) return "molding";
    if (path.indexOf("catalog") !== -1) return "catalog";
    if (path.indexOf("door_order") !== -1) return "door_order";
    if (path.indexOf("wallpanel") !== -1) return "wallpanel";
    if (path === "/" || path.indexOf("index.html") !== -1) return "index";
    return "other";
}

function getCtaLocation(el) {
    if (el.dataset.ctaLocation) return el.dataset.ctaLocation;
    if (el.classList.contains("floating-btn-circle") || el.closest(".floating-buttons")) return "floating";
    if (el.classList.contains("btn-kakao-inline")) return "inline";
    if (el.hasAttribute("data-phone-cta") && el.closest(".inquiry-banner")) return "group_banner";
    if (el.classList.contains("btn-kakao") || el.closest(".sidebar-cta-secondary")) return "calculator_sidebar";
    if (el.closest("header")) return "header";
    if (el.closest("footer")) return "footer";
    return "other";
}

// 캡처 단계에서 1회만 처리 — 한 요소가 여러 셀렉터에 걸려도(예: .btn-kakao는 카톡 링크이기도 함)
// closest()로 가장 가까운 CTA 하나만 골라 이벤트 1건만 보낸다.
document.addEventListener("click", function (e) {
    if (typeof gtag !== "function") return;

    const phoneEl = e.target.closest("a.floating-btn-circle.phone, a[data-phone-cta]");
    if (phoneEl) {
        if (!SITE_CONFIG.phoneEnabled) return;
        gtag("event", "phone_click", {
            cta_location: getCtaLocation(phoneEl),
            page_type: getPageType(),
            transport_type: "beacon"
        });
        return;
    }

    const kakaoEl = e.target.closest('a[href*="pf.kakao.com"], .btn-kakao, .btn-kakao-inline');
    if (kakaoEl) {
        gtag("event", "kakao_click", {
            cta_location: getCtaLocation(kakaoEl),
            page_type: getPageType(),
            transport_type: "beacon"
        });
    }
}, true);
