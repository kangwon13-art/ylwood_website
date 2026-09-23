# 파일 경로 설정
$path = "index.html"
$content = Get-Content -Raw -Encoding utf8 $path

# 1. toggleMobileSidebar 복원
$oldFunc = "function toggleMobileSidebar() {`r`n            const sidebar = document.getElementById(`"calcSidebar`");`r`n            if (sidebar) {`r`n                sidebar.classList.toggle(`"expanded`");`r`n            }`r`n        }"

$oldFuncLF = "function toggleMobileSidebar() {`n            const sidebar = document.getElementById(`"calcSidebar`");`n            if (sidebar) {`n                sidebar.classList.toggle(`"expanded`");`n            }`n        }"

$newFunc = "function toggleMobileSidebar() {`r`n            if (window.innerWidth <= 768) {`r`n                const sidebar = document.getElementById(`"calcSidebar`");`r`n                if (sidebar) {`r`n                    sidebar.classList.toggle(`"expanded`");`r`n                }`r`n            }`r`n        }"

$newFuncLF = "function toggleMobileSidebar() {`n            if (window.innerWidth <= 768) {`n                const sidebar = document.getElementById(`"calcSidebar`");`n                if (sidebar) {`n                    sidebar.classList.toggle(`"expanded`");`n                }`n            }`n        }"

if ($content.Contains($oldFunc)) {
    $content = $content.Replace($oldFunc, $newFunc)
    Write-Output "toggleMobileSidebar reverted to mobile-only (CRLF)."
} elseif ($content.Contains($oldFuncLF)) {
    $content = $content.Replace($oldFuncLF, $newFuncLF)
    Write-Output "toggleMobileSidebar reverted to mobile-only (LF)."
} else {
    # loose match
    $content = $content.Replace("function toggleMobileSidebar() {`r`n            const sidebar = document.getElementById(`"calcSidebar`");", "function toggleMobileSidebar() {`r`n            if (window.innerWidth <= 768) {`r`n                const sidebar = document.getElementById(`"calcSidebar`");")
    $content = $content.Replace("function toggleMobileSidebar() {`n            const sidebar = document.getElementById(`"calcSidebar`");", "function toggleMobileSidebar() {`n            if (window.innerWidth <= 768) {`n                const sidebar = document.getElementById(`"calcSidebar`");")
    # 닫는 괄호 복구
    $content = $content.Replace("if (sidebar) {`r`n                sidebar.classList.toggle(`"expanded`");`r`n            }`r`n        }", "if (sidebar) {`r`n                    sidebar.classList.toggle(`"expanded`");`r`n                }`r`n            }`r`n        }")
    $content = $content.Replace("if (sidebar) {`n                sidebar.classList.toggle(`"expanded`");`n            }`n        }", "if (sidebar) {`n                    sidebar.classList.toggle(`"expanded`");`n                }`n            }`n        }")
}

# 2. PC 버전 CSS 복원
$pcCssOld = @"
        /* PC Version Bottomsheet Layout */
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

$pcCssNew = @"
        /* PC Version: Restore to Right Sidebar layout (No Bottomsheet, No Slide-up) */
        @media (min-width: 769px) {
            .calc-container {
                display: grid !important;
                grid-template-columns: 1fr 340px !important;
                gap: 30px !important;
                align-items: start !important;
                margin-bottom: 0 !important;
            }
            .calc-sidebar {
                position: sticky !important;
                top: 100px !important;
                bottom: auto !important;
                left: auto !important;
                right: auto !important;
                width: 100% !important;
                height: auto !important;
                max-height: calc(100vh - 140px) !important;
                border-radius: 20px !important;
                border: 1px solid var(--color-border) !important;
                box-shadow: var(--shadow-premium) !important;
                overflow: hidden !important;
                display: flex !important;
                flex-direction: column !important;
                z-index: 10 !important;
                transform: none !important;
            }
            .calc-sidebar.expanded {
                height: auto !important;
            }
            .calc-sidebar .sidebar-inner-content {
                overflow-y: auto !important;
                max-height: calc(100vh - 240px) !important;
                padding: 24px !important;
                display: block !important;
            }
            .sidebar-toggle-arrow {
                display: none !important;
            }
            .summary-title {
                border-radius: 20px 20px 0 0 !important;
                cursor: default !important;
                padding: 20px !important;
                text-align: left !important;
            }
        }
"@

$pcCssOldLF = $pcCssOld.Replace("`r`n", "`n")
$pcCssNewLF = $pcCssNew.Replace("`r`n", "`n")

if ($content.Contains($pcCssOld)) {
    $content = $content.Replace($pcCssOld, $pcCssNew)
    Write-Output "PC CSS layout restored (CRLF)."
} elseif ($content.Contains($pcCssOldLF)) {
    $content = $content.Replace($pcCssOldLF, $pcCssNewLF)
    Write-Output "PC CSS layout restored (LF)."
} else {
    Write-Warning "PC CSS block template not found by exact string. Attempting fallback replace."
    # If the user's files have minor spacing variations, replace based on style tag end
    $content = $content.Replace("</style>", $pcCssNew + "`r`n</style>")
}

# UTF-8 BOM 없음으로 저장
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $content, $utf8)
Write-Output "Restore script run complete."
