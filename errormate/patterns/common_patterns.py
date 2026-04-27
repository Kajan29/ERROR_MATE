from errormate.patterns import ErrorPattern


COMMON_PATTERNS = [
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(EADDRINUSE|Address already in use|Only one usage of each socket address)",
        summary="Port already in use",
        meaning="Another process is already using the port required by this command.",
        fixes=[
            "Stop the process currently using the port.",
            "Change the app port in environment/config settings.",
            "Restart the terminal and run again.",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(could not connect to server|connection refused.*(5432|3306|1433)|Failed to configure a DataSource|SQLSTATE\[[0-9A-Z]+\]\s*\[[0-9]+\])",
        summary="Database connection failed",
        meaning="The application could not connect to the configured database server.",
        fixes=[
            "Check database host, port, username, and password.",
            "Ensure the database server is running.",
            "Verify network/firewall access to the database port.",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(Missing required environment variable|environment variable .* is not set|process\.env\.[A-Z0-9_]+.*undefined|ImproperlyConfigured: Set the .+ environment variable)",
        summary="Missing or invalid environment variable",
        meaning="A required environment variable is missing, empty, or invalid.",
        fixes=[
            "Check your .env file and variable names.",
            "Restart the process after changing environment variables.",
            "Confirm variables are loaded in your current shell session.",
        ],
    ),
    ErrorPattern(
        error_type="Permission Error",
        regex=r"(EACCES|EPERM|Permission denied|Access is denied)",
        summary="Permission denied",
        meaning="The process lacks permission to access a file, folder, or network resource.",
        fixes=[
            "Run with a user account that has required permissions.",
            "Adjust file/folder permissions.",
            "Avoid protected ports or directories when possible.",
        ],
    ),
]
