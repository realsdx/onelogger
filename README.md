# Onelogger
[![Build Status](https://travis-ci.com/realsdx/onelogger.svg?branch=master)](https://travis-ci.com/realsdx/onelogger) ![Code Size in bytes](https://img.shields.io/github/languages/code-size/realsdx/onelogger.svg?style=flat) ![Python Versions](https://img.shields.io/pypi/pyversions/django.svg?style=flat)

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg) [![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/kinda-sfw.svg)](https://forthebadge.com)

[![GSoC Heat](https://img.shields.io/badge/GSoC%20Heat-2019-orange.svg)](https://nitdgpos.github.io/gsoc_heat)


This is an open source IP Logger with Private IP Logging capability.
For now it can log any target's Public/Private IPs and User-Agent.

## For contributors

If you want to contribute to this project then have a look [CONTRIBUTING.md](CONTRIBUTING.md)

## Building from Source

1. Create a **virtual environment** with venv(install venv, if its not installed).

    ```
    python3 -m venv django-env

    ```

2. Clone the project in the same directory.

    ```
    git clone https://github.com/realsdx/onelogger.git

    ```

3. Activate the virtual environemnt.

    #### For Linux/Mac OSX   
    ```
    source dajngo-env/bin/activate

    ```
    ### For Windows
    `I don't care, find it yourself.`

4. Install the requirements.

    ```
    cd onelogger
    pip install -r requirements.txt

    ```


7.  Migrate your database and run the Django Development Server.

    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

    ```

8. Open `http://localhost:8000` in your browser.


