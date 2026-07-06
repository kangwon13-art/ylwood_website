$path = "index.html"
$bytes = [System.IO.File]::ReadAllBytes($path)
$text = [System.Text.Encoding]::UTF8.GetString($bytes)
$lines2 = $text -split "`r?`n"

# --- Unicode helpers ---
$mok = [string]::Join('', [char[]](0xBAA9, 0xC7AC))         # 목재
$gu  = [string]::Join('', [char[]](0xAD6C, 0xC870, 0xC7AC)) # 구조재
$bang = [string]::Join('', [char[]](0xBC29, 0xBD80, 0xBAA9)) # 방부목
$tuksu = [string]::Join('', [char[]](0xD2B9, 0xC218, 0xBAA9)) # 특수목
$hap = [string]::Join('', [char[]](0xD569, 0xC131, 0xBAA9)) # 합성목
$cheol = [string]::Join('', [char[]](0xCCA0, 0xBB3C))        # 철물
$bu   = [string]::Join('', [char[]](0xBD80, 0xC790, 0xC7AC)) # 부자재
$ruba = [string]::Join('', [char[]](0xB8E8, 0xBC14))         # 루바
$jib  = [string]::Join('', [char[]](0xC9D1, 0xC131, 0xD310)) # 집성판

# ---------- FIX 1 & 2: Replace <br> in category cards and calc tabs ----------
# Line 2082: category card "목재<br>구조재"  -> "목재/구조재"
$lines2[2082] = "                        <h3 class=`"category-name`">$mok/$gu</h3>"

# Line 2139: category card "방부목<br>특수목" -> "방부목/특수목/합성목"
$lines2[2139] = "                        <h3 class=`"category-name`">$bang/$tuksu/$hap</h3>"

# Line 2158: category card "철물<br>부자재" -> "철물/부자재"
$lines2[2158] = "                        <h3 class=`"category-name`">$cheol/$bu</h3>"

# Line 2212: calc tab "목재<br>구조재" -> "목재/구조재"
$lines2[2212] = "                            <button class=`"calc-tab`" onclick=`"switchCalcTab('timber')`" id=`"tab-timber`">$mok/$gu</button>"

# Line 2217: calc tab "방부목<br>특수목" -> "방부목/특수목"
$lines2[2217] = "                                id=`"tab-deck_timber`">$bang/$tuksu</button>"

# Line 2221: calc tab "철물<br>부자재" -> "철물/부자재"
$lines2[2221] = "                                id=`"tab-hardware`">$cheol/$bu</button>"

# ---------- FIX 3: Insert 루바/집성판 category card after 방부목 card (after line 2148) ----------
$newCard = @(
    "                <!-- 8.5. 루바/집성판 -->",
    "                <div class=`"category-card`" onclick=`"selectCategoryAndScroll('louver_wood')`">",
    "                    <div class=`"category-icon-wrap`">",
    "                        <svg viewBox=`"0 0 24 24`">",
    "                            <path d=`"M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z`" />",
    "                        </svg>",
    "                    </div>",
    "                    <div class=`"category-card-body`">",
    "                        <h3 class=`"category-name`">$ruba/$jib</h3>",
    "                        <p class=`"category-description`">루바, 집성판, 각종 폭판 등 인테리어 마감 및 목공 전용 목재 자재 전문 공급.</p>",
    "                    </div>",
    "                    <div class=`"category-footer-link`">",
    "                        단가 확인 및 견적 산출",
    "                        <svg viewBox=`"0 0 24 24`">",
    "                            <path d=`"M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z`" />",
    "                        </svg>",
    "                    </div>",
    "                </div>"
)

# Insert after index 2148 (0-based: line 2149 in 1-based, which is after the closing </div> of deck_timber card)
$before = $lines2[0..2148]
$after  = $lines2[2149..($lines2.Count - 1)]
$lines2 = $before + $newCard + $after

# ---------- Save UTF-8 no BOM ----------
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($path, $lines2, $utf8NoBom)
Write-Output "Done"
