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

## 합판 (지시서#12, 2026-09-18)

백색 코팅합판/미장(라미날 합판)/스페이스월 3개는 2026-09-15 NO 중복 사고 때 추가된 품목이 각자 단독 그룹으로 남아있는 것 — 감독 확인 결과 통합하지 않고 시트 값 그대로 9개 페이지로 진행(딥링크 일관성 + 구체적 검색어 SEO 가치 판단).

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| plywood | 합판 910x1820 | `plywood-3x6` | `/groups/plywood-3x6.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | 태고합판 910x1820 | `plywood-taego-3x6` | `/groups/plywood-taego-3x6.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | 일반합판 1220x2440 | `plywood-4x8-general` | `/groups/plywood-4x8-general.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | 코아합판 1220x2440 | `plywood-4x8-core` | `/groups/plywood-4x8-core.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | OSB 1220x2440 | `plywood-osb` | `/groups/plywood-osb.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | CRC 보드 | `plywood-crc` | `/groups/plywood-crc.html` | 생성 완료(로컬 커밋, push 대기) |
| plywood | 백색 코팅합판 | `plywood-white-coated` | `/groups/plywood-white-coated.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| plywood | 미장(라미날 합판) | `plywood-laminate` | `/groups/plywood-laminate.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| plywood | 스페이스월 | `plywood-spacewall` | `/groups/plywood-spacewall.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |

## 인테리어합판 (지시서#12, 2026-09-18)

레드오크합판은 1품목짜리 단독 그룹 — 합판 카테고리 때와 동일한 판단(딥링크 일관성 + 구체적 검색어 SEO 가치)으로 통합 없이 개별 페이지 진행.

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| interior_plywood | 미송합판 유절 | `interior-plywood-misong-knotted` | `/groups/interior-plywood-misong-knotted.html` | 생성 완료(로컬 커밋, push 대기) |
| interior_plywood | 미송합판 무절 | `interior-plywood-misong-clear` | `/groups/interior-plywood-misong-clear.html` | 생성 완료(로컬 커밋, push 대기) |
| interior_plywood | 낙엽송합판(라찌합판) | `interior-plywood-larch` | `/groups/interior-plywood-larch.html` | 생성 완료(로컬 커밋, push 대기) |
| interior_plywood | 오쿠메합판 | `interior-plywood-okoume` | `/groups/interior-plywood-okoume.html` | 생성 완료(로컬 커밋, push 대기) |
| interior_plywood | 레드오크합판 | `interior-plywood-red-oak` | `/groups/interior-plywood-red-oak.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| interior_plywood | 자작합판 | `interior-plywood-birch` | `/groups/interior-plywood-birch.html` | 생성 완료(로컬 커밋, push 대기) |
| interior_plywood | 타공판 | `interior-plywood-perforated` | `/groups/interior-plywood-perforated.html` | 생성 완료(로컬 커밋, push 대기) |

## 목재/구조재 (지시서#12, 2026-09-18)

**미해결 확인 요청**: "마감용 구조재" 그룹의 "60x60"/"90x90" 표기가 실제 판매 중인 구조재 규격(인치 기준 4x4/6x6일 가능성)과 일치하는지 감독이 실물 기준으로 확인 필요 — 이번 라운드는 시트 값(60x60/90x90) 그대로 진행. 틀리면 발주 오류로 직결되는 부분이라 코드/문서 판단으로 임의 정정하지 않음.

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| timber | 소송 각재 | `timber-sosong` | `/groups/timber-sosong.html` | 생성 완료(로컬 커밋, push 대기) |
| timber | 뉴송 각재 | `timber-newsong` | `/groups/timber-newsong.html` | 생성 완료(로컬 커밋, push 대기) |
| timber | 마감용 구조재 | `timber-structural` | `/groups/timber-structural.html` | 생성 완료(60x60/90x90 표기 확인 요청 중, 로컬 커밋, push 대기) |
| timber | 라왕 각재 | `timber-lawan` | `/groups/timber-lawan.html` | 생성 완료(로컬 커밋, push 대기) |

## 단열재 (지시서#12, 2026-09-18)

문서 원안(재질 설명형 명칭)과 품목 구성이 완전히 동일하고 그룹명만 단순화된 경우 — 구조적 이슈 없음. 글라스울/차음 충진재 2개는 1품목 단독 그룹, 지금까지와 동일한 논리로 개별 페이지 진행.

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| insulation | 아이소핑크/토이락 | `insulation-isopink-toirock` | `/groups/insulation-isopink-toirock.html` | 생성 완료(로컬 커밋, push 대기) |
| insulation | 단열재 이보드 | `insulation-eboard` | `/groups/insulation-eboard.html` | 생성 완료(로컬 커밋, push 대기) |
| insulation | 열반사 단열재 | `insulation-reflective` | `/groups/insulation-reflective.html` | 생성 완료(로컬 커밋, push 대기) |
| insulation | 스티로폼 | `insulation-styrofoam` | `/groups/insulation-styrofoam.html` | 생성 완료(로컬 커밋, push 대기) |
| insulation | 글라스울 | `insulation-glasswool` | `/groups/insulation-glasswool.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| insulation | 차음 충진재 | `insulation-filler` | `/groups/insulation-filler.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |

## 방부목/특수목/합성목 (지시서#12, 2026-09-18)

방킬라이/무방부 데크재 2개는 1품목 단독 그룹 — 지금까지와 동일한 논리로 개별 페이지 진행. "방부목 데크재/각재" 12개 품목 통합 그룹은 MDF(12개)에서 이미 검증된 표 길이라 별도 이슈 없음.

| 카테고리 키 | 시트상 그룹명 | 슬러그 | URL | 상태 |
|---|---|---|---|---|
| deck_timber | 방부목 데크재/각재 | `deck-timber-treated` | `/groups/deck-timber-treated.html` | 생성 완료(로컬 커밋, push 대기) |
| deck_timber | 방킬라이 | `deck-timber-bankirai` | `/groups/deck-timber-bankirai.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| deck_timber | 합성데크 | `deck-timber-composite` | `/groups/deck-timber-composite.html` | 생성 완료(로컬 커밋, push 대기) |
| deck_timber | 무방부 데크재 | `deck-timber-untreated` | `/groups/deck-timber-untreated.html` | 생성 완료(단독 품목 1개, 로컬 커밋, push 대기) |
| deck_timber | 라틱스 방부/PVC | `deck-timber-lattice` | `/groups/deck-timber-lattice.html` | 생성 완료(로컬 커밋, push 대기) |
| deck_timber | 사이딩 | `deck-timber-siding` | `/groups/deck-timber-siding.html` | 생성 완료(로컬 커밋, push 대기) |

