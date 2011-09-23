# Rakefile for GNTP Project

# You can set these variables from the command line.
SPHINXOPTS    = ""
SPHINXBUILD   = "sphinx-build"
BUILDDIR      = "build"

# Internal variables.
ALLSPHINXOPTS   = "-d #{BUILDDIR}/doctrees docs"

desc "Remove all generated files"
task :clean do |t|
	sh "rm -rf #{BUILDDIR}/*"
end

desc "Build standalone HTML files"
task :html do |t|
	sh "#{SPHINXBUILD} -b html #{ALLSPHINXOPTS} #{BUILDDIR}/html"
end

desc "Check code against PEP8"
task :check do |t|
	sh "pep8 ."
end
