@echo off
echo Starting Ultimon Full Stack...

echo Installing dependencies with pnpm...
pnpm install

echo Building the application with pnpm...
pnpm build

echo Starting the development server with pnpm...
pnpm dev

echo Ultimon Full Stack started.
pause
