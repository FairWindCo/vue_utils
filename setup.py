from setuptools import setup, find_packages

setup(name='vue_utils',
      version='0.3',
      description='Small VUE utils for django develop',
      long_description='Small pack classes and functions for for django develop that use VUE',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='django vue ajax',
      url='https://github.com/FairWindCo/vue_utils',
      author='FairWindCp',
      author_email='sergey.manenok@gmail.com',
      license='MIT',
      packages=find_packages(),
      # packages=['vue_utils', 'vue_utils.templatetags', 'vue_utils.tests'],
      package_data={'vue_utils': ['static/vue_utils/*/*', 'static/vue_utils/*/*/*', 'static/vue_utils/*',
                                  'templates/vue_utils/*.html']},
      install_requires=[
          'Pillow>=8.1.2', 'django>=3.1.7', 'requests>=2.25.1', 'num2words>=0.5.10'
      ],
      include_package_data=True,
      zip_safe=False)
