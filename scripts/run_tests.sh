#!/bin/bash

# Hybrid API Automation Framework - Test Runner Script
# This script runs tests across different frameworks and generates reports

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-dev}
FRAMEWORK=${2:-all}
PARALLEL=${3:-false}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Hybrid API Automation Framework${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Environment: ${GREEN}$ENVIRONMENT${NC}"
echo -e "Framework: ${GREEN}$FRAMEWORK${NC}"
echo -e "Parallel: ${GREEN}$PARALLEL${NC}"
echo ""

# Function to print section headers
print_section() {
    echo -e "${YELLOW}$1${NC}"
    echo "----------------------------------------"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_section "Checking Prerequisites"
    
    local missing_deps=()
    
    if ! command_exists java; then
        missing_deps+=("Java")
    fi
    
    if ! command_exists mvn; then
        missing_deps+=("Maven")
    fi
    
    if ! command_exists python3; then
        missing_deps+=("Python 3")
    fi
    
    if ! command_exists pip3; then
        missing_deps+=("pip3")
    fi
    
    if ! command_exists node; then
        missing_deps+=("Node.js")
    fi
    
    if ! command_exists npm; then
        missing_deps+=("npm")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}Missing dependencies:${NC}"
        printf '%s\n' "${missing_deps[@]}"
        echo -e "${RED}Please install missing dependencies and try again.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All prerequisites are installed.${NC}"
}

# Install dependencies
install_dependencies() {
    print_section "Installing Dependencies"
    
    echo "Installing Node.js dependencies..."
    npm install
    
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
    
    echo "Installing Maven dependencies..."
    mvn clean install -DskipTests
    
    echo -e "${GREEN}Dependencies installed successfully.${NC}"
}

# Run REST Assured tests
run_rest_assured_tests() {
    print_section "Running REST Assured Tests"
    
    if [ "$PARALLEL" = "true" ]; then
        mvn test -Dtest=TestRunner -Dparallel=classes -DthreadCount=4 -Denv=$ENVIRONMENT
    else
        mvn test -Dtest=TestRunner -Denv=$ENVIRONMENT
    fi
    
    echo -e "${GREEN}REST Assured tests completed.${NC}"
}

# Run Python tests
run_python_tests() {
    print_section "Running Python Tests"
    
    if [ "$PARALLEL" = "true" ]; then
        python3 -m pytest src/main/python/tests/ -v --html=reports/pytest-report.html --self-contained-html -n auto
    else
        python3 -m pytest src/main/python/tests/ -v --html=reports/pytest-report.html --self-contained-html
    fi
    
    echo -e "${GREEN}Python tests completed.${NC}"
}

# Run Postman tests
run_postman_tests() {
    print_section "Running Postman Tests"
    
    if ! command_exists newman; then
        echo "Installing Newman..."
        npm install -g newman
    fi
    
    newman run src/main/resources/postman/collections/User_API_Collection.json \
        -e src/main/resources/postman/environments/$ENVIRONMENT.json \
        --reporters cli,html \
        --reporter-html-export reports/newman-report.html
    
    echo -e "${GREEN}Postman tests completed.${NC}"
}

# Run Karate tests
run_karate_tests() {
    print_section "Running Karate Tests"
    
    mvn test -Dtest=KarateRunner -Denv=$ENVIRONMENT
    
    echo -e "${GREEN}Karate tests completed.${NC}"
}

# Generate reports
generate_reports() {
    print_section "Generating Reports"
    
    # Generate Allure report
    if command_exists allure; then
        allure generate reports/allure-results --clean
        echo "Allure report generated at reports/allure-report"
    fi
    
    # Generate combined HTML report
    echo "Generating combined HTML report..."
    python3 scripts/generate_combined_report.py
    
    echo -e "${GREEN}Reports generated successfully.${NC}"
}

# Main execution
main() {
    # Set environment variable
    export ENV=$ENVIRONMENT
    
    # Check prerequisites
    check_prerequisites
    
    # Install dependencies if needed
    if [ "$4" = "install" ]; then
        install_dependencies
    fi
    
    # Run tests based on framework selection
    case $FRAMEWORK in
        "restassured"|"java")
            run_rest_assured_tests
            ;;
        "python"|"pytest")
            run_python_tests
            ;;
        "postman"|"newman")
            run_postman_tests
            ;;
        "karate")
            run_karate_tests
            ;;
        "all")
            run_rest_assured_tests
            run_python_tests
            run_postman_tests
            run_karate_tests
            ;;
        *)
            echo -e "${RED}Invalid framework: $FRAMEWORK${NC}"
            echo "Valid options: restassured, python, postman, karate, all"
            exit 1
            ;;
    esac
    
    # Generate reports
    generate_reports
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Test execution completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Reports available at:"
    echo "- Allure: reports/allure-report/index.html"
    echo "- Pytest: reports/pytest-report.html"
    echo "- Newman: reports/newman-report.html"
    echo "- Combined: reports/combined-report.html"
}

# Run main function
main "$@" 