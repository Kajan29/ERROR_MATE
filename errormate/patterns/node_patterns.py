from errormate.patterns import ErrorPattern


NODE_PATTERNS = [
    ErrorPattern(
        error_type="Command Not Found Error",
        regex=r"(command not found|npm ERR! errno ENOENT|spawn ENOENT|'.+' is not recognized as an internal or external command)",
        summary="CLI command not found",
        meaning="The build tool command (e.g., vite, webpack, next) is not installed or not in your PATH. This happens when dependencies are missing or not installed.",
        fixes=[
            "Install the missing package: npm install -D vite (for React Vite projects)",
            "Run npm install to install all dependencies from package.json",
            "Check if the package exists in devDependencies in package.json",
            "Delete node_modules and package-lock.json, then run npm install again",
            "For React Vite: ensure you have vite installed: npm install -D vite @vitejs/plugin-react",
        ],
    ),
    ErrorPattern(
        error_type="Missing Package Error",
        regex=r"(Cannot find module ['\"].+['\"]|npm ERR! code E404|No matching version found for)",
        summary="Missing package or module",
        meaning="A required npm package/module is not installed or cannot be resolved. This prevents the application from running or building.",
        fixes=[
            "Run npm install or pnpm install to install missing dependencies",
            "Verify dependency names and versions in package.json",
            "Delete node_modules and lock file, then reinstall dependencies",
            "Check if the package exists on npm registry with correct name",
        ],
    ),
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(TypeError:\s+.+|ReferenceError:\s+.+|UnhandledPromiseRejectionWarning)",
        summary="JavaScript runtime error",
        meaning="The app failed while executing JavaScript at runtime due to type errors, undefined variables, or unhandled promise rejections.",
        fixes=[
            "Read the stack trace and inspect the failing line",
            "Validate undefined/null checks before property access",
            "Add logging around input values to debug",
            "Use try/catch blocks to handle promise rejections",
        ],
    ),
]


REACT_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(Module not found:.*|Can't resolve ['\"].+['\"]|Compiled with problems)",
        summary="React module not found",
        meaning="React bundler (Vite or Webpack) cannot find a required file or module during compilation. Check import paths and file names.",
        fixes=[
            "Check the import path and file name casing (React is case-sensitive)",
            "Install the missing package with npm install",
            "Restart the development server",
            "Verify the file exists in the correct directory",
            "Check for relative path issues (use ./ for same directory)",
        ],
    ),
    ErrorPattern(
        error_type="Syntax Error",
        regex=r"(SyntaxError:\s+.+|Unexpected token\s+.+)",
        summary="React syntax error",
        meaning="The JSX/TypeScript compiler found invalid syntax in your React components. Common issues include missing tags, invalid JSX, or TypeScript errors.",
        fixes=[
            "Inspect the file and line from the error output",
            "Fix missing braces, commas, or invalid JSX syntax",
            "Ensure all JSX tags are properly closed",
            "Run formatter/linter (ESLint/Prettier) to highlight syntax issues",
            "Check for TypeScript type errors if using TSX",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(EADDRINUSE.*?3000|Address already in use.*?3000)",
        summary="React dev server port conflict",
        meaning="Another process is already using the default React port (3000). Vite or Create React App cannot start.",
        fixes=[
            "Stop the process using port 3000",
            "Use a different port: PORT=3001 npm start (CRA) or npm run dev -- --port 3001 (Vite)",
            "Kill the process: npx kill-port 3000 or lsof -ti:3000 | xargs kill",
            "Check for other React dev servers running in background",
        ],
    ),
]


EXPRESS_PATTERNS = [
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Route\.(get|post|put|delete)\(\) requires a callback function|Cannot set headers after they are sent to the client)",
        summary="Express runtime error",
        meaning="An Express route handler is invalid or attempting to send multiple responses. Common causes include missing callbacks or double response sends.",
        fixes=[
            "Ensure every route handler is a valid function with (req, res) parameters",
            "Return after sending a response to avoid duplicate sends",
            "Add middleware error handling for thrown exceptions",
            "Check for async/await issues in route handlers",
            "Use res.send() only once per request",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(connect ECONNREFUSED.*?(3306|5432|27017)|MongoNetworkError|SequelizeConnectionError)",
        summary="Express database connection failed",
        meaning="Express cannot connect to your database (MySQL, PostgreSQL, MongoDB). Check database service status and connection settings.",
        fixes=[
            "Verify database host, port, username, and password in config",
            "Ensure the database service is running (docker-compose up or systemctl start)",
            "Check network/firewall access to the database port",
            "Test connection with database client tools",
            "Verify database connection string format",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(process\.env\.[A-Z0-9_]+.*undefined|Missing required environment variable)",
        summary="Express environment variable missing",
        meaning="A required environment variable (DB_URL, API_KEY, etc.) is undefined. Express cannot access configuration values.",
        fixes=[
            "Check your .env file and variable names",
            "Restart the server after changing environment variables",
            "Use dotenv package to load .env file: require('dotenv').config()",
            "Ensure .env is in project root and not in .gitignore",
            "Provide default values: process.env.PORT || 3000",
        ],
    ),
]


