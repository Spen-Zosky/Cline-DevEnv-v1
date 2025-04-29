@echo off
echo Starting Research Dashboard using Docker...

REM Navigate to the Docker directory
cd ..\..\infrastructure\docker

REM Start the research dashboard and its backend using Docker Compose
docker-compose up -d research-dashboard-backend research-dashboard

REM Wait for the services to start
timeout /t 5

REM Open the dashboard in the default browser
start http://localhost:3000

echo Dashboard started successfully!
echo The dashboard is running at http://localhost:3000
