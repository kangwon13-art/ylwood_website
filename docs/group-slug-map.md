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

## 나머지 61개 그룹 (지시서#12 전체 확산 시 슬러그 부여 예정)

파일럿 승인 후 #12에서 나머지 10개 카테고리(마감자재/MDF/합판/인테리어합판/목재구조재/단열재/방부목특수목/루바집성판/철물부자재/운반비 제외)의 그룹에 슬러그를 이 문서에 이어서 채운다. 이 문서는 파일럿 4개만 다루며, 아직 나머지는 부여하지 않았다.
