#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its
# containing dir.

import sphinx_utils

import sys
from pathlib import Path


DEFAULT_LIGHT_SYNTAX_THEME = 'friendly'
DEFAULT_DARK_SYNTAX_THEME = 'monokai'


def setup(app):
    # Note: After enabling/disabling an augment, run sphinx with
    #
    #   sphinx-build -b html -a -E docs/source docs/build/html
    #
    # to suppress build output and rebuild all files.

    augment = sphinx_utils.augment(app, 'programming-guides')
    augment.theme_switcher(
        [
            {'id': 'light', 'icon': '☼'},
            {'id': 'dark', 'icon': '☽'},
        ],
        syntax_themes=[
            DEFAULT_LIGHT_SYNTAX_THEME,
            DEFAULT_DARK_SYNTAX_THEME,
            'sphinx_utils.pygments_styles.cobalt2.Cobalt2Style',
        ],
        default_theme='window.matchMedia("(prefers-color-scheme: dark)").matches ? "{}" : "{}"'.format(DEFAULT_DARK_SYNTAX_THEME, DEFAULT_LIGHT_SYNTAX_THEME),
        default_syntax_theme='siteThemeId === "dark" ? "{}" : "{}"'.format(DEFAULT_DARK_SYNTAX_THEME, DEFAULT_LIGHT_SYNTAX_THEME),
    )

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '3.0.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'programming-advice'
author = 'Aran-Fey'
copyright = '2020, ' + author

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.1'
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


smartquotes = False

# -- Options for HTML output ----------------------------------------------

html_theme = "advice"
html_theme_path = [sphinx_utils.HTML_THEMES_DIR]
html_show_copyright = False
html_show_sphinx = False
html_title = "Aran-Fey's (python) programming guides"
html_favicon = "favicon.png"
