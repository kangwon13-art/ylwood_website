$path = "index.html"
$lines = [System.IO.File]::ReadAllLines($path)

# Mappings (Unicode representations)
$yoko = [string]::Join('', [char[]](0xC694, 0xAF2C, 0xD569, 0xD310))
$ojingeo = [string]::Join('', [char[]](0xC624, 0xC9D5, 0xC5B4, 0xD569, 0xD310))
$jang = [char]0xC7A5
$plaster_bond = [string]::Join('', [char[]](0xC11D, 0xACE0, 0xBCF8, 0xB4DC))
$po = [char]0xD3EC
$kijun_wanryo = [string]::Join('', [char[]](0xAE30, 0xC900, 0x0020, 0xC644, 0xB8CC))
$today = [string]::Join('', [char[]](0xC624, 0xB298))
$normal_hap = [string]::Join('', [char[]](0xC77C, 0xBC18, 0xD569, 0xD310))
$jun_naesu = [string]::Join('', [char[]](0xC900, 0xB0B4, 0xC218))

$hanam_jisan = [string]::Join('', [char[]](0xD558, 0xB0A8, 0xC2DC, 0x0020, 0xC9C0, 0xC2DD, 0xC0B0, 0xC5C5, 0xC13C, 0xD130))
$plaster_glasswool = [string]::Join('', [char[]](0xC11D, 0xACE0, 0xBCF4, 0xB4DC, 0x0020, 0xBC0F, 0x0020, 0xACBD, 0xB7C9, 0xCCA0, 0xACE8, 0x0020, 0xC790, 0xC7AC, 0x0020, 0xB0A9, 0xD488))
$incheon_geomdan = [string]::Join('', [char[]](0xC778, 0xCC9C, 0x0020, 0xAC80, 0xB2E8, 0x0020, 0xC2E0, 0xB3C4, 0xC2DC, 0x0020, 0xC544, 0xD30C, 0xD2B8))
$danryeol_glasswool = [string]::Join('', [char[]](0xB2E8, 0xC5F4, 0xC7AC, 0x0020, 0xBC0F, 0x0020, 0xADF8, 0xB77C, 0xC2A4, 0xC6B8, 0x0020, 0xB300, 0xB7C9, 0x0020, 0xB0A9, 0xD488))
$seoul_gangnam = [string]::Join('', [char[]](0xC11C, 0xC6B8, 0x0020, 0xAC15, 0xB0A8, 0xAD6C, 0x0020, 0xC624, 0xD53C, 0xC2A4, 0x0020, 0xBE4C, 0xB529))
$door_interior = [string]::Join('', [char[]](0xB3C4, 0xC5B4, 0x0020, 0xBC0F, 0x0020, 0xC778, 0xD14C, 0xB9AC, 0xC5B4, 0x0020, 0xB9C8, 0xAC10, 0xC7AC, 0x0020, 0xB0A9, 0xD488))

# New references fixes
$byeoksan = [string]::Join('', [char[]](0xBCBD, 0xC0B0))
$youngrim = [string]::Join('', [char[]](0xC601, 0xB9BC))

$outLines = New-Object System.Collections.Generic.List[string]
$inRefBlock = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]

    # 1. calc-tab nowrap
    if ($line -match '^\s*\.calc-tab\s*\{$') {
        $outLines.Add($line)
        $outLines.Add("            white-space: nowrap;")
        continue
    }

    # 2. heroDate span fix
    if ($line -match 'id="heroDate"' -and $line -match '<span') {
        $outLines.Add("                        <span class=`"hero-stat-value font-num`" id=`"heroDate`">$today 09:00 $kijun_wanryo</span>")
        continue
    }

    # 3. p9 (we explicitly check that it contains "id: 'p9'" and does NOT contain "ip9")
    if ($line -match 'id:\s*''p9''') {
        $outLines.Add("                { id: 'p9', code: '', name: '4mm 4x8 $yoko', spec: '$ojingeo / 4x8 (1220x2440mm)', unit: '$jang', price: 17500 },")
        continue
    }

    # 4. pl6
    if ($line -match 'id:\s*''pl6''') {
        $outLines.Add("                { id: 'pl6', code: '', name: '$plaster_bond', spec: '-', unit: '$po (25kg)', price: 12100 },")
        continue
    }

    # 5. renderReferences syntax error and fallback
    if ($line -match '^\s*const\s*$' -and $i -gt 2900 -and $i -lt 3000) {
        $outLines.Add("            let refs = [];")
        $outLines.Add("            const stored = localStorage.getItem('youngrim_admin_references') || localStorage.getItem('youngrim_references'); if(stored) { try { refs = JSON.parse(stored); } catch(e){} } if(!refs || refs.length === 0) { refs = [ { name: 'KCC / $hanam_jisan', spec: '$plaster_glasswool', unit: '2024.05' }, { name: '$byeoksan / $incheon_geomdan', spec: '$danryeol_glasswool', unit: '2024.04' }, { name: '$youngrim / $seoul_gangnam', spec: '$door_interior', unit: '2024.03' } ]; }")
        $inRefBlock = $true
        continue
    }
    if ($inRefBlock) {
        if ($line.Trim() -eq "") {
            continue
        }
        if ($line -match "refs\.forEach") {
            $inRefBlock = $false
            $outLines.Add($line)
        }
        continue
    }

    # 6. heroDate JS Fix
    if ($line -match 'heroDateEl\.innerText\s*=') {
        $outLines.Add('                heroDateEl.innerText = `' + '${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")} 09:00 ' + $kijun_wanryo + '`;')
        continue
    }

    # 7. dateSpan JS Fix
    if ($line -match 'dateSpan\.textContent\s*=') {
        $outLines.Add('            dateSpan.textContent = yyyy + "." + mm + "." + dd + " 09:00 ' + $kijun_wanryo + '";')
        continue
    }

    $outLines.Add($line)
}

# Save as UTF-8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($path, $outLines, $utf8NoBom)
Write-Output "Done"
