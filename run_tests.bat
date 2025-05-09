@echo off
for %%f in (test*.py) do (
    echo Running %%f...
    python %%f
    echo.
)
pause