from setuptools import setup, find_packages

setup(
    name='lii3ra',
    version="0.0.1",
    description="trading investment",
    author='1011',
    author_email='takeyuki.t@gmail.com',
    license='MIT',
    classifiers=[
        # https://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 1 - Planning"
    ],
    keywords='lii3ra',
    install_requires=[
        "pandas",
        "numpy",
        "yfinance",
        "oandapyV20",
        "iso8601"
        ],
)

