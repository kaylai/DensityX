import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DensityX",
    version="2.0.0",
    author="Kayla Iacovino",
    author_email="kaylaiacovino@gmail.com",
    description=("A python library for calculating silicate liquid densities."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaylai/DensityX",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
