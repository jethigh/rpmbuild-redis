def major = ''
def minor = ''
def patch = ''

pipeline {
    agent any 
    environment {
        REDIS_REPO = "https://github.com/redis/redis.git"
    }
    parameters {
        booleanParam(name: "RHEL7", defaultValue: true, description: "Build package for RHEL7")
        booleanParam(name: "RHEL8", defaultValue: true, description: "Build package for RHEL8")
        string(name: "REDIS_VERSION", defaultValue: "7.0.7", trim: true, description: "Please enter version from witch rpm package going to be builded.")
//        text(name: "TEST_TEXT", defaultValue: "Jenkins Pipeline Tutorial", description: "Sample multi-line text parameter")
//        password(name: "TEST_PASSWORD", defaultValue: "SECRET", description: "Sample password parameter")
//        choice(name: "TEST_CHOICE", choices: ["production", "staging", "development"], description: "Sample multi-choice parameter")
    }
    stages {
        stage('Download Redis sources') {
            steps {
                echo "Pulling Redis source code from: $REDIS_REPO"
                script {
                    (major, minor, patch) = params.REDIS_VERSION.tokenize('.')
                }
                sh """
                    cd ..
                    git clone $REDIS_REPO
                """
            }
        }

        stage('Select tag, compress and move to SOURCES') {
            steps {
            sh """
                cd ../redis
                git checkout tags/$REDIS_VERSION
                cd ..
                tar zcvf redis.tar.gz redis
                mv redis.tar.gz rpmbuild-redis_$env.BRANCH_NAME
            """
            }
        }
    }
}