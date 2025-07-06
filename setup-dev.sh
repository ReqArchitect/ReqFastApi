#!/bin/bash

# Development Setup Script for FastAPI Microservices
# This script sets up the development environment with pre-commit hooks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up development environment for FastAPI Microservices${NC}"
echo "================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+ first.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo -e "${RED}❌ pip is not installed. Please install pip first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker is not installed. Some features may not work.${NC}"
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose is not installed. Some features may not work.${NC}"
fi

echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo -e "${BLUE}🔧 Installing pre-commit hooks...${NC}"
pre-commit install

echo -e "${BLUE}🔍 Running initial pre-commit checks...${NC}"
pre-commit run --all-files

echo -e "${BLUE}🧪 Testing microservices structure...${NC}"
python3 test_microservices.py

echo -e "${BLUE}🔍 Validating Docker Compose configuration...${NC}"
docker-compose config --quiet

echo -e "${GREEN}✅ Development environment setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Make your changes to the code"
echo "2. Pre-commit hooks will run automatically on commit"
echo "3. Run 'pre-commit run --all-files' to check all files"
echo "4. Run 'docker-compose up' to start the services"
echo "5. Run './healthcheck.sh' to verify all services are healthy"
echo ""
echo -e "${BLUE}🔧 Available commands:${NC}"
echo "- pre-commit run --all-files    # Run all pre-commit hooks"
echo "- python3 test_microservices.py # Test microservices structure"
echo "- docker-compose up             # Start all services"
echo "- ./healthcheck.sh              # Check service health"
echo "- docker-compose down           # Stop all services" 