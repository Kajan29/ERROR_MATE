from errormate.patterns import ErrorPattern


DOTNET_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(error\s+CS\d{4}:\s+.+)",
        summary="C# compile error",
        meaning="The C# compiler found code that cannot be compiled.",
        fixes=[
            "Open the file and line reported by the compiler.",
            "Fix type mismatches, missing symbols, or syntax mistakes.",
            "Run dotnet restore and rebuild.",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(error\s+NU\d{4}:\s+.+|The type or namespace name\s+'.+'\s+could not be found)",
        summary="NuGet package or reference missing",
        meaning="A required package or project reference is missing.",
        fixes=[
            "Run dotnet restore.",
            "Check PackageReference entries in the project file.",
            "Verify project references for shared libraries.",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Unhandled exception\.\s+.+)",
        summary="Unhandled .NET exception",
        meaning="Application threw an unhandled runtime exception.",
        fixes=[
            "Read the exception type and stack trace.",
            "Validate configuration and runtime input values.",
            "Add defensive null/value checks around failing code.",
        ],
    ),
]
