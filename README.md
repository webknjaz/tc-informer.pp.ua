pip install https://bitbucket.org/webknjaz/blueberrypy-wk/get/ced830f454e1.zip
2to3 -w env/lib64/python3.2/site-packages/blueberrypy
2to3 -w env/lib64/python3.2/site-packages/dateutil


[tc-informer] (py3k)
┌─(wk@middle-earth:pts/2)─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────(~/private/kpi/4.1/pm/tc-informer.pp.ua)─┐
└─(1:3:00:%)── blueberrypy create                                                                                                                                                                                             ──(вт,гру18)─┘
Project name: Students Informer
Package name: StudentsSocialNotifier
Version (PEP 386): 1.0
Author name: Svyatoslav Sydorenko
Email: wk@sydorenko.pp.ua
Use controllers backed by a templating engine? [Y/n]
Use RESTful controllers? [y/N]
Use Jinja2 templating engine? [Y/n]
Use webassets asset management framework? [Y/n]
Use redis session? [y/N]
Use SQLAlchemy ORM? [Y/n]
SQLAlchemy database connection URL: mysql+mysqlconnector://ssn_app:LJ%h73yH)$mKML#T^kDF93@localhost/StudentsSocialNotifier

===========================================================================
Your project skeleton has been created under /home/wk/private/kpi/4.1/pm/tc-informer.pp.ua.

Subsystems chosen
-----------------
Routes (RESTful controllers): False
Jinja2: True
webassets: True
redis: False
SQLAlchemy: True

If you now install your package now the packages above will be automatically
installed as well.

e.g. $ pip install -e .

In unrestricted environments, you may also install 'MarkupSafe' and
'cdecimal' to speed up Jinja2 and SQLAlchemy's queries on Decimal fields
respectively. You may also install 'hiredis' if you have opted for the Redis
session storage.

e.g. $ pip install blueberrypy[speedups]

You should also install the appropriate database driver if you have decided
to use BlueberryPy's SQLAlchemy support.

For more information, the BlueberryPy documentation is available at
http://blueberrypy.readthedocs.org.

Happy coding!


pip install -e .
2to3 -w env/lib64/python3.2/site-packages/webassets
pip install mysql-connector-python
