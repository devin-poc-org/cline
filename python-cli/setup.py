from setuptools import setup, find_packages

setup(
    name="cline-cli-python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "grpcio>=1.50.0",
        "grpcio-tools>=1.50.0",
        "prompt_toolkit>=3.0.0",
        "rich>=13.0.0",
        "protobuf>=4.21.0",
    ],
    entry_points={
        "console_scripts": [
            "cline-py=cline_cli.main:cli",
        ],
    },
    python_requires=">=3.8",
    author="Cline",
    description="Python CLI for Cline AI coding assistant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
