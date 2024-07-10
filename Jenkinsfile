pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-iuda')
        IMAGE_NAME = "iuda194/sicst_back:prod"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Выполнение команды docker build . в корне проекта
                    sh 'docker build -t ${IMAGE_NAME} .'
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Логин в Docker Hub и пуш образа
                    sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push ${IMAGE_NAME}
                    '''
                }
            }
        }
    }

    post {
        always {
            // Очистка рабочего пространства после выполнения
            cleanWs()
        }
    }
}
