import groovy.json.JsonSlurper

/**
 * Unit Tests for Jenkinsfile
 * Tests core pipeline configuration, environment variables, and stage definitions
 */

class JenkinsfileTest {
    
    // Test properties
    static final String JENKINS_FILE = "Jenkinsfile"
    static String jenkinsfileContent
    
    /**
     * Initialize test suite - load Jenkinsfile content
     */
    static void setup() {
        File jenkinsFile = new File(JENKINS_FILE)
        if (!jenkinsFile.exists()) {
            throw new FileNotFoundException("Jenkinsfile not found at: ${JENKINS_FILE}")
        }
        jenkinsfileContent = jenkinsFile.text
        println("✓ Jenkinsfile loaded successfully")
    }
    
    /**
     * Test 1: Verify pipeline definition exists
     */
    static void testPipelineDefinition() {
        assert jenkinsfileContent.contains("pipeline {"), "Pipeline definition not found"
        assert jenkinsfileContent.contains("agent any"), "Agent definition not found"
        println("✓ Test 1 PASSED: Pipeline definition exists")
    }
    
    /**
     * Test 2: Verify all required environment variables are defined
     */
    static void testEnvironmentVariables() {
        Map<String, String> requiredEnvVars = [
            "PROJECT_DIR": "\${WORKSPACE}",
            "DOCKER_REGISTRY": "your_docker_registry",
            "DOCKER_IMAGE_NAME": "fullstack-langgraph-app",
            "DOCKER_IMAGE_TAG": "\${BUILD_NUMBER}",
            "GIT_REPOSITORY": "github.com",
            "GIT_BRANCH": "main",
            "VM_HOST": "136.113.95.72",
            "VM_PORT": "22",
            "VM_USER": "orion-dev",
            "VM_DEPLOY_DIR": "/opt/fullstack-langgraph",
            "DOCKER_COMPOSE_FILE": "docker-compose.yml",
            "APP_PORT": "2024",
            "FRONTEND_PORT": "5173"
        ]
        
        requiredEnvVars.each { key, value ->
            assert jenkinsfileContent.contains(key), "Environment variable '${key}' not found"
            println("  ✓ Environment variable found: ${key}")
        }
        
        println("✓ Test 2 PASSED: All required environment variables defined")
    }
    
    /**
     * Test 3: Verify all required stages exist
     */
    static void testRequiredStages() {
        List<String> requiredStages = [
            "Clone Repository",
            "Verify Project Structure",
            "Install Backend Dependencies",
            "Install Frontend Dependencies",
            "Build Frontend",
            "Lint and Test Backend",
            "Setup Environment Variables",
            "Docker Build",
            "Docker Compose Down",
            "Docker Compose Build",
            "Docker Compose Up",
            "Health Check",
            "API Health Check",
            "Verify Local Deployment",
            "Push Docker Image to Registry",
            "Deploy to Virtual Machine",
            "Build and Deploy Docker on VM",
            "Deploy Docker Compose on VM",
            "Health Check on VM",
            "Verify VM Deployment"
        ]
        
        requiredStages.each { stage ->
            assert jenkinsfileContent.contains("stage('${stage}'"), "Stage '${stage}' not found"
            println("  ✓ Stage found: ${stage}")
        }
        
        println("✓ Test 3 PASSED: All required stages exist")
    }
    
    /**
     * Test 4: Verify critical deployment configurations
     */
    static void testDeploymentConfig() {
        // VM Configuration
        assert jenkinsfileContent.contains("VM_HOST = \"136.113.95.72\""), "VM_HOST not correctly configured"
        assert jenkinsfileContent.contains("VM_USER = \"orion-dev\""), "VM_USER not correctly configured"
        assert jenkinsfileContent.contains("VM_DEPLOY_DIR = \"/opt/fullstack-langgraph\""), "VM_DEPLOY_DIR not correctly configured"
        
        // Ports
        assert jenkinsfileContent.contains("APP_PORT = \"2024\""), "APP_PORT not correctly configured"
        assert jenkinsfileContent.contains("FRONTEND_PORT = \"5173\""), "FRONTEND_PORT not correctly configured"
        
        // Docker
        assert jenkinsfileContent.contains("DOCKER_IMAGE_NAME = \"fullstack-langgraph-app\""), "DOCKER_IMAGE_NAME not correctly configured"
        assert jenkinsfileContent.contains("DOCKER_COMPOSE_FILE = \"docker-compose.yml\""), "DOCKER_COMPOSE_FILE not correctly configured"
        
        println("✓ Test 4 PASSED: Deployment configuration is correct")
    }
    
