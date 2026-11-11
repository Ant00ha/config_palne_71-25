@echo off
REM 
REM  1

if "%1"=="test" (
    echo [TEST MODE] Running with test repository...
    python src\main.py --package A --repo .\tests\test_graph.txt --mode test --version 1.0
) else (
    echo [REAL MODE] Running with real repository...
    python src\main.py --package bash --repo https://archive.ubuntu.com/ubuntu --mode real --version 5.0-4ubuntu1
)