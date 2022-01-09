from setuptools import setup, find_packages

setup(
        name="spilite",
        version="0.1",
        description="A lite wrapper for spidev with entry and exit",
        author="xdylanm",
        url="https://github.com/xdylanm/spilite",
        packages=find_packages(include=['spilite','spilite.*']),
        install_requires=[
            'spidev',
            'gpiozero'
        ]
)
