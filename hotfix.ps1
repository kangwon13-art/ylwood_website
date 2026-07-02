$ErrorActionPreference = 'Stop'

try {
    # 1. FIX INDEX.HTML
    $indexPath = "index.html"
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)

    # Task 2: Fix Date formatting (PadLeft -> padStart)
    $indexContent = $indexContent.Replace(".PadLeft(2, '0')", ".padStart(2, '0')")
    # Also fix the template literal issue if `${yyyy}` was replaced by empty string
    $indexContent = [regex]::Replace($indexContent, 'dateSpan\.textContent = `\.\. 09:00', 'dateSpan.textContent = `${yyyy}.${mm}.${dd} 09:00')
    $indexContent = [regex]::Replace($indexContent, 'dateSpan\.textContent = `\$\{yyyy\}\.\$\{mm\}\.\$\{dd\}', 'dateSpan.textContent = `${yyyy}.${mm}.${dd}')
    # Let's just replace the whole script block
    $badScript = 'dateSpan.textContent = `.. 09:00 기준 완료`;'
    $goodScript = 'dateSpan.textContent = `${yyyy}.${mm}.${dd} 09:00 기준 완료`;'
    $indexContent = $indexContent.Replace($badScript, $goodScript)

    # Task 3: Fix REFERENCES fallback and renderReferences syntax
    # First remove any old Antigravity references if we added them
    # But wait, we didn't add it to index.html last time!
    # Let's modify the EXISTING renderReferences() in index.html
    
    $oldRenderRef = @"
        function renderReferences() {
            const container = document.getElementById("referenceContainer");
            if (!container) return;
            container.innerHTML = "";
            const refs = PRODUCTS_DATA['references'] || [];
            
            refs.forEach(ref => {
"@

    $newRenderRef = @"
        function renderReferences() {
            const container = document.getElementById("referenceContainer");
            if (!container) return;
            container.innerHTML = "";
            
            // Antigravity: Load from localStorage or fallback
            let refs = [];
            const saved = localStorage.getItem('yw_references_data');
            if (saved) {
                try {
                    const parsed = JSON.parse(saved);
                    if (parsed && parsed.length > 0) {
                        // Map localStorage format to card format
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
            
            refs.forEach(ref => {
"@
    if ($indexContent.Contains($oldRenderRef)) {
        $indexContent = $indexContent.Replace($oldRenderRef, $newRenderRef)
    }

    # Task 4: calc-tab white-space nowrap
    # Find .calc-tab { ... white-space: normal; } and replace
    $indexContent = $indexContent.Replace("white-space: normal;", "white-space: nowrap;")
    $indexContent = $indexContent.Replace("white-space: normal !important;", "white-space: nowrap !important;")
    
    # Also in my injected CSS:
    # .category-card .category-name { font-size: 13px !important; text-align: center; margin-bottom: 0; }
    # wait, the tabs are `.calc-tab`. In index.html line 1530:
    # .calc-tab { white-space: normal; word-break: keep-all; }
    # Let's add CSS for the tabs specifically in our custom block or replace `white-space: normal`
    $cssFix = @"
            .calc-tab { white-space: nowrap !important; word-break: keep-all; font-size: 12px; padding: 4px; }
"@
    if (-not $indexContent.Contains("white-space: nowrap !important; word-break: keep-all; font-size: 12px;")) {
        $indexContent = $indexContent.Replace(".calc-tab { padding: 10px 18px;", "$cssFix`n            .calc-tab { padding: 10px 18px;")
        $indexContent = $indexContent.Replace(".calc-tab { aspect-ratio: 1 / 1;", ".calc-tab { aspect-ratio: 1 / 1; white-space: nowrap !important;")
    }

    [System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)


    # 2. FIX ADMIN.HTML SyntaxError
    $adminPath = "admin.html"
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)

    # Fix the broken template literal syntax
    $badLiteral1 = "value=`"``+item.title+```""
    $badLiteral2 = "value=`"``+item.items+```""
    $badLiteral3 = "value=`"``+item.date+```""
    $adminContent = $adminContent.Replace($badLiteral1, "value=`"`${item.title}`"")
    $adminContent = $adminContent.Replace($badLiteral2, "value=`"`${item.items}`"")
    $adminContent = $adminContent.Replace($badLiteral3, "value=`"`${item.date}`"")
    
    # Check if there's any other template literal breakage
    $adminContent = $adminContent.Replace("updateReference('``+item.id+``'", "updateReference('`${item.id}'")

    [System.IO.File]::WriteAllText($adminPath, $adminContent, [System.Text.Encoding]::UTF8)

    Write-Host "Hotfix complete."
} catch {
    Write-Error $_.Exception.Message
}
