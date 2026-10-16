$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Source = Join-Path $Root "integrations/codex/agents"
$CodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$Destination = Join-Path $CodexRoot "agents"

if (-not (Test-Path $Source)) {
    throw "Codex agent source directory not found: $Source"
}

$Files = Get-ChildItem -Path $Source -Filter "*.toml"
if ($Files.Count -eq 0) {
    throw "No Codex agent TOML files found"
}

foreach ($File in $Files) {
    $Text = Get-Content -Raw -Path $File.FullName
    foreach ($Required in @("name", "description", "developer_instructions")) {
        if ($Text -notmatch "(?m)^$Required\s*=") {
            throw "$($File.Name): missing $Required"
        }
    }
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$Installed = 0
$Preserved = 0
foreach ($File in $Files) {
    $Target = Join-Path $Destination $File.Name
    if ($null -ne (Get-Item -LiteralPath $Target -Force -ErrorAction SilentlyContinue)) {
        Write-Host "Preserved existing: $Target"
        $Preserved++
        continue
    }
    # CreateNew refuses to replace a file that appeared after the check.
    $Stream = [System.IO.File]::Open($Target, [System.IO.FileMode]::CreateNew,
        [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    try {
        $Bytes = [System.IO.File]::ReadAllBytes($File.FullName)
        $Stream.Write($Bytes, 0, $Bytes.Length)
    }
    finally {
        $Stream.Dispose()
    }
    $Installed++
}
Write-Host "Installed $Installed; preserved $Preserved existing Luna Codex agents in $Destination"
