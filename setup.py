from setuptools import setup, find_packages

long_description = """This is an unofficial API use to interact with the trading212 platform. It is still currently in
                   it's testing stages I created this API to challenge myself and also start creating a portfolio of
                   work that i can showcase to employers"""

setup(
    name="apit212",
    version="3.0.1",
    packages=find_packages(),
    requires=[
        'requests',
        'selenium',
    ],
    author="Flock92",
    author_email="stuwe_3000@outlook.com",
    description="Unofficial trading212 API",
    long_description=long_description,
    license="MIT",
    keywords="trading api" "python3" "trading212" "API",
    url="https://github.com/Flock92/aPit212",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ]
)
