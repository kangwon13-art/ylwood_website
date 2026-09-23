$ErrorActionPreference = 'Stop'

try {
    # INDEX.HTML MODIFICATIONS
    $indexPath = "index.html"
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)

    # 1. CSS Modifications
    $cssAdditions = @"
        /* Antigravity Custom Styles */
        @media (max-width: 768px) {
            .price-table thead { display: none !important; }
            .price-table tbody tr {
                display: flex;
                flex-wrap: wrap;
                flex-direction: column;
                padding: 15px 0;
                border-bottom: 1px solid var(--color-border);
            }
            .price-table tbody td {
                display: block;
                width: 100%;
                border: none;
                padding: 4px 16px;
                text-align: left;
            }
            .price-table tbody td:nth-child(1) { font-weight: 700; font-size: 15px; }
            .price-table tbody td:nth-child(1) .prod-spec { display: block; font-size: 12px; color: var(--color-text-muted); font-weight: 400; margin-top: 2px; }
            .price-table tbody td:nth-child(2), .price-table tbody td:nth-child(3) { display: inline-block; width: auto; padding: 2px 16px; font-size: 14px; }
            .price-table tbody td:nth-child(4) { margin-top: 8px; }
            .price-table tbody td:nth-child(4) .quantity-control { width: 100%; min-height: 44px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px; }
            .price-table tbody td:nth-child(4) .quantity-control button { width: 44px; height: 44px; }
            .price-table tbody td:nth-child(4) .quantity-control span { flex-grow: 1; text-align: center; }

            header .phone-call-btn, header .catalog-btn { display: none !important; }
            
            .category-grid { grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; }
            .category-card { padding: 10px 5px !important; height: auto !important; aspect-ratio: 1/1; justify-content: center; align-items: center; }
            .category-card .category-description, .category-card .category-footer-link { display: none !important; }
            .category-card .category-icon-wrap { width: 40px; height: 40px; margin-bottom: 5px; }
            .category-card .category-name { font-size: 13px !important; text-align: center; margin-bottom: 0; }
        }
        
        .sidebar-toggle-arrow { display: inline-block; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .calc-sidebar.expanded .sidebar-toggle-arrow { transform: rotate(180deg); }
"@

    if (-not $indexContent.Contains("Antigravity Custom Styles")) {
        $indexContent = $indexContent.Replace("</style>", "$cssAdditions`n</style>")
    }

    # 3. Remove floating-cta-bar block
    $indexContent = [regex]::Replace($indexContent, '<!-- MOBILE BOTTOM FLOATING CTA BAR -->[\s\S]*?<div class="floating-buttons">', '<div class="floating-buttons">')
    $indexContent = [regex]::Replace($indexContent, '<div class="floating-cta-bar">[\s\S]*?</div>\s*(?=<!-- SUCCESS POPUP MODAL -->|<div class="modal")', '')

    # 5. Bottom Sheet Arrow Insert
    if (-not $indexContent.Contains("sidebar-toggle-arrow")) {
        $indexContent = $indexContent.Replace(
            '<h3 class="summary-title" onclick="toggleSidebar()">',
            '<h3 class="summary-title" onclick="toggleSidebar()">`n                <span class="sidebar-toggle-arrow">∧</span><br>'
        )
    }

    # 8. catalog.html button
    if (-not $indexContent.Contains("catalog.html")) {
        $catBtn = '<a href="catalog.html" class="phone-call-btn catalog-btn" title="제품 카탈로그"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg> 제품 카탈로그</a>`n                        '
        $indexContent = $indexContent.Replace('<button class="quick-consult-btn"', $catBtn + '<button class="quick-consult-btn"')
    }

    # 10. Hero date automation
    if ($indexContent.Contains("오늘 09:00 기준 완료") -and -not $indexContent.Contains("hero-date")) {
        $indexContent = $indexContent.Replace("오늘 09:00 기준 완료", '<span id="hero-date">오늘 09:00 기준 완료</span>')
        $dateScript = @"
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const dateSpan = document.getElementById('hero-date');
            if(dateSpan) {
                const today = new Date();
                const yyyy = today.getFullYear();
                const mm = String(today.getMonth() + 1).PadLeft(2, '0');
                const dd = String(today.getDate()).PadLeft(2, '0');
                dateSpan.textContent = ``${yyyy}.${mm}.${dd} 09:00 기준 완료``;
            }
        });
    </script>
