$path = "index.html"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Fix 1: p9 error
$content = $content -replace "unit: '\?\?, price:", "unit: '장', price:"

# Fix 2: tab-btn
$content = $content.Replace(".calc-tab {`r`n            flex: 0 0 auto;", ".calc-tab {`r`n            white-space: nowrap;`r`n            flex: 0 0 auto;")
$content = $content.Replace(".calc-tab {`n            flex: 0 0 auto;", ".calc-tab {`n            white-space: nowrap;`n            flex: 0 0 auto;")

# Fix 3: REFERENCES fallback
$oldRef = "const `r`n            `r`n            refs.forEach(ref => {"
$newRef = "let refs = [];`r`n            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references');`r`n            if (stored) { try { refs = JSON.parse(stored); } catch(e){} }`r`n            if (!refs || refs.length === 0) { refs = [ { name: 'KCC / 하남시 지식산업센터', spec: 'KCC 석고보드 및 경량철골 자재 납품', unit: '2024.05' }, { name: '벽산 / 인천 검단 신도시 아파트', spec: '벽산 단열재 및 그라스울 대량 납품', unit: '2024.04' }, { name: '영림 / 서울 강남구 오피스 빌딩', spec: '영림 도어 및 인테리어 마감재 납품', unit: '2024.03' } ]; }`r`n            refs.forEach(ref => {"
$content = $content.Replace($oldRef, $newRef)

$oldRef2 = "const `n            `n            refs.forEach(ref => {"
$newRef2 = "let refs = [];`n            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references');`n            if (stored) { try { refs = JSON.parse(stored); } catch(e){} }`n            if (!refs || refs.length === 0) { refs = [ { name: 'KCC / 하남시 지식산업센터', spec: 'KCC 석고보드 및 경량철골 자재 납품', unit: '2024.05' }, { name: '벽산 / 인천 검단 신도시 아파트', spec: '벽산 단열재 및 그라스울 대량 납품', unit: '2024.04' }, { name: '영림 / 서울 강남구 오피스 빌딩', spec: '영림 도어 및 인테리어 마감재 납품', unit: '2024.03' } ]; }`n            refs.forEach(ref => {"
$content = $content.Replace($oldRef2, $newRef2)

# Fix 4: Hero Date
$oldDate = "window.addEventListener('DOMContentLoaded', () => {"
$oldDate2 = 'window.addEventListener("DOMContentLoaded", () => {'
$newDate = 'window.addEventListener("DOMContentLoaded", () => {' + "`r`n            const dateObj = new Date();`r`n            const yyyy = dateObj.getFullYear();`r`n            const mm = String(dateObj.getMonth() + 1).padStart(2, '0');`r`n            const dd = String(dateObj.getDate()).padStart(2, '0');`r`n            const heroDateEl = document.getElementById(`"heroDate`");`r`n            if(heroDateEl) heroDateEl.innerText = yyyy + '.' + mm + '.' + dd + ' 09:00 기준 완료';"
$content = $content.Replace($oldDate, $newDate)
$content = $content.Replace($oldDate2, $newDate)

[System.IO.File]::WriteAllBytes($path, [System.Text.Encoding]::UTF8.GetBytes($content))
