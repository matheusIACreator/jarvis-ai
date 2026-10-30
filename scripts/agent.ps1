<#
.SYNOPSIS
    Runs a task with Claude Code and falls back to Codex when Claude hits its usage limit.

.DESCRIPTION
    Both agents read AGENTS.md and the shared vault, so whichever one runs picks up
    the work-in-progress state from vault/em-andamento.md.
    Only works for non-interactive (headless) runs. An interactive session cannot be
    switched automatically; open the other agent and ask it to continue instead.

.EXAMPLE
    .\scripts\agent.ps1 "Do backlog item 1: set up the dev environment"
    .\scripts\agent.ps1 -Agent codex "Continue the task in progress"
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Task,

    [ValidateSet("claude", "codex")]
    [string]$Agent = "claude"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$prompt = @"
Follow the session protocol in AGENTS.md.
First read vault/em-andamento.md: if a task is in progress, continue it from its next step.
Keep vault/em-andamento.md updated after every meaningful step.
Task: $Task
"@

# Messages Claude Code prints when the subscription or API limit is reached.
$limitPattern = "usage limit|rate limit|limit reached|out of (extra )?usage|quota"

function Invoke-Codex {
    if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
        Write-Error "Codex CLI not found. Install it first (see vault/decisoes/0006-troca-entre-agentes.md)."
    }
    Write-Host "==> Running Codex" -ForegroundColor Cyan
    codex exec --sandbox workspace-write $prompt
    $codexExit = $LASTEXITCODE

    # Codex's workspace-write sandbox keeps .git read-only, so commit on its behalf.
    if (git status --porcelain) {
        Write-Host "==> Committing Codex changes" -ForegroundColor Cyan
        git add -A
        git commit -q -m "chore(codex): session changes" -m "Task: $Task" -m "Committed by scripts/agent.ps1 because the Codex sandbox cannot write to .git."
    }
    exit $codexExit
}

if ($Agent -eq "codex") {
    Invoke-Codex
}

Write-Host "==> Running Claude Code" -ForegroundColor Cyan
$output = claude -p $prompt --permission-mode acceptEdits --output-format json 2>&1 | Out-String
$exitCode = $LASTEXITCODE

$resultText = $output
$isError = $exitCode -ne 0
try {
    $json = $output | ConvertFrom-Json
    $resultText = $json.result
    if ($json.is_error) { $isError = $true }
} catch {
    # Not JSON (e.g. the CLI failed before starting); keep the raw output.
}

Write-Host $resultText

if ($isError -and ($output -match $limitPattern)) {
    Write-Host "==> Claude Code hit its usage limit; handing off to Codex" -ForegroundColor Yellow
    Invoke-Codex
}

exit $exitCode
