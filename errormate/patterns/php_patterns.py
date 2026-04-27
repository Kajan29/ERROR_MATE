from errormate.patterns import ErrorPattern


PHP_PATTERNS = [
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(PHP Parse error:\s+.+|Parse error:\s+syntax error,.+)",
        summary="PHP syntax error",
        meaning="PHP parser detected invalid syntax.",
        fixes=[
            "Check the file and line in the error output.",
            "Fix missing semicolons, brackets, or malformed statements.",
            "Run php -l on the file for quick syntax validation.",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Fatal error:\s+Uncaught\s+.+)",
        summary="PHP fatal runtime error",
        meaning="Application crashed due to an unhandled PHP runtime error.",
        fixes=[
            "Read stack trace and inspect failing class/method.",
            "Validate null checks and type assumptions.",
            "Enable detailed Laravel logs for context.",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Class\s+.+\s+not found|composer could not find a matching version)",
        summary="PHP class or Composer package missing",
        meaning="Required class autoloading or Composer package resolution failed.",
        fixes=[
            "Run composer install and composer dump-autoload.",
            "Verify namespace and class file paths.",
            "Check package version constraints in composer.json.",
        ],
    ),
]


LARAVEL_PATTERNS = [
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(No application encryption key has been specified|APP_KEY|.env file missing)",
        summary="Laravel environment configuration error",
        meaning="Laravel is missing required application environment configuration.",
        fixes=[
            "Create/update .env from .env.example.",
            "Run php artisan key:generate.",
            "Clear config cache with php artisan config:clear.",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(SQLSTATE\[[0-9A-Z]+\]\s*\[[0-9]+\].+|Connection refused)",
        summary="Laravel database connection failed",
        meaning="Laravel could not connect to the configured database server.",
        fixes=[
            "Verify DB_* values in .env.",
            "Ensure the database service is running.",
            "Check database user permissions and host accessibility.",
        ],
    ),
]
