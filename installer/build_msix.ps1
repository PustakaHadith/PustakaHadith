$ErrorActionPreference = "Stop"
$root   = "D:\Pustaka Quran Hadis\PustakaHadith"
$dist   = Join-Path $root "dist\PustakaHadith"
$assets = Join-Path $root "installer\Assets"
$stage  = Join-Path $root "installer\msix_stage"
$out    = Join-Path $root "installer\output"
$makeappx = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\makeappx.exe"
$signtool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\signtool.exe"
$pfx    = Join-Path $root "installer\msix_temp.pfx"
$pwtext = "PustakaMSIX2026"
$pw     = ConvertTo-SecureString -String $pwtext -Force -AsPlainText

# identiti
$id = @{}
(Get-Content (Join-Path $root "installer\msix_identity.txt")) | ForEach-Object {
    if ($_ -match "^(Package/[A-Za-z./]+)\s*=\s*(.+)$") { $id[$matches[1]] = $matches[2].Trim() }
}
$name = $id["Package/Identity/Name"]; $pub = $id["Package/Identity/Publisher"]; $disp = $id["Package/Properties/PublisherDisplayName"]

# staging
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Path $stage -Force | Out-Null
Copy-Item (Join-Path $dist "*") $stage -Recurse -Force
New-Item -ItemType Directory -Path (Join-Path $stage "Assets") -Force | Out-Null
Copy-Item (Join-Path $assets "*") (Join-Path $stage "Assets") -Force

# AppxManifest.xml
$manifest = @"
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities">
  <Identity Name="$name" Publisher="$pub" Version="1.0.0.0" ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>Pustaka Hadis</DisplayName>
    <PublisherDisplayName>$disp</PublisherDisplayName>
    <Description>Aplikasi rujukan hadis (PyInstaller onedir).</Description>
    <Logo>Assets\StoreLogo.png</Logo>
  </Properties>
  <Resources><Resource Language="ms-MY" /></Resources>
  <Applications>
    <Application Id="PustakaHadith" Executable="PustakaHadith.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="Pustaka Hadis" Description="Pustaka Hadis"
        BackgroundColor="#0B2545"
        Square150x150Logo="Assets\Square150x150Logo.png"
        Square44x44Logo="Assets\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
  <Capabilities><rescap:Capability Name="runFullTrust" /></Capabilities>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.19041.0" MaxVersionTested="10.0.22621.0" />
  </Dependencies>
</Package>
"@
Set-Content -Path (Join-Path $stage "AppxManifest.xml") -Value $manifest -Encoding UTF8

# self-signed cert (subject = Publisher CN) + pfx + trust
$cert = New-SelfSignedCertificate -Subject $pub -CertStoreLocation Cert:\CurrentUser\My `
    -KeyExportPolicy Exportable -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")
Export-PfxCertificate -Cert $cert -FilePath $pfx -Password $pw | Out-Null
Import-PfxCertificate -FilePath $pfx -Password $pw -CertStoreLocation Cert:\CurrentUser\TrustedPeople | Out-Null

# pack
New-Item -ItemType Directory -Path $out -Force | Out-Null
$msix = Join-Path $out "PustakaHadith_1.0.0.0_x64.msix"
if (Test-Path $msix) { Remove-Item $msix -Force }
& $makeappx pack /d "$stage" /p "$msix" /o 2>&1 | ForEach-Object { $_.ToString() }
"MAKEAPPX_EXIT=$LASTEXITCODE"

# sign
& $signtool sign /fd SHA256 /f "$pfx" /p "$pwtext" "$msix" 2>&1 | ForEach-Object { $_.ToString() }
"SIGN_EXIT=$LASTEXITCODE"
Get-Item $msix | ForEach-Object { "$($_.Name) $([math]::Round($_.Length/1MB,1))MB" }

# verify
& $signtool verify /pa "$msix" 2>&1 | ForEach-Object { $_.ToString() }
"VERIFY_EXIT=$LASTEXITCODE"
