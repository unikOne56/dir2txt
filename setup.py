from setuptools import setup, find_packages

setup(
    name="dir2txt",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dir2txt=dir2txt.__main__:main",
        ],
    },
    python_requires=">=3.7",
    author="unikOne56",
    description="Dump your entire project into one text file",
    license="MIT",
)