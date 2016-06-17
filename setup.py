# -*- coding: utf-8 -*-
import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


version = "0.0.0"
name = 'paratest-nunit'
description = "Paratest plugin to run nunit"
module = 'paratest-nunit.nunit'
url = 'https://github.com/paratestproject/paratest-nunit'
author = 'Daniel Aguado Araujo'
author_email = ''
datapath = (
    os.path.join(os.getenv('ProgramData'), 'paratest')
    if platform.system().lower() == 'windows'
    else '/usr/share/paratest'
)


def read_description():
    if not os.path.exists('README.rst'):
        return ""
    with open('README.rst') as fd:
        return fd.read()


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args or ['--cov-report=term-missing'])
        sys.exit(errno)

with open('nunit.paratest', 'w+') as fd:
    content = """
[Core]
Name = {name}
Module = {module}

[Documentation]
Author = {author}
Version = {version}
Website = {url}
Description = {description}
    """.format(
        version=version,
        description=description,
        name=name,
        module=module,
        author=author,
        url=url,
    ).strip()

    fd.write(content)


setup(
    name=name,
    version=version,
    description=description,
    long_description=read_description(),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: '
        'Libraries :: Application Frameworks',
    ],
    keywords='parallel test plugin',
    author='Miguel Ángel García',
    author_email='miguelangel.garcia@gmail.com',
    url=url,
    license='MIT',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={
        '': 'src',
    },
    data_files=[
        (datapath, ['nunit.paratest']),
    ],
    install_requires=[
        'yapsy == 1.11.223',
    ],
)
