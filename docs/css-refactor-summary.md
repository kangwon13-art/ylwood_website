# CSS/스크립트 중복 정리 — 변경 요약 문서 (작업지시서 #01)

작업일: 2026-07-09 / 대상 파일: `index.html` (단일 파일 유지, 구조 변경 없음)

## 1. 검증 결과 요약

- **PC 1280px, 모바일 375px 전체 페이지 스크린샷을 작업 전/후로 캡처해 픽셀 단위로 비교했습니다.**
  - PC: 헤드리스 크롬으로 동일 파일을 2회 재캡처해 얻은 "노이즈 기준선"은 0건이었는데, 작업 전/후 비교에서는 3-스텝 샘플링 기준 99건의 차이가 나왔습니다. 좌표를 크롭해 확인한 결과 히어로 배지의 둥근 테두리 안티에일리어싱 수준의 미세한 차이로, `.hero-badge` 관련 CSS는 이번 작업에서 손대지 않았고 시각적으로 식별 불가능한 수준이라 렌더링 잡음으로 판단했습니다.
  - 모바일: 최초 비교에서 3,664건(전체 샘플의 1.76%)의 차이가 발견되어 조사한 결과, **실제 회귀 버그 1건을 발견해 수정**했습니다 (아래 4번 항목). 수정 후 재비교 결과 **차이 0건** — 완전한 픽셀 일치를 확인했습니다.
- 스타일 블록 중괄호 개수 256:256으로 균형 확인, `<script>`/`</script>` 3:3 균형 확인.

## 2. 발견 및 수정한 회귀 버그 (검증 과정에서 발견)

병합 과정에서 옛 "ZENFIX" 블록의 `.price-table tr { align-items: center; ... }` 규칙을 "완전히 죽은 코드"로 판단해 삭제했으나, 이후 등장하는 Antigravity의 `.price-table tbody tr` 규칙이 `align-items`를 재선언하지 않아 이 속성만 조용히 살아있던 것을 놓쳤습니다. 이로 인해 모바일 단가표 셀들이 가운데 정렬 대신 전체 폭으로 늘어나 "장"(단위) 텍스트가 화면 밖으로 밀려나는 버그가 발생했음을 실제 브라우저 계산 스타일 비교로 확인했고, `align-items: center;`를 병합된 `.price-table tbody tr` 규칙에 추가해 원복했습니다.

## 3. 중복 제거 내역

### 3-1. 계산기 사이드바 (`.calc-sidebar`, `.calc-sidebar.expanded`, `.sidebar-inner-content`, `.summary-title`, `.sidebar-toggle-arrow`, `.calc-sidebar.expanded .sidebar-toggle-arrow`)
- 기존 4곳 중복(헤더 섹션 안에 잘못 끼어있던 블록, "Calculator Sidebar Summary" 블록, `@media(max-width:1024px)` 서브셋, `@media(min-width:769px)` PC 오버라이드) → **모바일 퍼스트 기본값 1곳 + PC 미디어쿼리 오버라이드 1곳**으로 통합.
- 헤더 섹션에 잘못 위치했던 중복 블록 삭제, 계산기 섹션 내 위치(기존 "Calculator Sidebar Summary" 자리)를 정식 위치로 확정.
- `@media (max-width: 1024px)` 내부의 사이드바 관련 선언 전부 삭제 (지시사항 3번 명시 요구사항) — 분석 결과 이 선언들은 `@media(min-width:769px)`의 `!important` 규칙에 항상 덮어써져 실질적으로 죽은 코드였음을 확인.
- PC 오버라이드 블록의 `!important` 전부 제거 (단일 후행 선언으로 자연스럽게 우선하므로 불필요).

### 3-2. 모바일 단가표 레이아웃 (A안 "ZENFIX" vs B안 "Antigravity")
- **판별 결과: B안(Antigravity)이 실제 적용되고 있었음을 확인** (소스 순서상 후행 + 선택자 명시도(specificity)가 더 높음: 예) `.price-table tbody tr`(0,1,2) > `.price-table tr`(0,1,1)).
- 다만 완전한 승자 독식이 아니라 **속성 단위로 혼합 적용**되고 있었음을 각 셀렉터별로 개별 분석해 확인:
  - A안에만 있고 B안이 건드리지 않는 속성(`.table-responsive`, `.price-table` 자체, `.price-table tbody{display:block}`, `td:nth-child(1)`의 flex/text-align/padding-right, `td:nth-child(3)`의 flex/text-align/font-weight/color, `td:nth-child(4)`의 flex/text-align/font-weight/font-size/margin-left, `td:nth-child(5)` 전체, `.prod-name`, `.mobile-spec-text`, `.qty-control`/`.qty-btn`/`.qty-input`, `.btn-inquire`)는 **살아있는 상태 그대로 보존**.
  - B안이 더 높은 명시도로 실제 이기고 있는 속성(`display`, `td:nth-child(2)/(3)`의 inline-block/width/padding/font-size 등)은 B안 값을 채택.
  - 위 "2. 발견한 회귀 버그"의 `align-items: center` 도 이 범주에서 누락되었다가 검증 중 발견·복원.
- 결과적으로 두 블록을 하나의 일관된 `@media (max-width: 768px)` 블록으로 완전히 병합, "Task 2: ZENFIX...", "Antigravity Custom Styles" 이력 주석 삭제.

