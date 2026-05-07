from errormate.patterns import ErrorPattern


JAVA_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(COMPILATION ERROR|cannot find symbol)",
        summary="Java compilation failed",
        meaning="Maven/Gradle could not compile source code due to symbol or type errors. Check for missing imports, incorrect types, or syntax errors.",
        fixes=[
            "Review the compiler line and class mentioned in the output",
            "Fix imports, method signatures, or missing classes",
            "Run a clean build after correcting source code: mvn clean install or gradle clean build",
            "Check for missing dependencies in pom.xml or build.gradle",
            "Verify Java version compatibility with project requirements",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Exception in thread \"main\"|Caused by:\s+.+)",
        summary="Java runtime exception",
        meaning="A runtime exception interrupted application startup or execution. Check the 'Caused by' section for root cause.",
        fixes=[
            "Inspect root cause under the first Caused by entry in stack trace",
            "Validate application properties and startup args in application.properties/yml",
            "Enable debug logging for deeper stack details: logging.level.root=DEBUG",
            "Check for null pointer exceptions and add null checks",
            "Review exception handling in your code",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Could not resolve dependencies for project|Could not find artifact)",
        summary="Maven/Gradle dependency resolution failed",
        meaning="Build tool cannot resolve required dependency artifacts from Maven Central or other repositories.",
        fixes=[
            "Check repository connectivity and credentials (settings.xml for Maven)",
            "Confirm dependency coordinates in pom.xml/build.gradle are correct",
            "Clear local cache for the dependency and retry: mvn dependency:purge-local-repository",
            "Check if artifact exists in Maven Central repository",
            "Verify network connection and proxy settings",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(java\.sql\.SQLException|Communications link failure|HikariPool.*?unable)",
        summary="Java database connection failed",
        meaning="Java application cannot connect to your database (MySQL, PostgreSQL, H2). Check connection string and database service status.",
        fixes=[
            "Verify database URL, username, and password in application.properties/yml",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check network/firewall access to the database port",
            "Test connection with database client tools (mysql, psql)",
            "Verify JDBC driver dependency is included in pom.xml/build.gradle",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(IllegalArgumentException.*?environment|Missing required property|java\.lang\.NullPointerException.*?environment)",
        summary="Missing Java environment variable",
        meaning="A required environment variable or configuration property is missing in application.properties/yml or environment.",
        fixes=[
            "Check application.properties or application.yml for missing keys",
            "Verify environment variables are set for the current profile (dev, prod)",
            "Restart the application after changing configuration",
            "Use @Value annotation with default values: @Value('${property:default}')",
            "Check for profile-specific configuration files",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(java\.net\.BindException.*?already in use|Address already in use.*?8080)",
        summary="Java port conflict",
        meaning="Another process is already using the required port (commonly 8080 for Spring Boot). The web server cannot start.",
        fixes=[
            "Stop the process using the port",
            "Change the port in application.properties: server.port=8081",
            "Kill the process: netstat -ano | findstr :8080 then taskkill /PID <pid> /F (Windows)",
            "Kill the process: lsof -ti:8080 | xargs kill (Linux/Mac)",
            "Check for other Java/Spring Boot applications running",
        ],
    ),
]
