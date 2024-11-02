from cx_Freeze import setup, Executable

   
   # Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["tkinter", "datetime", "ctypes"],
}

setup(
    name="NotePad py",
    version="0.7",
    description="Notepad with advanced options",
    options={"build_exe": build_exe_options},
    executables=[Executable("guifoo.py", base="gui")],
)