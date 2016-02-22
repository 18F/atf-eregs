from setuptools import setup

ns = "eregs_ns.parser"  # The namespace for regulations-parser extensions.
fs = "atf_regparser"  # The directory name for the package.
entry_points = {
    "%s.preprocessors" % ns: [
        "USCode = %s.preprocs:USCode" % fs
    ],
    "%s.test_suite" % ns: [
        "testsuite = %s.tests" % fs
    ]
}

setup(
    name=fs,
    version="1.0.0",
    packages=[fs],
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    entry_points=entry_points
)
