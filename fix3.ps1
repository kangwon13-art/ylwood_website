$lines = Get-Content -Path "index.html" -Encoding UTF8
$outLines = @()
$inRefBlock = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]

    # Fix 1: p9 syntax error
    if ($line -match "id: 'p9'" -and $line -match "17500") {
        $outLines += "                { id: 'p9', code: '', name: '4mm 4x8 일반합판', spec: '준내수 / 4x8 (1220x2440mm)', unit: '장', price: 17500 },"
        continue
    }

    # Fix 2: tab-btn
    if ($line -match "^\s*\.calc-tab\s*\{$") {
        $outLines += $line
        $outLines += "            white-space: nowrap;"
        continue
    }

    # Fix 3: REFERENCES fallback
    if ($line.Trim() -eq "const" -and $i -gt 2500) {
        $outLines += "            let refs = [];"
        $outLines += "            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references');"
        $outLines += "            if(stored) { try { refs = JSON.parse(stored); } catch(e){} }"
        $outLines += "            if(!refs || refs.length === 0) { refs = [ { name: 'KCC / 하남시 지식산업센터', spec: 'KCC 석고보드 및 경량철골 자재 납품', unit: '2024.05' }, { name: '벽산 / 인천 검단 신도시 아파트', spec: '벽산 단열재 및 그라스울 대량 납품', unit: '2024.04' }, { name: '영림 / 서울 강남구 오피스 빌딩', spec: '영림 도어 및 인테리어 마감재 납품', unit: '2024.03' } ]; }"
        $inRefBlock = $true
        continue
    }
    if ($inRefBlock) {
        if ($line.Trim() -eq "") {
            continue
        }
        if ($line -match "refs\.forEach") {
            $inRefBlock = $false
            $outLines += $line
        }
        continue
    }

    # Fix 4: Hero Date
    if ($line -match 'window\.addEventListener\("DOMContentLoaded"') {
        $outLines += $line
        $outLines += "            const dateObj = new Date();"
        $outLines += "            const yyyy = dateObj.getFullYear();"
        $outLines += "            const mm = String(dateObj.getMonth() + 1).padStart(2, '0');"
        $outLines += "            const dd = String(dateObj.getDate()).padStart(2, '0');"
        $outLines += "            const heroDateEl = document.getElementById(`"heroDate`");"
        $outLines += "            if(heroDateEl) heroDateEl.innerText = \``${yyyy}.\${mm}.\${dd} 09:00 기준 완료\``;"
        continue
    }

    $outLines += $line
}

Set-Content -Path "index.html" -Value $outLines -Encoding UTF8
