from pathlib import Path
p = Path('scripts/shared-mode.ps1')
data = p.read_bytes()
print('BOM', data[:4])
text = data.decode('utf-8-sig')
lines = text.splitlines()
print('total lines', len(lines))
for n in range(48, 62):
    print(n + 1, repr(lines[n]))
print('---99---', repr(lines[98]))
print('---104-end---')
for n in range(103, len(lines)):
    print(n + 1, repr(lines[n]))
# non-ascii quotes
for i, ch in enumerate(text):
    o = ord(ch)
    if o in (0x2018, 0x2019, 0x201C, 0x201D):
        print('fancy', hex(o), 'at', i, repr(text[max(0,i-30):i+30]))
# check default system encoding parse simulation
import subprocess, tempfile, os
script = r'''
$e=$null; $t=$null
[void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path 'scripts\shared-mode.ps1'), [ref]$t, [ref]$e)
if ($e) { $e | ForEach-Object { $_.Message + ' @ ' + $_.Extent.StartLineNumber + ':' + $_.Extent.StartColumnNumber } }
else { 'PARSE_OK' }
'''
Path('_parse_check.ps1').write_text(script, encoding='utf-8')
