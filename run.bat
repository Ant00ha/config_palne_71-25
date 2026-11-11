@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

if "%1"=="unittest" (
    echo [UNITTEST] Running automated tests...
    python -m unittest discover -s tests -v
    goto :eof
)

if not "%1"=="" (
    echo Неизвестный аргумент: %1
    echo Доступные аргументы для прямого запуска: unittest
    goto :eof
)

:menu
cls
echo.
echo  Выберите действие:
echo.
echo  --- Текстовый вывод (Этапы 2-4) ---
echo  1. Показать граф зависимостей для пакета A (тест)
echo  2. Показать граф зависимостей для пакета bash (реальный)
echo  3. Показать обратные зависимости для D (тест)
echo.
echo  --- Визуализация (Этап 5) ---
echo  4. Нарисовать граф для пакета A (тест)
echo  5. Нарисовать граф для пакета B (тест)
echo  6. Нарисовать граф для пакета bash (реальный)
echo.
echo  --- Служебные ---
echo  7. Запустить автотесты (unittest)
echo  0. Выход
echo.
set /p choice="Введите номер (0-7): "

if "%choice%"=="1" (
    python -m src.main --package A --repo .\tests\test_graph.txt --mode test --version 1.0
    pause
    goto :menu
)
if "%choice%"=="2" (
    python -m src.main --package bash --repo http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz --mode real --version 5.1-6ubuntu1
    pause
    goto :menu
)
if "%choice%"=="3" (
    python -m src.main --package D --repo .\tests\test_graph.txt --mode test --version 1.0 --reverse
    pause
    goto :menu
)
if "%choice%"=="4" (
    python -m src.main --package A --repo .\tests\test_graph.txt --mode test --version 1.0 --visualize
    pause
    goto :menu
)
if "%choice%"=="5" (
    python -m src.main --package B --repo .\tests\test_graph.txt --mode test --version 1.0 --visualize
    pause
    goto :menu
)
if "%choice%"=="6" (
    python -m src.main --package bash --repo http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz --mode real --version 5.1-6ubuntu1 --visualize
    pause
    goto :menu
)
if "%choice%"=="7" (
    python -m unittest discover -s tests -v
    pause
    goto :menu
)
if "%choice%"=="0" (
    exit /b 0
)

echo.
echo Неверный ввод. Пожалуйста, введите число от 0 до 7.
timeout /t 2 >nul
goto :menu