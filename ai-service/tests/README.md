# AI Service Tests

This directory contains all tests for the AI Service component.

## Test Files

### Core Tests
- **`test_service.py`** - End-to-end service testing
- **`test_providers.py`** - Multi-provider system testing
- **`test_fallback.py`** - Fallback mechanism testing

### Intelligent Routing Tests
- **`test_complexity_analysis.py`** - Query complexity analysis
- **`test_intelligent_routing.py`** - Provider routing logic
- **`test_final_routing_demo.py`** - Complete routing demonstration

### Specific Feature Tests
- **`test_four_emails.py`** - Email generation testing
- **`test_forced_provider_rotation.py`** - Provider rotation testing

## Running Tests

### Run All Tests
```bash
cd ai-service/tests
python run_tests.py
```

### Run Individual Tests
```bash
cd ai-service/tests
python test_service.py
python test_providers.py
python test_fallback.py
```

### Prerequisites
1. AI service must be running: `python ../main.py`
2. At least one API key configured in `../.env`
3. All dependencies installed: `pip install -r ../requirements.txt`

## Test Categories

### 1. Unit Tests
- `test_complexity_analysis.py` - Tests complexity analysis function

### 2. Integration Tests
- `test_service.py` - Tests API endpoints
- `test_providers.py` - Tests provider integration

### 3. System Tests
- `test_intelligent_routing.py` - Tests end-to-end routing
- `test_final_routing_demo.py` - Demonstrates complete system

### 4. Load Tests
- `test_four_emails.py` - Tests multiple concurrent requests
- `test_forced_provider_rotation.py` - Tests under provider failures

## Expected Results

All tests should pass when:
- ✅ Service is running on http://localhost:8000
- ✅ At least one provider API key is configured
- ✅ Network connectivity is available
- ✅ Provider services are operational

## Troubleshooting

### Common Issues

**"Service not responding"**
- Start the service: `python ../main.py`
- Check port 8000 is available

**"No providers available"**
- Set API keys in `../.env`
- Run `python ../setup_providers.py`

**"All providers failing"**
- Check API key validity
- Verify internet connection
- Check provider service status

### Debug Mode
```bash
export LOG_LEVEL=DEBUG
python test_service.py
```