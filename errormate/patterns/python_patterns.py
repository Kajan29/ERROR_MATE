from errormate.patterns import ErrorPattern


PYTHON_PATTERNS = [
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(ModuleNotFoundError:\s+No module named\s+['\"].+['\"]|ImportError:\s+cannot import name)",
        summary="Python package/module missing",
        meaning="A required Python package or module is not installed or import path is wrong. The interpreter cannot find the module in your virtual environment or system Python.",
        fixes=[
            "Install dependencies with pip install -r requirements.txt",
            "Activate the correct virtual environment: source venv/bin/activate or venv\\\\Scripts\\\\activate",
            "Check module names and local package structure",
            "Verify the package is installed: pip list",
            "Create and activate a virtual environment if not using one",
        ],
    ),
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(SyntaxError:\s+.+|IndentationError:\s+.+)",
        summary="Python syntax error",
        meaning="Python parser found invalid syntax or indentation. Common issues include missing colons, incorrect indentation, or invalid Python syntax.",
        fixes=[
            "Inspect line number from traceback",
            "Fix indentation (Python uses 4 spaces per level, not tabs)",
            "Check for missing colons after if/for/while/def/class statements",
            "Run a formatter like black: black .",
            "Use a linter like pylint or flake8 to highlight syntax issues",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Traceback \(most recent call last\):)",
        summary="Python runtime exception",
        meaning="An exception occurred while running Python code. Check the final exception line for the exact error type and message.",
        fixes=[
            "Read the final exception line for the exact failure",
            "Inspect input values and function assumptions",
            "Add targeted try/except logging around risky code",
            "Check for None values before accessing attributes",
            "Use debugger or print statements to trace variable values",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(psycopg2\.OperationalError|pymysql\.err\.OperationalError|sqlite3\.OperationalError|connection.*?refused)",
        summary="Python database connection failed",
        meaning="Python cannot connect to your database (PostgreSQL, MySQL, SQLite). Check database service, credentials, and connection parameters.",
        fixes=[
            "Verify database host, port, username, and password",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check network/firewall access to the database port",
            "Test connection with database client tools (psql, mysql client)",
            "Verify connection string format in your database configuration",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(KeyError:\s+['\"]?[A-Z0-9_]+['\"]?|os\.environ\[.*\]|ImproperlyConfigured.*?environment)",
        summary="Missing Python environment variable",
        meaning="A required environment variable is missing or undefined. Python cannot access configuration values from os.environ or .env file.",
        fixes=[
            "Check your .env file and variable names",
            "Use python-dotenv or os.getenv() with defaults: os.getenv('PORT', '3000')",
            "Restart the application after changing environment variables",
            "Ensure .env is in project root and loaded: from dotenv import load_dotenv; load_dotenv()",
            "Check variable name casing (environment variables are usually uppercase)",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(OSError.*?address already in use|EADDRINUSE.*?\d+)",
        summary="Python port conflict",
        meaning="Another process is already using the required port. Python web server cannot start.",
        fixes=[
            "Stop the process using the port",
            "Use a different port in your application configuration",
            "Kill the process: fuser -k <port>/tcp or lsof -ti:<port> | xargs kill (Linux/Mac)",
            "Kill the process: netstat -ano | findstr :<port> then taskkill /PID <pid> /F (Windows)",
            "Check for background Python processes",
        ],
    ),
]


DJANGO_PATTERNS = [
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(django\.core\.exceptions\.ImproperlyConfigured:.+|SECRET_KEY setting must not be empty)",
        summary="Django configuration error",
        meaning="Django settings are missing required configuration values like SECRET_KEY, DEBUG, or database settings. The app cannot start.",
        fixes=[
            "Set required variables in .env or settings module",
            "Generate SECRET_KEY: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'",
            "Ensure settings file reads environment variables correctly with os.getenv() or django-environ",
            "Restart the Django server after changes",
            "Check settings.py for missing required settings",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(django\.db\.utils\.OperationalError:.+|could not connect to server: Connection refused)",
        summary="Django database connection failed",
        meaning="Django cannot connect to your database (PostgreSQL, MySQL, SQLite). Check DATABASES settings and database service status.",
        fixes=[
            "Verify DATABASES settings and credentials in settings.py",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Apply migrations after connection is fixed: python manage.py migrate",
            "Test connection with database client tools",
            "Check database user permissions and host accessibility",
        ],
    ),
    ErrorPattern(
        error_type="Migration Error",
        regex=r"(django\.db\.migrations\.exceptions|No migrations to apply|AppRegistryNotReady)",
        summary="Django migration error",
        meaning="Django encountered an issue with database migrations. The database schema is out of sync with your models.",
        fixes=[
            "Run python manage.py makemigrations to create new migrations",
            "Run python manage.py migrate to apply pending migrations",
            "Check for conflicting migrations or database state issues",
            "Use python manage.py showmigrations to check migration status",
            "For fresh start: python manage.py migrate --run-syncdb",
        ],
    ),
    ErrorPattern(
        error_type="Template Error",
        regex=r"(TemplateDoesNotExist|TemplateSyntaxError)",
        summary="Django template error",
        meaning="Django cannot find or parse a template file. Check template directory structure and syntax.",
        fixes=[
            "Verify template exists in the correct templates directory",
            "Check TEMPLATES setting in Django settings for DIRS configuration",
            "Fix template syntax errors (missing tags, invalid filters, unclosed blocks)",
            "Ensure app is in INSTALLED_APPS if using app-specific templates",
            "Check template file extensions (.html, .txt)",
        ],
    ),
]


FASTAPI_PATTERNS = [
    ErrorPattern(
        error_type="Module Import Error",
        regex=r"(ModuleNotFoundError.*?No module named.*?main|ImportError.*?cannot import name.*?app|No module named 'main'|No module named 'app')",
        summary="FastAPI module not found",
        meaning="Uvicorn cannot find the specified module (e.g., main:app) in the uvicorn command. Check file structure and module path.",
        fixes=[
            "Verify the uvicorn command matches your file structure: uvicorn main:app or uvicorn app:app",
            "Ensure the Python file (main.py or app.py) exists in the current directory",
            "Check that the FastAPI app instance is named 'app' in your file",
            "Run from the correct directory containing your main.py/app.py file",
            "Check for Python path issues: PYTHONPATH=. uvicorn main:app",
        ],
    ),
    ErrorPattern(
        error_type="Uvicorn Startup Error",
        regex=r"(uvicorn\.error|AttributeError.*?ASGIApp|TypeError.*?ASGIApp|object has no attribute '__call__')",
        summary="Uvicorn ASGI server startup error",
        meaning="Uvicorn failed to start the ASGI application - the app instance is invalid or not callable. Check FastAPI app creation.",
        fixes=[
            "Ensure you create the FastAPI app correctly: app = FastAPI()",
            "Verify the app is exported/imported correctly in your module",
            "Check for circular imports in your application",
            "Verify uvicorn command syntax: uvicorn main:app --reload",
            "Ensure all dependencies are installed: pip install fastapi uvicorn",
        ],
    ),
    ErrorPattern(
        error_type="FastAPI Validation Error",
        regex=r"(fastapi\.exceptions\.RequestValidationError|pydantic\.ValidationError)",
        summary="FastAPI request validation failed",
        meaning="The request data does not match the expected schema defined by Pydantic models. Check request body and model definitions.",
        fixes=[
            "Check request body, query parameters, and path parameters match the model",
            "Review the Pydantic model definitions for required fields and types",
            "Ensure JSON data is properly formatted",
            "Use Pydantic's Field() to add validation and help text",
            "Check for type mismatches between request and model",
        ],
    ),
    ErrorPattern(
        error_type="FastAPI HTTP Exception",
        regex=r"(fastapi\.exceptions\.HTTPException)",
        summary="FastAPI HTTP exception raised",
        meaning="An HTTP exception was explicitly raised in the endpoint code. Check exception handling logic.",
        fixes=[
            "Check the endpoint code for raise HTTPException statements",
            "Verify the status code and detail message are appropriate",
            "Review the logic that triggers the exception",
            "Use try/except blocks to handle errors gracefully",
            "Check for missing authentication or authorization",
        ],
    ),
    ErrorPattern(
        error_type="FastAPI Starlette Error",
        regex=r"(starlette\.exceptions\.HTTPException|starlette\.exceptions\.|starlette\.routing)",
        summary="Starlette/FastAPI routing or middleware error",
        meaning="An error occurred in Starlette's routing, middleware, or exception handling. Check route definitions and middleware.",
        fixes=[
            "Check route definitions and path parameters",
            "Review middleware configuration and dependencies",
            "Ensure all dependencies are properly injected",
            "Check for duplicate route paths",
            "Verify CORS middleware configuration if needed",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(OSError.*?address already in use.*?8000|EADDRINUSE.*?8000|uvicorn.*?port.*?already in use)",
        summary="FastAPI/Uvicorn port conflict",
        meaning="Another process is already using the default FastAPI port (8000). Uvicorn cannot start.",
        fixes=[
            "Stop the process using port 8000",
            "Use a different port: uvicorn main:app --port 8001",
            "Kill the process: fuser -k 8000/tcp or lsof -ti:8000 | xargs kill (Linux/Mac)",
            "Kill the process: netstat -ano | findstr :8000 then taskkill /PID <pid> /F (Windows)",
            "Check for background uvicorn processes",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(sqlalchemy\.exc\.OperationalError|pymysql\.err\.OperationalError|psycopg2\.OperationalError)",
        summary="FastAPI database connection failed",
        meaning="FastAPI cannot connect to your database via SQLAlchemy. Check database connection string and service status.",
        fixes=[
            "Verify database connection string in settings/environment",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check database credentials and host accessibility",
            "Test connection with database client tools",
            "Verify SQLAlchemy engine configuration",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(KeyError:\s+['\"]?[A-Z0-9_]+['\"]?|pydantic_settings\.BaseSettings\.init|Missing required environment variable)",
        summary="Missing FastAPI environment variable",
        meaning="A required environment variable is missing in Pydantic Settings. The ConfigModule cannot load the variable.",
        fixes=[
            "Check your .env file and variable names",
            "Ensure Pydantic Settings model matches environment variables",
            "Restart the application after changing environment variables",
            "Use @pydantic_settings.BaseSettings with proper field names",
            "Ensure .env is in project root and loaded before app startup",
        ],
    ),
]
