import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--windowed',
    '--noconsole',
    '--icon=images/iconlogo.icns'
])