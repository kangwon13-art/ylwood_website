// 자동 생성 파일 — scripts/generate_group_pages.py가 관리함. 직접 수정하지 말 것.
const GROUP_PAGE_SLUGS = {
  "plaster": {
    "일반석고보드": "plaster-general",
    "방수석고보드": "plaster-waterproof",
    "방화석고보드": "plaster-fireproof",
    "차음/방균보드": "plaster-moisture"
  },
  "finishing": {
    "아쿠아보드": "finishing-aquaboard",
    "스톤플렉시블보드": "finishing-stone-flexible",
    "영림 월판넬": "finishing-wallsystem"
  },
  "mdf": {
    "MDF": "mdf-general"
  },
  "plywood": {
    "합판 910x1820": "plywood-3x6",
    "태고합판 910x1820": "plywood-taego-3x6",
    "일반합판 1220x2440": "plywood-4x8-general",
    "코아합판 1220x2440": "plywood-4x8-core",
    "OSB 1220x2440": "plywood-osb",
    "CRC 보드": "plywood-crc",
    "백색 코팅합판": "plywood-white-coated",
    "미장(라미날 합판)": "plywood-laminate",
    "스페이스월": "plywood-spacewall"
  },
  "interior_plywood": {
    "미송합판 유절": "interior-plywood-misong-knotted",
    "미송합판 무절": "interior-plywood-misong-clear",
    "낙엽송합판(라찌합판)": "interior-plywood-larch",
    "오쿠메합판": "interior-plywood-okoume",
    "레드오크합판": "interior-plywood-red-oak",
    "자작합판": "interior-plywood-birch",
    "타공판": "interior-plywood-perforated"
  },
  "timber": {
    "소송 각재": "timber-sosong",
    "뉴송 각재": "timber-newsong",
    "마감용 구조재": "timber-structural",
    "라왕 각재": "timber-lawan"
  },
  "insulation": {
    "아이소핑크/토이락": "insulation-isopink-toirock",
    "단열재 이보드": "insulation-eboard",
    "열반사 단열재": "insulation-reflective",
    "스티로폼": "insulation-styrofoam",
    "글라스울": "insulation-glasswool",
    "차음 충진재": "insulation-filler"
  },
  "deck_timber": {
    "방부목 데크재/각재": "deck-timber-treated",
    "방킬라이": "deck-timber-bankirai",
    "합성데크": "deck-timber-composite",
    "무방부 데크재": "deck-timber-untreated",
    "라틱스 방부/PVC": "deck-timber-lattice",
    "사이딩": "deck-timber-siding"
  },
  "louver_wood": {
    "원목루바": "louver-wood-solid",
    "히노끼 판재": "louver-wood-hinoki-plank",
    "라디에타파인 집성판": "louver-wood-radiata-pine",
    "레드파인 집성판": "louver-wood-red-pine",
    "삼목 집성판": "louver-wood-cedar",
    "히노끼 집성판": "louver-wood-hinoki-glulam",
    "고무나무 집성판": "louver-wood-rubberwood",
    "라왕 집성판": "louver-wood-lawan",
    "멀바우 집성판": "louver-wood-merbau",
    "오크 집성판": "louver-wood-oak",
    "애쉬 집성판": "louver-wood-ash",
    "아카시아 집성판": "louver-wood-acacia"
  },
  "hardware": {
    "접착재/본드": "hardware-adhesive-bond",
    "폼 / 부자재": "hardware-foam-supplies",
    "무초산 실리콘": "hardware-silicone-neutral",
    "바이오 실리콘": "hardware-silicone-bio",
    "수성 실리콘": "hardware-silicone-water",
    "외부용 실리콘": "hardware-silicone-exterior",
    "아연피스 목재용 외날": "hardware-screw-zinc-wood",
    "윙스크류 양날": "hardware-screw-wing",
    "석고피스 양날": "hardware-screw-drywall",
    "스텐피스 양날": "hardware-screw-stainless",
    "타카핀 U자": "hardware-staple-u",
    "타카핀 DT/T": "hardware-staple-dt-t",
    "타카핀 실타카": "hardware-staple-fine",
    "타카핀 F": "hardware-staple-f",
    "타카핀 ST": "hardware-staple-st",
    "점검구": "hardware-access-panel",
    "방부철물": "hardware-preservative-metal",
    "주춧돌": "hardware-post-base",
    "도어손잡이": "hardware-door-handle",
    "실리콘 부자재": "hardware-silicone-supplies",
    "톱날/부자재": "hardware-saw-blade",
    "오일스테인": "hardware-oil-stain",
    "사포": "hardware-sandpaper",
    "반코팅 장갑": "hardware-gloves-coated",
    "마대": "hardware-burlap-sack",
    "보양지/테이프": "hardware-protection-tape",
    "로라": "hardware-paint-roller",
    "코팅제 집성판 전용": "hardware-coating-glulam"
  }
};
