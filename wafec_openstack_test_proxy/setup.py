from setuptools import setup, find_packages


setup(
    name="wafec.openstack.test_proxy",
    version="1.0.0",
    author="Wallace",
    author_email="wallacefcardoso@gmail.com",
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'wrapt>=1.12.1',
        'Flask>=1.1.2',
        'requests>=2.0.0',
        'psutil>=5.7.0'
    ],
    entry_points={
        'console_scripts': [
            
        ]
    }
)
