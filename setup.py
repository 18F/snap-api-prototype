import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snap-api-prototype",
    version="0.0.1",
    author="Alex Soble",
    author_email="alex.soble@gsa.gov",
    description="A prototype web API that calculates SNAP eligibility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/18F/snap-api-prototype",
    package_dir={'': 'snap_financial_factors'},
    py_modules=['benefit_estimate'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
