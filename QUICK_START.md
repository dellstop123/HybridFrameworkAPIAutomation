# Quick Start Guide - Hybrid API Automation Framework

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites Check

Ensure you have the following installed:
- Java 11+ (`java -version`)
- Python 3.9+ (`python3 --version`)
- Node.js 16+ (`node --version`)
- Maven 3.6+ (`mvn --version`)

### 2. Setup Framework

```bash
# Clone and navigate to the framework
git clone <repository-url>
cd hybridFramework

# Make the test runner executable
chmod +x scripts/run_tests.sh

# Install all dependencies
./scripts/run_tests.sh dev all false install
```

### 3. Run Your First Test

```bash
# Run all tests (REST Assured + Python + Postman)
./scripts/run_tests.sh dev all false

# Or run specific framework
./scripts/run_tests.sh dev restassured false  # Java/REST Assured only
./scripts/run_tests.sh dev python false       # Python/Pytest only
./scripts/run_tests.sh dev postman false      # Postman/Newman only
```

### 4. View Reports

After test execution, check the reports:
- **Allure Report**: `reports/allure-report/index.html`
- **Pytest Report**: `reports/pytest-report.html`
- **Newman Report**: `reports/newman-report.html`

## 📁 Project Structure

```
hybridFramework/
├── src/main/java/          # Java tests (REST Assured)
├── src/main/python/        # Python tests (Pytest)
├── src/main/resources/     # Config & test data
├── tests/bdd/              # BDD scenarios
├── scripts/                # Utility scripts
└── reports/                # Test reports
```

## ⚙️ Configuration

### Environment Setup

Edit `src/main/resources/config/environment.json`:

```json
{
  "dev": {
    "baseUrl": "https://jsonplaceholder.typicode.com",
    "timeout": 30000
  }
}
```

### Test Data

Edit `src/main/resources/config/testdata.json`:

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

## 🧪 Writing Tests

### Java (REST Assured)

```java
@Test
public void testGetUser() {
    UserApiClient client = new UserApiClient();
    Response response = client.getUserById(1);
    Assert.assertEquals(response.getStatusCode(), 200);
}
```

### Python (Pytest)

```python
def test_get_user(self):
    response = self.api_client.get("/users/1")
    assert response.status_code == 200
```

### BDD (Cucumber)

```gherkin
Scenario: Get user by ID
  Given a user with ID "1" exists
  When I send a GET request to "/users/1"
  Then the response status code should be 200
```

## 🔧 Common Commands

```bash
# Run tests with different environments
./scripts/run_tests.sh dev all false    # Development
./scripts/run_tests.sh staging all false # Staging
./scripts/run_tests.sh prod all false   # Production

# Run with parallel execution
./scripts/run_tests.sh dev all true

# Run specific framework
./scripts/run_tests.sh dev restassured false
./scripts/run_tests.sh dev python false
./scripts/run_tests.sh dev postman false

# Clean and reinstall
./scripts/run_tests.sh dev all false install
```

## 📊 Available Reports

1. **Allure**: Rich interactive reports
2. **Pytest HTML**: Self-contained HTML reports
3. **Newman**: Postman collection reports
4. **Combined**: Aggregated framework reports

## 🐛 Troubleshooting

### Common Issues

1. **Dependencies Missing**
   ```bash
   ./scripts/run_tests.sh dev all false install
   ```

2. **Configuration Errors**
   - Check `src/main/resources/config/` files
   - Verify environment variables

3. **Network Issues**
   - Verify API endpoints are accessible
   - Check firewall settings

### Debug Mode

```bash
# Java debug
mvn test -Dtest=TestRunner -Dlog.level=DEBUG

# Python debug
pytest -v --log-cli-level=DEBUG

# Newman debug
newman run collection.json --verbose
```

## 📚 Next Steps

1. **Read the Full Guide**: `docs/FRAMEWORK_GUIDE.md`
2. **Explore Examples**: Check test files in `src/main/`
3. **Customize Configuration**: Modify config files for your APIs
4. **Add Your Tests**: Create new test classes/files
5. **Set Up CI/CD**: Use the provided GitHub Actions workflow

## 🆘 Need Help?

- Check the troubleshooting section
- Review the comprehensive guide
- Check logs in the `reports/` directory
- Verify your environment setup

---

**Happy Testing! 🎉** 