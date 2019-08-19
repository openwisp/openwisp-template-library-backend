Template Library Backend
========================

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

------------

Project goals
-------------
The main objective of this project is provide a backend in django for the library frontend.<br>
this enables the use of modules which have already being made available in OpenWISP Controller<br>
and OpenWISP Users to be used for the template library.

Dependencies
------------

* Python >= 3.6

Installation
------------

Install sqlite:

.. code-block:: shell

    sudo apt-get install sqlite3 libsqlite3-dev openssl libssl-dev


Setup your virtual environment and active it then, Fork and clone the project to your computer and

.. code-block::shell
    cd openwisp-template-library-backend
    python setup.py

Install test requirements:

.. code-block:: shell

    pip install -r requirements-test.txt

Start celeryy task:

.. code-block::shell
    celery -A template_library worker -l info

Create database:

.. code-block:: shell

    cd tests/
    ./manage.py migrate
    ./manage.py createsuperuser

Launch development server:

.. code-block:: shell

    ./manage.py runserver

You can access the admin interface at http://127.0.0.1:8000/admin/.

Run tests with:

.. code-block:: shell

    ./runtests.py


settings
--------

``CORS_ORIGIN_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~~
+--------------+-----------------------------------------------+
| **type**:    | ``list``                                      |
+--------------+-----------------------------------------------+
| **default**: | .. code-block:: python                        |
|              |                                               |
|              |   [                                           |
|              |     "http://localhost:8000",                  |
|              |     "http://localhost:3000"                   |
|              |   ]                                           |
+--------------+-----------------------------------------------+

This sets the Cross-Origin Resource sharing white list to the frontend and backend

CSRF_TRUSTED_ORIGINS
--------------------
+--------------+-----------------------------------------------+
| **type**:    | ``list``                                      |
+--------------+-----------------------------------------------+
| **default**: | .. code-block:: python                        |
|              |                                               |
|              |   [                                           |
|              |     "localhost:8000",                         |
|              |     "localhost:3000"                          |
|              |   ]                                           |
+--------------+-----------------------------------------------+
 This sets the CSRF trusted origins to the frontend and backend

 LOGIN_URL
 --------
 +--------------+-----------------------------------------------+
| **type**:    | ``string``                                     |
+--------------+-----------------------------------------------+
| **default**: | .. code-block:: python                        |
|              |                                               |
|              |                                               |
|              |      "http://localhost:3000/login             |
|              |                                               |
|              |                                               |
+--------------+-----------------------------------------------+
This sets the LOGIN_URL URL to that of the frontend


Contributing
------------

1. Announce your intentions in the `OpenWISP Mailing List <https://groups.google.com/d/forum/openwisp>`_
2. Fork this repo and install it
3. Follow `PEP8, Style Guide for Python Code`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage does not decrease
8. Document your changes
9. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/
.. _NetJSON: http://netjson.org
.. _netjsonconfig: http://netjsonconfig.openwisp.org
