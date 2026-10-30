
$e=$null; $t=$null
[void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path 'scripts\shared-mode.ps1'), [ref]$t, [ref]$e)
if ($e) { $e | ForEach-Object { $_.Message + ' @ ' + $_.Extent.StartLineNumber + ':' + $_.Extent.StartColumnNumber } }
else { 'PARSE_OK' }
