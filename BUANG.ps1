# Buang PustakaHadith daripada komputer ini.
#
# Dipanggil oleh BUANG.bat. Jangan klik dua kali fail ini terus.
#
# Guna $PSScriptRoot, bukan argumen laluan - lihat Lesson #19:
# %~dp0 tamat dengan '\' dan merosakkan penghantaran argumen.

param(
    [switch] $BuangPakej,     # tanggal PyQt5 / requests / pyperclip
    [switch] $BuangData       # padam hadis.db + tetapan + tanda buku
)

$ErrorActionPreference = 'Continue'

$AppDir = $PSScriptRoot
$log    = New-Object System.Collections.Generic.List[string]

function Lapor([string]$teks) {
    Write-Host "        $teks"
    $log.Add($teks) | Out-Null
}

Write-Host ""
Write-Host "        Folder apl : $AppDir"
Write-Host ""


# == 1. Pintasan ====================================================
Write-Host "  [1] Membuang pintasan..."

$folderPintasan = @(
    [Environment]::GetFolderPath('Desktop'),
    [Environment]::GetFolderPath('Programs'),
    [Environment]::GetFolderPath('CommonDesktopDirectory'),
    [Environment]::GetFolderPath('CommonPrograms')
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

$namaPintasan = @('Hadis.lnk', 'PustakaHadith.lnk', 'PustakaHadith.lnk')
$jumlahLnk = 0

foreach ($f in $folderPintasan) {
    foreach ($n in $namaPintasan) {
        $lnk = Join-Path $f $n
        if (Test-Path $lnk) {
            try {
                Remove-Item $lnk -Force -ErrorAction Stop
                Lapor "dibuang : $lnk"
                $jumlahLnk++
            } catch {
                Lapor "GAGAL   : $lnk - $($_.Exception.Message)"
            }
        }
    }
}

if ($jumlahLnk -eq 0) { Lapor "tiada pintasan dijumpai." }
Write-Host ""


# == 2. Pin di taskbar / Start ======================================
Write-Host "  [2] Menyemak pin taskbar..."

# Join-Path mesti DALAM pengawal: $env:APPDATA boleh null dan
# Join-Path melontar sebelum Test-Path sempat menilai (Lesson #19).
$adaPin = $false
$pinDir = $null
if ($env:APPDATA) {
    $pinDir = Join-Path $env:APPDATA 'Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar'
}

if ($pinDir -and (Test-Path $pinDir)) {
    foreach ($n in $namaPintasan) {
        $p = Join-Path $pinDir $n
        if (Test-Path $p) {
            try {
                Remove-Item $p -Force -ErrorAction Stop
                Lapor "pin dibuang : $n"
                $adaPin = $true
            } catch {
                Lapor "pin GAGAL   : $n"
            }
        }
    }
}

if (-not $adaPin) {
    Lapor "tiada pin dijumpai."
} else {
    Lapor "nota: ikon mungkin kekal di taskbar sehingga log keluar."
}
Write-Host ""


# == 3. Data pengguna ===============================================
if ($BuangData) {
    Write-Host "  [3] Membuang data pengguna..."
    $fail = @('hadis.db', 'hadis.db-wal', 'hadis.db-shm',
              'user_settings.json', 'bookmarks.json', '.env')
    $n = 0
    foreach ($f in $fail) {
        $path = Join-Path $AppDir $f
        if (Test-Path $path) {
            try {
                Remove-Item $path -Force -ErrorAction Stop
                Lapor "dibuang : $f"
                $n++
            } catch {
                Lapor "GAGAL   : $f - apl mungkin masih berjalan?"
            }
        }
    }
    if ($n -eq 0) { Lapor "tiada data dijumpai." }
} else {
    Write-Host "  [3] Data pengguna DIKEKALKAN"
    Lapor "hadis.db + tetapan + tanda buku tidak disentuh."
}
Write-Host ""


# == 4. Pakej Python ================================================
if ($BuangPakej) {
    Write-Host "  [4] Menanggalkan pakej Python..."
    Lapor "PyQt5 / requests / pyperclip"
    Lapor "(program Python lain mungkin memerlukannya)"
    Write-Host ""

    $py = Get-Command python.exe -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command py.exe -ErrorAction SilentlyContinue }

    if ($py) {
        & $py.Source -m pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip pyperclip
        Lapor "selesai. 'requests' dikekalkan - terlalu banyak program guna."
    } else {
        Lapor "Python tidak dijumpai - langkau."
    }
} else {
    Write-Host "  [4] Pakej Python DIKEKALKAN"
    Lapor "PyQt5 dsb. dibiar - tidak mengganggu."
}
Write-Host ""

exit 0
