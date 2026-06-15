@echo off
REM Douyin to Text Skill - Windows batch wrapper for Claude Code

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

cd /d "%PROJECT_ROOT%"

REM Activate virtual environment if exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Run the skill
python "%SCRIPT_DIR%dy2text.py" %*
