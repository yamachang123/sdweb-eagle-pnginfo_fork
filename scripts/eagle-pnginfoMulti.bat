@echo off
setlocal enabledelayedexpansion
set "PYTHON_EXECUTABLE=C:\Users\yamau\AppData\Local\Programs\Python\Python310\python.exe"
REM ドラッグアンドドロップされた全ての引数を処理
set "python_args="
for %%A in (%*) do (
    set "python_args=!python_args! "%%~A""
)

REM Python を一度だけ呼び出し
"%PYTHON_EXECUTABLE%" "C:\GitHub\sdweb-eagle-pnginfo_fork\scripts\eagle-pnginfoMulti.py" !python_args!
