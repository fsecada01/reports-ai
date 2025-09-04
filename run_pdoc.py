
import os
import sys
from pathlib import Path
import pdoc
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'docs.settings'

# Add the virtual environment's site-packages to sys.path
site_packages_path = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages')
sys.path.append(site_packages_path)

django.setup()

# Build docs: include API and Markdown pages. Place index.md last
# so it becomes the site homepage (docs/api/index.html).
inputs = [
    'reports_ai',
    'docs/usage.md',
    'docs/configuration.md',
    'docs/index.md',
]

pdoc.pdoc(*inputs, output_directory=Path('docs/api'))
