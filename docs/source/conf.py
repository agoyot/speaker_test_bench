# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import importlib
import inspect
import logging
import os
import sys
import warnings
from datetime import datetime

import jinja2
from sphinx.ext.autosummary import _import_by_name

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# General configuration
# -----------------------------------------------------------------------------

# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# WARNING: do not delete sphinx.ext.napoleon which supports Google style or
# Numpy docstrings otherwise -> unexpected indentation errors
extensions = [
    "sphinx.ext.napoleon",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_copybutton",
    "sphinx_panels",
    "sphinx_toggleprompt",
    "sphinx_togglebutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.duration",
    "nbsphinx",
    "sphinxemoji.sphinxemoji",
]

exclude_patterns = [
    "**.ipynb_checkpoints",
    # to ensure that include files (partial pages) aren't built, exclude them
    # https://github.com/sphinx-doc/sphinx/issues/1965#issuecomment-124732907
    "**/includes/**",
]

# Import nbconvert in order to include notebooks in the documentation
try:
    import nbconvert
except ImportError:
    # do not declare again a fallback library, notebook function will just be
    # skipped
    logger.warning("nbconvert not installed. Skipping notebooks.")
    exclude_patterns.append("**/*.ipynb")
else:
    try:
        nbconvert.utils.pandoc.get_pandoc_version()
    except nbconvert.utils.pandoc.PandocMissing:
        logger.warning("Pandoc not installed. Skipping notebooks.")
        exclude_patterns.append("**/*.ipynb")


source_path = os.path.dirname(os.path.abspath(__file__))
# sphinx_pattern can be '-api' to exclude the API pages, the path to a file,
# or a Python object (e.g. '.rst')
pattern = os.environ.get("SPHINX_PATTERN")
single_doc = pattern is not None and pattern not in ("-api", "whatsnew")
include_api = pattern is None or pattern == "whatsnew"
# Implement behavior to have when flags are given for Sphinx
if pattern:
    for dirname, dirs, filenames in os.walk(source_path):
        rel_dir = os.path.relpath(dirname, source_path)
        for filename in filenames:
            if os.path.splitext(filename)[-1] in (".rst", ".ipynb"):
                rel_filename = os.path.relpath(
                    os.path.join(dirname, filename), source_path
                )

                if (
                    rel_filename == "index.rst"
                    and os.path.abspath(dirname) == source_path
                ):
                    continue
                if pattern == "-api" and rel_dir.startswith("reference"):
                    exclude_patterns.append(rel_filename)
                elif (
                    pattern == "whatsnew"
                    and not rel_dir.startswith("reference")
                    and rel_dir != "whatsnew"
                ):
                    exclude_patterns.append(rel_filename)
                elif single_doc and rel_filename != pattern:
                    exclude_patterns.append(rel_filename)
# with open(os.path.join(source_path, "index.rst.template")) as f:
#     t = jinja2.Template(f.read())
# with open(os.path.join(source_path, "index.rst"), "w") as f:
#     f.write(
#         t.render(
#             include_api=include_api,
#             single_doc=(pattern if single_doc else None),
#         )
#     )

# matplotlib plot directive
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False
plot_pre_code = """import numpy as np
import pandas as pd"""


# nbsphinx do not use requirejs (breaks bootstrap)
nbsphinx_requirejs_path = ""

# sphinx-panels shouldn't add bootstrap css since the pydata-sphinx-theme
# already loads it
panels_add_bootstrap_css = False

# https://sphinx-toggleprompt.readthedocs.io/en/stable/#offset
toggleprompt_offset_right = 35

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = [".rst"]

# The encoding of source files.
source_encoding = "utf-8"

# The master toctree document.
master_doc = "index"

# The reST default role (used for this markup: `text`) to use for all documents
default_role = "autolink"

# General information about the project.
project = "speaker_test_bench"
# Custom "footer.html" template, using copyright for the current year
copyright = f"{datetime.now().year}"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import speaker_test_bench  # isort:skip

# version = '%s r%s' % (speaker_test_bench.__version__, svn_version())
version = str(speaker_test_bench.__version__)

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = "en"

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all
# documents. default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx"
# Option overriden by html_theme_options dictionary

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# see https://sphinxemojicodes.readthedocs.io/en/stable/
sphinxemoji_style = "twemoji"
# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = "pydata_sphinx_theme"

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'statsmodels.css'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

switcher_version = version
# NOTE: for now we do not use the convention dev and rc in naming
# if ".dev" in version:
#     switcher_version = "dev"
# elif "rc" in version:
#     switcher_version = version.split("rc", maxsplit=1)[0] + " (rc)"


# see for all pygments styles https://pygments.org/styles/
html_theme_options = {
    "external_links": [],
    "footer_start": ["footer"],
    "footer_end": ["sphinx-version"],
    "github_url": "",
    "logo": {
    },
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
    "switcher": {
        "json_url": "_static/versions.json",
        "version_match": switcher_version,
    },
    "pygment_light_style": "xcode",
    "pygment_dark_style": "github-dark",
    # "use_edit_page_button": True,
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = ["themes"]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = "package documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "Package documentation"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/"]
ipython_savefig_dir = "_static"
# If false, no module index is generated.
html_use_modindex = True
html_last_update_fmt = "%b %d, %Y"
html_file_suffix = ".html"

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.

header = f"""\
.. currentmodule:: speaker_test_bench

.. ipython:: python
   :suppress:
   
   import numpy as np
   import pandas as pd
   import json
   
   np.random.seed(123456)
   np.set_printoptions(precision=4, suppress=True)
   pd.options.display.max_rows=15
   
   import os
   os.chdir(r'{os.path.dirname(os.path.dirname(__file__))}')
"""


html_context = {
    "default_mode": "auto",
    "header": header,
    # "github_url": "<your-github-url>",
    # "github_user": "<your-github-org>",
    # "github_repo": "speaker_test_bench",
    # "github_version": "<your-branch>",
    # "doc_path": "<path-from-root-to-your-docs>"
}


# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "speaker_test_bench"


exclude_patterns = []

# -----------------------------------------------------------------------------
# Autosummary
# -----------------------------------------------------------------------------

autosummary_generate = True if include_api else ["index"]
autodoc_typehints = "none"

# -----------------------------------------------------------------------------
# Coverage checker
# -----------------------------------------------------------------------------
coverage_ignore_modules = r"""
    """.split()
coverage_ignore_functions = r"""
    test($|_) (some|all)true bitwise_not cumproduct pkgload
    generic\.
    """.split()
coverage_ignore_classes = r"""
    """.split()

coverage_c_path = []
coverage_c_regexes = {}
coverage_ignore_c_items = {}


# based on numpy doc/source/conf.py
def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    pass


# -----------------------------------------------------------------------------
# Extension Options
# -----------------------------------------------------------------------------
# With .go exclude outputs from copy/paste operation
# https://sphinx-copybutton.readthedocs.io/en/latest/use.html
copybutton_exclude = ".linenos, .gp, .go"
copybutton_remove_prompts = True
