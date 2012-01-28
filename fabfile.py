from fabric.api import local


def clean():
	"Remove all generated files"
	local("rm -rf build dist")
	local("find . -name *.pyc -delete")


def test():
	"Run unittests"
	local('py.test')


def html():
	"Generate Sphinx documentation"
	local("sphinx-build -b html -d build/doctrees docs build/html")


def build():
	local("python setup.py build")
