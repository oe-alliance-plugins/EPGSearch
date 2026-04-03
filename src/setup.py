from setuptools import setup
import setup_translate

pkg = 'Extensions.EPGSearch'
setup(name='enigma2-plugin-extensions-epgsearch',
       version='3.0',
       description='search the epg and list results',
       package_dir={pkg: 'EPGSearch'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo', 'maintainer.info', 'LICENSE', 'setup.xml']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
