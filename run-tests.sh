#!/bin/bash
# Jenkinsfile Unit Test Runner
# This script runs unit tests for the Jenkinsfile

set -e

echo "=========================================="
echo "Jenkinsfile Unit Test Runner"
echo "=========================================="
echo ""

# Check if Jenkinsfile exists
if [ ! -f "Jenkinsfile" ]; then
    echo "❌ Error: Jenkinsfile not found in current directory"
    exit 1
fi

# Check if Groovy is installed
if ! command -v groovy &> /dev/null; then
    echo "⚠️  Warning: Groovy is not installed"
    echo "Installing Groovy..."
    # This is optional - Groovy installation depends on your system
fi

# Run the tests
echo "Running JenkinsfileTest.groovy..."
echo ""

groovy JenkinsfileTest.groovy

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ All tests completed successfully!"
else
    echo "❌ Tests failed with exit code: $exit_code"
fi

exit $exit_code
