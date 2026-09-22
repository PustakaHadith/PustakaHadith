[Setup]
AppId={{7DF2553E-9E62-4ED4-929A-61C71AD1047F}
AppName=PustakaHadith
AppVersion=1.0.2
AppPublisher=opencodemk
DefaultDirName={localappdata}\PustakaHadith
DefaultGroupName=PustakaHadith
OutputDir=..\Output
OutputBaseFilename=PustakaHadith-Setup-1.0.2-x64
SetupIconFile=..\app.ico
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=PustakaHadith
UninstallDisplayIcon={app}\PustakaHadith.exe

[Files]
Source: "D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PustakaHadith"; Filename: "{app}\PustakaHadith.exe"
Name: "{group}\Uninstall PustakaHadith"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PustakaHadith"; Filename: "{app}\PustakaHadith.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Bina ikon atas desktop"; GroupDescription: "Pilihan tambahan:"

[Run]
Filename: "{app}\PustakaHadith.exe"; Description: "Jalankan PustakaHadith sekarang"; Flags: nowait postinstall skipifsilent
