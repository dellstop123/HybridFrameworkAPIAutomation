# Hybrid API Automation Framework Guide

## Overview

The Hybrid API Automation Framework is a comprehensive solution that supports multiple testing approaches and tools for API automation. This guide provides detailed information on how to use the framework effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Framework Architecture](#framework-architecture)
3. [Configuration Management](#configuration-management)
4. [Testing Approaches](#testing-approaches)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Java 11 or higher
- Python 3.9 or higher
- Node.js 16 or higher
- Maven 3.6 or higher

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hybridFramework
```

2. Install dependencies:
```bash
./scripts/run_tests.sh dev all false install
```

3. Verify installation:
```bash
./scripts/run_tests.sh dev all false
```

## Framework Architecture

### Directory Structure

```
hybridFramework/
├── src/main/java/          # Java-based tests (REST Assured)
├── src/main/python/        # Python-based tests (Pytest)
├── src/main/javascript/    # JavaScript-based tests
├── src/main/resources/     # Configuration and test data
├── tests/                  # BDD scenarios and test specifications
├── reports/                # Test reports
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

### Core Components

1. **Configuration Manager**: Centralized configuration management
2. **Base API Client**: Common functionality for API requests
3. **Test Data Management**: Centralized test data handling
4. **Reporting**: Multiple reporting options (Allure, HTML, etc.)

## Configuration Management

### Environment Configuration

The framework supports multiple environments through `src/main/resources/config/environment.json`:

```json
{
  "dev": {
    "baseUrl": "https://api-dev.example.com",
    "timeout": 30000,
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

### Test Data Configuration

Test data is managed in `src/main/resources/config/testdata.json`:

```json
{
  "users": {
    "valid_user": {
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
  }
}
```

### Environment Variables

Set environment variables for sensitive data:

```bash
export STAGING_TOKEN="your-staging-token"
export PROD_TOKEN="your-prod-token"
```

## Testing Approaches

### 1. REST Assured (Java)

#### Basic Usage

```java
public class UserApiTest {
    private UserApiClient userApiClient;
    
    @BeforeClass
    public void setUp() {
        userApiClient = new UserApiClient();
    }
    
    @Test
    public void testGetUser() {
        Response response = userApiClient.getUserById(1);
        Assert.assertEquals(response.getStatusCode(), 200);
    }
}
```

#### Running Tests

```bash
# Run all REST Assured tests
mvn test -Dtest=TestRunner

# Run specific test class
mvn test -Dtest=UserApiTest

# Run with specific environment
mvn test -Dtest=TestRunner -Denv=staging
```

### 2. Pytest (Python)

#### Basic Usage

```python
class TestUserApi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api_client = BaseApiClient()
        self.users_endpoint = "/users"
    
    def test_get_user(self):
        response = self.api_client.get(f"{self.users_endpoint}/1")
        assert response.status_code == 200
```

#### Running Tests

```bash
# Run all Python tests
pytest src/main/python/tests/ -v

# Run with HTML report
pytest src/main/python/tests/ -v --html=reports/pytest-report.html

# Run specific test
pytest src/main/python/tests/test_user_api.py::TestUserApi::test_get_user
```

### 3. Postman/Newman

#### Running Collections

```bash
# Run Postman collection
newman run src/main/resources/postman/collections/User_API_Collection.json \
  -e src/main/resources/postman/environments/dev.json \
  --reporters cli,html
```

### 4. BDD with Cucumber

#### Feature Files

```gherkin
Feature: User Management
  Scenario: Get user by ID
    Given a user with ID "1" exists
    When I send a GET request to "/users/1"
    Then the response status code should be 200
```

#### Step Definitions

```java
@Given("a user with ID {string} exists")
public void aUserWithIdExists(String userId) {
    // Implementation
}

@When("I send a GET request to {string}")
public void iSendAGetRequestTo(String endpoint) {
    // Implementation
}
```

## Best Practices

### 1. Test Organization

- Organize tests by API resource (users, posts, comments)
- Use descriptive test names
- Group related tests in the same class/file

### 2. Data Management

- Use centralized test data configuration
- Avoid hardcoding test data in tests
- Use data-driven testing for multiple scenarios

### 3. Error Handling

- Always validate response status codes
- Include proper error assertions
- Log relevant information for debugging

### 4. Performance

- Set appropriate timeouts
- Use parallel execution when possible
- Monitor response times

### 5. Reporting

- Generate comprehensive reports
- Include screenshots for UI tests
- Archive reports for historical analysis

### 6. Environment Management

- Use environment-specific configurations
- Keep sensitive data in environment variables
- Validate environment setup before running tests

## Test Execution

### Using the Test Runner Script

```bash
# Run all tests
./scripts/run_tests.sh dev all false

# Run specific framework
./scripts/run_tests.sh dev restassured false

# Run with parallel execution
./scripts/run_tests.sh dev all true

# Install dependencies and run tests
./scripts/run_tests.sh dev all false install
```

### Command Line Options

- `ENVIRONMENT`: dev, staging, prod, local
- `FRAMEWORK`: restassured, python, postman, karate, all
- `PARALLEL`: true, false
- `INSTALL`: install (optional)

### CI/CD Integration

The framework includes GitHub Actions workflow for automated testing:

```yaml
name: API Automation Tests
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

## Reporting

### Available Reports

1. **Allure Reports**: Rich HTML reports with detailed test information
2. **Pytest HTML Reports**: Self-contained HTML reports
3. **Newman Reports**: Postman collection execution reports
4. **Combined Reports**: Aggregated reports from all frameworks

### Accessing Reports

After test execution, reports are available in the `reports/` directory:

- `reports/allure-report/index.html`
- `reports/pytest-report.html`
- `reports/newman-report.html`
- `reports/combined-report.html`

## Troubleshooting

### Common Issues

1. **Configuration Not Found**
   - Verify configuration files exist
   - Check file paths in ConfigManager

2. **Dependencies Missing**
   - Run installation script
   - Check prerequisite versions

3. **Environment Variables**
   - Verify environment variables are set
   - Check token validity

4. **Network Issues**
   - Verify API endpoints are accessible
   - Check firewall settings

### Debug Mode

Enable debug logging:

```bash
# Java
mvn test -Dtest=TestRunner -Dlog.level=DEBUG

# Python
pytest -v --log-cli-level=DEBUG

# Newman
newman run collection.json --verbose
```

### Getting Help

1. Check the logs in `reports/` directory
2. Review configuration files
3. Verify environment setup
4. Consult framework documentation

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests for new features
3. Update documentation
4. Follow coding standards
5. Submit pull requests with detailed descriptions

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review existing documentation
3. Create detailed issue reports
4. Provide reproduction steps 