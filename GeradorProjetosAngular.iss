[Setup]
AppName=GeradorProjetosAngular
AppVersion=2.0
DefaultDirName={pf}\GeradorProjetosAngular
OutputDir=.
OutputBaseFilename=Setup_GeradorProjetosAngular
SetupIconFile="C:\Projetos\Projetos Python\GeradorAngular\ang.ico"

[Files]
Source: "C:\Projetos\Projetos Python\GeradorAngular\dist\geradorAngular.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\geradorAngular"; Filename: "{app}\geradorAngular.exe"; IconFilename: "{app}\geradorAngular.exe"

[Run]
Filename: "{app}\geradorAngular.exe"; Description: "Executar Gerador de Projetos Angular"; Flags: nowait postinstall skipifsilent
