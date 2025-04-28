# AI Research Platform

A comprehensive full-stack development platform for Agentive AI research, focusing on humanistic, scientific, and business applications.

## Overview

This platform integrates all the necessary tools and functionalities to create an Agentive AI dedicated to humanistic, scientific, and business research, with a focus on:

- **Data Management**: Data mining, crawling, scraping, collection, preprocessing, and storage in data lakes for both data management and ML training/validation.
- **Machine Learning Models**: Creation, training, and evaluation of models (NLP, computer vision, etc.).
- **API Management**: Complete management of APIs for inference and interaction with external products/tools.
- **Research Process Management**: Features for managing research processes and projects, including interactive dashboards, process automation, and website creation.

The platform uses Docker containers with docker-compose and Kubernetes orchestration to implement a microservices architecture. Everything that can be containerized is containerized.

## Architecture

The platform is built with a microservices architecture, with the following main components:

### Data Collection Services
- **Data Crawler**: Crawls websites and collects data.
- **Data Scraper**: Scrapes structured data from websites.

### Data Processing Services
- **Data Preprocessor**: Preprocesses data for machine learning.
- **Data Transformer**: Transforms data into different formats.

### Data Storage Services
- **MongoDB**: Stores unstructured data.
- **PostgreSQL**: Stores structured data.
- **MinIO**: Stores large files and datasets.

### Machine Learning Framework
- **ML Trainer**: Trains machine learning models.
- **ML Evaluator**: Evaluates machine learning models.

### API Gateway
- **API Gateway**: Provides a unified API for all services.

### Research Dashboard
- **Research Dashboard**: Provides a user interface for managing research projects.

### Web Generator
- **Web Generator**: Generates websites and web applications.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes (optional, for production deployment)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-research-platform.git
   cd ai-research-platform
   ```

2. Start the platform in development mode:
   ```bash
   ./deploy.sh dev
   ```

3. Access the Research Dashboard:
   ```
   http://localhost:3000
   ```

### Deployment

#### Development Environment

To start the platform in development mode:

```bash
./deploy.sh dev
```

#### Production Environment

To deploy the platform to a Kubernetes cluster:

```bash
./deploy.sh deploy-k8s
```

### Usage

#### Research Dashboard

The Research Dashboard provides a user interface for managing research projects. You can:

- Create and manage data collection jobs
- Preprocess and transform data
- Train and evaluate machine learning models
- Generate websites and web applications

#### API Gateway

The API Gateway provides a unified API for all services. You can:

- Create and manage data collection jobs
- Preprocess and transform data
- Train and evaluate machine learning models
- Generate websites and web applications

## Development

### Project Structure

```
.
├── deploy.sh                      # Deployment script
├── infrastructure/                # Infrastructure configuration
│   ├── docker/                    # Docker Compose configuration
│   └── kubernetes/                # Kubernetes configuration
└── services/                      # Microservices
    ├── api-gateway/               # API Gateway service
    ├── data-collection/           # Data Collection services
    │   ├── crawler/               # Data Crawler service
    │   └── scraper/               # Data Scraper service
    ├── data-processing/           # Data Processing services
    │   ├── preprocessor/          # Data Preprocessor service
    │   └── transformer/           # Data Transformer service
    ├── ml-framework/              # Machine Learning Framework services
    │   ├── trainer/               # ML Trainer service
    │   └── evaluator/             # ML Evaluator service
    ├── research-dashboard/        # Research Dashboard service
    └── web-generator/             # Web Generator service
```

### Adding a New Service

To add a new service:

1. Create a new directory in the appropriate services directory.
2. Create a Dockerfile for the service.
3. Add the service to the Docker Compose configuration.
4. Add the service to the Kubernetes configuration.
5. Update the API Gateway to include the new service.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)
- [MongoDB](https://www.mongodb.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [MinIO](https://min.io/)
