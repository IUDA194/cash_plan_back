pipeline {
    agent any

    environment {
        IMAGE_NAME = "iuda194/sicst_back:prod"
        REGISTRY_CREDENTIALS = credentials('docker-iuda')
    }
    stages {
        stage('Build Container Image') {
            steps {
                script {
                    // Создание образа с помощью buildah
                    sh '''
                    buildah bud -t ${IMAGE_NAME} .
                    '''
                }
            }
        }
        
        stage('Push Container Image') {
            steps {
                script {
                    // Логин в Quay.io и пуш образа
                    sh '''
                    buildah login -u $REGISTRY_CREDENTIALS_USR -p $REGISTRY_CREDENTIALS_PSW ${REGISTRY}
                    buildah push ${REGISTRY}/${IMAGE_NAME}
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
