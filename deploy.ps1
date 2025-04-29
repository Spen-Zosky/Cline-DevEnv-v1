
# deploy.ps1

# Define colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"
$White = "White"

# Function to display colored output
function Write-ColoredOutput {
    param(
        [string]$Color,
        [string]$Text
    )
    Write-Host -ForegroundColor $Color $Text
}
# Print header
Write-ColoredOutput -Color $Green -Text "========================================="
Write-ColoredOutput -Color $Green -Text "   AI Research Platform Deployment Tool  "
Write-ColoredOutput -Color $Green -Text "========================================="
Write-Host


$ErrorActionPreference = "Stop"
# Function to start the development environment
function Start-DevEnvironment {
    Write-ColoredOutput -Color $Cyan -Text "Starting development environment..."
    docker-compose -f "infrastructure/docker/docker-compose.yml" up -d
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to start development environment."
        exit 1
    }
    Write-ColoredOutput -Color $Green -Text "Development environment started."
    Write-ColoredOutput -Color $White -Text "Research Dashboard: http://localhost:3000"
    Write-ColoredOutput -Color $White -Text "Web Generator: http://localhost:3001"
    Write-ColoredOutput -Color $White -Text "API Gateway: http://localhost:8000"
    Write-ColoredOutput -Color $White -Text "MinIO Console: http://localhost:9001"
}

# Function to stop the development environment
function Stop-DevEnvironment {
    Write-ColoredOutput -Color $Cyan -Text "Stopping development environment..."
    docker-compose -f "infrastructure/docker/docker-compose.yml" down
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to stop development environment."
        exit 1
    }
    Write-ColoredOutput -Color $Green -Text "Development environment stopped."
}

# Function to build Docker images
function Build-Images {
    Write-ColoredOutput -Color $Cyan -Text "Building Docker images..."
    docker-compose -f "infrastructure/docker/docker-compose.yml" build
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to build Docker images."
        exit 1
    }
    Write-ColoredOutput -Color $Green -Text "Docker images built."
}

# Function to deploy to Kubernetes
function Deploy-Kubernetes {
    Write-ColoredOutput -Color $Cyan -Text "Deploying to Kubernetes..."
    kubectl apply -f "infrastructure/kubernetes/namespace.yaml"
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to apply namespace."
        exit 1
    }
    kubectl apply -k "infrastructure/kubernetes/"
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to deploy to Kubernetes. Check kubectl configuration."
        exit 1
    }
    Write-ColoredOutput -Color $Green -Text "Deployed to Kubernetes."
    Write-ColoredOutput -Color $White -Text "Use 'kubectl get pods -n ai-research-platform' to check the status of the pods."

}


# Function to clean up the environment
function Clean-Up {
    Write-ColoredOutput -Color $Cyan -Text "Cleaning up..."
    kubectl delete -k "infrastructure/kubernetes/"
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to delete Kubernetes resources."
    }
    kubectl delete -f "infrastructure/kubernetes/namespace.yaml"
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to delete namespace."
    }
    docker-compose -f "infrastructure/docker/docker-compose.yml" down
    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput -Color $Red -Text "Failed to stop docker-compose environment."
    }
    Write-ColoredOutput -Color $Green -Text "Cleaned up."
}

# Function to show the status of the environment
function Show-Status {
    Write-ColoredOutput -Color $Cyan -Text "Showing status..."
    docker-compose -f "infrastructure/docker/docker-compose.yml" ps
    kubectl get pods -n ai-research-platform
    Write-ColoredOutput -Color $Green -Text "Status displayed."
}

# Function to display logs
function Show-Logs {
    param(
        [string]$Service
    )
    Write-ColoredOutput -Color $Cyan -Text "Showing logs for service: $($Service)..."
    if ($Service) {
        docker-compose -f "infrastructure/docker/docker-compose.yml" logs -f $Service
    }
    else {
       docker-compose -f "infrastructure/docker/docker-compose.yml" logs --tail=100
    }
}

# Function to display help
function Show-Help {
    Write-ColoredOutput -Color $Yellow -Text "Usage: deploy.ps1 [options]"
    Write-ColoredOutput -Color $Yellow -Text "Options:"
    Write-ColoredOutput -Color $Yellow -Text "  dev          Start the platform in development mode using Docker Compose"
    Write-ColoredOutput -Color $Yellow -Text "  build        Build all Docker images"
    Write-ColoredOutput -Color $Yellow -Text "  deploy-k8s   Deploy to Kubernetes cluster"
    Write-ColoredOutput -Color $Yellow -Text "  stop-dev     Stop development environment"
    Write-ColoredOutput -Color $Yellow -Text "  clean        Remove all containers and volumes"
    Write-ColoredOutput -Color $Yellow -Text "  status       Show status of running services"
    Write-ColoredOutput -Color $Yellow -Text "  logs         Show logs for all services"
    Write-ColoredOutput -Color $Yellow -Text "  -logs <service> Show logs of a specific service"
    Write-ColoredOutput -Color $Yellow -Text "  -help        Show this help message"
}

# Main script logic
if ($args.Count -eq 0) {
    Show-Help
    exit 0
}

switch ($args[0]) {
    "dev" { Start-DevEnvironment }
    "stop-dev" { Stop-DevEnvironment }
    "build" { Build-Images }
    "deploy-k8s" { Deploy-Kubernetes }
    "clean" { Clean-Up }
    "status" { Show-Status }
    "logs" {
        if ($args.count -eq 2) {
            Show-Logs -Service $args[1]
        }
        else {
            Show-Logs
        }
    }
    "help" { Show-Help }
    default {
        Write-ColoredOutput -Color $Red -Text "Invalid option: $($args[0])"
        Show-Help
        exit 1
    }
}
