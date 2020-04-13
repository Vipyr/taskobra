
# Test Approach 

## Contents
- [Overview and Scope](#overview-and-scope)
- [Test Environment](#test-environment-and-tools)
- [Test Approach](#test-approach)
  - [Object Relational Model](#object-relational-model)
  - [Web Frontend](#web-frontend)
  - [Metric Collection Daemon](#metric-collection-daemon)
- [Continuous Integration](#continuous-integration)

## Overview and Scope (Miguel) 

- General overview stuff 
    - Project overview (what is it thats being tested)
    - Components that are going to be tested
    - Activities carried out in each phase of the project (bringup roadmappy stuff)

## Test Environment and Tools (Tom) 

- Tox and Virtual ENV
    - What is this stuff and why did we choose it?
    - How to set up the ENV?
    - etc

## Test Approach 

### Object Relational Model (Tom) 

- Testing PROCESSS
    - Define types of tests (unit, integration, regression, etc)
        - Unit Testing for Python
        - Integration testing for webserver (`python -m taskobra.web`)
        - ??? Other stuff / Risk 
        
### Web Frontend (Miguel) 

- Testing PROCESSS
    - Define types of tests (unit, integration, regression, etc)
        - Unit Testing for Python
        - Integration testing for webserver (`python -m taskobra.web`)
        - ??? Other stuff / Risk 

### Metric Collection Daemon (Tom) 

- Testing PROCESSS
    - Define types of tests (unit, integration, regression, etc)
        - Unit Testing for Python
        - Integration testing for webserver (`python -m taskobra.web`)
        - ??? Other stuff / Risk 

### Bug Reporting 

- Bug handling process 
    - Github Issues
    - Triage of GitHub issues
    - Handling pull requests 

## Continuous Integration (Miguel) 

- TRAVIS! 
    - How travis is set up
    - Why it is set up that way
    - Protected branches
    - PRs 
    
- Deployment?
    - Maybe Dockerhub stuff
    - nightly releases 
    - etc
