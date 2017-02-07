import enum
import os
import re

PARSE_REGEX = r'(\S+)'   # Get the mode atom
PARSE_REGEX += r'\s*'    # Elmiinate white space
PARSE_REGEX += r'(\S+)'  # Get the lhs atom
PARSE_REGEX += r'\s*'    # Elmiinate white space
PARSE_REGEX += r'(\*?)'  # Check for map atom
PARSE_REGEX += r'(\&?)'  # Check for script local
PARSE_REGEX += r'(\@?)'  # Check for buffer local
PARSE_REGEX += r'\s*'    # Elmiinate white space
PARSE_REGEX += r'(.*)'   # Get the rhs atom


class AtomEnum(enum.IntEnum):
    MODE = 1
    LHS = 2
    MAP = 3
    SCRIPT = 4
    BUFFER = 5
    RHS = 6


def parse(map_list, mode='n') -> list:
    """
    Parse the mapping list for the given mode.

    Returns a list of ParsedLine objects

    Emulates:  {{{
      for l:line in l:map_list
        if l:line =~# '^n'
          let l:mapped = descriptive_maps#parse_line(l:line)
          let l:map_dict[l:mapped['mode']][l:mapped['lhs']] = l:mapped
        elseif l:line =~? '\s*Last set from'
          let l:map_dict[l:mapped['mode']][l:mapped['lhs']]['source'] = descriptive_maps#parse_source(l:line)
        endif
      endfor

      for l:map in keys(l:map_dict['n'])
        " TODO: Try and fix this rather than just let it be.
        try
          let l:map_dict['n'][l:map]['comments'] = descriptive_maps#find_comments(l:map_dict['n'][l:map])
        catch
          let l:map_dict['n'][l:map]['comments'] = []
        endtry
      endfor }}}
    """
    parsed_list = []

    for line in map_list:
        if re.match('^' + mode, line):
            parsed_list.append(ParsedLine(line))

        elif re.match(r'\s*Last set from', line):
            parsed_list[-1].add_source_file_line(line)

    return parsed_list


class ParsedLine:
    """ {{{1 Replacement for old viml way:
    function! descriptive_maps#parse_line(line) abort
      let l:parse_string = '\(\S*\)'            " Get the mode atom
      let l:parse_string .= '\s*'               " Eliminate white space
      let l:parse_string .= '\(\S*\)'           " Get the lhs atom
      let l:parse_string .= '\s*'               " Eliminate white space
      let l:parse_string .= '\(\%[\*]\)'        " Optionally check for the map atom
      let l:parse_string .= '\(\%[&]\)'         " Optionally check for the script local atom
      let l:parse_string .= '\(\%[@]\)'         " Optionally check for the buffer-local atom
      let l:parse_string .= '\s*'               " Eliminate white space
      let l:parse_string .= '\(.*\)'            " Get the rhs atom

      let l:matched = matchlist(a:line, l:parse_string)[1:6]

      let l:mode_atom = 0
      let l:lhs_atom = 1
      let l:remap_atom = 2
      let l:script_atom = 3
      let l:remap_atom = 4
      let l:rhs_atom = 5

      return {
            \ 'raw': a:line,
            \ 'mode': l:matched[l:mode_atom],
            \ 'lhs': l:matched[l:lhs_atom],
            \ 'rhs': l:matched[l:rhs_atom],
            \ 'remap': l:matched[l:remap_atom] ==? '' ? v:false : v:true,
            \ 'source': '',
            \ }
    endfunction
    }}} """

    def __init__(self, line, source_file_line=''):
        self.line = line
        self.match = re.match(PARSE_REGEX, line)

        self.mode = self.match.group(AtomEnum.MODE)
        self.lhs = self.match.group(AtomEnum.LHS)
        self.rhs = self.match.group(AtomEnum.RHS)

        self.mapped = self.bool_group(self.match.group(AtomEnum.MAP))
        self.scripted = self.bool_group(self.match.group(AtomEnum.SCRIPT))
        self.buffered = self.bool_group(self.match.group(AtomEnum.BUFFER))

        # Have to figure out how to get the source file here
        self._source_file_line = source_file_line
        self.requires_update = False

    def bool_group(self, match):
        return match != ""

    def add_source_file_line(self, line):
        self._source_file_line = line
        self.requires_update = True

    @property
    def source_file(self) -> str:
        """
        function! descriptive_maps#parse_source(line) abort
          return matchlist(a:line, '\(\s*Last set from \)\(.*\)')[2]
        endfunction
        """
        if hasattr(self, '_source_file') and not self.requires_update:
            return self._source_file

        if not hasattr(self, '_source_file_line') \
                or self._source_file_line == '':
            return ''

        match = re.match(r'(\s*Last set from )(.*)', self._source_file_line)

        self._source_file = match.group(2)
        return match.group(2)

    @property
    def comments(self) -> list:
        if hasattr(self, '_comments') and not self.requires_update:
            return self._comments

        if not os.path.isfile(self.source_file):
            return []

        with open(self.source_file, 'r') as f:
            lines = f.readlines()

        comments = []
        complete_break = False
        for index, line in enumerate(lines):
            # Check if the right hand side is in the line
            # There might need to be more checking here at some point,
            # like a leader transformation and such.
            if self.rhs in line:
                while True:
                    if index < 0:
                        complete_break = True
                        break

                    match = re.search('^\s*"\s*(.*)', lines[index - 1])

                    if match is None:
                        complete_break = True
                        break

                    comments.insert(0, match.group(1))
                    index -= 1

            # Just be done if we found what we wanted
            if complete_break:
                break

        # Cache the result, so we never need to open the file again
        self._comments = comments
        return comments

    def __str__(self):
        return '<{0}: {1}>'.format(self.lhs, self.rhs)
        return '<{0}: {1} || {2}>'.format(self.lhs, self.rhs, self.source_file)
        return '<{0}: {1} || {2} -- {3}>'.format(self.lhs, self.rhs, self.source_file, self.comments[:10])
