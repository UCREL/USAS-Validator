# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
import logging
sys.path.insert(0, os.path.abspath("../../src"))

import usas_validator

project = 'USAS Validator'
copyright = '2026, UCREL Research Centre'
author = 'UCREL Research Centre'
release = usas_validator.__version__
version = usas_validator.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx_autodoc_typehints'
]

# autodoc settings
autodoc_default_options = {
    'members': True,              # Document all public members
    'undoc-members': True,        # Include members without docstrings
    'private-members': False,     # Exclude _private members
    'special-members': '__init__',# Include __init__ docstrings
    'show-inheritance': True,     # Show base classes
    'exclude-members': 'model_post_init, model_config'
}

autodoc_member_order = 'bysource'  # Keep source file ordering


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest', None)
}


class FilterSphinxAutodocTypehintsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if "Cannot resolve forward reference" in record.msg:
            return False
        if "Failed guarded type import" in record.msg:
            return False
        return True


logging.getLogger("sphinx").addFilter(FilterSphinxAutodocTypehintsFilter())