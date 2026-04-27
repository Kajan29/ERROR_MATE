from errormate.error_classifier import ErrorClassifier


def test_react_module_not_found_detection():
    output = "Module not found: Can't resolve 'axios' in './src/App.js'"
    report = ErrorClassifier().classify(output, "React")

    assert report is not None
    assert report.error_type == "Compile Error"
    assert report.main_error == "Module not found"


def test_dotnet_compile_error_detection():
    output = "Program.cs(10,14): error CS1002: ; expected"
    report = ErrorClassifier().classify(output, ".NET")

    assert report is not None
    assert report.error_type == "Compile Error"


def test_port_in_use_detection_from_common_patterns():
    output = "Error: listen EADDRINUSE: address already in use :::3000"
    report = ErrorClassifier().classify(output, "Express.js")

    assert report is not None
    assert report.error_type == "Port Already Used Error"


def test_no_match_returns_none():
    output = "Server started successfully on port 8000"
    report = ErrorClassifier().classify(output, "Django")

    assert report is None
