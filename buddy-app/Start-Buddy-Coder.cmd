@echo off
setlocal
title Buddy Coder
pushd "%~dp0" || exit /b 1

echo Starting Buddy Coder at http://127.0.0.1:4096/
echo If prompted, use username opencode and the password printed below.
if exist "%~dp0opencode.exe" (
  "%~dp0opencode.exe" serve --hostname 127.0.0.1 --port 4096
) else (
  call npm.cmd exec --yes --package=@opencode/cli@2.2.6 -- opencode serve --hostname 127.0.0.1 --port 4096
)

set "BUDDY_EXIT=%ERRORLEVEL%"
popd
if not "%BUDDY_EXIT%"=="0" pause
exit /b %BUDDY_EXIT%
