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
Copy-Item -Path (Join-Path $Source "*.toml") -Destination $Destination -Force
Write-Host "Validated and installed $($Files.Count) Luna Codex agents to $Destination"
