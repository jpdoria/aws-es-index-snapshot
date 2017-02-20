import os
from setuptools import setup, find_packages

with open('requirements.txt') as file_requirements:
    requirements = file_requirements.read().splitlines()

setup(
    name='aws_eis',
    version='1.0.3',
    author='John Paul P. Doria',
    author_email='jp@lazyadm.in',
    description=('Register snapshot directory and take and restore ' +
                 'snapshots of Elasticsearch Service indices.'),
    license='MIT',
    keywords='aws elasticsearch index snapshot',
    url='https://github.com/jpdoria/aws_eis',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aws_eis = aws_eis.aws_eis:main'
        ]
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
)
