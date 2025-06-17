from setuptools import setup, find_packages
import os

# Utility function to read the README file.
def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

setup(
    name='tigrinya_normalizer',
    version='0.1.0',
    description='A Tigrinya text normalizer',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Daniel Tesfai',
    author_email='d202361017@xs.ustb.edu.cn',
    url='https://github.com/dantesfai/tigrinya_normalizer',   
    
    packages=find_packages(),
    include_package_data=True,
    
    package_data={
        # Include dictionary files and any data files within the package
        'tigrinya_normalizer': ['dictionaries/*', 'data/*'],
    },
    
    entry_points={
        'console_scripts': [
            'tigrinya-normalize = tigrinya_normalizer.cli:main',
            'tigrinya-dictgen = tigrinya_normalizer.cli_dictgen:main',
        ],
    },

    python_requires='>=3.6',
    install_requires=[
        "regex",
        "numpy",
        "ujson",          # optional, you can mark this as optional in docs
            ],
        extras_require={
            "dev": [
                "pytest",
                "pytest-mock",
                "pytest-cov",
                "pyfakefs",
            ]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Tigrinya",
        "Topic :: Text Processing :: Linguistic",
    ],

)
