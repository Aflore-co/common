from setuptools import setup

setup(name='common',
      version='0.1.1',
      author='Unascribed',
      author_email='tech@polymathventures.co',
      description='Code intended to be used across Polymath Ventures repositories.',
      license='BSD',
      url='https://github.com/PolymathVentures/common',
      packages=['common', 'common.test'],
      install_requires=['PyYAML>=3.11', 'Flask>=0.10.1', 'Flask-SQLAlchemy>=2.0'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
      ],
      )
