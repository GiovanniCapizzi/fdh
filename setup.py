from setuptools import setup

setup(
    name='fdh',
    version='1.0.0',
    author='Giovanni Capizzi',
    # author_email='aac@example.com',
    packages=['fdh'],
    # url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE',
    description='FSK for data hiding',
    long_description=open('README.md').read(),
    install_requires=[
        "soundfile",
        "numpy",
    ],
)
