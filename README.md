# Test Case Management

### Introduction
This project is a FastAPI-based web application that provides endpoints for managing users, test cases, and execution results.

### Installation
1. Clone project
```bash
git clone https://github.com/MarioMedWilson/TestCaseManager.git
```

2. Change into the project directory
```bash
cd TestCaseManager
```

3. Create a virtual environment
```bash
python -m venv venv
```

4. Activate the virtual environment
```bash
source venv/bin/activate
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Run script
```bash
uvicorn main:app --reload
```

### Docker option
- Build project
```bash
docker build -t testcase-project .
```

- Run 
```bash
docker run -p 8000:8000 testcase-project
```
