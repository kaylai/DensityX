from setuptools import setup

setup(name='densityx',
      version='1.2.0',
      description='Library to calculate silicate melt density up to 3 GPa given melt composition, pressure, and temperature',
      url='https://github.com/kaylai/DensityX',
      author='Kayla Iacovino',
      author_email='kaylaiacovino@gmail.com',
      license='MIT',
      packages=['densityx'],
      install_requires=[
      		'pandas',
                  'openpyxl',
                  'numpy'
      ],
      zip_safe=False)