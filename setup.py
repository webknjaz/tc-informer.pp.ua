from setuptools import setup, find_packages

install_requires = ['SQLAlchemy', 'yuicompressor', 'webassets', 'mysql-connector-python']

setup(name='StudentsSocialNotifier',
      version='1.0',
      author='Svyatoslav Sydorenko',
      author_email='wk@sydorenko.pp.ua',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=["test**"]),
      install_requires=install_requires,
      zip_safe=False)