    /**
     * Test 5: Verify SSH configuration for VM deployment
     */
    static void testSSHConfiguration() {
        assert jenkinsfileContent.contains("ssh -o StrictHostKeyChecking=no"), "SSH StrictHostKeyChecking not configured"
        assert jenkinsfileContent.contains("-i \${VM_SSH_KEY}"), "SSH key variable not found"
        assert jenkinsfileContent.contains("-p \${VM_PORT}"), "SSH port variable not found"
        assert jenkinsfileContent.contains("\${VM_USER}@\${VM_HOST}"), "SSH user@host format not found"
        
        println("✓ Test 5 PASSED: SSH configuration is correct")
    }
    
    /**
     * Test 6: Verify Docker commands are present
     */
    static void testDockerCommands() {
        assert jenkinsfileContent.contains("docker build"), "docker build command not found"
        assert jenkinsfileContent.contains("docker-compose"), "docker-compose command not found"
        assert jenkinsfileContent.contains("docker push"), "docker push command not found"
        assert jenkinsfileContent.contains("docker ps"), "docker ps command not found"
        assert jenkinsfileContent.contains("docker images"), "docker images command not found"
        
        println("✓ Test 6 PASSED: Docker commands are present")
    }
    
    /**
     * Test 7: Verify file transfer mechanisms (SCP)
     */
    static void testFileTransfer() {
        assert jenkinsfileContent.contains("scp"), "SCP command not found for file transfer"
        assert jenkinsfileContent.contains("Dockerfile"), "Dockerfile copy not configured"
        assert jenkinsfileContent.contains("docker-compose.yml"), "docker-compose.yml copy not configured"
        assert jenkinsfileContent.contains(".env"), ".env file copy not configured"
        
        println("✓ Test 7 PASSED: File transfer mechanisms configured")
    }
    
    /**
     * Test 8: Verify health check endpoints
     */
    static void testHealthCheckEndpoints() {
        assert jenkinsfileContent.contains("curl"), "Health check using curl not found"
        assert jenkinsfileContent.contains("localhost:\${APP_PORT}"), "Local API endpoint check not found"
        assert jenkinsfileContent.contains("health"), "Health endpoint check not found"
        
        println("✓ Test 8 PASSED: Health check endpoints configured")
    }
    
    /**
     * Test 9: Verify post-build actions
     */
    static void testPostActions() {
        assert jenkinsfileContent.contains("post {"), "Post section not found"
        assert jenkinsfileContent.contains("success {"), "Success post action not found"
        assert jenkinsfileContent.contains("failure {"), "Failure post action not found"
        assert jenkinsfileContent.contains("always {"), "Always post action not found"
        
        println("✓ Test 9 PASSED: Post-build actions configured")
    }
    
    /**
     * Test 10: Verify deployment summary information
     */
    static void testDeploymentSummary() {
        assert jenkinsfileContent.contains("DEPLOYMENT SUMMARY"), "Deployment summary not found"
        assert jenkinsfileContent.contains("Frontend:"), "Frontend URL not in summary"
        assert jenkinsfileContent.contains("Backend API:"), "Backend API URL not in summary"
        assert jenkinsfileContent.contains("VM Host:"), "VM Host not in summary"
        
        println("✓ Test 10 PASSED: Deployment summary configured")
    }
    
    /**
     * Test 11: Verify backend and frontend dependencies installation
     */
    static void testDependencyInstallation() {
        assert jenkinsfileContent.contains("pip install"), "Python pip install not found"
        assert jenkinsfileContent.contains("npm install"), "Node npm install not found"
        assert jenkinsfileContent.contains("python -m venv"), "Python virtual environment not found"
        
        println("✓ Test 11 PASSED: Dependency installation configured")
    }
    
