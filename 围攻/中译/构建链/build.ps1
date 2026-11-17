# build.ps1 - one-shot rebuild for the SIEGE Chinese translation.
# Usage:  pwsh -File build.ps1            (PDF + docx)
#         pwsh -File build.ps1 -NoDocx    (PDF only)
# Chain: master md -> text-only md -> html -> headless Edge print-to-pdf -> docx (python-docx).
# Word is NOT used anywhere.

param(
    [switch]$NoDocx
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = Split-Path $here -Parent

function Resolve-Python {
    $cands = @()
    if ($env:DSH_HOME) {
        $cands += (Join-Path $env:DSH_HOME 'dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe')
    }
    if ($env:DSH_HOME) {
        $rt = Join-Path $env:DSH_HOME 'dsh-runtimes'
        if (Test-Path $rt) {
            $cands += (Get-ChildItem $rt -Directory -ErrorAction SilentlyContinue |
                ForEach-Object { Join-Path $_.FullName 'dependencies\python\python.exe' })
        }
    }
    $cands += 'C:\Users\28189\AppData\Local\Programs\Python\Python312\python.exe'
    $cands += (Get-Command python -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source)
    foreach ($c in $cands) {
        if ($c -and (Test-Path $c)) {
            $ok = & $c -c "import pymupdf" 2>$null
            if ($LASTEXITCODE -eq 0) { return $c }
        }
    }
    return $null
}

function Resolve-Edge {
    $cands = @(
        'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    )
    foreach ($c in $cands) { if (Test-Path $c) { return $c } }
    return $null
}

$py = Resolve-Python
if (-not $py) { throw 'python with pymupdf not found' }
$edge = Resolve-Edge
if (-not $edge) { throw 'Edge/Chrome not found' }

$md = Join-Path $root 'SIEGE-中译-第五版.md'
if (-not (Test-Path $md)) { throw "master md not found: $md" }

Write-Host "[1/3] text-only md"
& $py (Join-Path $here '1_make_text_only.py')
if ($LASTEXITCODE -ne 0) { throw 'step 1 failed' }

Write-Host "[2/3] html"
& $py (Join-Path $here '2_md2html.py')
if ($LASTEXITCODE -ne 0) { throw 'step 2 failed' }

Write-Host "[3/3] pdf via headless browser"
$html = Join-Path $root '_build\纯文字.html'
$pdf = Join-Path $root 'SIEGE-中译-第五版.pdf'
if (Test-Path $pdf) { Remove-Item $pdf -Force }
$uri = 'file:///' + ($html -replace '\\', '/')
$prev = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $edge --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$pdf" $uri 2>&1 | Out-Null
$ErrorActionPreference = $prev
if (-not (Test-Path $pdf)) { throw 'pdf not produced' }
Write-Host ("pdf {0:N0} bytes" -f (Get-Item $pdf).Length)

if (-not $NoDocx) {
    Write-Host "[extra] docx"
    & $py (Join-Path $here '3_build_docx.py')
}

Write-Host 'done.'
