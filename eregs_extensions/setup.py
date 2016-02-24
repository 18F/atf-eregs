from setuptools import setup, find_packages

ns = "eregs_ns.parser"  # The namespace for regulations-parser extensions.
fs = "atf_regparser"  # The directory name for the package.
entry_points = {
    "%s.layers" % ns: [
        "Rulings = %s.layers:Rulings" % fs
    ],
    "%s.preprocessors" % ns: [
        "USCode = %s.preprocs:USCode" % fs
    ],
    "%s.test_suite" % ns: [
        "testsuite = %s.tests" % fs
    ],
    "%s.term_definitions" % ns: [
        "atf_terms = %s.term_defs:term_defs" % fs
    ]
}

setup(
    name=fs,
    version="1.0.0",
    packages=find_packages(),
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    entry_points=entry_points,
    install_requires=['pyyaml'],
    package_data={
        fs: ['rulings.yml']
    }
)
