## Getting started

This is a web app written on Python Flask framework

All dependancies are in ``requirements.txt`` file.

After infrastructure deployment you need to put secret in `SecretManager` for application to work

There are two endpoints:
  1. Default page ``/`` where you can see encrypted "Hello World!"
  2. ``/secret`` Here you can change current password for encryption (Requires Basic Auth. User: ``coingate``  Pass: ``thebest``)
  
Workflows can be found in ``.github/workflows`` folder.
  
`task-definition.json` file is generated from infrastructure and is `required` for CI/CD
