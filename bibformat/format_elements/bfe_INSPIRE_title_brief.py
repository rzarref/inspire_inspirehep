# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2016 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Print titles in the most flexible reasonable fashion
"""

import re

def format_element(bfo, highlight="no", force_title_case="no", brief="no", esctitle='0', oldtitles="no", mode=None):
    """
    Prints a title, with optional subtitles, and optional highlighting.

    @param highlight highlights the words corresponding to search query if set to 'yes'
    @param force_title_case caps First Letter of Each World if set to 'yes'
    @param brief If yes, skip printing subtitles; if no, print complete title:subtitle
    @param esctitle How should escaping of titles in the database be handled?
    @param oldtitles Whether to show old titles in output
    @param mode In mode='tex' apply some TeX sequence escapes to output
    """

    out = ''
    esctitle = int(esctitle)

    titles = bfo.fields('245__', esctitle)
    old_titles = bfo.fields('246__', esctitle)

    # Concatenate all the regular titles (a) and (optionally) subtitles (b)
    for title in titles:
        out += title.get('a', '')
        if brief == "no" and title.has_key('b'):
            out += ' : ' + title['b']

    # Concatenate any old titles (a) and subtitles(b)
    if oldtitles == "yes":
        for old_title in old_titles:
            out += "<br /><b><i>" + old_title.get('a') + '</i></b>'
            if brief == "no" and old_title.has_key('b'):
                out += ' : ' + old_title['b']

    # Hilight matching words if requested
    if highlight == 'yes':
        from invenio import bibformat_utils
        out = bibformat_utils.highlight(out, bfo.search_pattern,
                                        prefix_tag="<span style='font-weight: bolder'>",
                                        suffix_tag='</span>')

    # Force title casing if requested
    if force_title_case.lower() == "yes" and (out.upper() == out or out.find('THE ') >= 0):
        #title is allcaps
        out = ' '.join([word.capitalize() for word in out.split(' ')])
        # .title() too dumb; don't cap 1 letter words


    if mode == 'tex':
        # TeX escape some common sequences
        if out.count('$') == 0:
            out = re.sub(r'(?<!\\)([_%&#])', r'\\\1', out)
            out = re.sub(r'-+&gt;', r'$\,\to\,$', out)
            out = re.sub(r'-+>', r'$\,\to\,$', out)
            out = re.sub(r'(?<!\\)\^', r'\\textasciicircum{}', out)
            greek = '|'.join(('alpha', 'beta', 'gamma', 'Gamma', 'delta', 'Delta', 'epsilon',
                              'zeta', 'eta', 'theta', 'Theta', 'kappa', 'lambda', 'Lambda',
                              'mu', 'nu', 'xi', 'Xi', 'pi', 'Pi', 'rho', 'sigma', 'Sigma',
                              'tau', 'upsilon', 'Upsilon', 'phi', 'Phi', 'chi', 'psi', 'Psi',
                              'omega', 'Omega'))
            out = re.sub(r'\\(' +  greek + r')\b', r'$\\\1$', out)
    return out


# we know the argument is unused, thanks
# pylint: disable-msg=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable-msg=W0613
