from setuptools import setup

setup(name='densityx',
      version='0.2',
      description='Library to calculate silicate melt density up to 3 GPa given melt composition, pressure, and temperature',
      url='https://github.com/kaylai/DensityX',
      author='Kayla Iacovino',
      author_email='kayla.iacovino@asu.edu',
      license='MIT',
      packages=['densityx'],
      install_requires=[
      		'pandas',
      ],
      zip_safe=False)