# Hybrid API Automation Framework

A comprehensive, flexible framework for API automation testing that supports multiple approaches and tools.

## Features

- **Multi-Protocol Support**: REST, GraphQL, SOAP
- **Multiple Testing Approaches**: 
  - Behavior Driven Development (BDD) with Cucumber
  - Test-Driven Development (TDD)
  - Data-Driven Testing
  - Keyword-Driven Testing
- **Framework Options**:
  - REST Assured (Java)
  - Pytest (Python)
  - Newman (Postman Collections)
  - Karate Framework
- **Reporting**: Allure, Extent, HTML reports
- **CI/CD Integration**: Jenkins, GitHub Actions, GitLab CI
- **Data Management**: Excel, JSON, CSV, Database
- **Environment Management**: Multi-environment support

## Project Structure

```
hybridFramework/
├── src/
│   ├── main/
│   │   ├── java/           # Java-based tests (REST Assured)
│   │   ├── python/         # Python-based tests (Pytest)
│   │   ├── javascript/     # JavaScript-based tests
│   │   └── resources/
│ │       ├── config/       # Configuration files
│ │       ├── data/         # Test data files
│ │       └── postman/      # Postman collections
├── tests/
│   ├── bdd/               # BDD scenarios
│   ├── api/               # API test specifications
│   └── integration/       # Integration tests
├── reports/               # Test reports
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## Quick Start

1. **Setup Environment**:
   ```bash
   # Install dependencies
   npm install
   pip install -r requirements.txt
   mvn clean install
   ```

2. **Run Tests**:
   ```bash
   # Run all tests
   npm run test:all
   
   # Run specific framework
   npm run test:restassured
   npm run test:pytest
   npm run test:postman
   ```

3. **Generate Reports**:
   ```bash
   npm run report:generate
   ```

## Configuration

Edit `config/environment.json` to configure your environments:
```json
{
  "dev": {
    "baseUrl": "https://api-dev.example.com",
    "timeout": 30000
  },
  "staging": {
    "baseUrl": "https://api-staging.example.com",
    "timeout": 30000
  },
  "prod": {
    "baseUrl": "https://api.example.com",
    "timeout": 30000
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tests
4. Submit a pull request

## License

MIT License 