"@
        $indexContent = $indexContent.Replace("</body>", "$dateScript`n</body>")
    }

    # 6. Admin data alignment in index.html
    $p9Rep = "{ id: 'p9', code: '', name: '4mm 4x8 일반합판', spec: '준내수 / 4x8 (1220x2440mm)', unit: '장', price: 17500 }"
    $pl6Rep = "{ id: 'pl6', code: '', name: '본드', spec: '-', unit: '포 (25kg)', price: 12100 }"
    $indexContent = [regex]::Replace($indexContent, "\{\s*id:\s*'p9'[^}]*\}", $p9Rep, [System.Text.RegularExpressions.RegexOptions]::None)
    $indexContent = [regex]::Replace($indexContent, "\{\s*id:\s*'pl6'[^}]*\}", $pl6Rep, [System.Text.RegularExpressions.RegexOptions]::None)

    # 9. Dynamic References in loadLocalData
    if ($indexContent.Contains("function loadLocalData()") -and -not $indexContent.Contains("renderReferences")) {
        $refJs = @"
        // Antigravity: Render references
        function renderReferences() {
            const grid = document.querySelector('.references-grid');
            if (!grid) return;
            const refData = JSON.parse(localStorage.getItem('yw_references_data'));
            if (refData && refData.length > 0) {
                grid.innerHTML = '';
                refData.forEach(item => {
                    const html = `
                        <div class="reference-card">
                            <div class="ref-date">`+ (item.date || '') +`</div>
                            <h3 class="ref-title">`+ (item.title || '') +`</h3>
                            <div class="ref-items">`+ (item.items || '') +`</div>
                        </div>
                    `;
                    grid.insertAdjacentHTML('beforeend', html);
                });
            }
        }
        renderReferences();
"@
        $indexContent = $indexContent.Replace("function loadLocalData() {", "function loadLocalData() {`n$refJs")
    }

    [System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)

    # ADMIN.HTML MODIFICATIONS
    $adminPath = "admin.html"
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)

    # 7. Backup/Restore Toolbar
    $backupHtml = @"
            <button class="btn btn-outline" onclick="backupData()">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>
                백업
            </button>
            <button class="btn btn-outline" onclick="document.getElementById('restoreInput').click()">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"/></svg>
                복원
            </button>
            <input type="file" id="restoreInput" accept=".json" style="display:none;" onchange="restoreData(event)">
"@
    if (-not $adminContent.Contains("backupData()")) {
        $adminContent = $adminContent.Replace('<div class="toolbar-actions">', "<div class=`"toolbar-actions`">`n$backupHtml")
        $backupJs = @"
        function backupData() {
            const data = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.startsWith('yw_')) {
                    data[key] = localStorage.getItem(key);
                }
            }
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const date = new Date().toISOString().split('T')[0];
            a.download = `yw_backup_` + date + `.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function restoreData(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (confirm('백업 데이터를 복원하시겠습니까? 기존 데이터는 덮어씌워집니다.')) {
                        for (const key in data) {
                            if (key.startsWith('yw_')) {
                                localStorage.setItem(key, data[key]);
                            }
                        }
                        alert('복원되었습니다.');
                        location.reload();
                    }
                } catch(err) {
                    alert('잘못된 백업 파일입니다.');
                }
                event.target.value = '';
            };
            reader.readAsText(file);
        }
"@
        $adminContent = $adminContent.Replace("</script>", "$backupJs`n</script>")
    }

    # 9. Admin References Tab
    $tabHtml = @"
            <input type="radio" name="admin-tab" id="tab-references" onchange="switchAdminTab('references')">
            <label for="tab-references" class="tab-label">납품실적</label>
