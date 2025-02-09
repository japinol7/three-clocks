from setuptools import setup

setup(
    name='threeclocks',
    author='Joan A. Pinol  (japinol)',
    version='1.0.0',
    license='MIT',
    description="Three Clocks",
    long_description="Three Clocks",
    url='https://github.com/japinol7/three-clocks',
    packages=['threeclocks'],
    python_requires='>=3.13',
    install_requires=['pygame-ce', 'pygame-gui'],
    entry_points={
        'console_scripts': [
            'threeclocks=threeclocks.__main__:main',
            ],
    },
)
