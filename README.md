# Steve Zissou

Flask front end for pulling data from and graphing data from [Eleanor](https://github.com/brett-smythe/eleanor).

To see how this fits in with the other repos please see [Aquatic Services Wiki](https://github.com/brett-smythe/ansible_configs/wiki)

## Install
Recommended to install and run in a virtualenv
```
python setup.py install
```

### External Dependencies
steve-zissou depends on having:
* If this is to be deployed in a more production environment you'll likely want to set this up with a WSGI server and likely a static server
* an instance of [Eleanor](https://github.com/brett-smythe/eleanor) running

## Usage
For development
```
steve-zissou
```
For production, as noted above you'll likely want to use a WSGI and static server
