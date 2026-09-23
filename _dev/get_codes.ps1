$path = "get_codes.txt"
$text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8).Trim()
$codes = New-Object System.Collections.Generic.List[string]
for ($i = 0; $i -lt $text.Length; $i++) {
    $c = $text[$i]
    if ($c -eq ' ') {
        $codes.Add(" ")
    } else {
        $codes.Add("0x{0:X4}" -f [int][char]$c)
    }
}
$codes -join ', ' | Out-File -FilePath codes.txt -Encoding ascii
