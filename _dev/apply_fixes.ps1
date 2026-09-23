$text = [System.IO.File]::ReadAllText("index.html", [System.Text.Encoding]::UTF8)

# 1. p9 syntax error
$text = $text.Replace("unit: '??, price:", "unit: '장', price:")

# 2. Hero Date Automation
$text = $text -replace 'window\.addEventListener\("DOMContentLoaded", \(\) => \{', "window.addEventListener(`"DOMContentLoaded`", () => {`r`n            const dateObj = new Date();`r`n            const yyyy = dateObj.getFullYear();`r`n            const mm = String(dateObj.getMonth() + 1).padStart(2, '0');`r`n            const dd = String(dateObj.getDate()).padStart(2, '0');`r`n            const heroDateEl = document.getElementById(`"heroDate`");`r`n            if(heroDateEl) heroDateEl.innerText = \``${yyyy}.\${mm}.\${dd} 09:00 기준 완료\``;"

# 3. REFERENCES fallback & SyntaxError
$oldRefRegex = "const\s+refs\.forEach\(ref => \{"
$newRef = "let refs = [];`r`n            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references');`r`n            if (stored) { try { refs = JSON.parse(stored); } catch(e){} }`r`n            if (!refs || refs.length === 0) { refs = [ { name: 'KCC / 하남시 지식산업센터', spec: 'KCC 석고보드 및 경량철골 자재 납품', unit: '2024.05' }, { name: '벽산 / 인천 검단 신도시 아파트', spec: '벽산 단열재 및 그라스울 대량 납품', unit: '2024.04' }, { name: '영림 / 서울 강남구 오피스 빌딩', spec: '영림 도어 및 인테리어 마감재 납품', unit: '2024.03' } ]; }`r`n            refs.forEach(ref => {"
$text = $text -replace $oldRefRegex, $newRef

# 4. Tab buttons nowrap
$text = $text.Replace(".calc-tab {`r`n            flex: 0 0 auto;", ".calc-tab {`r`n            white-space: nowrap;`r`n            flex: 0 0 auto;")
$text = $text.Replace(".calc-tab {`n            flex: 0 0 auto;", ".calc-tab {`n            white-space: nowrap;`n            flex: 0 0 auto;")

[System.IO.File]::WriteAllText("index.html", $text, [System.Text.Encoding]::UTF8)
