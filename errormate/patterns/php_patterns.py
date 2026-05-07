from errormate.patterns import ErrorPattern


PHP_PATTERNS = [
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(PHP Parse error:\s+.+|Parse error:\s+syntax error,.+)",
        summary="PHP syntax error",
        meaning="PHP parser detected invalid syntax in your code. Common issues include missing semicolons, brackets, or malformed statements.",
        fixes=[
            "Check the file and line in the error output",
            "Fix missing semicolons, brackets, or malformed statements",
            "Run php -l on the file for quick syntax validation: php -l filename.php",
            "Check for unclosed braces, parentheses, or quotes",
            "Verify variable naming conventions",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Fatal error:\s+Uncaught\s+.+)",
        summary="PHP fatal runtime error",
        meaning="Application crashed due to an unhandled PHP runtime error. Check stack trace for the failing class/method.",
        fixes=[
            "Read stack trace and inspect failing class/method",
            "Validate null checks and type assumptions",
            "Enable detailed Laravel logs: php artisan log:clear && tail -f storage/logs/laravel.log",
            "Add try/catch blocks to handle exceptions gracefully",
            "Check for undefined variables or array keys",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Class\s+.+\s+not found|composer could not find a matching version)",
        summary="PHP class or Composer package missing",
        meaning="Required class autoloading or Composer package resolution failed. The class or package cannot be found.",
        fixes=[
            "Run composer install and composer dump-autoload",
            "Verify namespace and class file paths match PSR-4 autoloading standards",
            "Check package version constraints in composer.json",
            "Clear Composer cache: composer clear-cache",
            "Ensure vendor directory exists and is not in .gitignore",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(SQLSTATE\[[0-9A-Z]+\]\s*\[[0-9]+\].+|mysqli_connect\(\)|PDO Connection failed)",
        summary="PHP database connection failed",
        meaning="PHP cannot connect to your database (MySQL, PostgreSQL, SQLite). Check database service and connection settings.",
        fixes=[
            "Verify database host, port, username, and password",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check database credentials and host accessibility",
            "Test connection with database client tools (mysql, psql)",
            "Verify PDO extension is enabled: php -m | grep pdo",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(Undefined index|Undefined variable|getenv\(\))",
        summary="Missing PHP environment variable",
        meaning="A required environment variable or array index is missing. PHP cannot access configuration values.",
        fixes=[
            "Check your .env file and variable names",
            "Use isset() or null coalescing operator ?? for safety: $_GET['id'] ?? null",
            "Restart the PHP-FPM or web server after changes",
            "Ensure .env is loaded with vlucas/phpdotenv or similar",
            "Check for typos in variable names",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(Address already in use.*?8000|Address already in use.*?9000)",
        summary="PHP port conflict",
        meaning="Another process is already using the required PHP server port. The built-in server cannot start.",
        fixes=[
            "Stop the process using the port",
            "Use a different port: php -S localhost:8001",
            "Kill the process: lsof -ti:8000 | xargs kill (Linux/Mac)",
            "Kill the process: netstat -ano | findstr :8000 then taskkill /PID <pid> /F (Windows)",
            "Check for background PHP processes",
        ],
    ),
]


LARAVEL_PATTERNS = [
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(No application encryption key has been specified|APP_KEY|.env file missing)",
        summary="Laravel environment configuration error",
        meaning="Laravel is missing required application environment configuration like APP_KEY. The app cannot start securely.",
        fixes=[
            "Create/update .env from .env.example: cp .env.example .env",
            "Run php artisan key:generate to generate APP_KEY",
            "Clear config cache with php artisan config:clear",
            "Ensure .env is in project root and not in .gitignore",
            "Restart the Laravel server after changes",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(SQLSTATE\[[0-9A-Z]+\]\s*\[[0-9]+\].+|Connection refused)",
        summary="Laravel database connection failed",
        meaning="Laravel cannot connect to your database (MySQL, PostgreSQL, SQLite). Check DB_* values in .env and database service status.",
        fixes=[
            "Verify DB_* values in .env (DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD)",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check database user permissions and host accessibility",
            "Test connection with database client tools",
            "Run php artisan migrate after connection is fixed",
        ],
    ),
    ErrorPattern(
        error_type="Migration Error",
        regex=r"(SQLSTATE\[42S02\]|Base table or view not found|Migration table not found)",
        summary="Laravel migration error",
        meaning="Laravel encountered an issue with database migrations or table structure. The database schema is out of sync.",
        fixes=[
            "Run php artisan migrate to apply pending migrations",
            "Run php artisan migrate:fresh to reset and re-run all migrations",
            "Check migration files for syntax errors or conflicts",
            "Run php artisan migrate:status to check migration status",
            "Ensure database connection is working before running migrations",
        ],
    ),
    ErrorPattern(
        error_type="Cache/Config Error",
        regex=r"(InvalidArgumentException.*?cache|failed to clear cache|config cache cleared)",
        summary="Laravel cache configuration error",
        meaning="Laravel encountered an issue with application cache or configuration. Stale cache may cause issues.",
        fixes=[
            "Run php artisan cache:clear to clear all caches",
            "Run php artisan config:clear to clear config cache",
            "Run php artisan view:clear to clear view cache",
            "Run php artisan route:clear to clear route cache",
            "Restart the Laravel server after clearing caches",
        ],
    ),
]