    /**
     * Test 12: Verify GitHub repository configuration
     */
    static void testGitHubConfiguration() {
        assert jenkinsfileContent.contains("GIT_REPOSITORY"), "GIT_REPOSITORY not defined"
        assert jenkinsfileContent.contains("GIT_BRANCH"), "GIT_BRANCH not defined"
        assert jenkinsfileContent.contains("github.com"), "GitHub URL not found"
        assert jenkinsfileContent.contains("git branch:"), "Git clone with branch not configured"
        
        println("✓ Test 12 PASSED: GitHub configuration is correct")
    }
    
    /**
     * Test 13: Verify environment file handling
     */
    static void testEnvironmentFileHandling() {
        assert jenkinsfileContent.contains(".env.example"), ".env.example not referenced"
        assert jenkinsfileContent.contains("export \$(cat .env"), "Environment variable loading not configured"
        
        println("✓ Test 13 PASSED: Environment file handling configured")
    }
    
    /**
     * Test 14: Verify error handling and cleanup
     */
    static void testErrorHandling() {
        assert jenkinsfileContent.contains("|| true"), "Error suppression not found (|| true)"
        assert jenkinsfileContent.contains("|| echo"), "Error logging not found"
        
        println("✓ Test 14 PASSED: Error handling configured")
    }
    
    /**
     * Test 15: Verify VM deployment stages follow correct sequence
     */
    static void testVMDeploymentSequence() {
        int deployToVMIndex = jenkinsfileContent.indexOf("stage('Deploy to Virtual Machine'")
        int buildAndDeployIndex = jenkinsfileContent.indexOf("stage('Build and Deploy Docker on VM'")
        int deployComposeIndex = jenkinsfileContent.indexOf("stage('Deploy Docker Compose on VM'")
        int healthCheckIndex = jenkinsfileContent.indexOf("stage('Health Check on VM'")
        int verifyIndex = jenkinsfileContent.indexOf("stage('Verify VM Deployment'")
        
        assert deployToVMIndex > 0, "Deploy to Virtual Machine stage not found"
        assert buildAndDeployIndex > deployToVMIndex, "Build and Deploy should come after Deploy to VM"
        assert deployComposeIndex > buildAndDeployIndex, "Deploy Compose should come after Build and Deploy"
        assert healthCheckIndex > deployComposeIndex, "Health Check should come after Deploy Compose"
        assert verifyIndex > healthCheckIndex, "Verify should come after Health Check"
        
        println("✓ Test 15 PASSED: VM deployment stages in correct sequence")
    }
    
    /**
     * Run all tests
     */
    static void runAllTests() {
        println("\n" + "="*60)
        println("JENKINSFILE UNIT TESTS")
        println("="*60 + "\n")
        
        try {
            setup()
            testPipelineDefinition()
            testEnvironmentVariables()
            testRequiredStages()
            testDeploymentConfig()
            testSSHConfiguration()
            testDockerCommands()
            testFileTransfer()
            testHealthCheckEndpoints()
            testPostActions()
            testDeploymentSummary()
            testDependencyInstallation()
            testGitHubConfiguration()
            testEnvironmentFileHandling()
            testErrorHandling()
            testVMDeploymentSequence()
            
            println("\n" + "="*60)
            println("ALL TESTS PASSED ✓")
            println("="*60)
            println("\nTotal Tests Run: 15")
            println("Total Tests Passed: 15")
            println("Total Tests Failed: 0")
            println("\n")
            
        } catch (AssertionError e) {
            println("\n" + "="*60)
            println("TEST FAILED ✗")
            println("="*60)
            println("\nAssertion Error: ${e.message}")
            println("\n")
            throw e
        } catch (Exception e) {
            println("\n" + "="*60)
            println("ERROR DURING TEST EXECUTION ✗")
            println("="*60)
            println("\nError: ${e.message}")
            println("\n")
            throw e
        }
    }
}

// Run tests if executed directly
if (this.class.name == 'JenkinsfileTest' || binding.variables.containsKey('args')) {
    JenkinsfileTest.runAllTests()
}
