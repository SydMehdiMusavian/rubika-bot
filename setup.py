from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="rubika-bot",
    version="1.0.0",
    author="Mehdi Mousavian",
    author_email="meti0513@email.com",
    description="Async Python framework for Rubika Bot API with FSM, filters, and multi-bot support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SydMehdiMusavian/rubika-bot",
    project_urls={
        "Bug Tracker": "https://github.com/SydMehdiMusavian/rubika-bot/issues",
        "Source Code": "https://github.com/SydMehdiMusavian/rubika-bot",
    },
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Communications :: Chat",
        "Intended Audience :: Developers",
    ],
    keywords="rubika, bot, api, async, fsm, framework, rubika-bot",
)