from setuptools import setup, find_packages

setup(
    name="toast-exports-sanitizer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "sanitize-data=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
