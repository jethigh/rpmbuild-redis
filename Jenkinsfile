def major = ''
def minor = ''
def patch = ''

pipeline {
    agent {
        kubernetes {
            cloud 'crc'
            defaultContainer 'jnlp'
            yamlFile 'buildPod.yaml'
        }
    }
    options { 
        timestamps() 
    } 
    environment {
        REDIS_REPO = "https://github.com/redis/redis.git"
    }
    parameters {
        booleanParam(name: "Centos7", defaultValue: true, description: "Build package for Centos7")
        booleanParam(name: "Centos8", defaultValue: true, description: "Build package for Centos8")
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
                git -c advice.detachedHead=false checkout tags/$REDIS_VERSION
                cd ..
                tar zcf redis.tar.gz redis
                mv redis.tar.gz rpmbuild-redis_$env.BRANCH_NAME
            """
            }
        }
            
        stage('Build RPM package for Centos7') {
            when {
                expression {
                    return params.Centos7
                }
            }
            steps {
                container('mock-rpmbuilder') {
                    echo "Buildig RPM package for Red Hat Enterprise Linux 7"
                }
            }
        }

        stage('Build RPM package for Centos8') {
            when {
                expression {
                    return params.Centos8
                }
            }
            steps {
                container('mock-rpmbuilder') {
                    echo "Buildig RPM package for Red Hat Enterprise Linux 8"
                }
            }
        }
    }

    post {
        always {
            echo "End of pipeline."
        }
    }
}