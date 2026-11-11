@echo off

if "%1"=="test" (
    echo [TEST MODE] Running with test repository...
    python -m src.main --package A --repo .\tests\test_graph.txt --mode test --version 1.0
) else if "%1"=="reverse" (
    echo [REVERSE MODE] Running reverse dependencies for test repository...
    python -m src.main --package D --repo .\tests\test_graph.txt --mode test --version 1.0 --reverse
) else if "%1"=="unittest" (
    echo [UNITTEST] Running automated tests...
    python -m unittest discover -s tests -v
) else (
    echo [REAL MODE] Running with real repository...
    python -m src.main --package bash --repo http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz --mode real --version 5.1-6ubuntu1
)