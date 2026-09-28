[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Source,
    [switch]$Replace,
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$nodeScript = Join-Path $PSScriptRoot 'register-distribution-content.mjs'

if ($Check) {
    if ($Replace -or $Source.Count -gt 0) {
        throw '-Check cannot be combined with content sources or -Replace.'
    }
    & node $nodeScript --check
    exit $LASTEXITCODE
}

if ($Source.Count -eq 0) {
    throw 'Provide one or more content-pack ZIP files or directories.'
}

$temporaryRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$workDirectory = Join-Path $temporaryRoot ("information-rain-register-" + [guid]::NewGuid().ToString('N'))
$nodeSources = [System.Collections.Generic.List[string]]::new()

function Expand-SafeArchiveTree {
    param(
        [Parameter(Mandatory = $true)][string]$Archive,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $pending = [System.Collections.Generic.Queue[object]]::new()
    $pending.Enqueue([pscustomobject]@{ Archive = $Archive; Destination = $Destination })
    $processed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

    while ($pending.Count -gt 0) {
        $item = $pending.Dequeue()
        $archivePath = [System.IO.Path]::GetFullPath($item.Archive)
        if (-not $processed.Add($archivePath)) { continue }

        $destinationPath = [System.IO.Path]::GetFullPath($item.Destination)
        New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
        $destinationPrefix = $destinationPath.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

        $zip = [System.IO.Compression.ZipFile]::OpenRead($archivePath)
        try {
            foreach ($entry in $zip.Entries) {
                $entryTarget = [System.IO.Path]::GetFullPath((Join-Path $destinationPath $entry.FullName))
                if (-not $entryTarget.StartsWith($destinationPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                    throw "Archive entry escapes the extraction directory: $($entry.FullName)"
                }
            }
        }
        finally {
            $zip.Dispose()
        }

        Expand-Archive -LiteralPath $archivePath -DestinationPath $destinationPath -Force
        Get-ChildItem -LiteralPath $destinationPath -Recurse -File -Filter '*.zip' | ForEach-Object {
            $nestedDestination = $_.FullName + '.expanded'
            $pending.Enqueue([pscustomobject]@{ Archive = $_.FullName; Destination = $nestedDestination })
        }
    }
}

try {
    New-Item -ItemType Directory -Path $workDirectory | Out-Null
    $index = 0
    foreach ($item in $Source) {
        $resolved = (Resolve-Path -LiteralPath $item).Path
        if (Test-Path -LiteralPath $resolved -PathType Container) {
            $nodeSources.Add($resolved)
            continue
        }
        if ([System.IO.Path]::GetExtension($resolved) -ne '.zip') {
            throw "Only content-pack directories and ZIP files are supported: $resolved"
        }
        $destination = Join-Path $workDirectory ("source-" + $index)
        Expand-SafeArchiveTree -Archive $resolved -Destination $destination
        $nodeSources.Add($destination)
        $index += 1
    }

    $nodeArgs = @($nodeScript)
    if ($Replace) { $nodeArgs += '--replace' }
    $nodeArgs += $nodeSources
    & node @nodeArgs
    exit $LASTEXITCODE
}
finally {
    $resolvedWork = [System.IO.Path]::GetFullPath($workDirectory)
    $requiredPrefix = Join-Path $temporaryRoot 'information-rain-register-'
    if ($resolvedWork.StartsWith($requiredPrefix, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolvedWork)) {
        Remove-Item -LiteralPath $resolvedWork -Recurse -Force
    }
}
