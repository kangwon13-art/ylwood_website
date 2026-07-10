# 작업 컨텍스트

## 프로젝트 개요
- 이 워크스페이스는 영림 사이트 폴더 내 정적 웹사이트 파일과 관련 보조 스크립트로 구성되어 있습니다.
- 주요 HTML 파일은 index.html, index_restored.html, admin.html, admin_restored.html 입니다.
- 추가로 PowerShell 및 Python 스크립트가 포함되어 있어 사이트 콘텐츠 수정 및 복구 작업을 지원합니다.

## 작업 규칙
- 모든 코딩 작업 전에 이 파일을 먼저 읽고, 이 문서에 기록된 규칙과 맥락을 우선으로 따라야 합니다.
- 작업 중 변경 사항이 발생하면 즉시 이 문서에 반영합니다.
- 작업이 끝난 후에는 진행 상태, 변경 내용, 검증 결과를 이 문서에 기록합니다.

## 현재 상태
- 2026-07-06 기준, 문서 기반 작업 규칙 파일을 초기화했습니다.
- index.html에서 MDF 전용 CSV 로직을 범용 Google Sheets 로더로 전환했습니다.
- 로컬스토리지 기반 상품 오버라이드 로직은 제거하고, 시트 데이터가 우선 적용되도록 정리했습니다.
- 깨진 한글 표시 메시지를 정상 텍스트로 수정했고, REFERENCES 섹션은 연동 준비 상태로 정리했습니다.
- 검증 결과: [index.html](../index.html) 에 대한 에디터 오류 확인 결과 문제 없음.
- 2026-07-07 기준, "주요 납품 실적" 섹션을 Google Sheets 연동으로 전환했습니다. SHEET_CONFIG에 references 탭(gid=1626176847) 추가, transformSheetRow 컬럼 별칭에 현장명/내용/납품일 계열 추가, renderReferences()의 하드코딩된 빈 배열을 SHEET_DATA.references로 교체.
- 검증 결과: 해당 시트 CSV를 직접 조회해 실데이터 3건(판교/강남/분당 현장) 정상 파싱 확인.
- Netlify 배포(endearing-cassata-cf0649.netlify.app) 반영 여부는 대시보드 접근 권한이 없어 미확인 상태 — 사용자 확인 필요.
- 2026-07-09 기준, "작업지시서 #01: CSS/스크립트 중복 정리" 완료. 사이드바(.calc-sidebar 등) 4중 선언을 모바일 퍼스트 1곳 + PC 미디어쿼리 1곳으로 통합, 모바일 단가표 레이아웃(ZENFIX/Antigravity 이중 블록)을 속성 단위 실효값 분석 후 1벌로 병합, 헤더 전화버튼/calc-tabs/calc-tab/카테고리그리드 카드 중복 정리, 죽은 CSS(.quantity-control) 삭제, heroDate 중복 스크립트 제거. 상세 내역은 [css-refactor-summary.md](css-refactor-summary.md) 참조.
- 검증 결과: PC 1280px/모바일 375px 전체 페이지 스크린샷을 작업 전/후로 픽셀 비교(헤드리스 크롬). 병합 과정에서 `.price-table tbody tr`의 `align-items: center` 누락으로 모바일 단가표 셀이 전체 폭으로 늘어나는 회귀를 발견해 수정 — 수정 후 모바일 픽셀 diff 0건, PC는 무관한 렌더링 잡음(0.017%) 수준만 확인.
- 2026-07-09 기준, "작업지시서 #02: 라이트 인더스트리얼 + 계산기 퍼스트" 완료. 시안(design-02-mockup.html) v2 전체 컨펌 후 착수. 백업 태그 `pre-design-refactor-02`(HEAD 438786b) 생성. `:root` 색상 토큰을 다크→라이트로 전환, 히어로→계산기→카테고리 순서로 섹션 재배치, 전역 검색바를 히어로로 승격(id 유지로 이벤트 바인딩 보존), 헤더 전화번호 버튼 강조 및 모바일 상시노출(기존엔 모바일에서 완전히 숨겨져 있었음), 카탈로그 링크를 `.catalog-link`로 분리, 단가표에 sticky header/지브라/tabular-nums 적용, html2canvas@1.4.1로 견적서 PNG 저장 기능 신규 구현. 상세 내역은 [design-02-summary.md](design-02-summary.md) 참조.
- 검증 결과: 구조 태그 개폐 전수 balanced 확인, 모바일 375px에서 scrollWidth(469)≤innerWidth(484)로 가로 오버플로우 없음 확인, PC/태블릿/모바일 3종 풀페이지 캡처(docs/captures-02/) 완료, html2canvas 기능은 스크립트 주입으로 3품목·합계 315,000원 견적서 PNG를 실제 생성해 육안 검수 완료. Lighthouse/PageSpeed는 미배포 상태라 실행 불가 — 배포 후 재확인 필요(사유는 design-02-summary.md 8번 참조). 아직 커밋/푸시 전 상태.
- 2026-07-09 후속, 1차 검수 피드백 3건 반영: (1) 모바일 단가표 행을 flex 세로나열→CSS Grid 2행 구조(품명+단가 1행 / 규격·단위 요약+수량컨트롤 2행)로 압축, 실측 77~83px(목표 88px 이하 충족), 규격 열은 요약 텍스트로 통합해 중복 노출 제거. (2) 모바일 카테고리 카드의 데스크톱용 hover 풀필(아이콘 오렌지 반전+리프트)을 무효화하고 `:active`에서만 옅은 오렌지 배경+테두리로 반응하도록 변경(풀필 없음). (3) 사이드바 CTA를 1순위(견적 문의하기, 52px)/2순위(카카오+PNG저장 2열, 36px=70%) 위계로 재조정하고, `toggleMobileSidebar()`에서 `body.sidebar-expanded` 클래스를 동기화해 사이드바 펼침 중 플로팅 전화/카카오 버튼을 숨김 처리. 상세는 [design-02-summary.md](design-02-summary.md) 10번 참조.
- 검증 결과: 행 높이/버튼 높이는 헤드리스 크롬 스크립트로 실측(77.0/83.0px, 52.0/36.0/36.0px). 이 과정에서 이 환경의 헤드리스 Chrome이 375px 등 작은 `--window-size` 요청 시 실제로는 약 500px로 강제 렌더링하며 스크린샷만 크롭하는 현상을 발견(빈 페이지 교차검증 완료) — 이후 캡처는 500px로 전환해 크롭 없이 확인. 캡처는 docs/captures-02-v2/. 아직 커밋 전 상태.
- 2026-07-10, "작업지시서 #03: 모바일 단가표 2단 구조 개편(그룹 카드+옵션 바텀시트)" G1(그룹 매핑표)/G2(MDF 시연) 완료. G1: 전 카테고리 340개 품목을 65개 그룹으로 매핑, 감독 피드백 전량 반영(원스톤 규격분리/구조재 통합/단열재 재질별 재편/철물·부자재 119→10그룹/토이락 XPS 이동) — 확정본 [g1-group-mapping-v2.md](g1-group-mapping-v2.md). G2: MDF 카테고리 1개만 신UI 적용 — PRODUCTS_DATA.mdf 각 항목에 `group:'MDF 4x8'` 필드 추가, `transformSheetRow`에 그룹 열 파싱+시트 미지원시 하드코딩 폴백(`GROUP_FALLBACK`) 추가, `GROUPED_UI_CATEGORIES=['mdf']`로 범위 제한한 그룹 카드 목록(`renderMobileGroupList`)/옵션 바텀시트(`openOptionSheet`/`closeOptionSheet`/`handleOptionAdd`) 신규 구현, 검색 결과 클릭 시 그룹형 카테고리는 시트 자동 오픈+옵션 하이라이트(`openGroupSheetForItem`)로 분기, 모바일 하단바를 장바구니 진입점으로 재정의(0개/1개 이상 상태 전환), 옵션시트 열림 중 사이드바/플로팅버튼 숨김. 착수 전 백업 태그 `pre-mobile-ia-03` 생성.
- 검증 결과: 구조 태그 개폐 전수 balanced, PC(1280px) MDF 카테고리 기존 플랫 테이블 그대로 렌더링되어 회귀 없음 확인, 모바일(500px) 목록/시트열림/담기 후 하단바 반영(2개 품목·23,200원 합계 수치 검산 일치)/견적문의 처리(테스트 전용 임시 price=0 주입, 실데이터 미변경) 4종 캡처 완료(docs/captures-03-g2/). 다른 카테고리는 group 필드가 없어 자동으로 기존 플랫 테이블 유지(회귀 없음). 아직 커밋/푸시 전 상태 — 감독 확인 후 전 카테고리 확산 예정.
- 2026-07-10 후속, 감독 지시로 375px 실뷰포트 재캡처 진행. 이 환경의 헤드리스 Chrome은 `--window-size`를 375~500 사이 어떤 값으로 줘도 실제로는 500px(뷰포트 484px)로 강제 렌더링하는 하드플로어가 있음을 확인(빈 페이지로 문턱값 이진탐색: 500=484, 505=489 — 500이 정확한 하한선). 우회책: iframe을 375×812로 고정한 wrapper 페이지를 만들어 그 wrapper를 (플로어 영향 없는) 900px 창에서 캡처한 뒤 iframe 영역만 크롭 — iframe 자체 CSS 폭은 창 크기와 무관해 실제 375px 미디어쿼리 문턱이 정확히 적용됨. 5종 재캡처 완료(docs/captures-03-g2-mobile375/).
- **이 과정에서 실제 버그 발견 및 수정**: `.option-sheet-body`가 `flex:1; min-height:0;` 없이 `overflow-y:auto`만 있어, 옵션이 5개 넘는 그룹에서 시트 자체 높이(`.option-sheet{max-height:85vh; overflow:hidden}`)에 막혀 6번째 이후 옵션이 스크롤로 진입 자체가 안 되는 상태였음(바텀시트 몸통이 스스로 스크롤 컨테이너를 형성하지 못함). `flex:1; min-height:0;` 추가로 수정 — MDF(12개 옵션)에서 처음 노출되는 리스크였고, 그대로 뒀으면 확산 시 옵션이 많은 카테고리(예: 합판 4x8 21개)에서 6번째 이후 옵션을 아예 선택할 수 없는 심각한 문제였음.
- 검색→그룹시트 자동오픈은 스크린샷/DOM 조회로 시트가 정확한 그룹("MDF 4×8")으로 열리고 하이라이트 클래스가 옵션 카드에 정확히 적용됨(`highlighted:true`)을 확인. 다만 해당 옵션까지의 내부 스크롤 이동 자체는 이 환경(중첩 iframe + 헤드리스 dump-dom/screenshot)에서 프로그래매틱 scrollTop 변경이 반영되지 않는 렌더링 한계로 스크린샷상 직접 확인은 못함(반면 페이지 레벨 스크롤은 정상 동작 확인) — 실기기 라이브 링크로 최종 확인 권장.
- 실기기 확인용 임시 링크 발급: 최초엔 같은 와이파이 LAN IP(`http://192.168.0.30:8080`, TcpListener 기반, HttpListener는 관리자 권한 URL ACL 필요해 실패)로 시도했으나 이 PC 네트워크가 Windows에서 "공용"으로 분류돼 방화벽에 막힐 위험이 있어, 이후 라운드부터는 `cloudflared.exe`(portable, 설치 없이 GitHub에서 직접 다운로드) quick tunnel로 전환 — 아웃바운드 연결만 사용해 인바운드 방화벽 규칙이 전혀 필요 없음. 단, HttpListener 기반 로컬 서버는 Host 헤더가 `localhost`가 아니면 "400 Invalid Hostname"을 반환해 cloudflared와 함께 쓸 수 없었고, TcpListener 기반(Host 헤더 무시) 서버로 교체해 해결.
- 2026-07-10 3차 라운드, 실기기 재확인 피드백 3건 반영: (1) **가로 스크롤(좌우 흔들림)** — 원인은 옵션시트가 아니라 모바일 카테고리 탭바(`.calc-tabs`)의 `grid-template-columns: repeat(3, 1fr)`가 긴 탭 라벨(예: "방부목/특수목/합성목")의 `white-space:nowrap` 최소폭 때문에 실제로는 429px로 계산되어 페이지 전체가 375px 뷰포트를 넘어서던 **전 카테고리 공통의 기존 버그**였음(옵션시트 기능과 무관, 375px 정밀 재캡처 중 발견). `grid-template-columns: repeat(3, minmax(0,1fr))` + `.calc-tab`에 `min-width:0`, 줄바꿈 허용(`white-space:normal`)으로 수정, scrollWidth 429→375 확인. (2) **배경 스크롤 잠금 누락** — `body{overflow:hidden}`만으로는 iOS/Android 터치 팬이 완전히 막히지 않아, 스크롤 위치를 저장한 뒤 `body{position:fixed}`로 고정하는 방식(`lockBodyScroll`/`unlockBodyScroll`)으로 교체, 기존 "선택 품목" 바텀시트(`sidebar-expanded`)에도 동일 적용. 프로그래매틱하게 배경 스크롤 시도 후 값이 변하지 않는 것까지 확인. (3) **시트 높이 85vh→92vh** 상향, 실측 92.0% 확인. 캡처: docs/captures-03-fix-round/.
- 자체 QA 한계 기록: 스크롤 잠금은 이전 라운드에서 CSS 선언 존재 여부만 코드로 확인했고 실제 터치 드래그 재현은 헤드리스로 불가능해 놓쳤음 — 실기기 검증이 유일한 검증 수단이라는 교훈.
- 3차 라운드 보고 직후 감독이 추가로 3건(견적 시트 좌우 여백 없음/시트가 헤더 아래로 가려짐(z-index)/품목명 좌측 잘림)을 지적했으나, 감독이 "확인 완료, 커밋하고 푸쉬" 지시로 전환해 **이 3건은 아직 코드 미반영 상태로 다음 라운드에 이월**. 다음 세션에서 반드시 먼저 처리할 것: `.selected-list`/`.cart-item`에 옵션시트와 동일한 좌우 padding 적용, `.option-sheet`/`.calc-sidebar.expanded`의 z-index를 `header`보다 높게 조정, `.cart-item-name`의 `white-space:nowrap`+좌측 잘림 원인 확인.
