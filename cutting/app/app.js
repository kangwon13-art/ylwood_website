/**
 * 영림 재단 견적 — 3분할 작업화면
 * 엔진(jaedan_engine_v2.js)의 solve()를 그대로 호출한다. 엔진 로직은 수정하지 않는다.
 * 배치도는 solve() 결과의 실계산 좌표(x,y,pw,pl)를 그대로 SVG로 변환한다 (임의 도면 금지).
 */

// ─── 상태 ──────────────────────────────────────────
let items = []; // {id, w, l, q, g}
let nextId = 1;
let activeSheetIdx = 0;
let lastResult = null;

const el = (id) => document.getElementById(id);

// ─── 입력 이벤트 ────────────────────────────────────
el('specSelect').addEventListener('change', recalc);
el('thicknessInput').addEventListener('input', recalc);
el('trimCheck').addEventListener('change', recalc);
el('grainAllToggle').addEventListener('change', () => {
  const checked = el('grainAllToggle').checked;
  items.forEach(it => it.g = checked);
  renderItemList();
  recalc();
});

el('addItemBtn').addEventListener('click', () => {
  const w = parseFloat(el('inputW').value);
  const l = parseFloat(el('inputL').value);
  const q = parseInt(el('inputQ').value, 10) || 1;
  const g = el('inputG').checked;

  if (!(w > 0) || !(l > 0) || !(q >= 1)) {
    alert('폭·길이는 0보다 큰 숫자, 수량은 1 이상이어야 합니다.');
    return;
  }
  items.push({ id: nextId++, w, l, q, g });
  el('inputW').value = '';
  el('inputL').value = '';
  el('inputQ').value = '1';
  el('inputG').checked = el('grainAllToggle').checked;
  el('inputW').focus();
  renderItemList();
  recalc();
});

function removeItem(id) {
  items = items.filter(it => it.id !== id);
  renderItemList();
  recalc();
}

// ─── 계산 ──────────────────────────────────────────
function recalc() {
  const specKey = el('specSelect').value;
  const thickness = parseFloat(el('thicknessInput').value) || 18;
  const useTrim = el('trimCheck').checked;

  if (items.length === 0) {
    lastResult = null;
    renderEmptyState();
    return;
  }

  const engineItems = items.map(it => ({ w: it.w, l: it.l, q: it.q, g: it.g }));
  lastResult = solve(engineItems, specKey, thickness, useTrim);
  lastResult._specKey = specKey;
  lastResult._thickness = thickness;
  lastResult._useTrim = useTrim;

  if (activeSheetIdx >= lastResult.sheets.length) activeSheetIdx = 0;

  renderSheetTabs();
  renderSheetView();
  renderSummary();
  renderUnplaced();
}

