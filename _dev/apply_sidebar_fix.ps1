# index.html 경로 설정
$path = "index.html"
$bytes = [System.IO.File]::ReadAllBytes($path)
$text = [System.Text.Encoding]::UTF8.GetString($bytes)

# 1. toggleMobileSidebar 함수에서 조건문 제거
$loosePattern = "(?s)function\s+toggleMobileSidebar\(\)\s*\{\s*if\s*\(\s*window\.innerWidth\s*<=\s*768\s*\)\s*\{\s*(.*?)\s*\}\s*\}"
if ($text -match $loosePattern) {
    # 내부 로직 추출해서 겉의 if문만 제거한 형태로 교체
    $inner = $Matches[1]
    # 인덴테이션 다듬기
    $newFunc = "function toggleMobileSidebar() {`r`n            $inner`r`n        }"
    $text = [regex]::Replace($text, $loosePattern, $newFunc)
    Write-Output "toggleMobileSidebar replaced."
} else {
    Write-Output "toggleMobileSidebar already replaced or not found."
}

# 2. PC용 CSS 추가 (중복 추가 방지)
if (-not $text.Contains("PC 버전 바텀시트 레이아웃")) {
    $pcCss = @"

        /* PC 버전 바텀시트 레이아웃 (하단 중앙 플로팅 배치) */
        @media (min-width: 769px) {
            .calc-sidebar {
                left: 50% !important;
                right: auto !important;
                bottom: 20px !important;
                transform: translateX(-50%) !important;
                width: 600px !important;
                max-width: calc(100% - 40px) !important;
                border: 1px solid var(--color-border) !important;
                border-radius: 16px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
                height: 66px;
                transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            .calc-sidebar.expanded {
                height: 560px !important;
                max-height: 75vh !important;
            }
            .summary-title {
                border-radius: 16px 16px 0 0 !important;
            }
        }
"@
    if ($text.Contains("</style>")) {
        $idx = $text.LastIndexOf("</style>")
        $text = $text.Substring(0, $idx) + $pcCss + "`r`n" + $text.Substring($idx)
        Write-Output "PC CSS added."
    }
} else {
    Write-Output "PC CSS already added."
}

# UTF-8 BOM 없음 인코딩 객체 생성 (New-Object 괄호 사용)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
Write-Output "Saved index.html successfully with UTF-8 (No BOM)."
