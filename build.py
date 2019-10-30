from pybuilder.core import init, use_plugin

@init
def initialize(project):
    # project.build_depends_on(name='protobuf', version='==3.9.1')
    # project.build_depends_on(name='PyGithub', version='==1.43.8')
    # project.build_depends_on(name='paramiko', version='==2.6.0')
    # project.build_depends_on(name='pymongo', version='==3.9.0')

    project.set_property('run_unit_tests_propagate_stdout', True)
    project.set_property('run_unit_tests_propagate_stderr', True)
    project.set_property('verbose', True)
    project.set_property('dir_source_unittest_python', 'unittest')

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')

default_task = ['clean']