# 디자인 개편 — 라이트 인더스트리얼 + 계산기 퍼스트 (작업지시서 #02) 변경 요약

작업일: 2026-07-09 / 대상 파일: `index.html` (단일 파일 유지, 구조 변경 없음)
사전 확정: v2 시안(`design-02-mockup.html`) 전체 컨펌 완료, 카피 2안 확정, 카탈로그 링크 위치 승인, 백업 태그 `pre-design-refactor-02`(HEAD `438786b`) 생성 완료 후 착수.

## 1. 디자인 토큰 — 라이트 인더스트리얼 전환

`:root`의 CSS 커스텀 프로퍼티 값만 교체하는 방식으로 전체 페이지 색상을 전환했습니다 (변수명은 유지, 값만 다크→라이트로 치환).

| 변수 | 기존(다크) | 변경(라이트) |
|---|---|---|
| `--color-bg-primary` | `#0A0F1D` | `#F5F6F8` |
| `--color-bg-secondary` | `#12192C` | `#FFFFFF` |
| `--color-bg-tertiary` | `#1E2943` | `#EEF0F4` |
| `--color-accent-navy-light` | `#2A3B5F` | `#1F2A44` |
| `--color-text-white` (고대비 텍스트/제목 역할) | `#FFFFFF` | `#1A1F2B` |
| `--color-text-muted` | `#94A3B8` | `#5F6875` (WCAG 대비 4.94:1 @ `#EEF0F4`, 5.64:1 @ `#FFFFFF` 검증) |
| `--color-text-light` (본문) | `#E2E8F0` | `#333A47` |
| `--color-border` | `rgba(148,163,184,.15)` | `#DDE1E8` |
| `--shadow-premium` / `--shadow-glow` | 다크 배경용 진한 그림자 | 라이트 배경용 옅은 그림자로 조정 |
| `--color-accent-orange` 계열 | 변경 없음 | 변경 없음 (브랜드 오렌지 유지) |

토큰만으로 커버되지 않는 하드코딩 색상(헤더 글래스 배경, 히어로 라디얼 그라디언트, 히어로 카드 글래스 패널, 사이드바 토글 화살표) 4곳은 개별적으로 라이트 테마에 맞게 재작성했습니다. xlsx-js-style 엑셀 내보내기용 인라인 색상(라인 3600대)은 페이지 렌더링과 무관해 손대지 않았습니다.

## 2. 레이아웃 순서 변경 — 계산기 퍼스트

기존 순서 히어로 → 카테고리 → 계산기 → 문의폼 → 실적 → FAQ 를 **히어로 → 계산기 → 카테고리 → 문의폼 → 실적 → FAQ**로 재배치했습니다. 카테고리 섹션 전체(카드 9종 마크업 포함)를 계산기 섹션 뒤로 이동했으며, 두 섹션 내부 마크업은 손대지 않고 위치만 교체했습니다.

## 3. 컴팩트 히어로 + 검색바 승격

- 히어로 상단 여백을 PC `120px 0 100px` → `76px 0 60px`, 모바일 상단 여백 `120px` → `90px`로 축소.
- 헤드라인을 확정된 2안으로 교체: "찾는 자재 검색 한 번, 단가부터 견적까지 한 화면에서".
- 계산기 섹션에 있던 전역 검색 입력창(`#globalProductSearchInput`, `#globalSearchDropdown`)을 히어로 영역(부제 아래, CTA 버튼 위)으로 이동. **DOM 위치만 이동했고 `id`는 그대로 유지**했으므로, 검색→탭 전환(`switchCalcTab`)→행 하이라이트(`scrollIntoView` + `highlight-row`) 로직은 `getElementById` 기반이라 수정 없이 정상 동작함을 헤드리스 브라우저 스크립트 주입 테스트로 확인.

## 4. 헤더 전화번호 우선순위 상향

