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
