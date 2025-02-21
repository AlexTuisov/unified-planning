#!/usr/bin/env python3

from setuptools import setup, find_packages # type: ignore
import unified_planning


long_description=\
"""============================================================
 Unified planning: A library that unifies planning frameworks
 ============================================================
    Insert long description here
"""

setup(name='unified_planning',
      version=unified_planning.__version__,
      description='Unified Planning Framework',
      author='AIPlan4EU Project',
      author_email='aiplan4eu@fbk.eu',
      url='https://www.aiplan4eu-project.eu',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.7',  # supported Python ranges
      install_requires=['pyparsing'],
      extras_require={
          'dev':['tarski[arithmetic]','pytest','pytest-cov','mypy'],
          'grpc': ['grpcio', 'grpcio-tools', 'grpc-stubs'],
          'tarski': ['tarski[arithmetic]'],
          'pyperplan': ['up-pyperplan==0.1.0.14.dev1'],
          'tamer': ['up-tamer==0.1.0.15.dev1'],
          'solvers': [
              'tarski[arithmetic]',
              'up-pyperplan==0.1.0.14.dev1',
              'up-tamer==0.1.0.15.dev1'
          ]
      },
      license='APACHE',
      keywords='planning logic STRIPS RDDL',
      classifiers=[
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',

          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'License :: OSI Approved :: Apache Software License',

          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
)
