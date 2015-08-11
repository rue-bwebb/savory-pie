#Savory Pie

Savory Pie is an API building library, we give you the pieces to build the API
you need. Currently Django is the main target, but the only dependencies on
Django are a single view and Resources and Fields that understand Django's ORM.


[![Build Status](https://travis-ci.org/RueLaLa/savory-pie.svg?branch=master)](https://travis-ci.org/RueLaLa/savory-pie) 
[![Coverage Status](https://coveralls.io/repos/RueLaLa/savory-pie/badge.svg?branch=master&service=github)](https://coveralls.io/github/RueLaLa/savory-pie?branch=master)

[![PyPI version](https://img.shields.io/pypi/v/savory-pie.svg)](https://pypi.python.org/pypi/savory-pie/)
[![PyPI downloads](https://img.shields.io/pypi/dm/savory-pie.svg)](https://pypi.python.org/pypi/savory-pie/)
[![PyPI](https://img.shields.io/pypi/l/savory-pie.svg)](https://pypi.python.org/pypi/savory-pie/)

Documentation
-----
http://savory-pie.readthedocs.org/en/latest/


Installing
----
Note: it's recommended that you use `ujson` over the built in `json` library due to increased performance
```
    pip install savory-pie
```

Installing for Django
-----
```
    pip install django_dirty_bits >= 0.1.3.2
    pip install Django > 1.4
```

Local Development Environment
-----
It is highly recommended to use a virtualenv
```
    pip install -r requirements.txt
    pip install -e .
```


Running Tests
-----
```
    python run_tests.py
```

Running Tests Coverage
-----
```
    python run_tests.py --with-coverage
    coverage report -m  # To check the %
    coverage html
```

Updating PyPi (to whom it may concern)
-----
This builds the project, and uploads it to PyPi (credentials needed)
```
python setup.py sdist register upload
```

```
its a pie, mate

        ---                       ---
    -.UU   UU.-     _____     -.UU    UU.-
   -UU       UU.------------.UU         UU-
   -U   ``                       ``     U-
    ~Uu  ```                   ```   uU~
     ~u                              u~
      '       ()            ()       '
       '           / "" \           '
      ~            |    |            ~
       ~           \    /           ~
       ~             ''             ~
        ~          /-----\         ~
          ~~~                  ~~~
              ~~~~~~~~~~~~~~~~
```
