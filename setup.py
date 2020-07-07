'''
@version: Python 3.7.3
@Author: Louis
@Date: 2020-05-29 16:54:33
@LastEditors: Louis
@LastEditTime: 2020-07-07 14:58:44
'''
from setuptools import setup, find_packages


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
        name='chengyujielong',
        version='2.0.0',
        description='cheng yu jie long solution provider',
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords='game chengyu',
        author='Louis Tian',
        author_email='dqyyrlfy@gmail.com',
        url='https://github.com/SleepAqua/ChengYuJieLong_Pandas',
        packages=find_packages(),
        install_requires =['pandas', 'pypinyin'],
        entry_points={
        "console_scripts": [
            "chengyujielong = chengyujielong.__main__:main"
        ]}
)
