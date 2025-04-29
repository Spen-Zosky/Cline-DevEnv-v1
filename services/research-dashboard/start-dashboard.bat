@echo off
echo Starting Research Dashboard using Docker...

REM Use absolute path for Docker Compose
cd /d %~dp0
cd ..\..\infrastructure\docker

REM Start the research dashboard and its backend using Docker Compose
echo Building and starting the research dashboard services...
docker-compose up -d --build research-dashboard-backend research-dashboard

REM Wait for the services to start
echo Waiting for services to start...
timeout /t 10

REM Open the dashboard in the default browser
echo Opening dashboard in browser...
start http://localhost:3000

echo Dashboard started successfully!
echo The dashboard is running at http://localhost:3000
