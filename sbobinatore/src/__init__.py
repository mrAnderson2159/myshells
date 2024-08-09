import os
import sys
from os.path import join, sep

proj_dir = sep.join(__file__.split(sep)[:-2])
credentials = join(proj_dir, '.sbobinatore-358016-23d7bb18397d.json')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
sys.path.append(os.path.expanduser('~/myshells/pyplugs'))