## 나머지 카테고리 (지시서#12 전수 감사 결과, 2026-09-18)

`g1-group-mapping-v2.md`에 카테고리별 시트 실제 그룹명·개수를 전부 정리해뒀다. 남은 진행 순서(사이트맵 우선순위 기준, 카테고리당 1~2개 라운드):

| 카테고리 키 | 카테고리명 | 시트 실제 그룹 수 | 슬러그 부여 상태 |
|---|---|---|---|
| mdf | MDF | 1 | `mdf-general` — 생성 완료(로컬 커밋, push 대기) |
| plywood | 합판 | 9 | 9개 전부 생성 완료(위 표 참조, 로컬 커밋, push 대기) |
| interior_plywood | 인테리어합판 | 7 | 7개 전부 생성 완료(위 표 참조, 로컬 커밋, push 대기) |
| timber | 목재/구조재 | 4 | 4개 전부 생성 완료(위 표 참조, 로컬 커밋, push 대기) |
| insulation | 단열재 | 6 | 6개 전부 생성 완료(위 표 참조, 로컬 커밋, push 대기) |
| deck_timber | 방부목/특수목/합성목 | 6 | 6개 전부 생성 완료(위 표 참조, 로컬 커밋, push 대기) |
| louver_wood | 루바/집성판 | 12 | 미부여 |
| hardware | 철물/부자재 | 27 (+ 그룹 미지정 12개) | **보류 — 시트 그룹 정리 후 재개** |

철물/부자재 제외 나머지 8개 카테고리 합계 약 45개 그룹(75개에서 마감자재 3개 기완료분 제외). 원래 "61개 그룹" 추정치는 `g1-group-mapping-v2.md` 원안(구 시트 상태) 기준이었고, 전수 감사 결과 실제로는 카테고리별 그룹 수가 달라져 있었다.
