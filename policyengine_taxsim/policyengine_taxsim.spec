import os
from pathlib import Path
import policyengine_us
import policyengine_taxsim

# Get required paths
pe_data_path = Path(policyengine_us.__file__).parent / ""
yaml_path = Path(policyengine_taxsim.__file__).parent / "config" / "variable_mappings.yaml"

a = Analysis(
    ['exe.py'],
    pathex=[],
    binaries=[],
    datas=[
        (str(pe_data_path), 'policyengine_us/'),
        (str(yaml_path), 'policyengine_taxsim/config'),
        (str(Path.cwd() / "core"), 'core'),
    ],
    hiddenimports=[
        'click',
        'pandas',
        'numpy',
        'policyengine_us',
        'yaml',
        'core',
        'core.input_mapper',
        'core.output_mapper',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*__pycache__*',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='policyengine-taxsim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)