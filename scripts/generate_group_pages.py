# -*- coding: utf-8 -*-
"""
지시서#11 — 그룹별 정적 URL 생성 스크립트.

calculator.html이 쓰는 것과 동일한 공개 구글시트 CSV export URL을 읽어와,
docs/group-slug-map.md에서 수동으로 정한 슬러그에 해당하는 그룹만 골라
groups/<slug>.html 정적 페이지로 굽는다.

실행: python scripts/generate_group_pages.py
(로컬에서 실행 후 결과 HTML을 git에 커밋하는 방식 — 배포 시 별도 빌드 스텝 없음)
"""
import csv
import io
import json
import re
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GROUPS_DIR = REPO_ROOT / "groups"

KST = timezone(timedelta(hours=9))

# calculator.html의 SHEET_CONFIG와 동일한 공개 CSV export URL (카테고리별).
SHEET_CONFIG = {
    "plaster": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1430273857",
    "finishing": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1810019476",
    "mdf": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=0",
}

# 헤더 인덱싱 버그(2026-08) 재발 방지: 최소한 이 별칭 중 하나는 헤더 행에 반드시 있어야 한다.
# 하나라도 없으면 시트 쪽 헤더가 바뀐 것으로 보고 생성을 중단한다.
REQUIRED_HEADER_ALIASES = {
    "no": ["no", "번호", "순번"],
    "name": ["name", "품명", "품목명", "제품명"],
    "spec": ["spec", "규격", "사양"],
    "unit": ["unit", "단위"],
    "price": ["price", "단가", "가격"],
    "group": ["group", "그룹"],
}

# docs/group-slug-map.md와 반드시 동기화할 것. (category, 시트상 그룹명) -> 페이지 메타.
GROUP_PAGE_MAP = {
    ("plaster", "일반석고보드"): {
        "slug": "plaster-general",
        "category_label": "석고보드",
        "title": "일반석고보드 단가 및 규격 안내",
        "description": "벽체·천장 마감의 기본 자재로, 시공이 쉽고 비용 효율이 좋아 인테리어 현장에서 가장 널리 쓰이는 석고보드입니다. 도배·페인트 마감 전 바탕재로 주로 사용됩니다.",
    },
    ("plaster", "방수석고보드"): {
        "slug": "plaster-waterproof",
        "category_label": "석고보드",
        "title": "방수석고보드 단가 및 규격 안내",
        "description": "화장실·주방·발코니 등 습기가 많은 공간에 사용하는 석고보드로, 일반 석고보드 대비 흡습으로 인한 변형과 곰팡이 발생 위험이 낮습니다.",
    },
    ("plaster", "방화석고보드"): {
        "slug": "plaster-fireproof",
        "category_label": "석고보드",
        "title": "방화석고보드 단가 및 규격 안내",
        "description": "화재 확산 지연을 위해 내화 성능을 강화한 석고보드로, 공동주택 세대 간 경계벽이나 방화구획이 필요한 부위에 사용됩니다.",
    },
    ("plaster", "차음/방균보드"): {
        "slug": "plaster-moisture",
        "category_label": "석고보드",
        "title": "차음/방균 석고보드 단가 및 규격 안내",
        "description": "곰팡이 억제 기능이나 층간소음 차단 성능을 보강한 석고보드로, 습도가 높거나 소음에 민감한 공간에 적합합니다.",
    },
    ("finishing", "아쿠아보드"): {
        "slug": "finishing-aquaboard",
        "category_label": "마감자재",
        "title": "아쿠아보드 단가 및 규격 안내",
        "description": "자연석 질감을 표현한 마감용 보드로, 실제 석재보다 가벼워 시공이 간편하고 벽면 포인트 마감재로 많이 사용됩니다. 실내 인테리어의 스톤 무늬 연출에 적합합니다.",
    },
    ("finishing", "스톤플렉시블보드"): {
        "slug": "finishing-stone-flexible",
        "category_label": "마감자재",
        "title": "원스톤 플렉시블 보드 단가 및 규격 안내",
        "description": "얇고 유연한 인조석 마감재로, 곡면이나 좁은 공간에도 시공이 가능합니다. 트래버틴·슬레이트 등 다양한 석재 패턴과 사이즈(600×1200mm/1200×2400mm)로 제공됩니다.",
    },
    ("finishing", "영림 월판넬"): {
        "slug": "finishing-wallsystem",
        "category_label": "마감자재",
        "title": "영림 월판넬(인피니월·월시스템와이드) 안내",
        "description": "벽면 마감을 위한 모듈형 월판넬 시스템으로, 현장 조건에 따라 맞춤 시공이 가능합니다. 정확한 사양과 단가는 상담을 통해 안내해 드립니다.",
        "inquiry_only": True,
    },
    ("mdf", "MDF"): {
        "slug": "mdf-general",
        "category_label": "MDF",
        "title": "MDF(중밀도섬유판) 단가 및 규격 안내",
        "description": "나무 섬유를 압축 성형해 만든 목재 판재로, 표면이 균일하고 가공이 쉬워 가구·몰딩·인테리어 마감재의 기초 자재로 널리 사용됩니다. 두께별로 다양한 규격을 제공합니다.",
    },
}

