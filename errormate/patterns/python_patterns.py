from errormate.patterns import ErrorPattern


PYTHON_PATTERNS = [
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(ModuleNotFoundError:\s+No module named\s+['\"].+['\"]|ImportError:\s+cannot import name)",
        summary="Python package/module missing",
        meaning="A required Python package or module is missing or import path is wrong.",
        fixes=[
            "Install dependencies with pip install -r requirements.txt.",
            "Activate the correct virtual environment.",
            "Check module names and local package structure.",
        ],
    ),
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(SyntaxError:\s+.+|IndentationError:\s+.+)",
        summary="Python syntax error",
        meaning="Python parser found invalid syntax or indentation.",
        fixes=[
            "Inspect line number from traceback.",
            "Fix indentation and punctuation.",
            "Run a formatter like black.",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Traceback \(most recent call last\):)",
        summary="Python runtime exception",
        meaning="An exception occurred while running Python code.",
        fixes=[
            "Read the final exception line for the exact failure.",
            "Inspect input values and function assumptions.",
            "Add targeted try/except logging around risky code.",
        ],
    ),
]


DJANGO_PATTERNS = [
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(django\.core\.exceptions\.ImproperlyConfigured:.+|SECRET_KEY setting must not be empty)",
        summary="Django configuration error",
        meaning="Django settings are missing required configuration values.",
        fixes=[
            "Set required variables in .env or settings module.",
            "Ensure settings file reads environment variables correctly.",
            "Restart the Django server after changes.",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(django\.db\.utils\.OperationalError:.+|could not connect to server: Connection refused)",
        summary="Django database connection failed",
        meaning="Django could not connect to the configured database.",
        fixes=[
            "Verify DATABASES settings and credentials.",
            "Check that the database service is running.",
            "Apply migrations after connection is fixed.",
        ],
    ),
]
