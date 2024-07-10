@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
)

REM Check if PyQt5 is installed
python -c "import PyQt5" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyQt5 is not installed. Installing PyQt5...
    pip install PyQt5
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyQt5. Please check your Python and pip installation.
        exit /b 1
    )
    echo PyQt5 has been successfully installed.
) ELSE (
    echo PyQt5 is already installed.
)

REM Check if pynput is installed
python -c "import pynput" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pynput is not installed. Installing pynput...
    pip install pynput
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install pynput. Please check your Python and pip installation.
        exit /b 1
    )
    echo pynput has been successfully installed.
) ELSE (
    echo pynput is already installed.
)

pause