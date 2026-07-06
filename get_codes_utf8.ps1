# "요꼬합판 석고본드 포 기준 완료 일반합판 준내수 KCC 하남시 지식산업센터 석고보드 및 경량철골 자재 납품 벽산 인천 검단 신도시 아파트 단열재 그라스울 대량 서울 강남구 오피스 빌딩 도어 인테리어 마감재 오늘"
$scriptPath = $MyInvocation.MyCommand.Path
$lines = [System.IO.File]::ReadAllLines($scriptPath, [System.Text.Encoding]::UTF8)
$targetLine = ""
foreach ($line in $lines) {
    if ($line.StartsWith("# `"" -or $line.StartsWith("# `")) {
        $targetLine = $line
        break
    }
}
$targetStr = $targetLine.Substring(3, $targetLine.Length - 4)

$codes = New-Object System.Collections.Generic.List[string]
for ($i = 0; $i -lt $targetStr.Length; $i++) {
    $c = $targetStr[$i]
    if ($c -eq ' ') {
        $codes.Add(" ")
    } else {
        $codes.Add("0x{0:X4}" -f [int][char]$c)
    }
}
$codes -join ', ' | Out-File -FilePath codes.txt -Encoding ascii
