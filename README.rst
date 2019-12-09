OpenWISP Template Library Backend
=================================

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

------------

Project goals
-------------
The main objective of this project is to provide a backend in django for the OpenWISP `library frontend
<https://github.com/openwisp/openwisp-template-library-frontend>`_
It uses `openwisp-controller <https://github.com/openwisp/openwisp-controller>`_
to handle template creation, list and search of public templates, view template
details and ``django-rest-auth`` for user registration and management.

Dependencies
------------

* Python >= 3.6

Installation
------------
Install sqlite:

.. code-block:: shell

    sudo apt-get install sqlite3 libsqlite3-dev openssl libssl-dev


Fork and clone the project and from the project's root directory,

install celery

.. code-block:: shell

    pip install celery

Install project's dependencies

.. code-block:: shell

    python setup.py develop

we need to make sure the gsoc2019 branch of the ``django-netjsonconfig`` and
``openwisp-controller`` repos are installed.
if they are not, you can get them installed with the following commands

.. code-block:: shell

    pip install --upgrade git+git://github.com/openwisp/openwisp-controller.git@gsoc2019#egg=openwisp_controller
    pip install --upgrade git+git://github.com/openwisp/django-netjsonconfig.git@gsoc2019#egg=django_netjsonconfig
    pip install --upgrade git+git://github.com/openwisp/openwisp-users.git@master#egg=openwisp_users
    pip install --upgrade git+git://github.com/openwisp/openwisp-utils.git@master#egg=openwisp_utils

Run migrations, create super user and start the server

.. code-block:: shell

    python tests/manage.py makemigrations
    python tests/manage.py migrate
    python tests/manage.py createsuperuser
    python tests/manage.py runserver

Make sure the redis server is running and then start the celery tasks

.. code-block:: shell

    celery -A template_library worker -l info

We should now have this backend running on ``http://localhost:8000/`` and the frontend to which it is connected to,
should be running on ``http://localhost:3000/`` . if this is not, you can get it up and running by
following the instructions from the `library frontend
<https://github.com/openwisp/openwisp-template-library-frontend>`_

* login to the admin interface and change the ``site`` domain from example.com to ``http://localhost:8000``.
* Create a Facebook and Google ``social application`` with the appropriate providers. You can use the following ``ID`` and ``secret`` for the social application making sure the site url is ``http://localhost:8000``

.. code-block::

    Facebook_client_id = 451356895715832
    Facebook_client_secret = b4bf9d52d91e802b94aec5e4ccd87849
    Google_client_id= 949742045903-rt3svj9go2qhdu7q8nijlhnud4frb0gg.apps.googleusercontent.com
    Google_client_secret = TxXfb0ixcuylgd2k59-6Dyce


Settings
--------
If you wish to deploy this application, then the following settings
need to be adjusted

``CORS_ORIGIN_WHITELIST``
.........................
+--------------+-----------------------------------------------+
| **type**:    | ``list``                                      |
+--------------+-----------------------------------------------+
| **default**: | .. code-block::                               |
|              |                                               |
|              |       [                                       |
|              |          "http://localhost:8000",             |
|              |          "http://localhost:3000"              |
|              |       ]                                       |
+--------------+-----------------------------------------------+

This sets the Cross-Origin Resource sharing white list to the
backend and frontend respectively

``CSRF_TRUSTED_ORIGINS``
........................
+--------------+-----------------------------------------------+
| **type**:    | ``list``                                      |
+--------------+-----------------------------------------------+
| **default**: | .. code-block::                               |
|              |                                               |
|              |      [                                        |
|              |         "localhost:8000",                     |
|              |         "localhost:3000"                      |
|              |      ]                                        |
+--------------+-----------------------------------------------+

This sets the CSRF trusted origins to the backend and frontend respectively

``LOGIN_URL``
.............
+--------------+------------------------------------------------+
| **type**:    | ``string``                                     |
+--------------+------------------------------------------------+
| **default**: | .. code-block::                                |
|              |                                                |
|              |      "http://localhost:3000/login"             |
|              |                                                |
|              |                                                |
+--------------+------------------------------------------------+

This sets the LOGIN_URL to that of the frontend


Contributing
------------
Please read the `OpenWISP contributing guidelines
<http://openwisp.io/docs/developer/contributing.html>`_

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
