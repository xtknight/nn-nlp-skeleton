# -*- coding: utf-8 -*-
import unicodedata
from jamo import h2j, j2hcj
from unicode_symbols import UnicodeSymbols

'''
Singleton class that handles normalization of Unicode input strings, and
also normalization of Korean to compatibility Jamo when necessary
'''


class Normalizer(object):
    """
    Normalize the specified string and return the normalized form
    """

    @staticmethod
    def normalize(s: str) -> str:
        # 1. Apply standard Unicode normalization
        # (convert full-width characters to half-width, and
        # also converts superscript/subscript to canonical form)
        # Normalization Form Compatibility Composition
        # https://en.wikipedia.org/wiki/Unicode_equivalence
        n_s = unicodedata.normalize('NFKC', s.strip())

        # 2. Apply custom normalization rules for symbols and whitespace
        n_s = Normalizer.normalize_symbols(n_s)

        # 3. Convert all Korean characters to compatibility Jamo
        n_s = Normalizer.normalize_to_compatibility_jamo(n_s)

        return n_s

    """
    Normalize symbols in the string and return the normalized form
    e.g., convert Asian quotes to normal quotes
    
    http://xahlee.info/comp/unicode_matching_brackets.html
    https://gist.github.com/goodmami/98b0a6e2237ced0025dd
    """

    @staticmethod
    def normalize_symbols(s: str) -> str:
        # 1. Normalize quotes, parentheses, square brackets, angle brackets,
        # and curly brackets

        for c in UnicodeSymbols.SYMBOLS_LEFTQUOTES:
            s = s.replace(c, "'")
        for c in UnicodeSymbols.SYMBOLS_RIGHTQUOTES:
            s = s.replace(c, "'")
        for c in UnicodeSymbols.SYMBOLS_GRAVE:
            s = s.replace(c, "'")

        for c in UnicodeSymbols.SYMBOLS_LEFTPARENTHESES:
            s = s.replace(c, '(')
        for c in UnicodeSymbols.SYMBOLS_RIGHTPARENTHESES:
            s = s.replace(c, ')')

        for c in UnicodeSymbols.SYMBOLS_LEFTSQUAREBRACKET:
            s = s.replace(c, '[')
        for c in UnicodeSymbols.SYMBOLS_RIGHTSQUAREBRACKET:
            s = s.replace(c, ']')

        for c in UnicodeSymbols.SYMBOLS_LEFTANGLEBRACKET:
            s = s.replace(c, '<')
        for c in UnicodeSymbols.SYMBOLS_RIGHTANGLEBRACKET:
            s = s.replace(c, '>')

        for c in UnicodeSymbols.SYMBOLS_LEFTCURLYBRACKET:
            s = s.replace(c, '{')
        for c in UnicodeSymbols.SYMBOLS_RIGHTCURLYBRACKET:
            s = s.replace(c, '}')

        # 3. Normalize spaces
        for c in UnicodeSymbols.SYMBOLS_WHITESPACE:
            s = s.replace(c, ' ')

        # replace double spaces with single spaces
        s = ' '.join(s.strip().split())

        return s

    """
    Return whether or not the specified character is in the
    non-compatible Jamo range
    """

    @staticmethod
    def is_non_compatibility_jamo(c: str) -> bool:
        assert len(c) == 1
        # HANGUL JAMO: (U+1100-U+11FF)
        if ord(c) >= 0x1100 and ord(c) <= 0x11FF:
            return True
        else:
            return False

    """
    Normalize all Korean characters in the specified string
    to the compatible Jamo range
    """

    @staticmethod
    def normalize_to_compatibility_jamo(s: str) -> str:
        out = ''
        for c in s:
            if Normalizer.is_non_compatibility_jamo(c):
                out += j2hcj(c)
            else:
                out += c
        assert len(s) == len(out)
        return out

    def __init__(self):
        assert None, 'singleton class should not be instantiated'