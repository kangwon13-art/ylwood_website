$path = "index.html"
$lines = [System.IO.File]::ReadAllLines($path)

# 1. calc-tab nowrap (index 699)
$lines[699] = "        .calc-tab {`r`n            white-space: nowrap;"

# 2. heroDate span fix (index 1970)
$lines[1970] = "                        <span class=`"hero-stat-value font-num`" id=`"heroDate`">오늘 09:00 기준 완료</span>"

# 3. p9 (index 2602)
$lines[2602] = "                { id: 'p9', code: '', name: '4mm 4x8 일반합판', spec: '준내수 / 4x8 (1220x2440mm)', unit: '장', price: 17500 },"

# 4. renderReferences (index 2990, 2991, 2992)
$lines[2990] = "            let refs = [];"
$lines[2991] = "            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references'); if(stored) { try { refs = JSON.parse(stored); } catch(e){} } if(!refs || refs.length === 0) { refs = [ { name: 'KCC / 하남시 지식산업센터', spec: 'KCC 석고보드 및 경량철골 자재 납품', unit: '2024.05' }, { name: '벽산 / 인천 검단 신도시 아파트', spec: '벽산 단열재 및 그라스울 대량 납품', unit: '2024.04' }, { name: '영림 / 서울 강남구 오피스 빌딩', spec: '영림 도어 및 인테리어 마감재 납품', unit: '2024.03' } ]; }"
$lines[2992] = "            refs.forEach(ref => {"

# 5. heroDate JS Fix (index 3043)
$lines[3043] = '                heroDateEl.innerText = `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")} 09:00 기준 완료`;'

# 6. dateSpan JS Fix (index 3652)
$lines[3652] = '            dateSpan.textContent = yyyy + "." + mm + "." + dd + " 09:00 기준 완료";'

# Write UTF-8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($path, $lines, $utf8NoBom)
