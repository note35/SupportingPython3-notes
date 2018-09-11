from setuptools import setup

setup(
    name="test",
    script=['test_print'],

    install_requires=(
        'flake8',
        'pytest',
    ),
)
