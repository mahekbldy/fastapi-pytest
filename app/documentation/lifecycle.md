```bash
Test Session Start
│
├── pytest_addoption        🔧 Add custom CLI options
├── pytest_configure        🧠 Setup config or environment
├── pytest_sessionstart     🚀 Session initialization
│
├── pytest_collection_modifyitems 🗃️ Modify selected test cases
│
├── For each test:
│   ├── pytest_runtest_setup   🔧 Before test runs
│   ├── pytest_runtest_call    🧪 Actual test runs here
│   └── pytest_runtest_teardown🧹 Cleanup after test
│
├── pytest_sessionfinish   ✅ After all tests finish
└── pytest_unconfigure     🧹 Final cleanup
```