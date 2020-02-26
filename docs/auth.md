# Authentication
[Home](../index.md)

![Grant Type Authentication Flow](images/auth_code_flow.png)

## Design Goals

Providing remote access to machine processes and metrics data could easily create a security risk, especially when using Taskobra outside of of a Local Area Network. To address this, we need to take into account modern authentication techniques and leverage them to provide the most secure platform possible.

When designing a system that will operate in the modern world, we need to be able to leverage all modern techniques, from 2-Factor Authentication to easily being able to reset a password when compromised, and secure storage of secrets. These are solved problems and we don't need to reinvent the wheel, so we are going to leverage the most popular authentication service protocol, OAuth2, to allow users to continue to use existing and trusted credentials while securing the process data.

## Features

#### Security Guaranteed
- By using OAuth2, we prevent the need for custom authentication code which has to be vetted and maintained
- OAuth2 uses third-party providers that guaruntee the saftey of user data already, and have full time teams maintaining security
- OAuth2 is a trusted standard that's been maintained for almost a decade

#### Optional OAuth2 Enablement
- When installing the server side packages, Users will have an option to enable OAuth2
    - This allows local instances without remote listeners to operate out of the box without additional setup
    - Due to the nature of OAuth2, setting up credentials and registering an app with a service can be unnecessarily time consuming

#### Support for Popular Services
- Google provides the most popular OAuth2 Support
    - Google's authentication services will work out of the box
    - Taskobra will use an extremely narrow scope of the Google API to do authentication
- Other service providers can be available via configuration
    - The callback URL provided to Taskobra just needs to have an email attribute in its response

## Implementation
- By default authentication will be disabled
    - Configuring OAuth2 for a deployment will be done simply via a Configuration file
    - Passing the Configuration to the deployment container will enable and require authentication for viewing the UI

- OAuth2 will be used for Authentication only
    - Tokens will not be persistent, requiring re-authentication after sessions expire
    - Tokens will be maintained in the user's browser session, ensuring we don't need to guard against data leaking on the server
    - Non-secret information relating to user identity will be stored in the database to segregate user data and allow for more than one user per deployment

- OAuth2 will be implemented on the Python-Flask backend
    - This requires a popular python library `requests_oauthlib`
    - Authentication will use the standard OAuth2 Web Application Flow
    - Several examples of this implementation can be found in the [References](references.md)


## Depdencies and Libraries

#### Requests
[https://requests.readthedocs.io/en/master/]()

#### OAuth Requests Lib
[https://requests-oauthlib.readthedocs.io/en/latest/]()



