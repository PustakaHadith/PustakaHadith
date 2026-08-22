# Pindahkan data pengguna dari pemasangan LAMA ke folder ini.
#
# MASALAH YANG DISELESAIKAN
# -------------------------
# Mengekstrak ZIP ke folder BAHARU memberi kod terkini tetapi
# meninggalkan hadis.db, tanda buku, tetapan dan .env di folder lama.
# Aplikasi kelihatan kosong walaupun sync telah dijalankan.
#
# `config.py` mengira DB_PATH relatif kepada folder skrip:
#     DB_PATH = os.path.join(BASE_DIR, "hadis.db")
# Jadi data MESTI berada bersebelahan kod yang dijalankan.
#
# GUNA
#   .\PINDAH_DATA.ps1 "D:\Pustaka Quran Hadis\pustaka"
#
# Fail sedia ada dalam folder ini TIDAK ditimpa melainkan -Force.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Lama,

    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$Baharu = $PSScriptRoot

Write-Host ""
Write-Host "  Dari : $Lama"
Write-Host "  Ke   : $Baharu"
Write-Host ""

if (-not (Test-Path -LiteralPath $Lama)) {
    Write-Host "  Folder lama tidak wujud." -ForegroundColor Red
    exit 1
}

$penuhLama   = (Resolve-Path -LiteralPath $Lama).Path
$penuhBaharu = (Resolve-Path -LiteralPath $Baharu).Path
if ($penuhLama -eq $penuhBaharu) {
    Write-Host "  Sumber dan sasaran sama. Tiada apa-apa dibuat." -ForegroundColor Yellow
    exit 0
}

# hadis.db-wal / -shm ialah fail Write-Ahead Log SQLite. Ia MESTI
# dipindah bersama hadis.db atau ditinggalkan sepenuhnya -- memindah
# db tanpa wal boleh kehilangan transaksi terakhir.
$fail = @(
    'hadis.db', 'hadis.db-wal', 'hadis.db-shm',
    'bookmarks.json', 'user_settings.json', '.env'
)
$folder = @('.cache_eng', '.cache_syarah', '.cache_he', '.cache_sema')

$disalin = 0
$dilangkau = 0

foreach ($f in $fail) {
    $src = Join-Path $penuhLama $f
    if (-not (Test-Path -LiteralPath $src)) { continue }
    $dst = Join-Path $penuhBaharu $f
    if ((Test-Path -LiteralPath $dst) -and (-not $Force)) {
        Write-Host ("  langkau  {0,-22} (sudah ada)" -f $f) -ForegroundColor Yellow
        $dilangkau++
        continue
    }
    Copy-Item -LiteralPath $src -Destination $dst -Force
    $saiz = (Get-Item -LiteralPath $dst).Length
    Write-Host ("  salin    {0,-22} {1,12:N0} bait" -f $f, $saiz) -ForegroundColor Green
    $disalin++
}

foreach ($d in $folder) {
    $src = Join-Path $penuhLama $d
    if (-not (Test-Path -LiteralPath $src)) { continue }
    $dst = Join-Path $penuhBaharu $d
    if ((Test-Path -LiteralPath $dst) -and (-not $Force)) {
        Write-Host ("  langkau  {0,-22} (sudah ada)" -f $d) -ForegroundColor Yellow
        $dilangkau++
        continue
    }
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
    Write-Host ("  salin    {0,-22} (folder cache)" -f $d) -ForegroundColor Green
    $disalin++
}

Write-Host ""
if ($disalin -eq 0 -and $dilangkau -eq 0) {
    Write-Host "  Tiada fail data dijumpai dalam folder lama." -ForegroundColor Yellow
    Write-Host "  Adakah laluan itu betul?"
} else {
    Write-Host "  Selesai: $disalin disalin, $dilangkau dilangkau."
    if ($dilangkau -gt 0) {
        Write-Host "  Guna -Force untuk menimpa yang dilangkau."
    }
}
Write-Host ""
Write-Host "  Fail ASAL tidak disentuh. Sahkan aplikasi berfungsi"
Write-Host "  sebelum memadam folder lama."
Write-Host ""

$db = Join-Path $penuhBaharu 'hadis.db'
if (Test-Path -LiteralPath $db) {
    python (Join-Path $penuhBaharu 'semak_db.py')
}
