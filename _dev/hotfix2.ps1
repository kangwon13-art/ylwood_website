$ErrorActionPreference = 'Stop'

try {
    # 2. FIX ADMIN.HTML SyntaxError
    $adminPath = "admin.html"
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)

    # Completely replace the broken renderAdminReferences function
    $pattern = 'function renderAdminReferences\(\)\s*\{[\s\S]*?tbody\.appendChild\(tr\);\s*\}\);?\s*\}'
    $fixedRender = @"
        function renderAdminReferences() {
            const tbody = document.querySelector('#table-references tbody');
            if (!tbody) return;
            tbody.innerHTML = '';
            referencesData.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><input type="text" class="form-input" value="` + item.title + `" onchange="updateReference('` + item.id + `', 'title', this.value)"></td>
                    <td><input type="text" class="form-input" value="` + item.items + `" onchange="updateReference('` + item.id + `', 'items', this.value)"></td>
                    <td><input type="text" class="form-input" value="` + item.date + `" onchange="updateReference('` + item.id + `', 'date', this.value)"></td>
                    <td><button class="btn btn-outline" style="color:red;border-color:red" onclick="removeReference('` + item.id + `')">삭제</button></td>
                `;
                tbody.appendChild(tr);
            });
        }
"@

    # In javascript, template literal strings inside template literal is bad. We can just use standard JS concatenation or template literal with ${}
    $fixedRender = @"
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
"@

    $adminContent = [regex]::Replace($adminContent, $pattern, $fixedRender)
    [System.IO.File]::WriteAllText($adminPath, $adminContent, [System.Text.Encoding]::UTF8)

    # 1. FIX INDEX.HTML renderReferences fallback
    $indexPath = "index.html"
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)
    
    $indexPattern = 'function renderReferences\(\)\s*\{[\s\S]*?\}'
    # wait, there's multiple closing braces. We better replace the inner contents.
    
    $indexContent = $indexContent.Replace('refs = PRODUCTS_DATA[''references''] || [];', 
        "let refs = []; 
        const saved = localStorage.getItem('yw_references_data');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (parsed && parsed.length > 0) {
                    refs = parsed.map(item => ({ name: item.title, spec: item.items, unit: item.date }));
                }
            } catch(e) {}
        }
        if (refs.length === 0) { refs = PRODUCTS_DATA['references'] || []; }")
        
    [System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)

    Write-Host "Hotfix 2 complete."
} catch {
    Write-Error $_.Exception.Message
}
