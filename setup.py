from setuptools import setup, find_packages

setup(
    name="WaterMarkTool",
    version="0.0.8",
    packages=find_packages(),
    install_requires=["solana <= 0.30.2"],
    author='GamingGGa',
    author_email='GabrielGaming1443@gmail.com',
    description="A little tool to add water mark on various pictures",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/GamingGGa/WaterMarkTool",
    project_urls={
        'Source': 'https://github.com/GamingGGa/WaterMarkTool',
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6",
)