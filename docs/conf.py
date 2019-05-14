import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('_themes'))

import pochta

project = 'fs-pochta-api'
copyright = '2019, Fogstream'
author = 'Daniil Kharkov'
master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
source_suffix = ['.md', '.rst']
exclude_patterns = ['_build']

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'm2r',
    'sphinx_git',
]

autodoc_default_flags = [':members:']
autoclass_content = 'both'

version = pochta.__version__
# The full version, including alpha/beta/rc tags.
release = pochta.__version__

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, 'Created using Sphinx' is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, '(C) Copyright ...' is shown in the HTML footer. Default is True.
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'fs-pochta-apidoc'
