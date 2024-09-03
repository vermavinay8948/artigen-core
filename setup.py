from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='artigen-core',
    version='0.1',
    packages=find_packages(include=['artigen_core', 'artigen_core.*']),
    install_requires=requirements,
    include_package_data=True,
    description='Common library with shared code for microservices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/common_lib',
    author='Vinay Verma',
    author_email='vinay.verma@tarkas.ai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
