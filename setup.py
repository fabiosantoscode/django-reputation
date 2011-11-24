try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    'django-appconf>=0.4.1'
]


setup(
    name='django-reputation',
    version="0.1.0",
    description='Generic user reputation application for Django',
    url='http://github.com/vad/django-reputation',
    packages=['reputation'],
    zip_safe=True,
    license='BSD',
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
    install_requires=install_requires,
)