PRICE_CHANGE_WARN_RATIO = 0.20  # ±20% 이상 튀면 경고


def fetch_csv_rows(url):
    with urllib.request.urlopen(url, timeout=20) as resp:
        raw = resp.read().decode("utf-8-sig")
    reader = csv.reader(io.StringIO(raw))
    rows = [row for row in reader if any(cell.strip() for cell in row)]
    return rows


def build_header_index(header_row):
    idx = {}
    for i, v in enumerate(header_row):
        key = str(v or "").strip().lower()
        if key not in idx:
            idx[key] = i
    return idx


def validate_header(header_index, category):
    missing = []
    for field, aliases in REQUIRED_HEADER_ALIASES.items():
        if not any(a in header_index for a in aliases):
            missing.append(field)
    if missing:
        raise RuntimeError(
            f"[헤더 검증 실패] 카테고리 '{category}' 시트 헤더에서 다음 필드를 찾을 수 없습니다: "
            f"{missing} — 시트 컬럼명이 바뀌었을 수 있습니다. 생성을 중단합니다."
        )


def get_value(row, header_index, aliases):
    for a in aliases:
        if a in header_index:
            i = header_index[a]
            if i < len(row):
                return row[i]
    return ""


def transform_row(row, category, header_index):
    no_raw = get_value(row, header_index, REQUIRED_HEADER_ALIASES["no"])
    name = get_value(row, header_index, REQUIRED_HEADER_ALIASES["name"]).strip()
    spec = get_value(row, header_index, REQUIRED_HEADER_ALIASES["spec"]).strip()
    unit = get_value(row, header_index, REQUIRED_HEADER_ALIASES["unit"]).strip()
    price_raw = get_value(row, header_index, REQUIRED_HEADER_ALIASES["price"])
    group = get_value(row, header_index, REQUIRED_HEADER_ALIASES["group"]).strip()
    code = get_value(row, header_index, ["code", "품목코드", "코드"]).strip()

    price_digits = re.sub(r"[^0-9]", "", str(price_raw))
    price = int(price_digits) if price_digits else 0

    slug_src = (code or no_raw or name or "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug_src) or "item"

    try:
        no = int(re.sub(r"[^0-9\-]", "", str(no_raw)))
    except ValueError:
        no = None

    return {
        "id": f"{category}_{slug}",
        "no": no,
        "name": name,
        "spec": spec,
        "unit": unit,
        "price": price,
        "group": group,
    }


def load_category(category):
    url = SHEET_CONFIG[category]
    rows = fetch_csv_rows(url)
    if not rows:
        raise RuntimeError(f"[생성 중단] 카테고리 '{category}' CSV가 비어 있습니다.")
    header_index = build_header_index(rows[0])
    validate_header(header_index, category)
    items = [transform_row(r, category, header_index) for r in rows[1:]]
    items = [it for it in items if it["name"]]
    items.sort(key=lambda it: (it["no"] is None, it["no"] if it["no"] is not None else 0))
    return items


def extract_previous_snapshot(html_path):
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"<!-- SNAPSHOT_JSON: (.*?) -->", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def check_price_outliers(slug, items, html_path):
    prev = extract_previous_snapshot(html_path)
    if not prev:
        return []
    prev_by_id = {it["id"]: it["price"] for it in prev.get("items", [])}
    warnings = []
    for it in items:
        old = prev_by_id.get(it["id"])
        if old is None or old == 0 or it["price"] == 0:
            continue
        diff_ratio = abs(it["price"] - old) / old
        if diff_ratio >= PRICE_CHANGE_WARN_RATIO:
            warnings.append(
                f"  - [{slug}] {it['name']}: {old:,}원 -> {it['price']:,}원 "
                f"({diff_ratio * 100:.0f}% 변동) — 오타/헤더 오정렬 가능성, 수동 확인 권장"
            )
    return warnings


def format_price(price):
    if price <= 0:
        return "견적문의"
    return f"{price:,}원"


HEAD_CSS = """
        :root {
            --color-bg-primary: #F5F6F8;
            --color-bg-secondary: #FFFFFF;
            --color-bg-tertiary: #EEF0F4;
            --color-accent-orange: #FF6B35;
            --color-accent-orange-hover: #E8551E;
            --color-accent-orange-light: rgba(255, 107, 53, 0.08);
            --color-text-white: #1A1F2B;
            --color-text-muted: #5F6875;
            --color-text-light: #333A47;
            --color-border: #DDE1E8;
            --font-family-base: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
            --font-family-alt: 'Montserrat', sans-serif;
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --shadow-premium: 0 10px 30px -10px rgba(31, 42, 68, 0.12);
            --shadow-glow: 0 4px 12px rgba(255, 107, 53, 0.25);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; scroll-behavior: smooth; }
        body { background-color: var(--color-bg-primary); color: var(--color-text-light); font-family: var(--font-family-base); line-height: 1.6; overflow-x: hidden; }
        a { color: inherit; text-decoration: none; }
        .font-num { font-family: var(--font-family-alt); font-variant-numeric: tabular-nums; }
        .container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        @media (min-width: 769px) {
            .container { max-width: 1400px; }
            .header-wrap { max-width: 1600px; }
        }

        header { position: sticky; top: 0; z-index: 100; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--color-border); padding: 15px 0; transition: var(--transition-smooth); }
        .header-wrap { display: flex; align-items: center; justify-content: space-between; }
        .logo-area { display: flex; align-items: center; gap: 8px; }
        .logo-area svg { width: 32px; height: 32px; }
        .logo-word-group { display: flex; align-items: center; gap: 12px; }
        .logo-wordmark { font-size: 20px; font-weight: 800; letter-spacing: 1.5px; color: var(--color-text-white); }
        .logo-endorsement { font-size: 12px; color: var(--color-text-muted); white-space: nowrap; }
        .header-right-group { display: flex; align-items: center; gap: 24px; }
        .header-phone { display: flex; align-items: center; gap: 8px; }
        .header-phone-icon { width: 30px; height: 30px; border-radius: 50%; background: var(--color-accent-orange); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .header-phone-icon svg { width: 16px; height: 16px; fill: #FFFFFF; }
        .header-phone-number { font-size: 15px; font-weight: 700; color: var(--color-text-white); white-space: nowrap; }
        .header-nav-group { display: flex; align-items: center; flex-wrap: wrap; justify-content: flex-end; gap: 4px; }
        .nav-tab-link { font-size: 13.5px; font-weight: 600; color: var(--color-text-muted); text-decoration: none; white-space: nowrap; padding: 8px 12px; border-radius: 8px; transition: var(--transition-smooth); }
        .nav-tab-link:hover { color: var(--color-text-light); background: var(--color-bg-tertiary); }
        .nav-tab-link.active { color: var(--color-accent-orange); background: var(--color-accent-orange-light); font-weight: 700; }
        @media (max-width: 1024px) {
            .nav-tab-link { padding: 6px 10px; font-size: 13px; }
        }
        @media (max-width: 1024px) {
            header { padding: 6px 0 !important; }
            .logo-word-group { gap: 10px; }
            .logo-wordmark { font-size: 17px; letter-spacing: 1px; }
            .header-phone { display: none; }
            header .nav-tab-link { display: none; }
        }

        .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 16px 28px; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; transition: var(--transition-smooth); border: none; word-break: keep-all; }
        .btn-primary { background: var(--color-accent-orange); color: var(--color-text-white); }
        .btn-primary:hover { background: var(--color-accent-orange-hover); transform: translateY(-3px); box-shadow: var(--shadow-glow); }
        .btn-full { width: 100%; padding: 14px; font-size: 15px; }

        .floating-buttons { position: fixed; bottom: 20px; right: 20px; display: flex; flex-direction: column; gap: 12px; z-index: 9999; }
        .floating-btn-circle { width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25); transition: transform 0.2s ease, box-shadow 0.2s ease; color: #fff; text-decoration: none; cursor: pointer; border: none; outline: none; }
        .floating-btn-circle:hover { transform: translateY(-4px); box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3); }
        .floating-btn-circle.phone { background-color: var(--color-accent-orange); }
        .floating-btn-circle.kakao { background-color: #FEE500; color: #191919; }

        footer { background-color: #050811; padding: 60px 0 100px; border-top: 1px solid var(--color-border); font-size: 14px; color: var(--color-text-muted); }
        .footer-wrap { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; margin-bottom: 40px; }
        .footer-info { display: flex; flex-direction: column; gap: 15px; }
        .footer-logo { font-size: 18px; font-weight: 800; letter-spacing: 1px; color: var(--color-text-white); }
        .footer-logo-endorsement { font-size: 12px; font-weight: 400; letter-spacing: normal; color: var(--color-text-muted); margin-left: 6px; }
        .footer-details { font-size: 14px; line-height: 1.8; }
        .footer-copyright { margin-top: 20px; font-size: 12px; }
        .footer-links { display: flex; flex-direction: column; gap: 20px; align-items: flex-end; }
        .footer-tel { font-size: 24px; font-weight: 800; color: var(--color-text-white); font-family: var(--font-family-alt); }
        .footer-tel span { color: var(--color-accent-orange); }
        .footer-bottom-nav { display: flex; gap: 20px; flex-wrap: wrap; }
        .footer-bottom-nav a:hover { color: var(--color-text-white); text-decoration: underline; }
        @media (max-width: 1024px) {
            .footer-wrap { grid-template-columns: 1fr; gap: 30px; }
            .footer-links { align-items: flex-start; }
        }

        /* GROUP PAGE CONTENT */
        .group-main { padding: 40px 0 80px; }
        .breadcrumb { font-size: 13px; color: var(--color-text-muted); margin-bottom: 20px; }
        .breadcrumb a { color: var(--color-text-muted); }
        .breadcrumb a:hover { color: var(--color-accent-orange); text-decoration: underline; }
        .breadcrumb .sep { margin: 0 6px; }
        .group-title { font-size: 30px; font-weight: 800; color: var(--color-text-white); margin-bottom: 6px; word-break: keep-all; }
        .group-category-tag { display: inline-block; font-size: 12.5px; font-weight: 700; color: var(--color-accent-orange); background: var(--color-accent-orange-light); border-radius: 50px; padding: 4px 12px; margin-bottom: 14px; }
        .group-desc { font-size: 15px; color: var(--color-text-light); line-height: 1.8; max-width: 720px; margin-bottom: 20px; word-break: keep-all; }
        .breadcrumb { word-break: keep-all; }
        .snapshot-note { font-size: 12.5px; color: var(--color-text-muted); background: var(--color-bg-tertiary); border-radius: 8px; padding: 10px 14px; margin-bottom: 28px; display: inline-block; word-break: keep-all; }
        .snapshot-note a { color: var(--color-accent-orange); font-weight: 700; text-decoration: underline; }
        .group-table-wrap { background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: 12px; overflow-x: auto; margin-bottom: 28px; box-shadow: var(--shadow-premium); }
        table.group-table { width: 100%; min-width: 520px; border-collapse: collapse; }
        table.group-table th { text-align: left; font-size: 12.5px; color: var(--color-text-muted); background: var(--color-bg-tertiary); padding: 12px 16px; font-weight: 700; white-space: nowrap; }
        table.group-table td { padding: 14px 16px; border-top: 1px solid var(--color-border); font-size: 14px; color: var(--color-text-light); white-space: nowrap; }
        table.group-table td.name-col { font-weight: 700; color: var(--color-text-white); }
        table.group-table td.price-col { text-align: right; font-weight: 700; color: var(--color-accent-orange); white-space: nowrap; }
        .group-cta-wrap { max-width: 360px; }
        .inquiry-banner { background: var(--color-accent-orange-light); border: 1px solid rgba(255, 107, 53, 0.3); border-radius: 12px; padding: 18px 20px; margin-bottom: 28px; word-break: keep-all; }
        .inquiry-banner strong { display: block; font-size: 15px; color: var(--color-text-white); margin-bottom: 6px; }
        .inquiry-banner p { font-size: 13.5px; color: var(--color-text-light); line-height: 1.7; margin-bottom: 14px; }
        .inquiry-cta-row { display: flex; gap: 10px; flex-wrap: wrap; }
        .inquiry-cta-row a { flex: 1; min-width: 140px; }
        .btn-kakao-inline { background: #FEE500; color: #191919; }
        .btn-kakao-inline:hover { background: #f5dc00; transform: translateY(-2px); }
        @media (max-width: 1024px) {
            .group-main { padding: 24px 0 100px; }
            .group-title { font-size: 24px; }
            .group-table-wrap { -webkit-overflow-scrolling: touch; }
        }
"""


def render_page(category, group_name, meta, items, generated_at, gid_no):
    slug = meta["slug"]
    canonical = f"https://infill-wood.kr/groups/{slug}.html"
    title_tag = f"{meta['title']} | INFILL"
    rep_id = items[0]["id"]
    calc_link = f"/calculator.html?cat={category}&id={rep_id}"
    gen_date_str = generated_at.strftime("%Y-%m-%d")

    rows_html = ""
    ld_offers = []
    for it in items:
        rows_html += f"""
                        <tr>
                            <td class="name-col">{it['name']}</td>
                            <td>{it['spec'] or '-'}</td>
                            <td>{it['unit'] or '-'}</td>
                            <td class="price-col font-num">{format_price(it['price'])}</td>
                        </tr>"""
        if it["price"] > 0:
            ld_offers.append({
                "@type": "Offer",
                "name": it["name"],
                "price": it["price"],
                "priceCurrency": "KRW",
                "availability": "https://schema.org/InStock",
                "url": canonical,
            })

    json_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": meta["title"],
        "itemListElement": [
            {"@type": "Product", "name": it["name"], "sku": it["id"]}
            for it in items
        ],
    }

    snapshot = {
        "generated_at": generated_at.isoformat(),
        "category": category,
        "group": group_name,
        "items": [{"id": it["id"], "name": it["name"], "price": it["price"]} for it in items],
    }

    inquiry_only = bool(meta.get("inquiry_only"))
    if inquiry_only:
        note_or_banner_html = f"""<div class="inquiry-banner">
                <strong>실시간 단가 준비 중인 품목입니다</strong>
                <p>정확한 사양과 단가는 카카오톡 또는 전화 상담으로 빠르게 안내해 드립니다.</p>
                <div class="inquiry-cta-row">
                    <a href="tel:02-1234-5678" class="btn btn-primary">전화 문의</a>
                    <a href="https://pf.kakao.com/_LixnwX/chat" target="_blank" class="btn btn-kakao-inline">카카오톡 문의</a>
                </div>
            </div>"""
        cta_html = f'<a href="{calc_link}" class="btn btn-primary btn-full">계산기에서 확인하기</a>'
    else:
        note_or_banner_html = f'<div class="snapshot-note">기준일 {gen_date_str} · 실시간 최신 단가는 <a href="{calc_link}">계산기에서 확인</a>하세요</div>'
        cta_html = f'<a href="{calc_link}" class="btn btn-primary btn-full">계산기에서 담기 · 견적 받기</a>'

    html = f"""<!DOCTYPE html>
<html lang="ko">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-B8ZLZEVV7E"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-B8ZLZEVV7E');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_tag}</title>
    <link rel="canonical" href="{canonical}">
    <meta name="description" content="{meta['description']}">
    <meta property="og:title" content="{title_tag}">
    <meta property="og:description" content="{meta['description']}">
    <meta property="og:type" content="product.group">
    <meta property="og:url" content="{canonical}">

    <link rel="icon" type="image/svg+xml" href="/assets/logo/app-icon.svg">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <link rel="stylesheet" as="style" crossorigin
        href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet">

    <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>

    <style>{HEAD_CSS}
    </style>
</head>

<body>

    <header id="header">
        <div class="container header-wrap">
            <a href="/index.html" class="logo-area">
                <svg viewBox="0 0 100 100" aria-hidden="true">
                    <polygon points="90,52 70,86.64 30,86.64 10,52 30,17.36 70,17.36" fill="none" stroke="#1A1F2B" stroke-width="7" />
                    <rect x="32" y="34" width="36" height="32" rx="3" fill="#FF6B35" />
                    <line x1="36" y1="46" x2="64" y2="46" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" />
                    <line x1="36" y1="56" x2="64" y2="56" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" />
                </svg>
                <div class="logo-word-group">
                    <span class="logo-wordmark">INFILL</span>
                    <span class="logo-endorsement">by 영림우드</span>
                </div>
            </a>
            <div class="header-right-group">
                <div class="header-nav-group">
                    <a href="/calculator.html" class="nav-tab-link">최신단가표</a>
                    <a href="/catalog.html" class="nav-tab-link">영림카탈로그</a>
                    <a href="/door_order.html" class="nav-tab-link">문짝·문틀 주문</a>
                    <a href="/molding_catalog.html" class="nav-tab-link">몰딩 주문</a>
                    <a href="/wallpanel.html" class="nav-tab-link">월판넬 주문</a>
                    <a href="/index.html#inquiry-form-sec" class="nav-tab-link">간편 유선 상담 신청</a>
                </div>
                <div class="header-phone">
                    <span class="header-phone-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 011 1V20a1 1 0 01-1 1C10.61 21 3 13.39 3 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.46.57 3.58a1 1 0 01-.25 1.01l-2.2 2.2z"/></svg>
                    </span>
                    <span class="header-phone-number">02-1234-5678</span>
                </div>
            </div>
        </div>
    </header>

    <main class="group-main">
        <div class="container">
            <div class="breadcrumb">
                <a href="/index.html">홈</a><span class="sep">›</span><a href="/calculator.html?cat={category}">최신단가표</a><span class="sep">›</span><a href="/calculator.html?cat={category}">{meta['category_label']}</a><span class="sep">›</span>{group_name}
            </div>
            <span class="group-category-tag">{meta['category_label']}</span>
            <h1 class="group-title">{meta['title']}</h1>
            <p class="group-desc">{meta['description']}</p>
            {note_or_banner_html}

            <div class="group-table-wrap">
                <table class="group-table">
                    <thead>
                        <tr>
                            <th>품명</th>
                            <th>규격</th>
                            <th>단위</th>
                            <th style="text-align:right;">단가</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}
                    </tbody>
                </table>
            </div>

            <div class="group-cta-wrap">
                {cta_html}
            </div>
        </div>
    </main>

    <div class="floating-buttons">
        <a href="tel:02-1234-5678" class="floating-btn-circle phone" title="전화 연결">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-2.824-1.502-5.114-3.792-6.616-6.616l1.293-.97c.362-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
            </svg>
        </a>
        <a href="https://pf.kakao.com/_LixnwX/chat" target="_blank" class="floating-btn-circle kakao" title="카카오톡 문의">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                <path
                    d="M12 3c-4.97 0-9 3.185-9 7.115 0 2.51 1.86 4.717 4.655 5.92-.187.697-.68 2.537-.777 2.923-.12.483.178.477.375.343.153-.103 2.454-1.68 3.447-2.355C11.14 17.065 11.57 17.1 12 17.1c4.97 0 9-3.185 9-7.115S16.97 3 12 3z" />
            </svg>
        </a>
    </div>

    <footer>
        <div class="container">
            <div class="footer-wrap">
                <div class="footer-info">
                    <div class="footer-logo">INFILL<span class="footer-logo-endorsement">by 영림우드</span></div>
                    <div class="footer-details">
                        (주)영림우드 | 대표이사: 허강원 | 사업자등록번호: 124-87-19164<br>
                        본사/물류창고: 경기도 수원시 권선구 서부로 1628<br>
                        이메일: ylwood0009@naver.com | 팩스: 031-291-4629
                    </div>
                    <div class="footer-copyright">
                        &copy; 2026 Younglim Wood Corporation. All Rights Reserved.
                    </div>
                </div>
                <div class="footer-links">
                    <div class="footer-tel">고객센터 <span>02-1234-5678</span></div>
                    <div class="footer-bottom-nav">
                        <a href="/calculator.html">최신단가표</a>
                        <a href="/door_order.html">문짝·문틀 주문</a>
                        <a href="/molding_catalog.html">몰딩 주문</a>
                        <a href="/wallpanel.html">월판넬 주문</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- generated: {generated_at.isoformat()}, source rows: {len(items)} -->
    <!-- SNAPSHOT_JSON: {json.dumps(snapshot, ensure_ascii=False)} -->

</body>

</html>
"""
    return html


