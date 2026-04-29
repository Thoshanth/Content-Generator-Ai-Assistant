# Testing Documentation

This directory contains integration and end-to-end tests for the Creo AI Content Generation Platform.

## 📁 Test Organization

### Root Tests Directory (`/tests`)
Contains cross-service integration and end-to-end tests:

- **test_end_to_end.py** - Complete workflow tests across all services
- **test_integration.py** - Integration tests between services
- **test_frontend_backend.html** - Frontend-backend integration tests
- **test_openrouter_models.py** - OpenRouter model testing
- **test-login.ps1** - PowerShell login test script
- **wait_for_index.py** - Utility for waiting on service startup

### AI Service Tests (`/ai-service/tests`)
Contains Python tests for the FastAPI AI service:

**Test Runners:**
- `run_all_tests.py` - Execute all test suites
- `run_tests.py` - Standard test runner
- `run_tests_simple.py` - Simplified test runner

**Provider Tests:**
- `test_all_providers.py` - Test all AI providers
- `test_providers.py` - Provider functionality tests
- `test_providers_fixed.py` - Fixed provider tests
- `test_fallback.py` - Provider fallback mechanism

**Routing Tests:**
- `test_intelligent_routing.py` - Smart provider routing
- `test_final_routing_demo.py` - Routing demonstration
- `test_forced_provider_rotation.py` - Provider rotation tests
- `test_complexity_analysis.py` - Content complexity analysis

**Feature Tests:**
- `test_v5_features.py` - Version 5 features
- `test_service.py` - Core service functionality
- `test_non_streaming_endpoint.py` - Non-streaming endpoints
- `test_pdf_export.py` - PDF export functionality
- `test_resume_quick.py` - Quick resume generation
- `test_four_emails.py` - Email generation tests

**Documentation:**
- `TESTING_GUIDE.md` - Comprehensive testing guide
- `README.md` - AI service test documentation

### Frontend Tests (`/frontend/src/test`)
Contains React component and integration tests:

- **FollowUpQuestions.test.jsx** - Follow-up questions component tests
- **FollowUpQuestionsDemo.jsx** - Demo component for testing follow-up questions

### Backend Tests (`/backend/src/test/java`)
Contains Java/Spring Boot tests:

Located in standard Maven test directory structure:
- Unit tests for controllers, services, and models
- Integration tests for API endpoints
- Security and authentication tests

## 🚀 Running Tests

### AI Service Tests
```bash
cd ai-service
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run all tests
python tests/run_all_tests.py

# Run specific test
python -m pytest tests/test_providers.py

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Backend Tests
```bash
cd backend

# Run all tests
./mvnw test

# Run specific test class
./mvnw test -Dtest=AuthControllerTest

# Run with coverage
./mvnw test jacoco:report
```

### Frontend Tests
```bash
cd frontend

# Run all tests
npm run test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

### Integration Tests
```bash
# From root directory
cd tests

# Run Python integration tests
python test_integration.py
python test_end_to_end.py

# Run HTML integration tests (open in browser)
# Open test_frontend_backend.html in a browser
```

## 📊 Test Coverage Goals

- **AI Service**: 80%+ coverage
- **Backend**: 75%+ coverage
- **Frontend**: 70%+ coverage
- **Integration**: All critical paths covered

## 🧪 Test Types

### Unit Tests
- Test individual functions and components in isolation
- Mock external dependencies
- Fast execution

### Integration Tests
- Test interaction between components
- Use test databases/services
- Moderate execution time

### End-to-End Tests
- Test complete user workflows
- Use real services (or staging)
- Slower execution

## 📝 Writing New Tests

### AI Service (Python/Pytest)
```python
import pytest
from services.ai_client import AIClient

def test_content_generation():
    client = AIClient()
    result = client.generate_content(
        prompt="Test prompt",
        content_type="email"
    )
    assert result is not None
    assert len(result) > 0
```

### Backend (Java/JUnit)
```java
@Test
public void testUserRegistration() {
    RegisterRequest request = new RegisterRequest();
    request.setEmail("test@example.com");
    request.setUsername("testuser");
    
    ResponseEntity<?> response = authController.register(request);
    assertEquals(HttpStatus.OK, response.getStatusCode());
}
```

### Frontend (Jest/React Testing Library)
```javascript
import { render, screen } from '@testing-library/react';
import FollowUpQuestions from './FollowUpQuestions';

test('renders follow-up questions', () => {
  render(<FollowUpQuestions questions={['Q1', 'Q2']} />);
  expect(screen.getByText('Q1')).toBeInTheDocument();
});
```

## 🔧 Test Configuration

### AI Service
- **Framework**: Pytest
- **Config**: `pytest.ini` or `pyproject.toml`
- **Fixtures**: Defined in `conftest.py`

### Backend
- **Framework**: JUnit 5
- **Config**: `pom.xml` (Maven)
- **Properties**: `application-test.properties`

### Frontend
- **Framework**: Jest + React Testing Library
- **Config**: `jest.config.js`
- **Setup**: `setupTests.js`

## 📚 Additional Resources

- [AI Service Testing Guide](../ai-service/tests/TESTING_GUIDE.md)
- [Main Testing Guide](../TESTING_GUIDE.md)
- [Setup Guide](../SETUP_GUIDE.md)

## 🐛 Troubleshooting

### Common Issues

**AI Service Tests Failing:**
- Ensure API keys are set in `.env`
- Check if services are running
- Verify Python dependencies are installed

**Backend Tests Failing:**
- Check Firebase credentials
- Ensure test database is accessible
- Verify Java version (17+)

**Frontend Tests Failing:**
- Clear node_modules and reinstall
- Check for missing dependencies
- Verify React version compatibility

## 🎯 Best Practices

1. **Write tests before fixing bugs** - Reproduce the bug in a test first
2. **Keep tests independent** - Each test should run in isolation
3. **Use descriptive names** - Test names should explain what they test
4. **Mock external services** - Don't rely on external APIs in unit tests
5. **Test edge cases** - Include boundary conditions and error scenarios
6. **Maintain test data** - Keep test fixtures up to date
7. **Run tests before commits** - Ensure all tests pass before pushing

## 📈 Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branch
- Scheduled nightly builds

CI/CD pipeline configuration:
- GitHub Actions: `.github/workflows/`
- Test reports generated automatically
- Coverage reports published

---

**Last Updated**: April 30, 2026
