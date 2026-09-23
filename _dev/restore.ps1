$badPath = "index.html"
$badText = [System.IO.File]::ReadAllText($badPath, [System.Text.Encoding]::UTF8)
$cp949 = [System.Text.Encoding]::GetEncoding(949)
$utf8 = [System.Text.Encoding]::UTF8

# Encode the garbage string back to bytes using CP949
$originalBytes = $cp949.GetBytes($badText)

# Write the original bytes back as a file
[System.IO.File]::WriteAllBytes("index_restored.html", $originalBytes)

$badAdminPath = "admin.html"
$badAdminText = [System.IO.File]::ReadAllText($badAdminPath, [System.Text.Encoding]::UTF8)
$originalAdminBytes = $cp949.GetBytes($badAdminText)
[System.IO.File]::WriteAllBytes("admin_restored.html", $originalAdminBytes)
