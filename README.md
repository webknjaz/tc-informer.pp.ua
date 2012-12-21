##Students Informer

###Setting up environment

    # emerge -avu dev-lang/python:3 virtualenv
    $ git clone git@github.com:webknjaz/tc-informer.pp.ua.git
    $ cd tc-informer.pp.ua
      Create virtualenv:
    $ virtualenv --prompt "[tc-informer] (py3k)
    " -p python3.2 --clear env
      and activate it:
    $ source env/bin/activate
      Install required packages then:
    $ pip install https://bitbucket.org/webknjaz/blueberrypy-wk/get/ced830f454e1.zip
    $ pip install mysql-connector-python webassets requests
    $ sed "s/\\.decode\(.*ascii.*\)//" env/lib/python3.2/site-packages/requests/packages/oauthlib/{common.py,oauth1/rfc5849/utils.py}
    $ pip install git+https://github.com/saippuakauppias/pyvka.git
    $ pip install https://bitbucket.org/webknjaz/vkontakte/get/964dcaacfe2f.zip
    $ 2to3-3.2 -w env/lib64/python3.2/site-packages/{blueberrypy,dateutil,webassets,requests}

###Note: Project creation log

    [tc-informer] (py3k)
    ┌─(wk@middle-earth:pts/2)─────────────────────────────────────────────────────(~/private/kpi/4.1/pm/tc-informer.pp.ua)─┐
    └─(1:3:00:%)── blueberrypy create                                                                         ──(вт,гру18)─┘
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
    SQLAlchemy database connection URL: mysql+mysqlconnector://ssn_app:<PASSWD>@localhost/StudentsSocialNotifier
    
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

###Installing app into environmet

    $ pip install -e .

###Running app
    $ blueberrypy serve [-b 0.0.0.0:7777] [-d]
      or
    $ ./init
