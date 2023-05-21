REM Configure this .bat file to run as a windows service with nssm (non-sucking-service-manager)

@echo off
:loop
REM Path to python.exe in your venv + path to the script file
"C:\Users\fejes\OneDrive\Dokumentumok\GitHub\hardverapro-lookup\venv\scripts\python.exe" "C:\Users\fejes\OneDrive\Dokumentumok\GitHub\hardverapro-lookup\lookup-bot.py"

REM Delay for 5 minutes (300 seconds)
timeout /t 300 >NUL

REM Go back to the start of the loop
goto loop

