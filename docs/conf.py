# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pygments.token import (Comment, Error, Generic, Name, Number, Operator,
                            String, Text, Whitespace, Keyword)
sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'Youtube Scraping API'
copyright = '2021, The Silly Coder'
author = 'The Silly Coder'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    'autodocsumm'
]

dirty_model_property_label = ''
dirty_model_add_classes_to_toc = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

autodoc_default_options = {
    'autosummary': True,
}

autodata_content = 'both'

autosummary_generate = True
autodoc_default_flags = ['members']
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_static_path = ['_static']
html_css_files = ["mod.css"]
html_js_files = ['jquery.visible.min.js']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinxawesome_theme"
html_domain_indices = True
html_favicon = '_static/favicon.ico'

import pygments.styles, pygments.token
def monkeypatch_pygments(name, base_name='default', attrs={}):
    import importlib, sys
    base_module = importlib.import_module('.'.join(['pygments', 'styles', base_name]))

    def name_to_class_name(name):
        return name.replace('_', ' ').title().replace(' ', '') + 'Style'
    base_class = getattr(base_module, name_to_class_name(base_name))
    styles = getattr(base_class, 'styles', {}).copy()
    styles.update(attrs.pop('styles', {}))
    attrs['styles'] = styles
    class_name = name_to_class_name(name)
    Style = type(class_name, (base_class,), attrs)
    module = type(base_module)(name)
    setattr(module, class_name, Style)
    setattr(pygments.styles, name, module)
    pygments.styles.STYLE_MAP[name] = f'{name}::{class_name}'
    sys.modules['.'.join(['pygments', 'styles', name])] = module

BLUE_LIGHT = '#0080ff'
BLUE = '#2c5dcd'
GREEN = '#65B315'
GREEN_LIGHT = '#65B315'
GREEN_NEON = '#65B315'
GREY = '#aaaaaa'
GREY_LIGHT = '#cbcbcb'
GREY_DARK = '#4d4d4d'
PURPLE = '#9682FA'
RED = '#cc0000'
RED_DARK = '#FC6A7E'
RED_LIGHT = '#ffcccc'
RED_BRIGHT = '#ff0000'
WHITE = '#ffffff'
TURQUOISE = '#318495'
ORANGE = '#ff8000'  

pygments_style = 'custom'  # Arbitrary name of new style
monkeypatch_pygments(
    pygments_style,
    'rainbow_dash',  # Name of base style to use
    {
        'styles': {
            Comment: 'italic #A9AEB9',
            Comment.Preproc: 'noitalic',
            Comment.Special: 'bold',

            Error: '#FC0000',

            Keyword: '#E0A800',
            Keyword.Pseudo: 'nobold',
            Keyword.Type: PURPLE,

            Name.Attribute: 'italic {}'.format(BLUE),
            Name.Builtin: PURPLE,
            Name.Class: 'underline',
            Name.Constant: TURQUOISE,
            Name.Decorator: PURPLE,
            Name.Entity: 'bold {}'.format(PURPLE),
            Name.Exception: PURPLE,
            Name.Function: '#00B0D4',
            Name.Tag: 'bold {}'.format(BLUE),

            Number: '#ED7940',

            Operator: '#868D9C',
            Operator.Word: '',

            String: GREEN,
            String.Doc: 'italic #A9AEB9',
            String.Escape: RED_DARK,
            String.Other: TURQUOISE,
            String.Symbol: RED_DARK,

            Text: GREY_DARK,

            Whitespace: GREY_LIGHT
        }
    }
)