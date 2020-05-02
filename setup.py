from setuptools import setup, find_packages

setup(
    name="log_parser",
    version="0.1.0",
    description="Parsing Arecibo CIMA logs and PUPPI command file for NANOGrav",
    author="David Kaplan",
    author_email="kaplan@uwm.edu",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "parse_cimalog=log_parser.scripts.parse_cimalog:main",
            "parse_gbtlog=log_parser.scripts.parse_gbtlog:main",
            "parse_puppi=log_parser.scripts.parse_puppi:main",
        ],
    },
    python_requires=">=2.7",
    include_package_data=True,
    zip_safe=False,
)
