from setuptools import setup

setup(
    name='image_dashboard',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=['image_dashboard',
              ],
    license='MIT',
    long_description=open('README.md').read(),
)
