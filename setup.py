import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfiler",
    version="0.0.1",
    author="Cameron Merricck",
    author_email="cameron.merrick@optiv.com",
    description="Automated filesystem routing / filing using prefix-specifiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plasmar/pyfiler
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
