# creating executable
python -m PyInstaller --noconsole -F -i $wd"icon.ico" "sfzmapper_gui.py"

# move executable to root path
mv dist/sfzmapper_gui.exe .