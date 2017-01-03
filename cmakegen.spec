import os

script_files = [
    'cmakegen.py'
]

script_paths = [
    os.path.dirname(os.path.abspath(file)) for file in script_files
]

anz = Analysis(
    script_files,
    pathex=script_paths,
    binaries=None,
    datas=None,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None)

pyz = PYZ(
    anz.pure,
    anz.zipped_data,
    cipher=None)

exe = EXE(
    pyz,
    anz.scripts,
    anz.binaries,
    anz.zipfiles,
    anz.datas,
    name='cmakegen',
    debug=False,
    strip=False,
    upx=True,
    console=True)