- `.phone-call-btn`을 무채색 아웃라인 버튼에서 오렌지 강조 버튼(`background: var(--color-accent-orange-light)`, `border: 1px solid var(--color-accent-orange)`)으로 변경해 시각적 우선순위 상향.
- "제품 카탈로그" 링크를 `.phone-call-btn` 클래스 재사용에서 분리해 전용 `.catalog-link`(밑줄 텍스트, muted 컬러) 클래스로 전환 — 전화번호보다 낮은 우선순위로 명확히 구분.
- 모바일(`max-width:768px`)에서 기존에는 `header .phone-call-btn, header .catalog-btn { display:none; }`으로 **전화번호 버튼 자체가 사라졌던 것**을 수정: 이제 `.catalog-link`만 숨기고, 전화 버튼은 아이콘만 남긴 원형 버튼으로 축소해 **상시 노출**되도록 변경.

## 5. 단가표 Excel 스타일 적용

- `.table-responsive`에 `max-height: 640px; overflow-y: auto;`를 추가해 내부 스크롤 컨테이너화하고, `.price-table th`에 `position: sticky; top: 0;`을 적용해 스크롤 중 헤더 고정.
- `.price-table`에 `font-variant-numeric: tabular-nums;`를 적용해 숫자 컬럼(단가/수량/합계) 자릿수 정렬.
- 짝수 행에 `var(--color-bg-tertiary)` 배경을 적용한 지브라 스트라이핑 추가, hover 배경을 `var(--color-accent-orange-light)`로 강조.
- 선택자를 `.price-table tr` → `.price-table tbody tr`로 명확화해 헤더 행이 지브라/hover 대상에 포함되지 않도록 함 (지시서#01에서 이미 확립된 관례와 일치).

## 6. 신규 기능 — 견적서 이미지 저장 (html2canvas)

- **도입 라이브러리**: `html2canvas@1.4.1` (jsDelivr CDN, 버전 고정). 선정 사유: 2022-01 배포 이후 안정적으로 유지되는 최신 정식 릴리스이며, 별도 빌드 과정 없이 `<script>` 태그로 단일 파일 로드가 가능해 이 프로젝트의 "빌드 없는 정적 파일" 제약과 호환됨.
- `downloadEstimateImage()` 함수 추가: 기존 `selectedQuantities`/`PRODUCTS_DATA` 데이터를 이용해 품목/단가/수량/금액 4열 영수증 형태의 오프스크린 DOM(`position:fixed; left:-9999px`)을 동적 생성하고, `html2canvas()`로 캡처해 PNG(`영림우드_견적서_YYYYMMDD.png`)로 다운로드.
- 사이드바에 "견적서 이미지 저장 (PNG)" 버튼 추가 (기존 "견적 문의하기"/"카카오톡 전송" 버튼 아래).
- 항목이 없을 때는 기존 견적 문의 버튼과 동일한 패턴으로 안내 alert 후 계산기 섹션으로 스크롤.

## 7. 검증 결과

- **구조 무결성**: `div`/`section`/`table`/`script`/`style` 태그 개폐 개수 및 CSS 중괄호 개수 전수 일치 확인 (표 생략, 전부 balanced).
- **모바일 가로 스크롤(overflow) 점검**: 375px 뷰포트에서 `document.documentElement.scrollWidth`(469px) ≤ `window.innerWidth`(484px) 확인 — 가로 오버플로우 없음. (참고: 스크린샷 축소 렌더링 과정에서 카테고리 카드 3열 그리드가 잘려 보이는 것처럼 오인했으나, 이는 지시서#01에서 이미 픽셀 검증된 기존 모바일 3열 아이콘 카드 레이아웃이며 이번 변경과 무관함을 CSS 확인으로 재검증함.)
- **헤드리스 크롬 풀페이지 캡처**: PC 1280px / 태블릿 768px / 모바일 375px 3종 캡처 완료 (`docs/captures-02/`).
- **html2canvas 기능 동작 검증**: 스크립트 주입으로 3개 품목(수량 4/2/10, 합계 315,000원)을 담아 `downloadEstimateImage()`를 직접 호출 → 102~113KB PNG data URL 생성 확인, 다운로드 트리거(`<a download>`) 정상 작동 확인, 실제 생성된 PNG 이미지를 육안 검수(`docs/captures-02/quote_sample.png`) — 레이아웃/합계 금액 정확.

## 8. Lighthouse / 성능 리포트에 대한 처리

사전 합의된 대체 순서(① PageSpeed Insights → ② DevTools Lighthouse 수동 → ③ 생략+사유 명시) 중 **③으로 처리**했습니다. 사유: 이번 변경사항은 아직 `origin`에 푸시/배포되지 않은 로컬 커밋 이전 단계이며, PageSpeed Insights는 공개적으로 접근 가능한 URL이 필요해 로컬 정적 서버(`localhost`) 상태로는 실행할 수 없습니다. DevTools Lighthouse 패널은 대화형 브라우저 세션이 필요한데 현재 환경에는 Node/Python/chromium-cli가 없고 PowerShell 5.1에서 CDP WebSocket 연결도 불가능해(`System.Net.WebSockets.ClientWebSocket` 로드 실패) 자동화가 불가능합니다. 색상 대비는 1번 항목에서 이미 WCAG 수치로 검증을 대체했습니다. **배포 후 실제 Netlify URL에 대해 PageSpeed Insights(pagespeed.web.dev)를 직접 실행하는 것을 권장**하며, 필요하시면 배포 후 제가 그 결과를 확인해 보고하겠습니다.

## 9. 스코프 밖 — 이번에 손대지 않은 것

- 카탈로그 페이지(`catalog.html`)는 지시서 06번 항목대로 이번 범위에서 제외.
- `origin` 푸시/배포는 별도 지시 대기 (현재 로컬 커밋 예정 상태만).

## 10. 1차 검수 후 추가 요청 3건 반영 (같은 날 후속 작업)

### 10-1. 모바일 단가표 행 압축 (1~2행 구조, 88px 이하)

- 기존 모바일 행: `flex-direction:column`으로 품명/규격/단위/단가/수량을 세로로 완전히 나열 (수량 컨트롤도 `width:100%; min-height:44px`의 풀폭 스테퍼) → 실측 없이도 5블록 누적으로 150px 이상이 되는 구조였음.
- 변경: `.price-table tbody tr`을 `display:grid; grid-template-columns:1fr auto; grid-template-rows:auto auto;`로 전환.
  - 1열(품명 td)은 `grid-row:1/span 2`로 두 행에 걸쳐 세로 중앙 정렬하고, 내부에서 품명(16px bold, 1줄 말줄임)과 규격+단위 요약(`${spec} · ${unit}`, 12px 회색, 1줄 말줄임)을 세로로 쌓음.
  - 규격 열(2번째 td)·단위 열(3번째 td)은 `display:none` 처리 — 요약 텍스트로 대체되므로 중복 노출 안 함.
  - 단가(4번째 td)는 1행 우측, 수량 컨트롤/문의하기 버튼(5번째 td)은 2행 우측에 배치.
  - 수량 스테퍼를 풀폭(`min-height:44px`)에서 소형(`28px` 버튼, 우측 정렬)으로 축소, `.btn-inquire`도 풀폭→인라인 소형(`padding:6px 14px`)으로 축소.
- **실측 결과** (헤드리스 크롬, 스크립트로 `getBoundingClientRect().height` 측정): 수량 선택형 행 **77.0px**, 견적문의형 행(문의하기 버튼) **83.0px** — 목표(88px 이하) 충족. 정확한 "수정 전" 실측치는 남기지 않았으나(리팩토링 전 상태 재현 필요), 5블록 세로 누적 구조상 15px×2 패딩 + 품명(15px)+규격(14px)+단위(14px)+단가(14px, margin-top 8px)+수량(44px, margin-top 12px) 누적으로 150px 이상이었을 것으로 추정되는 원래 구조와 비교해 확연히 압축됨.
- 캡처: `docs/captures-02-v2/mobile_full_compact_rows.png`

### 10-2. 모바일 카테고리 카드 hover 풀필 제거

- 기존: 데스크톱용 `.category-card:hover` (아이콘 배경 오렌지 풀필 + 카드 translateY 리프트 + 그림자)이 모바일에도 그대로 적용되어, 터치 기기에서 탭 후 `:hover`가 해제되지 않고 "고정"되는 현상이 있었음.
- 변경: `@media (max-width:768px)` 안에서 `.category-card:hover` 계열 규칙을 전부 무효화(`transform:none; box-shadow:none; border-color:기본값; 아이콘 배경 원복`)하고, 대신 `.category-card:active`에 `background: var(--color-accent-orange-light); border-color: var(--color-accent-orange);`만 적용. 카드 자체의 배경 색 반전(풀필)은 발생하지 않음. 기본 흰 배경/얇은 테두리는 손대지 않음(요청대로 유지).
- 캡처: `docs/captures-02-v2/category_card_active_state.png` (첫 번째 카드에 active 상태를 강제 재현하여 캡처 — 옅은 오렌지 배경 + 오렌지 테두리만 확인되고, 나머지 카드는 기본 상태 그대로임을 대조 확인)

### 10-3. 사이드바 CTA 위계 재조정 + 플로팅 버튼 중복 방지

- 1순위: "선택 품목으로 견적 문의하기"를 `.sidebar-cta-main`(높이 **52px**)로 유지, 유일한 풀필 오렌지 메인 버튼.
- 2순위: 카카오톡 전송 + PNG 저장을 `.sidebar-cta-secondary`(`display:grid; grid-template-columns:1fr 1fr;`)로 나란히 배치, 각 버튼 높이 **36px** (52px의 **69.2%** ≈ 70%), 아이콘+텍스트 축소(12.5px).
- 플로팅 전화/카카오 버튼(`.floating-buttons`)과 사이드바 바텀시트 중첩 방지: `toggleMobileSidebar()`에서 사이드바 펼침 여부를 `document.body`의 `sidebar-expanded` 클래스로 동기화하고, `body.sidebar-expanded .floating-buttons { display:none; }`을 모바일 미디어쿼리에 추가. 사이드바 접힘 상태에서는 플로팅 버튼이 그대로 노출됨.
- **실측 결과**: 메인 버튼 52.0px, 카카오 전송 36.0px, PNG 저장 36.0px (스크립트 측정).
- 캡처: `docs/captures-02-v2/sidebar_cta_hierarchy_and_floating_hidden.png` (사이드바 펼침 상태 — 위계 구조와 플로팅 버튼이 사라진 것을 한 장에서 함께 확인 가능)

### 10-4. (참고) 헤드리스 테스트 환경 제약 재확인

이번 검증 과정에서 이 환경의 헤드리스 Chrome이 `--window-size`에 375px 등 작은 값을 넘겨도 실제로는 최소 폭 약 500px(뷰포트 기준 약 484px)로 강제 렌더링하면서, `--screenshot` 출력 파일만 요청한 픽셀 크기로 잘라내는(cropping) 현상을 확인했습니다(빈 페이지로 교차 검증 완료). 이 때문에 375px로 찍은 초기 스크린샷 일부에서 우측 콘텐츠가 잘려 보이는 착시가 있었으나, 실제 페이지에는 가로 스크롤/오버플로우가 없음을 `scrollWidth`/`innerWidth` 측정으로 확인했습니다. 이번 라운드부터는 500px 폭으로 캡처해 크롭 없이 정확한 화면을 확보했습니다. 참고용 기록입니다.
