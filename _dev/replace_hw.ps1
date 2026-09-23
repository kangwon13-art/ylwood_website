$newHw = Get-Content "new_hardware.txt" -Raw

$indexPath = "index.html"
$indexContent = Get-Content $indexPath -Raw
$indexContent = [regex]::Replace($indexContent, '            hardware: \[(?s).*?\],', $newHw)
$indexContent | Set-Content $indexPath -Encoding UTF8

$adminPath = "admin.html"
$adminContent = Get-Content $adminPath -Raw
$adminContent = [regex]::Replace($adminContent, '            hardware: \[(?s).*?\],', $newHw)
$adminContent | Set-Content $adminPath -Encoding UTF8
