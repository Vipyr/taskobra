
# Test Approach

## Contents
- [Test Approach](#test-approach)
  - [Contents](#contents)
  - [Overview and Scope (Miguel)](#overview-and-scope-miguel)
  - [Test Environment and Tools](#test-environment-and-tools)
  - [Test Approach](#test-approach-1)
    - [Object Relational Model](#object-relational-model)
    - [Web Frontend (Miguel)](#web-frontend-miguel)
    - [Metric Collection Daemon](#metric-collection-daemon)
    - [Bug Reporting](#bug-reporting)
  - [Continuous Integration (Miguel)](#continuous-integration-miguel)

## Overview and Scope (Miguel)

- General overview stuff
    - Project overview (what is it thats being tested)
    - Components that are going to be tested
    - Activities carried out in each phase of the project (bringup roadmappy stuff)

## Test Environment and Tools

`taskobra` is tested primarily using Python's builtin `unittest` library.  Since it's part of the standard library, there is no additional setup required to run the test suite.  To ensure proper isolation, we recommend using a virtual environment, pip installing `taskobra` in "editable" mode there, then running the unittests.

Testing against multiple python versions is both important, and can be difficult to manage manually.  To solve thise problem, `taskobra` uses [`tox`](https://tox.readthedocs.io/en/latest/) to manage them declaratively.  This allows both our CI/CD platform and developers to easily execute the same test suites in identical environments.

Install `virtualenv`
```
$ pip install virtualenv
```
Install `tox`
```
$ pip install tox
```
Clone and start testing!
```
$ git clone https://github.com/<username>/taskobra
$ cd taskobra
$ tox
```

## Test Approach

### Object Relational Model

The ORM has two main components, the Objects and the Relationships.  To test that our ORM is working properly, we have to test certain properties for each of these types.  For Objects, we must ensure that they are initialized with sane values, can modified in place, and that an object inserted into the database can be positively identified when queried back out.  For Relationships, we must ensure that they propagate through all related objects on database insertion of an Object, and that when an Object in the graph of Relationships is queried out, all other related objects are as well.

### Web Frontend (Miguel)

- Testing PROCESSS
    - Define types of tests (unit, integration, regression, etc)
        - Unit Testing for Python
        - Integration testing for webserver (`python -m taskobra.web`)
        - ??? Other stuff / Risk

### Metric Collection Daemon

The metric collection daemon has two parts to test.  First is the collection of metrics, where each metric must be tested on each supported platform.  Second is the reporting of these metrics, in the form of a Snapshot, to the database.  This can be accomplished by mocking the metric collection functions, replacing them with deterministic sequences, and then checking that the expected snapshot data can be retrieved from the database.

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
