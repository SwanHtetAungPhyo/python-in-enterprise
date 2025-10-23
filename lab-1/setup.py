from setuptools import setup, find_packages

setup(
    name="data_analyzer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "analyze-data=cli.main:main",
        ],
    },
    python_requires=">=3.7",
    include_package_data=True,
)


# analyze-data --file data.json --thres 5