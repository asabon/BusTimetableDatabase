# ライブラリ移行用ファイルコピースクリプト
# 
# 使い方:
# 1. このスクリプトを BusTimeTableDatabase リポジトリのルートで実行
# 2. アプリのリポジトリのパスを指定
# 3. GitHub Actions からダウンロードした AAR ファイルのパスを指定

param(
    [Parameter(Mandatory = $true)]
    [string]$AppRepoPath,
    
    [Parameter(Mandatory = $true)]
    [string]$AarFilePath
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ライブラリ移行用ファイルコピー" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# パスの検証
if (-not (Test-Path $AppRepoPath)) {
    Write-Host "エラー: アプリのリポジトリが見つかりません: $AppRepoPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $AarFilePath)) {
    Write-Host "エラー: AARファイルが見つかりません: $AarFilePath" -ForegroundColor Red
    exit 1
}

# 現在のディレクトリを取得（BusTimeTableDatabase のルート）
$LibraryRepoPath = Get-Location

Write-Host "コピー元: $LibraryRepoPath" -ForegroundColor Green
Write-Host "コピー先: $AppRepoPath" -ForegroundColor Green
Write-Host "AARファイル: $AarFilePath" -ForegroundColor Green
Write-Host ""

# ステップ1: ドキュメント用ディレクトリを作成
Write-Host "[1/3] ドキュメント用ディレクトリを作成中..." -ForegroundColor Yellow
$DocsDir = Join-Path $AppRepoPath "docs\library"
New-Item -ItemType Directory -Force -Path $DocsDir | Out-Null
Write-Host "  ✓ 作成完了: $DocsDir" -ForegroundColor Green
Write-Host ""

# ステップ2: ドキュメントをコピー
Write-Host "[2/3] ドキュメントをコピー中..." -ForegroundColor Yellow

$DocumentsToCopy = @(
    "client\android\docs\INTEGRATION_GUIDE.md",
    "client\android\docs\APP_INTEGRATION_CHECKLIST.md",
    "client\android\docs\MIGRATION_GUIDE.md",
    "client\android\docs\API_SPEC.md",
    "client\android\docs\VERSION_MANAGEMENT.md",
    "client\android\docs\QUICKSTART_MIGRATION.md",
    "client\android\README.md"
)

foreach ($doc in $DocumentsToCopy) {
    $sourcePath = Join-Path $LibraryRepoPath $doc
    $fileName = Split-Path $doc -Leaf
    $destPath = Join-Path $DocsDir $fileName
    
    if (Test-Path $sourcePath) {
        # コンテンツを読み込んでリンクを修正（階層構造の変更に対応）
        $content = Get-Content $sourcePath -Raw
        
        # README.md からのリンクを修正 (docs/xxx.md -> xxx.md)
        $content = $content -replace "docs/INTEGRATION_GUIDE.md", "INTEGRATION_GUIDE.md"
        $content = $content -replace "docs/API_SPEC.md", "API_SPEC.md"
        
        # docs/*.md からのリンクを修正 (../README.md -> README.md)
        $content = $content -replace "\.\./README.md", "README.md"
        
        Set-Content -Path $destPath -Value $content -Force
        Write-Host "  ✓ コピー完了: $fileName" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠ スキップ (ファイルが見つかりません): $fileName" -ForegroundColor Yellow
    }
}
Write-Host ""

# ステップ3: AARファイルをコピー
Write-Host "[3/3] AARファイルをコピー中..." -ForegroundColor Yellow
$LibsDir = Join-Path $AppRepoPath "app\libs"
New-Item -ItemType Directory -Force -Path $LibsDir | Out-Null

$destAarPath = Join-Path $LibsDir "bustimetable-library.aar"
Copy-Item $AarFilePath $destAarPath -Force
Write-Host "  ✓ コピー完了: bustimetable-library.aar" -ForegroundColor Green
Write-Host ""

# 完了メッセージ
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "コピー完了！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. アプリのリポジトリを VS Code で開く" -ForegroundColor White
Write-Host "2. docs/library/MIGRATION_GUIDE.md を開く" -ForegroundColor White
Write-Host "3. 「ステップ2: 別ワークスペースでAIに指示する内容」に従って作業を進める" -ForegroundColor White
Write-Host ""
Write-Host "コピーされたファイル:" -ForegroundColor Yellow
Write-Host "  - docs/library/*.md (ドキュメント)" -ForegroundColor White
Write-Host "  - app/libs/bustimetable-library.aar (ライブラリ)" -ForegroundColor White
Write-Host ""
