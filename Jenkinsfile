pipeline {
    agent { label 'cri-o' } // Укажите метку 'cri-o'

    environment {
        REGISTRY = "quay.io" // CRI-O по умолчанию работает с Quay.io, замените на ваш регистратор
        IMAGE_NAME = "iuda194/sicst_back:prod"
        REGISTRY_CREDENTIALS = credentials('iuda-quay') // Обновите с вашими учетными данными для Quay.io
    }
    stages {
        stage('Build Container Image') {
            steps {
                script {
                    // Создание образа с помощью buildah
                    sh '''
                    buildah bud -t ${REGISTRY}/${IMAGE_NAME} .
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
