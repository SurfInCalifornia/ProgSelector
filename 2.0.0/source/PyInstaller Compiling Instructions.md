PyInstaller Compiling Instructions for ProgSelector 2.0.0:



In the same folder as your script and icons, open a Command Prompt window and then enter the command below:



pyinstaller --onedir --windowed --icon=logo.ico ProgSelector.pyw --add-data "logo2.ico;." --add-data "logo.ico;."
