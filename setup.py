from setuptools import setup, find_packages

setup(
name="WaterMarkTool",
version="0.0.5",
description="A little tool to add water mark on various pictures",
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
packages=find_packages(),
install_requires=[
    'pillow <= 10.2.0',
],
url="https://pypi.org/project/WaterMarkTool/",
download_url="https://files.pythonhosted.org/packages/f8/78/62f49f1724ecd30cd4f998d5f9c2a4e041a56cb4dc7adaec21df502b7b95/WaterMarkTool-0.0.2.tar.gz",
license="MIT",
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires=">=3.6",
)