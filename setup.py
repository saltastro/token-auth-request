import setuptools

setuptools.setup(
    name="token_auth_request",
    version="0.1.0",
    url="https://github.com/saltastro/token-auth-request",

    author="SAAO/SALT",
    author_email="salthelp@salt.ac.za",

    description="HTTP requests with token-based authentication",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
