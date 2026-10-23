@Library('Shared')_

pipeline {
    agent { label 'Ash' }

    stages {
        stage("Code clone") {
            steps {
                sh "whoami"
                clone("https://github.com/Ashish20034/django-notes-stqa.git", "main")
            }
        }

        stage("Code Build") {
            steps {
                dockerbuild("notes-app", "latest")
            }
        }

        stage("Test") {
            steps {
                sh 'docker run --rm notes-app:latest python manage.py test api --settings=notesapp.test_settings -v 2'
            }
        }

        stage("Push to DockerHub") {
            steps {
                dockerpush("dockerHubCreds", "notes-app", "latest")
            }
        }

        stage("Deploy") {
            steps {
                deploy()
            }
        }
    }
}
