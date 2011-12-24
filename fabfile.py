from fabric.api import local

def clean():
	"Remove all generated files"
	local("rm -rf build dist")

def test():
	"Run unittests"
	local('py.test')

def html():
	"Generate Sphinx documentation"
	local("make html")
