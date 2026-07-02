$ErrorActionPreference = 'Stop'

try {
    # 1. Modify index.html
    $indexPath = "index.html"
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)

    # TASKS 2 & 3: Hardware Array (index.html)
    if ($indexContent -match 'hardware:\s*\[([\s\S]*?)\]') {
        $hwStr = $matches[1]
        $pattern = '(\{\s*id:\s*''(.*?)'',\s*code:\s*''.*?'',\s*name:\s*''.*?'',\s*spec:\s*''(.*?)'',\s*unit:\s*''.*?'',\s*price:\s*\d+(?:,\s*sub:\s*''.*?'')?\s*\})'
        $hwMatches = [regex]::Matches($hwStr, $pattern)
        
        $hwDict = @{}
        foreach ($m in $hwMatches) {
            $itemFull = $m.Groups[1].Value
            $itemId = $m.Groups[2].Value
            $itemSpec = $m.Groups[3].Value
            
            $num = -1
            if ($itemId.StartsWith('h')) {
                [int]::TryParse($itemId.Substring(1), [ref]$num) | Out-Null
            }
            
            $keepSpec = $false
            if ($num -ge 23 -and $num -le 32) { $keepSpec = $true }
            if ($num -ge 59 -and $num -le 64) { $keepSpec = $true }
            if ($num -ge 89 -and $num -le 102) { $keepSpec = $true }
            if ($num -eq 107) { $keepSpec = $true }
            if ($num -ge 108 -and $num -le 110) { $keepSpec = $true }
            
            if (-not $keepSpec) {
                $itemFull = $itemFull.Replace("spec: '$itemSpec'", "spec: '-'")
            }
            $hwDict[$itemId] = $itemFull
        }

        $newHwList = New-Object System.Collections.Generic.List[string]
        
        # 3-2 Order
        $order = @('h4', 'h5', 'h1', 'h2', 'h3', 'h6')
        foreach ($id in $order) {
            if ($hwDict.Contains($id)) {
                $newHwList.Add($hwDict[$id])
                $hwDict.Remove($id)
            }
        }
        
        # 3-3 Remaining and remove h88
        foreach ($m in $hwMatches) {
            $id = $m.Groups[2].Value
            if ($hwDict.Contains($id) -and $id -ne 'h88') {
                $newHwList.Add($hwDict[$id])
                $hwDict.Remove($id)
            }
        }
        
        $newHwStr = [string]::Join(",`r`n                    ", $newHwList)
        $indexContent = $indexContent.Replace($hwStr, "`r`n                    " + $newHwStr + "`r`n                ")
        # Handle cases where line endings differ
        if ($indexContent.IndexOf($hwStr) -eq -1) {
             $indexContent = $indexContent.Replace($hwStr, "`n                    " + $newHwStr + "`n                ")
        }
    }

    # Insulation Array (index.html)
    if ($indexContent -match 'insulation:\s*\[([\s\S]*?)\]') {
        $insStr = $matches[1]
        $pattern = '(\{\s*id:\s*''(.*?)'',\s*code:\s*''.*?'',\s*name:\s*''.*?'',\s*spec:\s*''(.*?)'',\s*unit:\s*''.*?'',\s*price:\s*\d+(?:,\s*sub:\s*''.*?'')?\s*\})'
        $insMatches = [regex]::Matches($insStr, $pattern)
        
        $insDict = @{}
        foreach ($m in $insMatches) {
            $insDict[$m.Groups[2].Value] = $m.Groups[1].Value
        }
        
        if (-not $insDict.Contains('h88')) {
            $insDict['h88'] = "{ id: 'h88', code: '', name: '충진재 50T', spec: '50x450x1000mm', unit: '장', price: 2000 }"
        }
        
        $insOrder = @('i3', 'i4', 'i7', 'i8', 'i9', 'i15', 'i16', 'i17', 'i18', 'i11', 'i12', 'i13', 'i14', 'i1', 'i2', 'i10', 'h88')
        $newInsList = New-Object System.Collections.Generic.List[string]
        
        foreach ($id in $insOrder) {
            if ($insDict.Contains($id)) {
                $newInsList.Add($insDict[$id])
            }
        }
        
        $newInsStr = [string]::Join(",`r`n                    ", $newInsList)
        $indexContent = [regex]::Replace($indexContent, 'insulation:\s*\[([\s\S]*?)\]', "insulation: [`r`n                    $newInsStr`r`n                ]")
    }

    [System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)

    # 2. Modify admin.html (same logic)
    $adminPath = "admin.html"
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)

    if ($adminContent -match 'hardware:\s*\[([\s\S]*?)\]') {
        $hwStr = $matches[1]
        $pattern = '(\{\s*id:\s*''(.*?)'',\s*code:\s*''.*?'',\s*name:\s*''.*?'',\s*spec:\s*''(.*?)'',\s*unit:\s*''.*?'',\s*price:\s*\d+(?:,\s*sub:\s*''.*?'')?\s*\})'
        $hwMatches = [regex]::Matches($hwStr, $pattern)
        
        $hwDict = @{}
        foreach ($m in $hwMatches) {
            $itemFull = $m.Groups[1].Value
            $itemId = $m.Groups[2].Value
            $itemSpec = $m.Groups[3].Value
            
            $num = -1
            if ($itemId.StartsWith('h')) {
                [int]::TryParse($itemId.Substring(1), [ref]$num) | Out-Null
            }
            
            $keepSpec = $false
            if ($num -ge 23 -and $num -le 32) { $keepSpec = $true }
            if ($num -ge 59 -and $num -le 64) { $keepSpec = $true }
            if ($num -ge 89 -and $num -le 102) { $keepSpec = $true }
            if ($num -eq 107) { $keepSpec = $true }
            if ($num -ge 108 -and $num -le 110) { $keepSpec = $true }
            
            if (-not $keepSpec) {
                $itemFull = $itemFull.Replace("spec: '$itemSpec'", "spec: '-'")
            }
            $hwDict[$itemId] = $itemFull
        }

        $newHwList = New-Object System.Collections.Generic.List[string]
        
        $order = @('h4', 'h5', 'h1', 'h2', 'h3', 'h6')
        foreach ($id in $order) {
            if ($hwDict.Contains($id)) {
                $newHwList.Add($hwDict[$id])
                $hwDict.Remove($id)
            }
        }
        
        foreach ($m in $hwMatches) {
            $id = $m.Groups[2].Value
            if ($hwDict.Contains($id) -and $id -ne 'h88') {
                $newHwList.Add($hwDict[$id])
                $hwDict.Remove($id)
            }
        }
        
        $newHwStr = [string]::Join(",`r`n                    ", $newHwList)
        $adminContent = [regex]::Replace($adminContent, 'hardware:\s*\[([\s\S]*?)\]', "hardware: [`r`n                    $newHwStr`r`n                ]")
    }

    if ($adminContent -match 'insulation:\s*\[([\s\S]*?)\]') {
        $insStr = $matches[1]
        $pattern = '(\{\s*id:\s*''(.*?)'',\s*code:\s*''.*?'',\s*name:\s*''.*?'',\s*spec:\s*''(.*?)'',\s*unit:\s*''.*?'',\s*price:\s*\d+(?:,\s*sub:\s*''.*?'')?\s*\})'
        $insMatches = [regex]::Matches($insStr, $pattern)
        
        $insDict = @{}
        foreach ($m in $insMatches) {
            $insDict[$m.Groups[2].Value] = $m.Groups[1].Value
        }
        
        if (-not $insDict.Contains('h88')) {
            $insDict['h88'] = "{ id: 'h88', code: '', name: '충진재 50T', spec: '50x450x1000mm', unit: '장', price: 2000 }"
        }
        
        $insOrder = @('i3', 'i4', 'i7', 'i8', 'i9', 'i15', 'i16', 'i17', 'i18', 'i11', 'i12', 'i13', 'i14', 'i1', 'i2', 'i10', 'h88')
        $newInsList = New-Object System.Collections.Generic.List[string]
        
        foreach ($id in $insOrder) {
            if ($insDict.Contains($id)) {
                $newInsList.Add($insDict[$id])
            }
        }
        
        $newInsStr = [string]::Join(",`r`n                    ", $newInsList)
        $adminContent = [regex]::Replace($adminContent, 'insulation:\s*\[([\s\S]*?)\]', "insulation: [`r`n                    $newInsStr`r`n                ]")
    }

    [System.IO.File]::WriteAllText($adminPath, $adminContent, [System.Text.Encoding]::UTF8)

    Write-Host "Success!"
} catch {
    Write-Error $_.Exception.Message
}
