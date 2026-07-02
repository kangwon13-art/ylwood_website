$lines = Get-Content "hardware_lines.txt" | ForEach-Object { $_.Trim() }
$lines = $lines | Where-Object { $_ -notmatch "'h88'" }
$lines = $lines | ForEach-Object { $_ -replace ",$","" }

$preserve = @(23..32) + @(59..64) + @(89..102) + @(107) + @(108..110)
$preserveSet = New-Object System.Collections.Generic.HashSet[int]
foreach ($p in $preserve) { $preserveSet.Add($p) | Out-Null }

$items = @{}
foreach ($line in $lines) {
    if ($line -match "id: 'h(\d+)'") {
        $idNum = [int]$matches[1]
        if (-not $preserveSet.Contains($idNum)) {
            $line = $line -replace "spec: '[^']*'", "spec: '-'"
        }
        $items[$idNum] = $line
    }
}

$orderedIds = @(4, 5, 1, 2, 3, 6)
$output = @()

foreach ($id in $orderedIds) {
    if ($items.ContainsKey($id)) {
        $output += $items[$id]
        $items.Remove($id)
    }
}

$remainingKeys = $items.Keys | Sort-Object
foreach ($k in $remainingKeys) {
    $output += $items[$k]
}

$result = "            hardware: [`n                " + ($output -join ",`n                ") + "`n            ],"
$result | Set-Content "new_hardware.txt" -Encoding UTF8