"@
    if (-not $adminContent.Contains("tab-references")) {
        $adminContent = $adminContent.Replace("</nav>", "$tabHtml</nav>")
    }

    $refSection = @"
        <!-- 납품실적 관리 섹션 -->
        <section id="section-references" class="admin-section" style="display: none;">
            <div class="section-header">
                <h2 class="section-title">납품실적 관리</h2>
                <button class="btn btn-primary" onclick="addReferenceItem()">+ 실적 추가</button>
            </div>
            <div class="table-responsive">
                <table class="admin-table" id="table-references">
                    <thead>
                        <tr>
                            <th>프로젝트명 (타이틀)</th>
                            <th>납품품목</th>
                            <th>완료일 (날짜)</th>
                            <th width="80">관리</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </section>
"@
    if (-not $adminContent.Contains("section-references")) {
        $adminContent = [regex]::Replace($adminContent, "(</main>)", "$refSection`n`$1")
    }

    $refJsAdmin = @"
        let referencesData = [];
        const DEFAULT_REFERENCES = [
            { id: 'r1', title: '송파구 대규모 아파트 신축', items: '석고보드, 경량철골 외', date: '2024.05' },
            { id: 'r2', title: '강남구 지식산업센터', items: '천장재, 단열재, 목재', date: '2024.04' },
            { id: 'r3', title: '성남 물류센터', items: '경량철골, 석고보드, 도어', date: '2024.03' }
        ];

        function loadReferencesData() {
            const saved = localStorage.getItem('yw_references_data');
            if (saved) {
                referencesData = JSON.parse(saved);
            } else {
                referencesData = JSON.parse(JSON.stringify(DEFAULT_REFERENCES));
                localStorage.setItem('yw_references_data', JSON.stringify(referencesData));
            }
            renderAdminReferences();
        }

        function renderAdminReferences() {
            const tbody = document.querySelector('#table-references tbody');
            if (!tbody) return;
            tbody.innerHTML = '';
            referencesData.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><input type="text" class="form-input" value="`+item.title+`" onchange="updateReference('`+item.id+`', 'title', this.value)"></td>
                    <td><input type="text" class="form-input" value="`+item.items+`" onchange="updateReference('`+item.id+`', 'items', this.value)"></td>
                    <td><input type="text" class="form-input" value="`+item.date+`" onchange="updateReference('`+item.id+`', 'date', this.value)"></td>
                    <td><button class="btn btn-outline" style="color:red;border-color:red" onclick="removeReference('`+item.id+`')">삭제</button></td>
                `;
                tbody.appendChild(tr);
            });
        }

        function addReferenceItem() {
            const newId = 'r' + Date.now();
            referencesData.unshift({ id: newId, title: '', items: '', date: '' });
            saveReferences();
            renderAdminReferences();
        }

        function updateReference(id, field, value) {
            const item = referencesData.find(i => i.id === id);
            if (item) {
                item[field] = value;
                saveReferences();
            }
        }

        function removeReference(id) {
            if(confirm('이 실적을 삭제하시겠습니까?')) {
                referencesData = referencesData.filter(i => i.id !== id);
                saveReferences();
                renderAdminReferences();
            }
        }

        function saveReferences() {
            localStorage.setItem('yw_references_data', JSON.stringify(referencesData));
        }

        const originalInit2 = window.onload;
        window.onload = function() {
            if(originalInit2) originalInit2();
            loadReferencesData();
        };
"@
    if (-not $adminContent.Contains("DEFAULT_REFERENCES")) {
        $adminContent = $adminContent.Replace("</script>", "$refJsAdmin`n</script>")
    }

    [System.IO.File]::WriteAllText($adminPath, $adminContent, [System.Text.Encoding]::UTF8)

    Write-Host "Modifications complete."
} catch {
    Write-Error $_.Exception.Message
}
