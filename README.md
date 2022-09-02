## Getting started

This is a web app written on Python Flask framework

All dependancies are in ``requirements.txt`` file.

After infrastructure deployment you need to put secret in `SecretManager` for application to work

There are two endpoints:
  1. Default page ``/`` where you can see encrypted "Hello World!"
  2. ``/secret`` Here you can change current password for encryption (Requires Basic Auth. User: ``coingate``  Pass: ``thebest``)
  
Workflows can be found in ``.github/workflows`` folder.
  
`task-definition.json` file is generated from infrastructure and is `required` for CI/CD


#### You can check running app here: http://cg-testas-lb-prod-1146727359.eu-central-1.elb.amazonaws.com/




## Original task: 

Deploy a publicly available application to the ECS on GitHub push trigger.
The application must provide two endpoints:
- One endpoint prints an encrypted "Hello, World!" string using AES with a secret value pulled from AWS Secret Manager.
- The second is the protected (authentication, IP whitelist, etc. Your choice.) endpoint which updates the secret value used to encrypt the "Hello, World!" string in AWS Secret Manager. All changes must be logged in S3 with the old secret value, IP and user agent of whom the change was made.
- Use any programming language you want.
- Infrastructure must be described with Terraform.
- The deployment must be zero downtime.
- Use load balancer.
