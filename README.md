bulk_web_forward_add
======================

This is an example script that will add both apex and www 301 redirects for a specified zone to a chosen destination in UltraDNS. The input is through a CSV file as shown in test.csv. This script requires the [UltraDNS REST API Client](https://github.com/ultradns/python_rest_api_client) library.

```
$ python web_forward_add.py help
Expected use: python web_forward_add.py username password example.csv [use_http host:port]
Argument 1:
        web_forward_mod.py -- The name of your python file
Argument 2:
        username -- Username of the UltraDNS account
Argument 3:
        password -- UltraDNS account password
Argument 4:
        account_name -- The name of your UltraDNS account
Arguments 5 and 6 (optional):
        use_http -- Specify this value as 'True' if you wish to use a test environment
        host:port -- The hostname and port of your test environment (Example: test-restapi.ultradns.com:443)
```
