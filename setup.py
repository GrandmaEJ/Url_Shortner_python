"""URL Shortener v2.0 Setup Configuration"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

requirements = read_requirements("requirements.txt")

setup(
    name="url-shortener-v2",
    version="2.0.0",
    author="URL Shortener Team",
    author_email="team@urlshortener.dev",
    description="Professional URL shortening service with analytics and bulk operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandmaEJ/api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-flask>=1.2.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "isort>=5.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "url-shortener=run:cli",
            "urlshortener=run:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "url_shortener": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
    zip_safe=False,
    keywords="url shortener analytics flask sqlite bulk-operations",
    project_urls={
        "Bug Reports": "https://github.com/GrandmaEJ/api/issues",
        "Source": "https://github.com/GrandmaEJ/api",
        "Documentation": "https://url-shortener.readthedocs.io/",
    },
)