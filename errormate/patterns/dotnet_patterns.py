from errormate.patterns import ErrorPattern


DOTNET_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(error\s+CS\d{4}:\s+.+)",
        summary="C# compile error",
        meaning="The C# compiler found code that cannot be compiled due to type mismatches, missing symbols, or syntax errors in your .cs files.",
        fixes=[
            "Open the file and line reported by the compiler",
            "Fix type mismatches, missing using statements, or syntax mistakes",
            "Run dotnet restore and rebuild: dotnet clean && dotnet build",
            "Check for missing NuGet packages or project references",
            "Verify namespace declarations match file locations",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(error\s+NU\d{4}:\s+.+|The type or namespace name\s+'.+'\s+could not be found)",
        summary="NuGet package or reference missing",
        meaning="A required NuGet package or project reference is missing. The compiler cannot find the required assembly or namespace.",
        fixes=[
            "Run dotnet restore to download missing packages",
            "Check PackageReference entries in the .csproj project file",
            "Verify project references for shared libraries in Solution Explorer",
            "Clear NuGet cache: dotnet nuget locals all --clear",
            "Check package version compatibility with target framework",
        ],
    ),
    ErrorPattern(
        error_type="Configuration Error",
        regex=r"(Exactly one database provider must be enabled\..+)",
        summary="Conflicting database provider configuration",
        meaning="The app stopped during startup because multiple database providers (MySQL, PostgreSQL) are enabled simultaneously. Exactly one must be active.",
        fixes=[
            "Choose one provider for this environment and keep only that flag enabled",
            "For MySQL set MYSQL=true and POSTGRES=false in .env or appsettings.json",
            "For PostgreSQL set MYSQL=false and POSTGRES=true in .env or appsettings.json",
            "Search .env, appsettings*.json, and Properties/launchSettings.json for duplicate or conflicting values",
            "Restart the app after changing the active environment variables or config file",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(System\.Data\.SqlClient\.SqlException|Npgsql\.PostgresException|MongoDB\.Driver\.MongoConnectionException|connection.*?refused)",
        summary=".NET database connection failed",
        meaning="The application cannot connect to your database (SQL Server, PostgreSQL, MongoDB). Check connection string and database service status.",
        fixes=[
            "Verify connection string in appsettings.json or environment variables",
            "Ensure the database service is running (docker-compose up or SQL Server service)",
            "Check network/firewall access to the database port",
            "Test connection with database client tools like SSMS or pgAdmin",
            "Verify database credentials (username, password) in connection string",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(Configuration error.*?environment variable|Missing required configuration|InvalidOperationException.*?configuration)",
        summary=".NET environment configuration error",
        meaning="A required configuration value or environment variable is missing in appsettings.json, appsettings.{Environment}.json, or environment variables.",
        fixes=[
            "Check appsettings.json and appsettings.{Environment}.json for missing keys",
            "Verify environment variables are set for the current environment (Development, Production)",
            "Restart the application after changing configuration",
            "Use IConfiguration pattern to load configuration correctly in Startup.cs/Program.cs",
            "Check for JSON syntax errors in configuration files",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(Only one usage of each socket address.*?is permitted|Address already in use.*?5000|EADDRINUSE)",
        summary=".NET port conflict",
        meaning="Another process is already using the required port (default 5000 for ASP.NET Core). The web server cannot start.",
        fixes=[
            "Stop the process using the port",
            "Change the port in launchSettings.json or command line: dotnet run --urls 'http://localhost:5001'",
            "Restart the application with a different port",
            "Kill the process: netstat -ano | findstr :5000 then taskkill /PID <pid> /F",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Unhandled exception\.\s+(?!.*Exactly one database provider must be enabled\.).+)",
        summary="Unhandled .NET exception",
        meaning="Application threw an unhandled runtime exception during execution. Check the exception type and stack trace for root cause.",
        fixes=[
            "Read the exception type and stack trace from the error output",
            "Validate configuration and runtime input values",
            "Add defensive null/value checks around failing code",
            "Use try/catch blocks to handle exceptions gracefully",
            "Enable detailed error pages in Development environment",
        ],
    ),
]