def main():
    GROUPS_DIR.mkdir(exist_ok=True)
    generated_at = datetime.now(KST)
    all_warnings = []
    generated_files = []

    categories_needed = sorted({cat for (cat, _grp) in GROUP_PAGE_MAP})
    items_by_category = {}
    for cat in categories_needed:
        print(f"[fetch] {cat} CSV 가져오는 중...")
        items_by_category[cat] = load_category(cat)
        print(f"  -> {len(items_by_category[cat])}개 품목 로드")

    gid_counter = 0
    for (category, group_name), meta in GROUP_PAGE_MAP.items():
        items = [it for it in items_by_category[category] if it["group"] == group_name]
        if not items:
            raise RuntimeError(
                f"[생성 중단] 카테고리 '{category}' 그룹 '{group_name}'에 해당하는 품목을 시트에서 찾지 못했습니다. "
                f"docs/group-slug-map.md의 그룹명이 시트 실제값과 일치하는지 확인하세요."
            )
        gid_counter += 1
        out_path = GROUPS_DIR / f"{meta['slug']}.html"

        warnings = check_price_outliers(meta["slug"], items, out_path)
        all_warnings.extend(warnings)

        html = render_page(category, group_name, meta, items, generated_at, gid_counter)
        out_path.write_text(html, encoding="utf-8")
        generated_files.append(str(out_path.relative_to(REPO_ROOT)))
        print(f"[생성 완료] {out_path.relative_to(REPO_ROOT)} ({len(items)}개 품목)")

    print()
    print(f"총 {len(generated_files)}개 페이지 생성: {generated_files}")
    if all_warnings:
        print()
        print("!! 가격 이상치 경고 (직전 스냅샷 대비 ±20% 이상 변동) — 수동 확인 후 커밋 권장:")
        for w in all_warnings:
            print(w)
    else:
        print("가격 이상치 경고 없음.")


if __name__ == "__main__":
    main()
