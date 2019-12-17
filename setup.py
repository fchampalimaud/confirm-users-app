import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="confirm_users",
    version="0.0",
    description="confirm auto registered users app",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fchampalimaud/confirm-user-app/",
    author=["Ricardo Ribeiro"],
    author_email=["ricardo.ribeiro@research.fchampalimaud.org"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Framework :: Django :: 2.2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="django pyforms-web",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    include_package_data=True,
    install_requires=["django>2.1.0", "django-allauth", "django-notifications-hq>=1.5", "notifications-central"],
    extras_require={"dev": ["black==19.3b0"]},
)