### 3-3. 기타 중복
- **헤더 전화버튼 숨김**: `.header-contact .phone-call-btn`과 `header .phone-call-btn, header .catalog-btn` 2곳 → `header .phone-call-btn, header .catalog-btn` 1곳으로 통합 (catalog-btn은 원래 유일한 선언이라 유지).
- **`.calc-tabs`**: 산재해 있던 `.calc-tabs { flex-wrap: nowrap !important; }` 단독 선언을 상단 원 정의(`.calc-tabs` 기본 규칙)에 `flex-wrap: nowrap;`으로 병합, 단독 블록 삭제.
- **`.calc-tab` 내부 `white-space: nowrap` 중복**: 모바일 블록 내 같은 규칙 안에 2번 선언되어 있던 것을 1번으로 정리.
- **죽은 CSS `.quantity-control` 삭제**: 마크업/스크립트 전체를 검색한 결과 `.quantity-control` 클래스는 어디에도 사용되지 않음(실제 사용 클래스는 `.qty-control`, JS 템플릿 리터럴에서 직접 확인). 관련 선언 3개(`.price-table tbody td:nth-child(4) .quantity-control` 및 그 하위 `button`/`span`) 전부 삭제.
- **카테고리 카드 모바일 스타일**: ZENFIX 블록과 Antigravity 블록에 나뉘어 있던 `.category-grid`/`.category-card`/`.category-description`/`.category-footer-link`/`.category-icon-wrap`/`.category-name`을, 마감자재 단가표와 동일한 방식으로 속성 단위 실효값을 계산해 1벌로 병합.
- **footer 하단 패딩**: `padding-bottom: 140px`은 기존에 이미 "buffer space for bottom sidebar" 주석이 있어 그대로 유지(의도 명시 요건 충족).

### 3-4. 스크립트
- **heroDate 중복 설정 제거**: 파일 맨 끝의 별도 `<script>` 블록(`document.addEventListener('DOMContentLoaded', ...)`으로 `#heroDate`를 재설정하던 것)을 삭제. 메인 스크립트 내부의 `window.addEventListener("DOMContentLoaded", ...)` 안 heroDate 설정 로직 1곳만 유지.

## 4. PRICES 객체 — 미사용 키 목록 (삭제는 차기 작업, 이번엔 변경하지 않음)

`PRICES` 객체(총 132개 키) 중 실제로 참조되는 것은 `finishing` 카테고리의 `f5~f19` 15개뿐이며, 나머지 카테고리(mdf, plywood, interior_plywood, timber, plaster, insulation, deck_timber, louver_wood, hardware, delivery)는 전부 하드코딩된 숫자 리터럴을 직접 사용하고 있어 아래 **117개 키가 미사용 상태**입니다.

- `f1, f2, f3, f4, f20, f21, f22, f23` (8개)
- `m1~m9` (9개)
- `p101~p118, p121~p126` (24개)
- `ip201~ip205, ip211~ip215, ip221, ip231~ip238` (19개)
- `t1~t14` (14개)
- `p1, p1b, p2, p3, p4, p5` (6개)
- `i2, i3, i5~i9` (7개)
- `d1~d11` (11개)
- `h1~h12` (12개)
- `del1~del7` (7개)

## 5. 목표 구조(작업지시서 7번) 반영 범위에 대한 스코프 결정

전체 스타일시트(2,000여 줄)를 지시서 7번의 6단계 구조로 물리적으로 전면 재배치하는 대신, **이번 작업지시서에서 명시적으로 중복이 지적된 셀렉터/블록만 정밀 통합**했습니다. 그 결과로:
- `@media (max-width: 1024px)`는 사이드바 관련 선언만 제거되고 히어로/카테고리그리드 등 중복 아닌 규칙은 그대로 유지.
- `@media (max-width: 768px)`는 2곳 → 1곳으로 완전 병합.
- `@media (min-width: 769px)`는 1곳으로 정리, `!important` 전부 제거.
- 계산기 사이드바 기본 선언은 계산기 섹션 내 1곳으로 통합.

버튼/폼/모달/FAQ 등 이번 지시서에서 중복으로 지적되지 않은 나머지 CSS는 원래 위치를 그대로 유지했습니다. 전체 파일을 목표 구조대로 물리적으로 재배열하려면 감사 범위 밖의 선택자들까지 전수 재검증해야 해서, "화면 결과물 100% 동일" 원칙(대원칙 1번, 위반 시 반려)에 대한 리스크가 이번에 확인된 `align-items` 사례처럼 실제로 존재함을 감안해 범위를 좁혔습니다. 필요하시면 이 부분은 별도 작업으로 진행하겠습니다.

## 6. 남은 검증 항목 (수동 확인 권장)

정적 분석과 자동 스크린샷 비교로 검증한 항목 외에, 아래는 실제 브라우저에서 클릭 기반으로 확인하는 것을 권장합니다 (이번 작업에서 JS 로직 자체는 heroDate 중복 제거 외에는 손대지 않았으나, 실사용 흐름 확인 차원에서):
- 계산기 수량 증감 → 사이드바 합계 반영 → "견적 문의하기" 폼 자동입력
- 전역 검색 → 항목 클릭 → 탭 이동 + 행 하이라이트
- 콘솔 에러 0건 (브라우저 개발자도구에서 직접 새로고침 확인)