// ─── 좌: 항목 리스트 렌더링 ─────────────────────────
function renderItemList() {
  const body = el('itemListBody');
  body.innerHTML = '';
  el('emptyHint').classList.toggle('hidden', items.length > 0);
  items.forEach(it => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${it.w}</td>
      <td>${it.l}</td>
      <td>${it.q}</td>
      <td>${it.g ? 'O' : '-'}</td>
      <td><button class="del-btn" type="button" aria-label="삭제">✕</button></td>
    `;
    tr.querySelector('.del-btn').addEventListener('click', () => removeItem(it.id));
    body.appendChild(tr);
  });
}

// ─── 중앙: 배치도 렌더링 ────────────────────────────
function renderEmptyState() {
  el('sheetTabs').innerHTML = '';
  el('sheetView').innerHTML = '<p class="empty-hint">재단 항목을 추가하면 배치도가 표시됩니다.</p>';
  el('summaryCard').innerHTML = '';
  el('unplacedCard').classList.add('hidden');
}

function renderSheetTabs() {
  const tabs = el('sheetTabs');
  tabs.innerHTML = '';
  if (!lastResult || lastResult.sheets.length === 0) return;
  lastResult.sheets.forEach((sheet, i) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = `원장 ${i + 1} (${sheet.type})`;
    btn.className = i === activeSheetIdx ? 'active' : '';
    btn.addEventListener('click', () => {
      activeSheetIdx = i;
      renderSheetTabs();
      renderSheetView();
    });
    tabs.appendChild(btn);
  });
}

function renderSheetView() {
  const view = el('sheetView');
  view.innerHTML = '';
  if (!lastResult || lastResult.sheets.length === 0) {
    if (lastResult && lastResult.unplaced.length > 0 && items.length > 0) {
      view.innerHTML = '<p class="empty-hint">배치 가능한 항목이 없습니다. 우측 미배치 안내를 확인하세요.</p>';
    }
    return;
  }
  const sheet = lastResult.sheets[activeSheetIdx];
  const title = document.createElement('div');
  title.className = `sheet-title type-${sheet.type.toLowerCase()}`;
  title.textContent = `원장 ${activeSheetIdx + 1} — ${lastResult._specKey} / ${lastResult._thickness}T — ${sheet.type}·${sheet.cuts}컷 — ${sheet.cost.toLocaleString()}원`;
  view.appendChild(title);
  view.appendChild(buildSheetSvg(sheet, lastResult._specKey, lastResult._useTrim, lastResult.topTrim, lastResult.leftTrim));
}

/**
 * 엔진 결과(sheet.items[].x/y/pw/pl, sheet.freeRects)를 그대로
 * 물리적 원장 좌표(폭축=세로, 길이축=가로)로 변환해 SVG를 그린다.
 * 도면은 90도 눕혀 길이 방향이 가로가 되도록 표시한다.
 */
function buildSheetSvg(sheet, specKey, useTrim, topTrim, leftTrim) {
  const spec = SPECS[specKey];
  const rawW = spec.w, rawL = spec.l;

  const allFL = sheet.items.every(it => it.src.isFullL);
  const insetTop = useTrim ? topTrim : 0;              // 폭축 인셋 (상전단, 항상)
  const insetLeft = (useTrim && !allFL) ? leftTrim : 0;  // 길이축 인셋 (좌전단, 전길이만이면 생략)

  // 화면 좌표 변환: X축(가로) = 길이 방향, Y축(세로) = 폭 방향 (엔진 좌표계는 x=폭,y=길이 고정)
  function toScreen(x, y, pw, pl) {
    return { sx: insetLeft + y, sy: insetTop + x, sw: pl, sh: pw };
  }

  const maxW = 720;
  const scale = maxW / rawL;
  const svgW = rawL * scale;
  const svgH = rawW * scale;

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('viewBox', `0 0 ${svgW} ${svgH}`);
  svg.setAttribute('width', svgW);
  svg.setAttribute('height', svgH);

  // 전체 원장 외곽선
  const outline = document.createElementNS(svgNS, 'rect');
  outline.setAttribute('class', 'sheet-outline');
  outline.setAttribute('x', 0); outline.setAttribute('y', 0);
  outline.setAttribute('width', svgW); outline.setAttribute('height', svgH);
  svg.appendChild(outline);

  // 전단 영역 표시
  if (useTrim) {
    if (insetTop > 0) {
      svg.appendChild(rectEl(svgNS, 0, 0, svgW, insetTop * scale, 'trim-rect'));
    }
    if (insetLeft > 0) {
      svg.appendChild(rectEl(svgNS, 0, 0, insetLeft * scale, svgH, 'trim-rect'));
    }
  }

  // 잔재 — 엔진이 계산한 자유영역(freeRects)을 그대로 표시
  (sheet.freeRects || []).forEach(fr => {
    const g = toScreen(fr.x, fr.y, fr.w, fr.l);
    svg.appendChild(rectEl(svgNS, g.sx * scale, g.sy * scale, g.sw * scale, g.sh * scale, 'scrap-rect'));
  });

  // 조각 배치 (엔진 실계산 좌표 그대로)
  sheet.items.forEach((it, idx) => {
    const g = toScreen(it.x, it.y, it.pw, it.pl);
    svg.appendChild(rectEl(svgNS, g.sx * scale, g.sy * scale, g.sw * scale, g.sh * scale,
      `piece-rect type-${sheet.type.toLowerCase()}`));

    const label = document.createElementNS(svgNS, 'text');
    label.setAttribute('class', 'piece-label');
    label.setAttribute('x', (g.sx + g.sw / 2) * scale);
    label.setAttribute('y', (g.sy + g.sh / 2) * scale);
    label.textContent = `#${idx + 1} ${Math.round(g.sw)}×${Math.round(g.sh)}`;
    svg.appendChild(label);
  });

  return svg;
}

function rectEl(svgNS, x, y, w, h, cls) {
  const r = document.createElementNS(svgNS, 'rect');
  r.setAttribute('x', x); r.setAttribute('y', y);
  r.setAttribute('width', Math.max(w, 0)); r.setAttribute('height', Math.max(h, 0));
  r.setAttribute('class', cls);
  return r;
}

