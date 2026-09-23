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
    "plywood": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=2105087312",
    "interior_plywood": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1502465421",
    "timber": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1035321209",
    "insulation": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1422880070",
    "deck_timber": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1255269005",
    "louver_wood": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1375140463",
    "hardware": "https://docs.google.com/spreadsheets/d/1ZdtOewDMmYCZ4leyrbBHDRLfMh-NgvO6iPNI24YQ7Lk/export?format=csv&gid=1436943636",
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
    ("plywood", "합판 910x1820"): {
        "slug": "plywood-3x6",
        "category_label": "합판",
        "title": "합판 910x1820(3x6) 단가 및 규격 안내",
        "description": "2.7mm~11.5mm 다양한 두께로 구성된 소형 규격(910×1820mm) 합판입니다. 가구 제작이나 부분 보수 등 소량 시공에 적합합니다.",
    },
    ("plywood", "태고합판 910x1820"): {
        "slug": "plywood-taego-3x6",
        "category_label": "합판",
        "title": "태고합판 910x1820(3x6) 단가 및 규격 안내",
        "description": "표면에 코팅 처리를 더한 태고합판으로, 별도 마감 없이도 깔끔한 표면을 얻을 수 있어 소형 규격 시공에 사용됩니다.",
    },
    ("plywood", "일반합판 1220x2440"): {
        "slug": "plywood-4x8-general",
        "category_label": "합판",
        "title": "일반합판 1220x2440(4x8) 단가 및 규격 안내",
        "description": "2.7mm~17.5mm까지 다양한 두께와 등급(BB·CC 등)을 갖춘 표준 규격(1220×2440mm) 합판으로, 건축·인테리어 현장에서 가장 널리 쓰이는 기본 자재입니다.",
    },
    ("plywood", "코아합판 1220x2440"): {
        "slug": "plywood-4x8-core",
        "category_label": "합판",
        "title": "코아합판 1220x2440(4x8) 단가 및 규격 안내",
        "description": "알비자·라왕 등의 코아를 사용한 합판으로, 일반 합판보다 강도와 내구성이 우수해 구조용 마감재로 사용됩니다.",
    },
    ("plywood", "OSB 1220x2440"): {
        "slug": "plywood-osb",
        "category_label": "합판",
        "title": "OSB 1220x2440(4x8) 단가 및 규격 안내",
        "description": "작은 목재 조각을 압축 성형한 구조용 판재로, 바닥재나 벽체 하지재로 주로 사용됩니다.",
    },
    ("plywood", "CRC 보드"): {
        "slug": "plywood-crc",
        "category_label": "합판",
        "title": "CRC 보드(콘보드) 단가 및 규격 안내",
        "description": "시멘트와 섬유를 혼합해 만든 불연성 보드로, 내화·방수 성능이 필요한 부위의 마감재로 사용됩니다.",
    },
    ("plywood", "백색 코팅합판"): {
        "slug": "plywood-white-coated",
        "category_label": "합판",
        "title": "백색 코팅합판(포리톤) 단가 및 규격 안내",
        "description": "표면에 백색 코팅을 입힌 합판으로, 별도 도장 없이 깔끔한 화이트 마감을 낼 수 있습니다.",
    },
    ("plywood", "미장(라미날 합판)"): {
        "slug": "plywood-laminate",
        "category_label": "합판",
        "title": "미장(라미날 합판) 단가 및 규격 안내",
        "description": "무늬목 라미네이트를 표면에 적용한 합판으로, 자연스러운 나무 질감의 마감이 필요한 곳에 사용됩니다.",
    },
    ("plywood", "스페이스월"): {
        "slug": "plywood-spacewall",
        "category_label": "합판",
        "title": "스페이스월 단가 및 규격 안내",
        "description": "벽면 마감용 자재로, 백색 쫄대가 포함되어 시공 마무리까지 한 번에 처리할 수 있습니다.",
    },
    ("interior_plywood", "미송합판 유절"): {
        "slug": "interior-plywood-misong-knotted",
        "category_label": "인테리어합판",
        "title": "미송합판 유절 단가 및 규격 안내",
        "description": "나무 옹이(유절) 무늬가 자연스럽게 드러나는 미송 합판으로, 목재 본연의 질감을 살린 마감이 필요한 곳에 사용됩니다. 다양한 두께(4.6mm~18mm)로 제공됩니다.",
    },
    ("interior_plywood", "미송합판 무절"): {
        "slug": "interior-plywood-misong-clear",
        "category_label": "인테리어합판",
        "title": "미송합판 무절 단가 및 규격 안내",
        "description": "옹이가 없는 매끈한 표면의 미송 합판으로, 깔끔한 마감이 필요한 가구·인테리어 제작에 적합합니다.",
    },
    ("interior_plywood", "낙엽송합판(라찌합판)"): {
        "slug": "interior-plywood-larch",
        "category_label": "인테리어합판",
        "title": "낙엽송합판(라찌합판) 단가 및 규격 안내",
        "description": "낙엽송을 사용한 합판으로, 일반 합판보다 강도가 높고 내구성이 우수해 구조재나 바닥 하지재로 많이 사용됩니다.",
    },
    ("interior_plywood", "오쿠메합판"): {
        "slug": "interior-plywood-okoume",
        "category_label": "인테리어합판",
        "title": "오쿠메합판 단가 및 규격 안내",
        "description": "가볍고 가공이 쉬운 오쿠메 원목을 사용한 합판으로, 곡면 가공이나 선박·차량 내장재 등 특수 용도에도 사용됩니다.",
    },
    ("interior_plywood", "레드오크합판"): {
        "slug": "interior-plywood-red-oak",
        "category_label": "인테리어합판",
        "title": "레드오크합판 단가 및 규격 안내",
        "description": "붉은빛이 도는 오크 무늬목을 표면에 적용한 합판으로, 고급스러운 원목 질감의 마감이 필요한 가구·인테리어에 사용됩니다.",
    },
    ("interior_plywood", "자작합판"): {
        "slug": "interior-plywood-birch",
        "category_label": "인테리어합판",
        "title": "자작합판 단가 및 규격 안내",
        "description": "층이 촘촘하고 단면이 아름다운 자작나무 합판으로, 절단면을 그대로 노출하는 디자인 가구나 마감재로 인기가 높습니다. 두께별로 폭넓게 제공됩니다.",
    },
    ("interior_plywood", "타공판"): {
        "slug": "interior-plywood-perforated",
        "category_label": "인테리어합판",
        "title": "타공판 단가 및 규격 안내",
        "description": "일정한 간격으로 구멍(홀) 또는 선(라인) 형태의 타공 가공을 더한 판재로, 수납 공구 벽이나 환기가 필요한 마감재로 사용됩니다.",
    },
    ("timber", "소송 각재"): {
        "slug": "timber-sosong",
        "category_label": "목재/구조재",
        "title": "소송 각재 단가 및 규격 안내",
        "description": "각재 형태로 가공된 소나무 목재로, 한치각·투바이 등 다양한 규격을 갖춰 인테리어 및 소규모 목공 작업의 기본 자재로 사용됩니다.",
    },
    ("timber", "뉴송 각재"): {
        "slug": "timber-newsong",
        "category_label": "목재/구조재",
        "title": "뉴송 각재 단가 및 규격 안내",
        "description": "폼다루끼·투바이·오비끼 등 용도별로 세분화된 뉴송 각재로, 거푸집 공사나 구조 보강 작업에 주로 사용됩니다.",
    },
    ("timber", "마감용 구조재"): {
        "slug": "timber-structural",
        "category_label": "목재/구조재",
        "title": "마감용 구조재 단가 및 규격 안내",
        "description": "폭별로 다양한 규격을 갖춘 구조용 목재로, 벽체·천장 프레임 시공 등 건축 구조를 잡는 기초 작업에 사용됩니다.",
    },
    ("timber", "라왕 각재"): {
        "slug": "timber-lawan",
        "category_label": "목재/구조재",
        "title": "라왕 각재 단가 및 규격 안내",
        "description": "라왕 원목으로 가공한 각재로, 일반 소나무 각재보다 강도가 높아 하중이 걸리는 부위나 고급 마감이 필요한 곳에 사용됩니다.",
    },
    ("insulation", "아이소핑크/토이락"): {
        "slug": "insulation-isopink-toirock",
        "category_label": "단열재",
        "title": "아이소핑크/토이락 단가 및 규격 안내",
        "description": "압출법 단열재의 대표 제품군으로, 두께별(10T~100T)로 다양하게 구성되어 있어 벽체·바닥 등 용도에 맞는 단열 시공에 사용됩니다.",
    },
    ("insulation", "단열재 이보드"): {
        "slug": "insulation-eboard",
        "category_label": "단열재",
        "title": "단열재 이보드 단가 및 규격 안내",
        "description": "두께와 표면 마감(도배용/페인트용)에 따라 세분화된 이보드로, 마감 방식에 맞춰 선택해 시공할 수 있습니다.",
    },
    ("insulation", "열반사 단열재"): {
        "slug": "insulation-reflective",
        "category_label": "단열재",
        "title": "열반사 단열재 단가 및 규격 안내",
        "description": "은박 양면 접착 처리된 단열재로, 좁은 공간에서도 효과적인 열 반사 성능을 발휘해 얇은 두께로 단열이 필요한 곳에 사용됩니다.",
    },
    ("insulation", "스티로폼"): {
        "slug": "insulation-styrofoam",
        "category_label": "단열재",
        "title": "스티로폼 단가 및 규격 안내",
        "description": "가볍고 경제적인 단열재로, 벽체나 바닥 하지 단열 등 일반적인 단열 시공에 널리 사용됩니다.",
    },
    ("insulation", "글라스울"): {
        "slug": "insulation-glasswool",
        "category_label": "단열재",
        "title": "글라스울 단가 및 규격 안내",
        "description": "유리섬유를 압축해 만든 단열재로, 단열과 함께 흡음 성능도 갖춰 소음 차단이 필요한 벽체·천장에 사용됩니다.",
    },
    ("insulation", "차음 충진재"): {
        "slug": "insulation-filler",
        "category_label": "단열재",
        "title": "차음 충진재 단가 및 규격 안내",
        "description": "벽체나 바닥 사이 빈 공간을 채워 소음을 차단하는 충진용 자재로, 층간소음 저감 시공에 사용됩니다.",
    },
    ("deck_timber", "방부목 데크재/각재"): {
        "slug": "deck-timber-treated",
        "category_label": "방부목/특수목/합성목",
        "title": "방부목 데크재/각재 단가 및 규격 안내",
        "description": "야외 환경에 강한 방부 처리 목재로, 데크 시공용 판재부터 구조용 각재까지 다양한 규격을 갖춰 테라스·야외 데크 시공 전반에 사용됩니다.",
    },
    ("deck_timber", "방킬라이"): {
        "slug": "deck-timber-bankirai",
        "category_label": "방부목/특수목/합성목",
        "title": "방킬라이 단가 및 규격 안내",
        "description": "내구성이 뛰어난 하드우드 계열 목재로, 습기와 마모에 강해 야외 데크나 계단 등 하중이 걸리는 부위에 사용됩니다.",
    },
    ("deck_timber", "합성데크"): {
        "slug": "deck-timber-composite",
        "category_label": "방부목/특수목/합성목",
        "title": "합성데크 단가 및 규격 안내",
        "description": "목분과 플라스틱을 합성해 만든 데크재로, 방부목 대비 변색·부식에 강하고 유지관리가 쉬워 장기간 사용하는 야외 시공에 적합합니다.",
    },
    ("deck_timber", "무방부 데크재"): {
        "slug": "deck-timber-untreated",
        "category_label": "방부목/특수목/합성목",
        "title": "무방부 데크재 단가 및 규격 안내",
        "description": "방부 처리 없이 가공한 데크재로, 실내나 방부 처리가 필요 없는 환경의 데크 시공에 사용됩니다.",
    },
    ("deck_timber", "라틱스 방부/PVC"): {
        "slug": "deck-timber-lattice",
        "category_label": "방부목/특수목/합성목",
        "title": "라틱스 방부/PVC 단가 및 규격 안내",
        "description": "울타리나 파고라 등에 사용하는 라틱스(격자) 자재로, 방부목과 PVC 소재 중 선택할 수 있습니다.",
    },
    ("deck_timber", "사이딩"): {
        "slug": "deck-timber-siding",
        "category_label": "방부목/특수목/합성목",
        "title": "사이딩 단가 및 규격 안내",
        "description": "건물 외벽 마감용 판재로, 방부 처리 또는 삼목 소재로 제공되어 외부 마감재로 사용됩니다.",
    },
    ("louver_wood", "원목루바"): {
        "slug": "louver-wood-solid",
        "category_label": "루바/집성판",
        "title": "원목루바 단가 및 규격 안내",
        "description": "미송·삼목·히노끼 등 원목 소재로 만든 루바로, 벽면이나 천장에 세로 라인 무늬를 연출하는 인테리어 마감재로 사용됩니다.",
    },
    ("louver_wood", "히노끼 판재"): {
        "slug": "louver-wood-hinoki-plank",
        "category_label": "루바/집성판",
        "title": "히노끼 판재 단가 및 규격 안내",
        "description": "편백나무(히노끼) 원목 판재로, 은은한 향과 항균 효과가 있어 사우나·욕실 등 습한 공간의 마감재로 많이 사용됩니다.",
    },
    ("louver_wood", "라디에타파인 집성판"): {
        "slug": "louver-wood-radiata-pine",
        "category_label": "루바/집성판",
        "title": "라디에타파인 집성판 단가 및 규격 안내",
        "description": "여러 조각의 목재를 접합해 만든 라디에타파인 집성판으로, 두께별로 폭넓게 구성되어 있어 가구·선반 제작에 널리 사용됩니다.",
    },
    ("louver_wood", "레드파인 집성판"): {
        "slug": "louver-wood-red-pine",
        "category_label": "루바/집성판",
        "title": "레드파인 집성판 단가 및 규격 안내",
        "description": "붉은빛이 도는 소나무 계열 집성판으로, 자연스러운 우드 톤의 가구나 인테리어 마감재로 사용됩니다.",
    },
    ("louver_wood", "삼목 집성판"): {
        "slug": "louver-wood-cedar",
        "category_label": "루바/집성판",
        "title": "삼목 집성판 단가 및 규격 안내",
        "description": "삼나무를 접합해 만든 집성판으로, 가볍고 향이 좋아 수납장이나 선반 등 다양한 목공 작업에 사용됩니다.",
    },
    ("louver_wood", "히노끼 집성판"): {
        "slug": "louver-wood-hinoki-glulam",
        "category_label": "루바/집성판",
        "title": "히노끼 집성판 단가 및 규격 안내",
        "description": "편백나무 집성판으로, 무절·유절 등급에 따라 표면 무늬가 달라 용도에 맞게 선택할 수 있습니다.",
    },
    ("louver_wood", "고무나무 집성판"): {
        "slug": "louver-wood-rubberwood",
        "category_label": "루바/집성판",
        "title": "고무나무 집성판 단가 및 규격 안내",
        "description": "단단하고 무늬가 균일한 고무나무 집성판으로, 식탁 상판이나 가구 제작에 많이 사용됩니다.",
    },
    ("louver_wood", "라왕 집성판"): {
        "slug": "louver-wood-lawan",
        "category_label": "루바/집성판",
        "title": "라왕 집성판 단가 및 규격 안내",
        "description": "강도가 높은 라왕 원목 집성판으로, 규격이 다양해 구조용 가구부터 마감재까지 폭넓게 사용됩니다.",
    },
    ("louver_wood", "멀바우 집성판"): {
        "slug": "louver-wood-merbau",
        "category_label": "루바/집성판",
        "title": "멀바우 집성판 단가 및 규격 안내",
        "description": "짙은 색상과 뛰어난 내구성을 가진 멀바우 집성판으로, 계단재·손스침 등 고급 마감이 필요한 부위에 사용됩니다.",
    },
    ("louver_wood", "오크 집성판"): {
        "slug": "louver-wood-oak",
        "category_label": "루바/집성판",
        "title": "오크 집성판 단가 및 규격 안내",
        "description": "오크 원목을 접합한 집성판으로, 고급스러운 무늬와 내구성을 갖춰 가구 상판이나 계단판으로 사용됩니다.",
    },
    ("louver_wood", "애쉬 집성판"): {
        "slug": "louver-wood-ash",
        "category_label": "루바/집성판",
        "title": "애쉬 집성판 단가 및 규격 안내",
        "description": "애쉬(물푸레나무) 집성판으로, 일반 애쉬와 탄화 처리된 애쉬가 있어 원하는 색감에 맞게 선택할 수 있습니다.",
    },
    ("louver_wood", "아카시아 집성판"): {
        "slug": "louver-wood-acacia",
        "category_label": "루바/집성판",
        "title": "아카시아 집성판 단가 및 규격 안내",
        "description": "단단하고 무늬가 독특한 아카시아 집성판으로, 식탁이나 도마 등 실용적인 가구 제작에 사용됩니다.",
    },
    ("hardware", "접착재/본드"): {
        "slug": "hardware-adhesive-bond",
        "category_label": "철물/부자재",
        "title": "접착재/본드 단가 및 규격 안내",
        "description": "목공·건축 현장에서 쓰이는 범용 본드류로, 합판·MDF·석고보드 등 다양한 자재의 접착에 사용됩니다.",
    },
    ("hardware", "폼 / 부자재"): {
        "slug": "hardware-foam-supplies",
        "category_label": "철물/부자재",
        "title": "폼 / 부자재 단가 및 규격 안내",
        "description": "문틀·창호 시공 시 틈새를 채우는 발포 폴리우레탄 폼과 전용 건(gun)으로, 단열과 고정을 동시에 처리할 때 사용됩니다.",
    },
    ("hardware", "무초산 실리콘"): {
        "slug": "hardware-silicone-neutral",
        "category_label": "철물/부자재",
        "title": "무초산 실리콘 단가 및 규격 안내",
        "description": "금속·유리 등 다양한 소재에 부식 없이 사용 가능한 중성 실리콘으로, 다양한 색상으로 마감 부위별 코킹 작업에 사용됩니다.",
    },
    ("hardware", "바이오 실리콘"): {
        "slug": "hardware-silicone-bio",
        "category_label": "철물/부자재",
        "title": "바이오 실리콘 단가 및 규격 안내",
        "description": "곰팡이 억제 성분이 포함된 실리콘으로, 습기가 많은 욕실·주방 등의 코킹 작업에 사용됩니다.",
    },
    ("hardware", "수성 실리콘"): {
        "slug": "hardware-silicone-water",
        "category_label": "철물/부자재",
        "title": "수성 실리콘 단가 및 규격 안내",
        "description": "물로 희석·정리가 가능한 수성 타입 실리콘으로, 도장 마감이 필요한 부위의 코킹에 사용됩니다.",
    },
    ("hardware", "외부용 실리콘"): {
        "slug": "hardware-silicone-exterior",
        "category_label": "철물/부자재",
        "title": "외부용 실리콘 단가 및 규격 안내",
        "description": "자외선과 온도 변화에 강한 실외 전용 실리콘으로, 외벽·창호 등 외부 마감 코킹에 사용됩니다.",
    },
    ("hardware", "아연피스 목재용 외날"): {
        "slug": "hardware-screw-zinc-wood",
        "category_label": "철물/부자재",
        "title": "아연피스 목재용 외날 단가 및 규격 안내",
        "description": "아연 도금 처리된 목재용 나사로, 부식에 강해 목재 구조물 및 가구 조립에 사용됩니다.",
    },
    ("hardware", "윙스크류 양날"): {
        "slug": "hardware-screw-wing",
        "category_label": "철물/부자재",
        "title": "윙스크류 양날 단가 및 규격 안내",
        "description": "양쪽에 날이 있어 목재에 쉽게 파고드는 윙스크류로, 두꺼운 목재 자재의 고정에 사용됩니다.",
    },
    ("hardware", "석고피스 양날"): {
        "slug": "hardware-screw-drywall",
        "category_label": "철물/부자재",
        "title": "석고피스 양날 단가 및 규격 안내",
        "description": "석고보드 시공 전용 나사로, 경량철골이나 목재 틀에 석고보드를 고정할 때 사용됩니다.",
    },
    ("hardware", "스텐피스 양날"): {
        "slug": "hardware-screw-stainless",
        "category_label": "철물/부자재",
        "title": "스텐피스 양날 단가 및 규격 안내",
        "description": "녹슬지 않는 스테인리스 재질의 나사로, 습기에 노출되는 부위나 외부 목공 작업의 고정에 사용됩니다.",
    },
    ("hardware", "타카핀 U자"): {
        "slug": "hardware-staple-u",
        "category_label": "철물/부자재",
        "title": "타카핀 U자 단가 및 규격 안내",
        "description": "U자형 타카핀으로, 얇은 판재나 몰딩 마감 시 압정형 고정에 사용됩니다.",
    },
    ("hardware", "타카핀 DT/T"): {
        "slug": "hardware-staple-dt-t",
        "category_label": "철물/부자재",
        "title": "타카핀 DT/T 단가 및 규격 안내",
        "description": "DT/T 규격 타카핀으로, 가구 및 목공 조립 시 프레임 고정에 사용됩니다.",
    },
    ("hardware", "타카핀 실타카"): {
        "slug": "hardware-staple-fine",
        "category_label": "철물/부자재",
        "title": "타카핀 실타카 단가 및 규격 안내",
        "description": "가는 실선 형태의 실타카핀으로, 몰딩이나 얇은 마감재의 정밀 고정에 사용됩니다.",
    },
    ("hardware", "타카핀 F"): {
        "slug": "hardware-staple-f",
        "category_label": "철물/부자재",
        "title": "타카핀 F 단가 및 규격 안내",
        "description": "F자 규격 타카핀으로, 합판·석고보드 등 넓은 면적의 고정 작업에 사용됩니다.",
    },
    ("hardware", "타카핀 ST"): {
        "slug": "hardware-staple-st",
        "category_label": "철물/부자재",
        "title": "타카핀 ST 단가 및 규격 안내",
        "description": "ST 규격 타카핀으로, 목재 프레임 및 구조재 조립 고정에 사용됩니다.",
    },
    ("hardware", "점검구"): {
        "slug": "hardware-access-panel",
        "category_label": "철물/부자재",
        "title": "점검구 단가 및 규격 안내",
        "description": "천장이나 벽체 내부 설비 점검을 위한 개폐형 점검구로, 배관·전기 설비 유지보수 동선 확보에 사용됩니다.",
    },
    ("hardware", "방부철물"): {
        "slug": "hardware-preservative-metal",
        "category_label": "철물/부자재",
        "title": "방부철물 단가 및 규격 안내",
        "description": "방부 처리된 목재 구조용 철물로, 데크나 파고라 등 외부 목구조물의 접합부 보강에 사용됩니다.",
    },
    ("hardware", "주춧돌"): {
        "slug": "hardware-post-base",
        "category_label": "철물/부자재",
        "title": "주춧돌 단가 및 규격 안내",
        "description": "목재 기둥 하부에 설치하는 받침 철물로, 지면과의 접촉을 차단해 기둥의 부식을 방지합니다.",
    },
    ("hardware", "도어손잡이"): {
        "slug": "hardware-door-handle",
        "category_label": "철물/부자재",
        "title": "도어손잡이 단가 및 규격 안내",
        "description": "문짝에 설치하는 손잡이 철물로, 다양한 디자인으로 문짝 시공 마감에 사용됩니다.",
    },
    ("hardware", "실리콘 부자재"): {
        "slug": "hardware-silicone-supplies",
        "category_label": "철물/부자재",
        "title": "실리콘 부자재 단가 및 규격 안내",
        "description": "실리콘 시공에 필요한 보조 자재로, 코킹 작업의 마감 품질을 높일 때 사용됩니다.",
    },
    ("hardware", "톱날/부자재"): {
        "slug": "hardware-saw-blade",
        "category_label": "철물/부자재",
        "title": "톱날/부자재 단가 및 규격 안내",
        "description": "목재 절단용 톱날 및 관련 부자재로, 현장 재단 작업에 사용됩니다.",
    },
    ("hardware", "오일스테인"): {
        "slug": "hardware-oil-stain",
        "category_label": "철물/부자재",
        "title": "오일스테인 단가 및 규격 안내",
        "description": "목재 표면에 도포하는 오일 스테인으로, 목재의 색상 표현과 방수·방오 마감에 사용됩니다.",
    },
    ("hardware", "사포"): {
        "slug": "hardware-sandpaper",
        "category_label": "철물/부자재",
        "title": "사포 단가 및 규격 안내",
        "description": "목재·도장면 연마용 사포로, 마감 전 표면 정리 작업에 사용됩니다.",
    },
    ("hardware", "반코팅 장갑"): {
        "slug": "hardware-gloves-coated",
        "category_label": "철물/부자재",
        "title": "반코팅 장갑 단가 및 규격 안내",
        "description": "손바닥 부분이 코팅된 작업용 장갑으로, 현장 작업 시 손 보호와 그립력 확보에 사용됩니다.",
    },
    ("hardware", "마대"): {
        "slug": "hardware-burlap-sack",
        "category_label": "철물/부자재",
        "title": "마대 단가 및 규격 안내",
        "description": "현장에서 자재 운반이나 폐자재 정리에 사용하는 마대자루입니다.",
    },
    ("hardware", "보양지/테이프"): {
        "slug": "hardware-protection-tape",
        "category_label": "철물/부자재",
        "title": "보양지/테이프 단가 및 규격 안내",
        "description": "시공 중 바닥이나 마감면을 보호하는 보양지와 테이프로, 오염·손상 방지에 사용됩니다.",
    },
    ("hardware", "로라"): {
        "slug": "hardware-paint-roller",
        "category_label": "철물/부자재",
        "title": "로라 단가 및 규격 안내",
        "description": "도장 작업용 페인트 롤러로, 넓은 면적의 균일한 도장 작업에 사용됩니다.",
    },
    ("hardware", "코팅제 집성판 전용"): {
        "slug": "hardware-coating-glulam",
        "category_label": "철물/부자재",
        "title": "코팅제 집성판 전용 단가 및 규격 안내",
        "description": "집성판 전용 표면 코팅제로, 집성판의 내구성과 마감 품질을 높일 때 사용됩니다.",
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
        .group-siblings { margin-top: 36px; padding-top: 24px; border-top: 1px solid var(--color-border); }
        .group-siblings-title { font-size: 13px; font-weight: 700; color: var(--color-text-muted); margin-bottom: 12px; }
        .group-siblings-list { display: flex; flex-wrap: wrap; gap: 8px; }
        .group-siblings-list a { font-size: 13px; color: var(--color-text-light); background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: 50px; padding: 7px 14px; text-decoration: none; transition: var(--transition-smooth); }
        .group-siblings-list a:hover { color: var(--color-accent-orange); border-color: var(--color-accent-orange); }
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


def render_page(category, group_name, meta, items, generated_at, gid_no, siblings=None):
    slug = meta["slug"]
    canonical = f"https://infill-wood.kr/groups/{slug}.html"
    title_tag = f"{meta['title']} | INFILL"
    rep_id = items[0]["id"]
    calc_link = f"/calculator.html?cat={category}&id={rep_id}"
    gen_date_str = generated_at.strftime("%Y-%m-%d")

    rows_html = ""
    product_entries = []
    for i, it in enumerate(items):
        rows_html += f"""
                        <tr>
                            <td class="name-col">{it['name']}</td>
                            <td>{it['spec'] or '-'}</td>
                            <td>{it['unit'] or '-'}</td>
                            <td class="price-col font-num">{format_price(it['price'])}</td>
                        </tr>"""
        product = {"@type": "Product", "name": it["name"], "sku": it["id"]}
        if it["price"] > 0:
            product["offers"] = {
                "@type": "Offer",
                "price": it["price"],
                "priceCurrency": "KRW",
                "availability": "https://schema.org/InStock",
                "url": canonical,
            }
        product_entries.append({
            "@type": "ListItem",
            "position": i + 1,
            "item": product,
        })

    calc_cat_link = f"/calculator.html?cat={category}"
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ItemList",
                "name": meta["title"],
                "itemListElement": product_entries,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://infill-wood.kr/"},
                    {"@type": "ListItem", "position": 2, "name": "최신단가표", "item": f"https://infill-wood.kr{calc_cat_link}"},
                    {"@type": "ListItem", "position": 3, "name": meta["category_label"], "item": f"https://infill-wood.kr{calc_cat_link}"},
                    {"@type": "ListItem", "position": 4, "name": group_name, "item": canonical},
                ],
            },
        ],
    }

    snapshot = {
        "generated_at": generated_at.isoformat(),
        "category": category,
        "group": group_name,
        "items": [{"id": it["id"], "name": it["name"], "price": it["price"]} for it in items],
    }

    sibling_links = ""
    if siblings:
        for sib_name, sib_slug in siblings:
            if sib_slug == slug:
                continue
            sibling_links += f'<a href="/groups/{sib_slug}.html">{sib_name}</a>'
    siblings_html = ""
    if sibling_links:
        siblings_html = f"""<div class="group-siblings">
                <div class="group-siblings-title">{meta['category_label']}의 다른 그룹</div>
                <div class="group-siblings-list">{sibling_links}</div>
            </div>"""

    inquiry_only = bool(meta.get("inquiry_only"))
    if inquiry_only:
        note_or_banner_html = f"""<div class="inquiry-banner">
                <strong>실시간 단가 준비 중인 품목입니다</strong>
                <p>정확한 사양과 단가는 카카오톡 또는 전화 상담으로 빠르게 안내해 드립니다.</p>
                <div class="inquiry-cta-row">
                    <a href="tel:02-1234-5678" class="btn btn-primary" data-phone-cta>전화 문의</a>
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
    <meta property="og:image" content="https://infill-wood.kr/assets/og/og-default.png">

    <link rel="icon" type="image/svg+xml" href="/assets/logo/app-icon.svg">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <link rel="stylesheet" as="style" crossorigin
        href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet">

    <!-- 대표전화 등 공통 설정 (지시서 SEO-01 F) -->
    <script src="/site-config.js"></script>

    <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>

    <style>{HEAD_CSS}
    </style>
</head>

<body>

    <header id="header">
        <div class="container header-wrap">
            <a href="/" class="logo-area">
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
                <a href="/">홈</a><span class="sep">›</span><a href="/calculator.html?cat={category}">최신단가표</a><span class="sep">›</span><a href="/calculator.html?cat={category}">{meta['category_label']}</a><span class="sep">›</span>{group_name}
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

            {siblings_html}
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


def write_groups_index_js():
    """calculator.html이 카테고리·그룹명 -> 그룹 페이지 슬러그를 찾아 내부 링크를 붙일 때 쓰는 매핑.
    이 스크립트가 유일한 소스 — 재생성할 때마다 함께 갱신된다(지시서 SEO-01 E)."""
    by_category = {}
    for (category, group_name), meta in GROUP_PAGE_MAP.items():
        by_category.setdefault(category, {})[group_name] = meta["slug"]
    js = "// 자동 생성 파일 — scripts/generate_group_pages.py가 관리함. 직접 수정하지 말 것.\n"
    js += "const GROUP_PAGE_SLUGS = " + json.dumps(by_category, ensure_ascii=False, indent=2) + ";\n"
    (REPO_ROOT / "groups-index.js").write_text(js, encoding="utf-8")
    print(f"[생성 완료] groups-index.js ({len(GROUP_PAGE_MAP)}개 그룹 매핑)")


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

    siblings_by_category = {}
    for (category, group_name), meta in GROUP_PAGE_MAP.items():
        siblings_by_category.setdefault(category, []).append((group_name, meta["slug"]))

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

        html = render_page(category, group_name, meta, items, generated_at, gid_counter,
                            siblings=siblings_by_category.get(category))
        out_path.write_text(html, encoding="utf-8")
        generated_files.append(str(out_path.relative_to(REPO_ROOT)))
        print(f"[생성 완료] {out_path.relative_to(REPO_ROOT)} ({len(items)}개 품목)")

    write_groups_index_js()

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
