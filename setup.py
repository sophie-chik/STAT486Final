from setuptools import setup, find_packages

setup(
    name="rsi_strategy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "yfinance",
        "scikit-learn",
        "ta",
        "matplotlib",
        "seaborn",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "rsi-strategy=rsi_strategy.cli:main"
        ]
    },
    author="Sophie Chikhladze",
    description="A library for dynamic RSI threshold trading using machine learning."
)
