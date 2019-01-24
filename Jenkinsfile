#!/usr/bin/env groovy

pipeline {
  triggers {
    pollSCM('*/5 * * * *')
  }
  agent {
    dockerfile {
      filename 'tests/Dockerfile.tests'
    }
  }
  stages {
    stage('Testing') {
      steps {
        sh 'python tests/test_ProxyParser.py'
        sh 'python tests/test_UserAgentParser.py'
      }
    }
  }
}