// ─── 우: 결과 요약 ──────────────────────────────────
function renderSummary() {
  const card = el('summaryCard');
  if (!lastResult) { card.innerHTML = ''; return; }
  const r = lastResult;
  card.innerHTML = `
    <h2>결과 요약</h2>
    <div class="row"><span>필요 원장 수</span><span class="val">${r.totalSheets}장</span></div>
    ${r._useTrim ? `<div class="row"><span>적용 전단</span><span class="val">상 ${r.topTrim}mm · 좌 ${r.leftTrim}mm</span></div>` : ''}
    <div class="row"><span>로스율</span><span class="val">${(r.lossRate * 100).toFixed(1)}%</span></div>
    <div class="row"><span>총 컷 수</span><span class="val">${r.totalCuts}회</span></div>
    <div class="row"><span>&nbsp;&nbsp;1D 컷 / 원장</span><span class="val">${r.cuts1D}회 / ${r.sheets1D}장</span></div>
    <div class="row"><span>&nbsp;&nbsp;2D 컷 / 원장</span><span class="val">${r.cuts2D}회 / ${r.sheets2D}장</span></div>
    <div class="row total"><span>총 재단비</span><span class="val">${r.totalCost.toLocaleString()}원</span></div>
  `;
}

function renderUnplaced() {
  const card = el('unplacedCard');
  if (!lastResult || lastResult.unplacedSummary.length === 0) {
    card.classList.add('hidden');
    card.innerHTML = '';
    return;
  }
  const totalCount = lastResult.unplacedSummary.reduce((a, u) => a + u.count, 0);
  card.classList.remove('hidden');
  card.innerHTML = `
    <h3>⚠ 원장에 안 들어가는 항목 ${totalCount}개</h3>
    <ul>
      ${lastResult.unplacedSummary.map(u =>
        `<li>${u.w}×${u.l} — ${u.count}개 (선택한 규격/전단 조건에서 배치 불가)</li>`
      ).join('')}
    </ul>
  `;
}

// ─── 재단 계획서 미리보기 / PDF ─────────────────────
el('previewBtn').addEventListener('click', () => {
  if (!lastResult || items.length === 0) {
    alert('먼저 재단 항목을 입력해 주세요.');
    return;
  }
  renderPlan();
  el('planOverlay').classList.remove('hidden');
});
el('planCloseBtn').addEventListener('click', () => el('planOverlay').classList.add('hidden'));
el('pdfBtn').addEventListener('click', () => window.print());

function renderPlan() {
  const r = lastResult;
  const spec = SPECS[r._specKey];
  const now = new Date();
  const dateStr = `${now.getFullYear()}년 ${now.getMonth() + 1}월 ${now.getDate()}일 ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

  const content = el('planContent');
  content.innerHTML = `
    <div class="plan-header">
      <h2>재단 계획서</h2>
      <div class="plan-date">${dateStr}</div>
    </div>

    <div class="plan-section">
      <h3>판재 정보</h3>
      <table class="plan-table">
        <tr><th>규격</th><td>${r._specKey} (${spec.w}×${spec.l})</td>
            <th>두께</th><td>${r._thickness}T</td>
            <th>전단</th><td>${r._useTrim ? `적용 (상 ${r.topTrim}mm · 좌 ${r.leftTrim}mm)` : '미적용'}</td></tr>
      </table>
    </div>

    <div class="plan-section">
      <h3>재단 결과</h3>
      <table class="plan-table">
        <tr><th>총 판재 수</th><th>재단 횟수</th><th>총 재단비</th></tr>
        <tr>
          <td>${r.totalSheets}장</td>
          <td>${r.totalCuts}회</td>
          <td>${r.totalCost.toLocaleString()}원</td>
        </tr>
      </table>
    </div>

    <div class="plan-section">
      <h3>재단 항목</h3>
      <table class="plan-table">
        <thead><tr><th>폭</th><th>길이</th><th>수량</th><th>결지킴</th></tr></thead>
        <tbody>
          ${items.map(it => `<tr><td>${it.w}</td><td>${it.l}</td><td>${it.q}</td><td>${it.g ? 'O' : '-'}</td></tr>`).join('')}
        </tbody>
      </table>
      ${r.unplacedSummary.length > 0 ? `
        <p style="color:#c0392b;font-size:12px;margin-top:8px;">
          ⚠ 미배치: ${r.unplacedSummary.map(u => `${u.w}×${u.l} ${u.count}개`).join(', ')}
        </p>` : ''}
    </div>

    <div class="plan-section">
      <h3>배치도</h3>
      <div id="planSheets"></div>
    </div>
  `;

  const planSheets = content.querySelector('#planSheets');
  r.sheets.forEach((sheet, i) => {
    const wrap = document.createElement('div');
    wrap.style.marginBottom = '16px';
    const title = document.createElement('div');
    title.className = `sheet-title type-${sheet.type.toLowerCase()}`;
    title.textContent = `원장 ${i + 1} — ${sheet.type}·${sheet.cuts}컷 — ${sheet.cost.toLocaleString()}원`;
    wrap.appendChild(title);
    wrap.appendChild(buildSheetSvg(sheet, r._specKey, r._useTrim, r.topTrim, r.leftTrim));
    planSheets.appendChild(wrap);
  });
}

// ─── 초기화 ─────────────────────────────────────────
renderItemList();
renderEmptyState();
