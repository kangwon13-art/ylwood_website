# 파일 경로 설정
$path = "index.html"
$bytes = [System.IO.File]::ReadAllBytes($path)
$text = [System.Text.Encoding]::UTF8.GetString($bytes)

# CRLF/LF 정규화하여 교체 대상 준비
$targetFunc = "function toggleMobileSidebar() {`r`n            if (window.innerWidth <= 768) {`r`n                const sidebar = document.getElementById(`"calcSidebar`");`r`n                if (sidebar) {`r`n                    sidebar.classList.toggle(`"expanded`");`r`n                }`r`n            }`r`n        }"

$replacementFunc = "function toggleMobileSidebar() {`r`n            const sidebar = document.getElementById(`"calcSidebar`");`r`n            if (sidebar) {`r`n                sidebar.classList.toggle(`"expanded`");`r`n            }`r`n        }"

# LF 개행 버전도 준비
$targetFuncLF = $targetFunc.Replace("`r`n", "`n")
$replacementFuncLF = $replacementFunc.Replace("`r`n", "`n")

if ($text.Contains($targetFunc)) {
    $text = $text.Replace($targetFunc, $replacementFunc)
    Write-Output "Replaced CRLF version."
} elseif ($text.Contains($targetFuncLF)) {
    $text = $text.Replace($targetFuncLF, $replacementFuncLF)
    Write-Output "Replaced LF version."
} else {
    # 단순화된 찾기
    Write-Output "Using simplified replace."
    $text = $text.Replace("if (window.innerWidth <= 768) {`r`n                const sidebar = document.getElementById(`"calcSidebar`");`r`n                if (sidebar) {`r`n                    sidebar.classList.toggle(`"expanded`");`r`n                }`r`n            }", "const sidebar = document.getElementById(`"calcSidebar`");`r`n            if (sidebar) {`r`n                sidebar.classList.toggle(`"expanded`");`r`n            }")
    $text = $text.Replace("if (window.innerWidth <= 768) {`n                const sidebar = document.getElementById(`"calcSidebar`");`n                if (sidebar) {`n                    sidebar.classList.toggle(`"expanded`");`n}`n            }", "const sidebar = document.getElementById(`"calcSidebar`");`n            if (sidebar) {`n                sidebar.classList.toggle(`"expanded`");`n            }")
}

# CSS 주석이 깨져 보였던 부분 보정
$text = $text.Replace("/* PC 踰꾩쟾 諛뷀??쒗듃 ?덉씠?꾩썐 (?섎떒 以묒븰 ?뚮줈??諛곗튂) */", "/* PC Version Bottomsheet Layout */")

# UTF-8 BOM 없음으로 저장
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
Write-Output "Saved successfully."
