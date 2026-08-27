# Cipta pintasan "Hadis" di Desktop dan Start Menu.
#
# Skrip ini menentukan SENDIRI folder apl ($PSScriptRoot) dan lokasi
# pythonw.exe. Sengaja TIDAK menerima laluan folder sebagai argumen:
#
#   powershell -File skrip.ps1 -AppDir "%~dp0"        <-- ROSAK
#
# kerana %~dp0 sentiasa tamat dengan '\', jadi cmd.exe menghantar
#   "D:\Pustaka Quran Hadis\"
# dan PowerShell membaca \" sebagai petikan yang di-escape, lalu
# menelan argumen berikutnya. Pintasan gagal dicipta tanpa sebarang
# mesej ralat.
#
# Pintasan menunjuk TERUS kepada pythonw.exe. Tidak guna .vbs
# perantara kerana perkaitan fail .vbs kerap dirampas program lain.

$ErrorActionPreference = 'Stop'

$AppDir = $PSScriptRoot
$mainPy = Join-Path $AppDir 'main.py'
$icon   = Join-Path $AppDir 'app.ico'

Write-Host ""
Write-Host "        Folder apl : $AppDir"

if (-not (Test-Path $mainPy)) {
    Write-Host "        [X] main.py tidak dijumpai."
    exit 1
}

# -- Cari pythonw.exe ------------------------------------------------
# pythonw.exe = Python tanpa tetingkap konsol hitam.
$pythonw = $null

# 1) venv dalam folder projek
foreach ($v in @('.venv', 'venv')) {
    $cand = Join-Path $AppDir "$v\Scripts\pythonw.exe"
    if (Test-Path $cand) { $pythonw = $cand; break }
}

# 2) sebelah python.exe yang aktif dalam PATH
if (-not $pythonw) {
    $py = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($py) {
        $cand = Join-Path (Split-Path $py.Source) 'pythonw.exe'
        if (Test-Path $cand) { $pythonw = $cand }
    }
}

# 3) pythonw.exe terus dalam PATH
if (-not $pythonw) {
    $pw = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($pw) { $pythonw = $pw.Source }
}

# 4) Python Launcher - sandaran terakhir
if ((-not $pythonw) -and $env:WINDIR) {
    $cand = Join-Path $env:WINDIR 'pyw.exe'
    if (Test-Path $cand) { $pythonw = $cand }
}

if (-not $pythonw) {
    Write-Host "        [X] pythonw.exe tidak dijumpai."
    exit 1
}

Write-Host "        Python     : $pythonw"
Write-Host ""

# -- Cipta pintasan --------------------------------------------------
$shell = New-Object -ComObject WScript.Shell

$sasaran = @(
    @{ Nama = 'Desktop';    Path = [Environment]::GetFolderPath('Desktop')  },
    @{ Nama = 'Start Menu'; Path = [Environment]::GetFolderPath('Programs') }
)

$berjaya = 0

foreach ($t in $sasaran) {
    try {
        if ([string]::IsNullOrWhiteSpace($t.Path)) { throw "folder tidak dijumpai" }
        if (-not (Test-Path $t.Path)) { New-Item -ItemType Directory -Path $t.Path -Force | Out-Null }

        # buang pintasan lama daripada versi terdahulu
        foreach ($n in @('PustakaHadith.lnk', 'PustakaHadith.lnk')) {
            $lama = Join-Path $t.Path $n
            if (Test-Path $lama) { Remove-Item $lama -Force -ErrorAction SilentlyContinue }
        }

        $lnk = Join-Path $t.Path 'Hadis.lnk'
        if (Test-Path $lnk) { Remove-Item $lnk -Force -ErrorAction SilentlyContinue }

        $s = $shell.CreateShortcut($lnk)
        $s.TargetPath       = $pythonw
        $s.Arguments        = '"' + $mainPy + '"'   # petik: laluan mungkin ada ruang
        $s.WorkingDirectory = $AppDir
        $s.Description      = 'Hadis - Pustaka Koleksi Kitab Hadis'
        $s.WindowStyle      = 1
        if (Test-Path $icon) { $s.IconLocation = $icon }
        $s.Save()

        Start-Sleep -Milliseconds 150      # beri masa shell tulis fail

        if (Test-Path $lnk) {
            Write-Host ("        {0,-11}: OK  ->  {1}" -f $t.Nama, $lnk)
            $berjaya++
        } else {
            throw "fail .lnk tidak terhasil"
        }
    }
    catch {
        Write-Host ("        {0,-11}: GAGAL - {1}" -f $t.Nama, $_.Exception.Message)
    }
}

Write-Host ""

if ($berjaya -eq 0) { exit 1 }
exit 0
