from setuptools import setup, find_packages

setup(
    name="pysoda",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pysoda",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openpyxl",
        # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)