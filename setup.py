from setuptools import setup

setup(
    name='thumb_cutter',
    version='v.1',
    packages=['thumb_cutter'],
    url='https://github.com/jonp92/thumb-cutter',
    license='MIT',
    author='Jonathan Pressler',
    author_email='jonathan@pressler.tech',
    description='A small Python program to strip thumbnails from .gcode files and save them as a .png'
                ' and then uploading to another server using SCP.',
    install_requires=[
        'watchdog',
    ],
)
