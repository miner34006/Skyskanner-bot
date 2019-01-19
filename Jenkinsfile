#!/usr/bin/env groovy

pipeline {
  agent any
  stages {
        stage('Test') {
            steps {
                sh 'python ./tests/test_ProxyParser.py'
                sh 'python ./tests/test_UserAgentParser.py'
            }
        }
  }
}