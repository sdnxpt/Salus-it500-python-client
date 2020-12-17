# Salus IT500 python client
This is a simple python client for Salus IT500 thermostat.

## How to use it ?
```python
# PASSWORD should be your md5 hash of your plain password
salus = SalusAPI({'username': USERNAME, 'password_hash': PASSWORD})
salus.login()
print(salus.device())
salus.set_temperature(18)
print(salus.device())
```

## Special thanks to [matthewturner](https://github.com/matthewturner/)!
Inspired by [smartheat-clients](https://github.com/matthewturner/smartheat-clients)
