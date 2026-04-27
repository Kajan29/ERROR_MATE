from errormate.patterns import ErrorPattern


NODE_PATTERNS = [
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Cannot find module ['\"].+['\"]|npm ERR! code E404|No matching version found for)",
        summary="Missing package or module",
        meaning="A required npm package/module is not installed or cannot be resolved.",
        fixes=[
            "Run npm install or pnpm install.",
            "Verify dependency names and versions in package.json.",
            "Delete node_modules and lock file, then reinstall dependencies.",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(TypeError:\s+.+|ReferenceError:\s+.+|UnhandledPromiseRejectionWarning)",
        summary="JavaScript runtime error",
        meaning="The app failed while executing JavaScript at runtime.",
        fixes=[
            "Read the stack trace and inspect the failing line.",
            "Validate undefined/null checks before property access.",
            "Add logging around input values.",
        ],
    ),
]


REACT_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(Module not found:.*|Can't resolve ['\"].+['\"]|Compiled with problems)",
        summary="Module not found",
        meaning="A required package or file cannot be found during bundling.",
        fixes=[
            "Check the import path and file name casing.",
            "Install the missing package.",
            "Restart the development server.",
        ],
    ),
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(SyntaxError:\s+.+|Unexpected token\s+.+)",
        summary="Syntax error in source code",
        meaning="The compiler found invalid JavaScript/TypeScript syntax.",
        fixes=[
            "Inspect the file and line from the error output.",
            "Fix missing braces, commas, or invalid JSX syntax.",
            "Run formatter/linter to highlight syntax issues.",
        ],
    ),
]


EXPRESS_PATTERNS = [
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Route\.(get|post|put|delete)\(\) requires a callback function|Cannot set headers after they are sent to the client)",
        summary="Express runtime error",
        meaning="An Express route or response flow is invalid at runtime.",
        fixes=[
            "Ensure every route handler is a valid function.",
            "Return after sending a response to avoid duplicate sends.",
            "Add middleware error handling for thrown exceptions.",
        ],
    ),
]


NEXTJS_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(Failed to compile|Module not found:|Error: Cannot find module)",
        summary="Next.js compile failure",
        meaning="Next.js could not compile the project due to missing modules or build issues.",
        fixes=[
            "Install missing dependencies and check import paths.",
            "Clear .next cache and rerun dev/build command.",
            "Verify tsconfig/jsconfig path aliases.",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(Missing Env Value|NEXT_PUBLIC_[A-Z0-9_]+\s+is\s+not\s+defined)",
        summary="Missing Next.js environment variable",
        meaning="A required Next.js environment variable is missing.",
        fixes=[
            "Define the variable in .env.local.",
            "Restart Next.js after updating environment variables.",
            "Use NEXT_PUBLIC_ prefix for client-side variables.",
        ],
    ),
]


NESTJS_PATTERNS = [
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Nest can't resolve dependencies of|Error:\s+Cannot find module ['\"].+['\"])",
        summary="NestJS dependency resolution failed",
        meaning="NestJS DI container could not resolve one or more providers.",
        fixes=[
            "Verify module imports/exports and provider registration.",
            "Check constructor injection tokens and circular dependencies.",
            "Rebuild project after dependency updates.",
        ],
    ),
]
