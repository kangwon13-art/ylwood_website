 = Get-Content "hardware_lines.txt" | ForEach-Object { $_.Trim() }
 = $lines | Where-Object { $_ -notmatch "'h88'" }
 = $lines | ForEach-Object { $_ -replace ",$","" }

 = @(23..32) + @(59..64) + @(89..102) + @(107) + @(108..110)
 = New-Object System.Collections.Generic.HashSet[int]
foreach ($p in $preserve) { $preserveSet.Add($p) | Out-Null }

 = @{}
foreach ($line in $lines) {
    if ($line -match "id: 'h(\d+)'") {
        $idNum = [int]$matches[1]
        if (-not $preserveSet.Contains($idNum)) {
            $line = $line -replace "spec: '[^']*'", "spec: '-'"
        }
        $items[$idNum] = $line
    }
}

 = @(4, 5, 1, 2, 3, 6)
 = @()

foreach ($id in $orderedIds) {
    if ($items.ContainsKey($id)) {
        $output += $items[$id]
        $items.Remove($id)
    }
}

 = $items.Keys | Sort-Object
foreach ($k in $remainingKeys) {
    $output += $items[$k]
}

$result = "            hardware: [
                " + ($output -join ",
                ") + "
            ],"
$result | Set-Content "new_hardware.txt" -Encoding UTF8
