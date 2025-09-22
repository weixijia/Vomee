"""
Setup script for Vomee multimodal sensing platform.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vomee",
    version="1.0.0",
    author="Vomee Research Team",
    author_email="contact@vomee.io",
    description="A Multimodal Sensing Platform for Video, Audio, mmWave and Skeleton Data Capturing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weixijia/Vomee",
    project_urls={
        "Bug Tracker": "https://github.com/weixijia/Vomee/issues",
        "Documentation": "https://weixijia.github.io/Vomee",
        "Source Code": "https://github.com/weixijia/Vomee",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "sphinx>=4.0.0",
        ],
        "skeleton": [
            "mediapipe>=0.8.10",
            "tensorflow>=2.8.0",
        ],
        "mmwave": [
            "pyserial>=3.5",
        ],
        "audio": [
            "librosa>=0.9.0",
            "soundfile>=0.10.0",
        ],
        "web": [
            "flask>=2.0.0",
            "flask-socketio>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vomee=vomee.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)