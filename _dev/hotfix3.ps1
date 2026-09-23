$ErrorActionPreference = 'Stop'

try {
    # 1. Clean up admin.html
    $adminPath = "admin.html"
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)

    # Remove all backupData script blocks
    $adminContent = [regex]::Replace($adminContent, '(?s)function backupData\(\).*?function restoreData\(event\) \{.*?\};\s*reader\.readAsText\(file\);\s*\}', '')
    
    # Remove all references scripts
    $adminContent = [regex]::Replace($adminContent, '(?s)let referencesData = \[\];.*?loadReferencesData\(\);\s*\};?', '')
    $adminContent = [regex]::Replace($adminContent, '(?s)function renderAdminReferences\(\) \{.*?\};?', '')
    
    # Re-inject backupData and references correctly right before </body>
    $correctAdminScripts = @"
<script>
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
            tr.innerHTML = '<td><input type="text" class="form-input" value="' + item.title + '" onchange="updateReference(\'' + item.id + '\', \'title\', this.value)"></td>' +
                           '<td><input type="text" class="form-input" value="' + item.items + '" onchange="updateReference(\'' + item.id + '\', \'items\', this.value)"></td>' +
                           '<td><input type="text" class="form-input" value="' + item.date + '" onchange="updateReference(\'' + item.id + '\', \'date\', this.value)"></td>' +
                           '<td><button class="btn btn-outline" style="color:red;border-color:red" onclick="removeReference(\'' + item.id + '\')">삭제</button></td>';
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

    const originalInitAdmin = window.onload;
    window.onload = function() {
        if(originalInitAdmin) originalInitAdmin();
        loadReferencesData();
    };
</script>
</body>
"@

    $adminContent = [regex]::Replace($adminContent, '</body>', $correctAdminScripts)

    # Make sure we don't duplicate scripts if running again.
    # We stripped them out above so it should be fine.

    [System.IO.File]::WriteAllText($adminPath, $adminContent, [System.Text.Encoding]::UTF8)

    # 2. Clean up index.html
    $indexPath = "index.html"
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)

    # Remove bad date script
    $indexContent = [regex]::Replace($indexContent, '(?s)<script>\s*document\.addEventListener\(''DOMContentLoaded'', \(\) => \{\s*const dateSpan.*?\}\);\s*</script>', '')

    # Fix hero date ID and injection
    $dateScriptCorrect = @"
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const dateSpan = document.getElementById('heroDate');
        if(dateSpan) {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            dateSpan.textContent = yyyy + "." + mm + "." + dd + " 09:00 기준 완료";
        }
    });
</script>
</body>
"@
    $indexContent = [regex]::Replace($indexContent, '</body>', $dateScriptCorrect)

    # Fix fallback for REFERENCES
    $renderRefOld = 'const refs = PRODUCTS_DATA[''references''] || \[\];'
    $renderRefNew = @"
        let refs = [];
        const savedRefs = localStorage.getItem('yw_references_data');
        if (savedRefs) {
            try {
                const parsed = JSON.parse(savedRefs);
                if (parsed && parsed.length > 0) {
                    refs = parsed.map(item => ({
                        name: item.title,
                        spec: item.items,
                        unit: item.date
                    }));
                }
            } catch(e) {}
        }
        if (refs.length === 0) {
            refs = PRODUCTS_DATA['references'] || [];
        }
"@
    # Remove previous bad injected code from index.html if it exists
    $indexContent = [regex]::Replace($indexContent, '(?s)let refs = \[\];\s*const saved = localStorage\.getItem.*?if \(refs\.length === 0\) \{ refs = PRODUCTS_DATA\[.*?\] \|\| \[\]; \}', '')
    
    # Insert new correctly
    if ($indexContent -match 'const refs = PRODUCTS_DATA\[''references''\] \|\| \[\];') {
        $indexContent = [regex]::Replace($indexContent, 'const refs = PRODUCTS_DATA\[''references''\] \|\| \[\];', $renderRefNew)
    } elseif ($indexContent -match 'const refs = PRODUCTS_DATA\.references \|\| \[\];') {
        $indexContent = [regex]::Replace($indexContent, 'const refs = PRODUCTS_DATA\.references \|\| \[\];', $renderRefNew)
    }

    # Fix white-space: nowrap for calc-tab
    if (-not $indexContent.Contains("white-space: nowrap !important;")) {
        $indexContent = $indexContent.Replace(".calc-tab { white-space: normal;", ".calc-tab { white-space: nowrap !important;")
        $indexContent = $indexContent.Replace("white-space: normal !important;", "white-space: nowrap !important;")
    }

    # Ensure the syntax error is cleared if there's any remaining bad script.
    
    [System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)

    Write-Host "Hotfix 3 complete."
} catch {
    Write-Error $_.Exception.Message
}
