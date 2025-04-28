#!/bin/bash

# AI Research Platform Deployment Script
# This script helps with the deployment of the AI Research Platform

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}   AI Research Platform Deployment Tool  ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Function to display help
function show_help {
    echo -e "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  dev             - Start the platform in development mode using Docker Compose"
    echo "  build           - Build all Docker images"
    echo "  deploy-k8s      - Deploy to Kubernetes cluster"
    echo "  stop-dev        - Stop development environment"
    echo "  clean           - Remove all containers and volumes"
    echo "  status          - Show status of running services"
    echo "  logs [service]  - Show logs for a specific service or all services"
    echo "  help            - Show this help message"
    echo ""
}

# Function to start development environment
function start_dev {
    echo -e "${YELLOW}Starting development environment...${NC}"
    cd infrastructure/docker
    docker-compose up -d
    echo -e "${GREEN}Development environment started!${NC}"
    echo -e "Research Dashboard: http://localhost:3000"
    echo -e "Web Generator: http://localhost:3001"
    echo -e "API Gateway: http://localhost:8000"
    echo -e "MinIO Console: http://localhost:9001"
}

# Function to build all Docker images
function build_images {
    echo -e "${YELLOW}Building Docker images...${NC}"
    cd infrastructure/docker
    docker-compose build
    echo -e "${GREEN}Docker images built successfully!${NC}"
}

# Function to deploy to Kubernetes
function deploy_k8s {
    echo -e "${YELLOW}Deploying to Kubernetes...${NC}"
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}kubectl is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Check if kustomize is installed
    if ! command -v kustomize &> /dev/null; then
        echo -e "${YELLOW}kustomize is not installed. Using kubectl apply -k instead.${NC}"
        kubectl apply -k infrastructure/kubernetes
    else
        cd infrastructure/kubernetes
        kustomize build | kubectl apply -f -
    fi
    
    echo -e "${GREEN}Deployment to Kubernetes completed!${NC}"
    echo -e "Use 'kubectl get pods -n ai-research-platform' to check the status of the pods."
}

# Function to stop development environment
function stop_dev {
    echo -e "${YELLOW}Stopping development environment...${NC}"
    cd infrastructure/docker
    docker-compose down
    echo -e "${GREEN}Development environment stopped!${NC}"
}

# Function to clean up
function clean_env {
    echo -e "${YELLOW}Cleaning up containers and volumes...${NC}"
    cd infrastructure/docker
    docker-compose down -v
    echo -e "${GREEN}Cleanup completed!${NC}"
}

# Function to show status
function show_status {
    echo -e "${YELLOW}Showing status of services...${NC}"
    cd infrastructure/docker
    docker-compose ps
}

# Function to show logs
function show_logs {
    if [ -z "$1" ]; then
        echo -e "${YELLOW}Showing logs for all services...${NC}"
        cd infrastructure/docker
        docker-compose logs --tail=100
    else
        echo -e "${YELLOW}Showing logs for $1...${NC}"
        cd infrastructure/docker
        docker-compose logs --tail=100 $1
    fi
}

# Main script logic
case "$1" in
    dev)
        start_dev
        ;;
    build)
        build_images
        ;;
    deploy-k8s)
        deploy_k8s
        ;;
    stop-dev)
        stop_dev
        ;;
    clean)
        clean_env
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs $2
        ;;
    help|*)
        show_help
        ;;
esac
