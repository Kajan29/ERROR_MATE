from errormate.patterns import ErrorPattern


JAVA_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(COMPILATION ERROR|cannot find symbol)",
        summary="Java compilation failed",
        meaning="Maven/Gradle could not compile source code due to symbol or type errors.",
        fixes=[
            "Review the compiler line and class mentioned in the output.",
            "Fix imports, method signatures, or missing classes.",
            "Run a clean build after correcting source code.",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Exception in thread \"main\"|Caused by:\s+.+)",
        summary="Java runtime exception",
        meaning="A runtime exception interrupted application startup or execution.",
        fixes=[
            "Inspect root cause under the first Caused by entry.",
            "Validate application properties and startup args.",
            "Enable debug logging for deeper stack details.",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Could not resolve dependencies for project|Could not find artifact)",
        summary="Maven dependency resolution failed",
        meaning="Build tool cannot resolve required dependency artifacts.",
        fixes=[
            "Check repository connectivity and credentials.",
            "Confirm dependency coordinates in pom.xml/build.gradle.",
            "Clear local cache for the dependency and retry.",
        ],
    ),
]
