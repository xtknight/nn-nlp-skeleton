# -*- coding: utf-8 -*-
import unicodedata
from typing import List

'''
Singleton class that handles tokenization of Unicode input strings
(splits sentence into a series of tokens)

This involves tokenization of punctuation.
Assumes input has been normalized.
'''


class Tokenizer(object):
    """
    Tokenize the specified string and return the tokenized form.
    Typically meant to be used on sentences.
    
    - Whitespace, symbols, and punctuation are set as token boundaries
    - Multiple subsequent punctuation/symbol characters are considered to be 
    separate tokens
    - Punctuation/symbols can be kept or discarded, but the fact that 
    punctuation and symbols are boundaries remains the same
    """

    @staticmethod
    def tokenize(input_str: str, keep_punctuation: bool = True, keep_symbols:
    bool = True) -> List[str]:
        """
        :param input_str: input string
        :param keep_punctuation: whether or not to retain punctuation tokens 
        :param keep_symbols: whether or not to retain symbol tokens
        """

        tokens = []
        last_str = ''

        def commit():
            if last_str:
                tokens.append(last_str)

        for c in input_str:
            cat = unicodedata.category(c)

            if cat.startswith('Z'):
                # whitespace: split at this point
                # commit current token buffer
                commit()

                # empty token buffer
                last_str = ''
            elif cat.startswith('P'):
                # punctuation: split at this point
                # commit current token buffer
                commit()

                if keep_punctuation:
                    last_str = c
                    # commit punctuation token separately
                    commit()

                # empty token buffer
                last_str = ''
            elif cat.startswith('S'):
                # symbol (e.g., ■): split at this point
                commit()

                if keep_symbols:
                    last_str = c
                    # commit symbol token separately
                    commit()

                # empty token buffer
                last_str = ''
            else:
                last_str += c

        # commit whatever tokens we haven't yet after
        # reaching the end of the string
        commit()

        return tokens

    def __init__(self):
        assert None, 'singleton class should not be instantiated'
