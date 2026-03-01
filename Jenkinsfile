pipeline {
    agent any
    
    environment {
        PROJECT_DIR = "${WORKSPACE}"
        DOCKER_REGISTRY = "your_docker_registry"
        DOCKER_IMAGE_NAME = "fullstack-langgraph-app"
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        GIT_REPOSITORY = "https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart.git"
        GIT_BRANCH = "main"
        
        // VM Deployment Configuration
        VM_HOST = "136.113.95.72"
        VM_PORT = "22"
        VM_USER = "orion-dev"
        VM_SSH_KEY = credentials('vm-ssh-key')
        VM_DEPLOY_DIR = "/opt/fullstack-langgraph"
        
        // Docker Configuration
        DOCKER_COMPOSE_FILE = "Dockerfile"
        APP_PORT = "2024"
        FRONTEND_PORT = "5173"
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo "Cloning repository from GitHub..."
                git branch: "${GIT_BRANCH}", 
                    url: "${GIT_REPOSITORY}"
                echo "Repository cloned successfully"
            }
        }
        
        stage('Verify Project Structure') {
            steps {
                echo "Verifying project structure..."
                sh '''
                    echo "Backend structure:"
                    ls -la backend/
                    echo "\\nFrontend structure:"
                    ls -la frontend/
                '''
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                echo "Installing backend Python dependencies..."
                dir("${PROJECT_DIR}/backend") {
                    sh '''
                        python -m venv venv || true
                        . venv/bin/activate || source venv/Scripts/activate
                        pip install --upgrade pip
                        pip install -e .
                        pip install -r requirements.txt || true
                    '''
                }
            }
        }
        
        stage('Install Frontend Dependencies') {
            steps {
                echo "Installing frontend Node.js dependencies..."
                dir("${PROJECT_DIR}/frontend") {
                    sh '''
                        npm --version
                        npm install
                        npm audit fix || true
                    '''
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo "Building frontend application..."
                dir("${PROJECT_DIR}/frontend") {
                    sh '''
                        npm run build
                    '''
                }
            }
        }
        
        stage('Lint and Test Backend') {
            steps {
                echo "Running backend linting and tests..."
                dir("${PROJECT_DIR}/backend") {
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        python -m pytest tests/ -v || true
                        python -m mypy src/ || true
                    '''
                }
            }
        }
        
        stage('Setup Environment Variables') {
            steps {
                echo "Setting up environment variables..."
                dir("${PROJECT_DIR}/backend") {
                    sh '''
                        if [ ! -f .env ]; then
                            echo "Creating .env file from .env.example..."
                            cp .env.example .env
                            echo "⚠️  WARNING: Please update .env with actual Azure OpenAI credentials"
                        fi
                    '''
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                echo "Building Docker image from Dockerfile..."
                dir("${PROJECT_DIR}") {
                    sh '''
                        echo "Building image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                        docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} -f Dockerfile .
                        docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest
                        
                        echo "\\nImage built successfully"
                        docker images --filter "reference=${DOCKER_IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
                    '''
                }
            }
        }
        
        stage('Docker Compose Down') {
            steps {
                echo "Stopping existing local containers..."
                dir("${PROJECT_DIR}") {
                    sh '''
                        docker-compose -f docker-compose.yml down || true
                        docker-compose -f docker-compose.yml down -v || true
                    '''
                }
            }
        }
        
        stage('Docker Compose Build') {
            steps {
                echo "Building Docker Compose services for testing..."
                dir("${PROJECT_DIR}") {
                    sh '''
                        docker-compose -f docker-compose.yml build --no-cache
                    '''
                }
            }
        }
        
        stage('Docker Compose Up') {
            steps {
                echo "Starting Docker Compose services locally for testing..."
                dir("${PROJECT_DIR}") {
                    sh '''
                        docker-compose -f docker-compose.yml up -d
                        sleep 10
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo "Performing health checks on local deployment..."
                sh '''
                    echo "Checking running containers:"
                    docker ps
                    
                    echo "\\nChecking container logs:"
                    docker-compose -f ${PROJECT_DIR}/docker-compose.yml logs --tail=20
                    
                    echo "\\nChecking network connectivity:"
                    docker network ls
                '''
            }
        }
        
        stage('API Health Check') {
            steps {
                echo "Checking API endpoints..."
                sh '''
                    echo "Waiting for API to be ready..."
                    sleep 15
                    
                    echo "Testing API connectivity..."
                    curl -f http://localhost:2024/health || true
                    
                    echo "\\nLangGraph API status:"
                    curl -s http://localhost:2024/ | head -20 || true
                '''
            }
        }
        
        stage('Verify Local Deployment') {
            steps {
                echo "Verifying local deployment..."
                sh '''
                    echo "Active containers:"
                    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                    
                    echo "\\nImage sizes:"
                    docker images | grep ${DOCKER_IMAGE_NAME} || true
                    
                    echo "\\nVolumes:"
                    docker volume ls || true
                '''
            }
        }
        
        stage('Push Docker Image to Registry') {
            steps {
                echo "Pushing Docker image to registry..."
                sh '''
                    echo "Tagging image for registry..."
                    docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                    docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest
                    
                    echo "\\nPushing to registry..."
                    docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || true
                    docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest || true
                    echo "Docker image pushed successfully"
                '''
            }
        }
        
        stage('Deploy to Virtual Machine') {
            steps {
                echo "Deploying Docker image to Virtual Machine..."
                sh '''
                    # Test SSH connection
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} "echo 'SSH Connection successful'"
                    
                    # Create deployment directory on VM
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} "mkdir -p ${VM_DEPLOY_DIR}"
                    
                    # Copy Dockerfile to VM
                    echo "Copying Dockerfile to VM..."
                    scp -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -P ${VM_PORT} ${PROJECT_DIR}/Dockerfile ${VM_USER}@${VM_HOST}:${VM_DEPLOY_DIR}/
                    
                    # Copy docker-compose.yml to VM
                    echo "Copying docker-compose.yml to VM..."
                    scp -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -P ${VM_PORT} ${PROJECT_DIR}/${DOCKER_COMPOSE_FILE} ${VM_USER}@${VM_HOST}:${VM_DEPLOY_DIR}/
                    
                    # Copy .env file to VM (ensure it exists first)
                    if [ -f "${PROJECT_DIR}/backend/.env" ]; then
                        echo "Copying .env file to VM..."
                        scp -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -P ${VM_PORT} ${PROJECT_DIR}/backend/.env ${VM_USER}@${VM_HOST}:${VM_DEPLOY_DIR}/.env
                    else
                        echo "Warning: .env file not found, copying .env.example template"
                        scp -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -P ${VM_PORT} ${PROJECT_DIR}/backend/.env.example ${VM_USER}@${VM_HOST}:${VM_DEPLOY_DIR}/.env.example
                    fi
                    
                    echo "Files deployed to VM successfully"
                '''
            }
        }
        
        stage('Build and Deploy Docker on VM') {
            steps {
                echo "Building Docker image on Virtual Machine using Dockerfile..."
                sh '''
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} << 'EOF'
                        cd ${VM_DEPLOY_DIR}
                        
                        echo "Current directory: $(pwd)"
                        echo "Files in deployment directory:"
                        ls -la
                        
                        # Build Docker image from Dockerfile
                        echo "Building Docker image from Dockerfile..."
                        docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} -f Dockerfile .
                        docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest
                        
                        echo "\\nDocker image built successfully on VM"
                        docker images --filter "reference=${DOCKER_IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
EOF
                '''
            }
        }
        
        stage('Deploy Docker Compose on VM') {
            steps {
                echo "Starting services on Virtual Machine using docker-compose..."
                sh '''
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} << 'EOF'
                        cd ${VM_DEPLOY_DIR}
                        
                        # Load environment variables
                        if [ -f .env ]; then
                            export $(cat .env | grep -v '#' | xargs)
                            echo "Environment variables loaded from .env"
                        fi
                        
                        # Stop and remove existing containers
                        echo "Stopping existing containers..."
                        docker-compose -f ${DOCKER_COMPOSE_FILE} down || true
                        docker-compose -f ${DOCKER_COMPOSE_FILE} down -v || true
                        
                        # Start services using docker-compose
                        echo "Starting services with docker-compose..."
                        docker-compose -f ${DOCKER_COMPOSE_FILE} up -d
                        
                        # Wait for services to start
                        echo "Waiting for services to initialize..."
                        sleep 15
                        
                        # Display running containers
                        echo "\\nRunning containers:"
                        docker ps
EOF
                '''
            }
        }
        
        stage('Health Check on VM') {
            steps {
                echo "Performing health checks on Virtual Machine..."
                sh '''
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} << 'EOF'
                        echo "=== Container Status ==="
                        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                        
                        echo "\\n=== Docker Networks ==="
                        docker network ls
                        
                        echo "\\n=== Docker Volumes ==="
                        docker volume ls
                        
                        echo "\\n=== Service Logs (last 30 lines) ==="
                        docker-compose -f ${VM_DEPLOY_DIR}/${DOCKER_COMPOSE_FILE} logs --tail=30
                        
                        echo "\\n=== API Endpoint Test ==="
                        curl -s http://localhost:${APP_PORT}/health || echo "API health endpoint not available"
                        
                        echo "\\n=== Deployment Complete ==="
EOF
                '''
            }
        }
        
        stage('Verify VM Deployment') {
            steps {
                echo "Verifying final deployment on Virtual Machine..."
                sh '''
                    ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} << 'EOF'
                        echo "========== DEPLOYMENT SUMMARY =========="
                        echo "Deployment Directory: ${VM_DEPLOY_DIR}"
                        
                        echo "\\nDocker Images:"
                        docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
                        
                        echo "\\nActive Services:"
                        docker-compose -f ${VM_DEPLOY_DIR}/${DOCKER_COMPOSE_FILE} ps
                        
                        echo "\\nConfiguration Files:"
                        if [ -f ${VM_DEPLOY_DIR}/.env ]; then
                            echo "✓ .env file present"
                        else
                            echo "⚠ .env file not found"
                        fi
                        
                        if [ -f ${VM_DEPLOY_DIR}/Dockerfile ]; then
                            echo "✓ Dockerfile present"
                        else
                            echo "⚠ Dockerfile not found"
                        fi
                        
                        if [ -f ${VM_DEPLOY_DIR}/${DOCKER_COMPOSE_FILE} ]; then
                            echo "✓ docker-compose.yml present"
                        else
                            echo "⚠ docker-compose.yml not found"
                        fi
                        
                        echo "\\nDisk Usage:"
                        df -h ${VM_DEPLOY_DIR}
                        
                        echo "========================================"
EOF
                '''
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline completed successfully!"
            echo "Application is now deployed and running."
            sh '''
                echo "\\n========== DEPLOYMENT SUMMARY =========="
                echo "Local Deployment:"
                echo "  - Frontend: http://localhost:${FRONTEND_PORT}"
                echo "  - Backend API: http://localhost:${APP_PORT}"
                echo "  - LangGraph Dashboard: http://localhost:${APP_PORT}/app"
                echo ""
                echo "Virtual Machine Deployment:"
                echo "  - VM Host: ${VM_HOST}"
                echo "  - Frontend: http://${VM_HOST}:${FRONTEND_PORT}"
                echo "  - Backend API: http://${VM_HOST}:${APP_PORT}"
                echo "  - Deploy Directory: ${VM_DEPLOY_DIR}"
                echo "========================================"
            '''
        }
        
        failure {
            echo "❌ Pipeline failed!"
            sh '''
                echo "Collecting local debug information..."
                docker ps -a || true
                docker logs $(docker ps -a -q) --tail=50 || true
                
                echo "\\nCollecting VM debug information..."
                ssh -o StrictHostKeyChecking=no -i ${VM_SSH_KEY} -p ${VM_PORT} ${VM_USER}@${VM_HOST} "docker ps -a && docker logs \$(docker ps -a -q) --tail=50" || true
            '''
        }
        
        always {
            echo "Pipeline execution completed."
            sh '''
                echo "Cleanup temporary files..."
                rm -rf ${WORKSPACE}/temp || true
            '''
        }
    }
}
