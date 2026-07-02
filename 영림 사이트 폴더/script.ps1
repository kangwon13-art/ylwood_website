$path = 'C:\Users\1\Desktop\영림\영림우드 자료\영림 사이트 폴더\index.html'
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# TASK 1
$content = $content.Replace(".hero-desc {`r`n            font-size: 18px;", ".hero-desc {`r`n            font-size: 20px;")
$content = $content.Replace(".hero-desc {`n            font-size: 18px;", ".hero-desc {`n            font-size: 20px;")

$content = $content.Replace(".section-desc {`r`n            font-size: 16px;", ".section-desc {`r`n            font-size: 18px;")
$content = $content.Replace(".section-desc {`n            font-size: 16px;", ".section-desc {`n            font-size: 18px;")

$content = $content.Replace(".category-description {`r`n            font-size: 14px;", ".category-description {`r`n            font-size: 16px;")
$content = $content.Replace(".category-description {`n            font-size: 14px;", ".category-description {`n            font-size: 16px;")

$content = $content.Replace(".faq-content {`r`n            padding: 0 24px 24px 44px;`r`n            font-size: 14px;`r`n            color: var(--color-text-muted);`r`n            line-height: 1.7;", ".faq-content {`r`n            padding: 0 24px 24px 44px;`r`n            font-size: 16px;`r`n            color: var(--color-text-muted);`r`n            line-height: 1.8;")
$content = $content.Replace(".faq-content {`n            padding: 0 24px 24px 44px;`n            font-size: 14px;`n            color: var(--color-text-muted);`n            line-height: 1.7;", ".faq-content {`n            padding: 0 24px 24px 44px;`n            font-size: 16px;`n            color: var(--color-text-muted);`n            line-height: 1.8;")

$content = $content.Replace("footer {`r`n            background-color: #050811;`r`n            padding: 60px 0 100px;`r`n            border-top: 1px solid var(--color-border);`r`n            font-size: 13px;", "footer {`r`n            background-color: #050811;`r`n            padding: 60px 0 100px;`r`n            border-top: 1px solid var(--color-border);`r`n            font-size: 14px;")
$content = $content.Replace("footer {`n            background-color: #050811;`n            padding: 60px 0 100px;`n            border-top: 1px solid var(--color-border);`n            font-size: 13px;", "footer {`n            background-color: #050811;`n            padding: 60px 0 100px;`n            border-top: 1px solid var(--color-border);`n            font-size: 14px;")

$content = $content.Replace(".footer-details {`r`n            line-height: 1.8;`r`n        }", ".footer-details {`r`n            font-size: 14px;`r`n            line-height: 1.8;`r`n        }")
$content = $content.Replace(".footer-details {`n            line-height: 1.8;`n        }", ".footer-details {`n            font-size: 14px;`n            line-height: 1.8;`n        }")

$content = $content.Replace(".price-table td {`r`n            padding: 16px;`r`n            border-bottom: 1px solid var(--color-border);`r`n            font-size: 14px;", ".price-table td {`r`n            padding: 16px;`r`n            border-bottom: 1px solid var(--color-border);`r`n            font-size: 15px;")
$content = $content.Replace(".price-table td {`n            padding: 16px;`n            border-bottom: 1px solid var(--color-border);`n            font-size: 14px;", ".price-table td {`n            padding: 16px;`n            border-bottom: 1px solid var(--color-border);`n            font-size: 15px;")

$content = $content.Replace(".prod-spec {`r`n            font-size: 12px;", ".prod-spec {`r`n            font-size: 14px;")
$content = $content.Replace(".prod-spec {`n            font-size: 12px;", ".prod-spec {`n            font-size: 14px;")

$content = $content.Replace("<span class=`"prod-spec`" style=`"font-size:13px; color: var(--color-text-muted);`">`${item.spec}</span>", "<span class=`"prod-spec`" style=`"font-size:14px; color: var(--color-text-muted);`">`${item.spec}</span>")

[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
