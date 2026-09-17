# 그룹별 정적 URL 슬러그 맵 (지시서#11)

`g1-group-mapping-v2.md`의 그룹은 한글명만 있고 안정적인 id가 없어, 이 문서에서 그룹마다 영문 슬러그를 한 번만 수동으로 부여하고 이후 고정한다(그룹명이 바뀌어도 슬러그는 유지). `scripts/generate_group_pages.py`가 이 매핑을 그대로 사용한다.

**중요**: 아래 "시트상 그룹명" 컬럼은 `g1-group-mapping-v2.md` 문서가 아니라 **구글시트 "그룹" 컬럼의 실제 현재 값**을 기준으로 한다(코드의 `transformSheetRow`가 시트 값을 우선 사용하므로 매칭이 정확해야 한다). 2026-09-16 확인 시점에 문서상 "방균/차음"과 시트 실제값 "차음/방균보드"가 단어 순서·표기가 달라 이 문서는 시트 값을 기준으로 삼았다 — 향후 시트 쪽 그룹명이 또 바뀌면 이 매핑도 함께 갱신 필요.

## 석고보드 (파일럿 대상, 2026-09-16)

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| plaster | 일반석고보드 | `plaster-general` | `/groups/plaster-general.html` | 파일럿 완료 |
| plaster | 방수석고보드 | `plaster-waterproof` | `/groups/plaster-waterproof.html` | 파일럿 완료 |
| plaster | 방화석고보드 | `plaster-fireproof` | `/groups/plaster-fireproof.html` | 파일럿 완료 |
| plaster | 차음/방균보드 | `plaster-moisture` | `/groups/plaster-moisture.html` | 파일럿 완료 |

`석고본드`는 그룹이 아니라 단독 품목(`g1-group-mapping-v2.md` 확정)이므로 그룹 페이지 대상에서 제외했다 — "석고보드 카테고리 4개 그룹" 지시와 일치.

## 마감자재 (지시서#12, 2026-09-18)

2026-09-18 지시서#12 전수 감사에서 `g1-group-mapping-v2.md` 원안(5그룹)과 시트 실제 그룹(3그룹)이 다른 것을 확인 — 시트 값 기준으로 슬러그 부여(상세는 `g1-group-mapping-v2.md` 마감자재 섹션 참조).

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| finishing | 아쿠아보드 | `finishing-aquaboard` | `/groups/finishing-aquaboard.html` | 생성 완료(로컬 커밋, push 대기) |
| finishing | 스톤플렉시블보드 | `finishing-stone-flexible` | `/groups/finishing-stone-flexible.html` | 생성 완료(로컬 커밋, push 대기) |
| finishing | 영림 월판넬 | `finishing-wallsystem` | `/groups/finishing-wallsystem.html` | 생성 완료(전 품목 견적문의 — 문의유도형 템플릿, 로컬 커밋, push 대기) |

## 나머지 카테고리 (지시서#12 전수 감사 결과, 2026-09-18)

`g1-group-mapping-v2.md`에 카테고리별 시트 실제 그룹명·개수를 전부 정리해뒀다. 남은 진행 순서(사이트맵 우선순위 기준, 카테고리당 1~2개 라운드):

| 카테고리 키 | 카테고리명 | 시트 실제 그룹 수 | 슬러그 부여 상태 |
|---|---|---|---|
| mdf | MDF | 1 | 미부여 |
| plywood | 합판 | 9 | 미부여 (백색 코팅합판/미장(라미날 합판)/스페이스월 3개는 각자 단독 그룹 — 통합 여부 확인 필요) |
| interior_plywood | 인테리어합판 | 7 | 미부여 |
| timber | 목재/구조재 | 4 | 미부여 |
| insulation | 단열재 | 6 | 미부여 |
| deck_timber | 방부목/특수목/합성목 | 6 | 미부여 |
| louver_wood | 루바/집성판 | 12 | 미부여 |
| hardware | 철물/부자재 | 27 (+ 그룹 미지정 12개) | **보류 — 시트 그룹 정리 후 재개** |

철물/부자재 제외 나머지 8개 카테고리 합계 약 45개 그룹(75개에서 마감자재 3개 기완료분 제외). 원래 "61개 그룹" 추정치는 `g1-group-mapping-v2.md` 원안(구 시트 상태) 기준이었고, 전수 감사 결과 실제로는 카테고리별 그룹 수가 달라져 있었다.
