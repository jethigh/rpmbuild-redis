pipeline {
    agent any 
    environment {
        REDIS_REPO = "https://github.com/redis/redis.git"
    }
    stages {
        stage('Download Redis sources') {
            steps {
                echo "Pulling Redis source code from: $REDIS_REPO"
            }
        }
    }
}