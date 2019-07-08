import os

from setuptools import find_packages, setup

from template_library import get_version

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        if line.startswith('#') or line == '' or line.startswith('http') or line.startswith('git'):
            continue
        requirements.append(line)
    return requirements


setup(
    name='template-library',
    version=get_version(),
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    license='GPL3',
    description='Backend for the template library website',
    long_description=README,
    url='https://github.com/openwisp/openwisp-template-library-backend',
    author='Noumbissi Valere Gille Geovan',
    author_email='noumbissivalere@gmail.com',
    install_requires=get_install_requires(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking',
        'Intended Audience :: Administrators',
        'License :: OSI Approved :: GPL-3 License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
    ],
)
