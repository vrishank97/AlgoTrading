import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algotrader",
    version="0.1dev",
    author="Vrishank Bhardwaj",
    author_email="vrishank1997@gmail.com",
    description="Python implementations of commonly used trading algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vrishank97/AlgoTrading",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