NEXTJS_PATTERNS = [
    ErrorPattern(
        error_type="Compile Error",
        regex=r"(Failed to compile|Module not found:|Error: Cannot find module)",
        summary="Next.js compile failure",
        meaning="Next.js cannot compile your project due to missing modules, import errors, or build configuration issues. Check your code and dependencies.",
        fixes=[
            "Install missing dependencies and check import paths",
            "Clear .next cache and rerun dev/build command",
            "Verify tsconfig/jsconfig path aliases in next.config.js",
            "Check for circular dependencies in imports",
            "Ensure all files have correct extensions (.js, .jsx, .ts, .tsx)",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(Missing Env Value|NEXT_PUBLIC_[A-Z0-9_]+\s+is\s+not\s+defined)",
        summary="Next.js environment variable missing",
        meaning="Next.js requires a specific environment variable (NEXT_PUBLIC_* for client-side). The variable is not set in .env or not loaded.",
        fixes=[
            "Define the variable in .env.local (not .env for production)",
            "Restart Next.js after updating environment variables",
            "Use NEXT_PUBLIC_ prefix for client-side variables",
            "Check next.config.js for env variable configuration",
            "Ensure .env.local is in project root",
        ],
    ),
    ErrorPattern(
        error_type="Port Already Used Error",
        regex=r"(EADDRINUSE.*?3000|Address already in use.*?3000|Port 3000 is already in use)",
        summary="Next.js dev server port conflict",
        meaning="Another process is using the default Next.js port (3000). Next.js dev server cannot start.",
        fixes=[
            "Stop the process using port 3000",
            "Use a different port: npm run dev -- -p 3001",
            "Kill the process: npx kill-port 3000 or lsof -ti:3000 | xargs kill",
            "Check for other Next.js dev servers running",
        ],
    ),
]


NESTJS_PATTERNS = [
    ErrorPattern(
        error_type="Runtime Error",
        regex=r"(Nest can't resolve dependencies of|Error:\s+Cannot find module ['\"].+['\"])",
        summary="NestJS dependency injection failed",
        meaning="NestJS Dependency Injection container cannot resolve providers. Common causes include missing imports, circular dependencies, or incorrect module configuration.",
        fixes=[
            "Verify module imports/exports and provider registration in @Module decorators",
            "Check constructor injection tokens and ensure they match provider names",
            "Rebuild project after dependency updates: npm run build",
            "Check for circular dependencies and use forwardRef() if needed",
            "Ensure all providers are listed in the providers array of the module",
        ],
    ),
    ErrorPattern(
        error_type="Database Connection Error",
        regex=r"(connect ECONNREFUSED.*?(3306|5432|27017)|TypeOrmError|MongoNetworkError)",
        summary="NestJS database connection failed",
        meaning="NestJS cannot connect to your database via TypeORM or Mongoose. Check database service, credentials, and connection configuration.",
        fixes=[
            "Verify database connection settings in TypeOrmModule.forRoot() or MongooseModule.forRoot()",
            "Ensure the database service is running",
            "Check database credentials and host accessibility",
            "Test connection with database client tools",
            "Verify connection string format in app.module.ts or .env",
        ],
    ),
    ErrorPattern(
        error_type="Environment Variable Error",
        regex=r"(process\.env\.[A-Z0-9_]+.*undefined|Missing required environment variable|ConfigService error)",
        summary="NestJS environment variable missing",
        meaning="NestJS ConfigModule cannot load a required environment variable. The variable is missing in .env or not configured in ConfigModule.",
        fixes=[
            "Check your .env file and variable names",
            "Ensure ConfigModule is properly configured with .env path in app.module.ts",
            "Restart the application after changing environment variables",
            "Use @IsOptional() decorator for optional config fields",
            "Verify .env is in project root and loaded before app bootstrap",
        ],
    ),
]
