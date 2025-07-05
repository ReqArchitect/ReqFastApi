from setuptools import setup, find_packages

setup(
    name='architecture_suite_sdk',
    version='0.1.0',
    description='Python SDK for architecture_suite platform',
    author='architecture_suite Team',
    packages=find_packages(),
    install_requires=[
        'urllib3 >=1.25.3',
        'python-dateutil',
        'setuptools',
        'requests'
    ],
    python_requires='>=3.7',
)
