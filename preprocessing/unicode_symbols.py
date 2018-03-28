# -*- coding: utf-8 -*-
class UnicodeSymbols(object):
    '''
    OPEN_QUOTES = (
        '\u0022'  # quotation mark (")
        '\u0027'  # apostrophe (')
        '\u00ab'  # left-pointing double-angle quotation mark
        '\u00bb'  # right-pointing double-angle quotation mark
        '\u2018'  # left single quotation mark
        '\u2019'  # right single quotation mark
        '\u201a'  # single low-9 quotation mark
        '\u201b'  # single high-reversed-9 quotation mark
        '\u201c'  # left double quotation mark
        '\u201d'  # right double quotation mark
        '\u201e'  # double low-9 quotation mark
        '\u201f'  # double high-reversed-9 quotation mark
        '\u2039'  # single left-pointing angle quotation mark
        '\u203a'  # single right-pointing angle quotation mark
        '\u300c'  # left corner bracket
        '\u300d'  # right corner bracket
        '\u300e'  # left white corner bracket
        '\u300f'  # right white corner bracket
        '\u301d'  # reversed double prime quotation mark
        '\u301e'  # double prime quotation mark
        '\u301f'  # low double prime quotation mark
        '\ufe41'  # presentation form for vertical left corner bracket
        '\ufe42'  # presentation form for vertical right corner bracket
        '\ufe43'  # presentation form for vertical left corner white bracket
        '\ufe44'  # presentation form for vertical right corner white bracket
        '\uff02'  # fullwidth quotation mark
        '\uff07'  # fullwidth apostrophe
        '\uff62'  # halfwidth left corner bracket
        '\uff63'  # halfwidth right corner bracket
    )

    # mapping of {open: close} quotes extracted from
    #   https://en.wikipedia.org/wiki/Quotation_mark
    # and augmented with other observed patterns
    # note: adding grave accent (`) and comma (,) as they've been observed
    #       serving as quotes
    QUOTEPAIRS = {
        '\u0022': ['\u0022'],  # quotation mark (")
        '\u0027': ['\u0027'],  # apostrophe (')
        '\u002c': ['\u0027', '\u0060'],  # comma/(apostrophe|grave-accent)
        '\u0060': ['\u0027'],  # grave-accent/apostrophe
        '\u00ab': ['\u00bb'],  # left/right-pointing double-angle quotation mark
        '\u00bb': ['\u00ab', '\u00bb'],
    # right/(left|right)-pointing double-angle quotation mark
        '\u2018': ['\u2019'],  # left/right single quotation mark
        '\u2019': ['\u2019'],  # right single quotation mark
        '\u201a': ['\u201b', '\u2018', '\u2019'],
    # single low-9/(high-reversed-9|left-single|right-single) quotation mark
        '\u201b': ['\u2019'],
    # single high-reversed-9/right-single quotation mark
        '\u201c': ['\u201d'],  # left/right double quotation mark
        '\u201d': ['\u201d'],  # right double quotation mark
        '\u201e': ['\u201c', '\u201d'],
    # double-low-9/(left-double|right-double) quotation mark
        '\u201f': ['\u201d'],
    # double-high-reversed-9/right-double quotation mark
        '\u2039': ['\u203a'],  # single left/right-pointing angle quotation mark
        '\u203a': ['\u2039', '\u203a'],
    # single right/(left|right)-pointing angle quotation mark
        '\u300c': ['\u300d'],  # left/right corner bracket
        '\u300e': ['\u300f'],  # left/right white corner bracket
        '\u301d': ['\u301e'],  # reversed/* double prime quotation mark
        '\u301f': ['\u301e'],  # low/* double prime quotation mark
        '\ufe41': ['\ufe42'],
    # presentation form for vertical left/right corner bracket
        '\ufe43': ['\ufe44'],
    # presentation form for vertical left/right corner white bracket
        '\uff02': ['\uff02'],  # fullwidth quotation mark
        '\uff07': ['\uff07'],  # fullwidth apostrophe
        '\uff62': ['\uff63']  # halfwidth left/right corner bracket
    }

    SYMBOLS_OPENQUOTES = ''.join(QUOTEPAIRS.keys())
    SYMBOLS_CLOSEQUOTES = ''.join(q for qs in QUOTEPAIRS.values() for q in qs)'''

    SYMBOLS_LEFTQUOTES = (
        # common
        '\u0022', # quotation mark
        '\uff02', # fullwidth quotation mark
        '\u0027', # apostrophe
        '\uff07', # fullwidth apostrophe
        '\U000E0022',  # tag quotation mark
        '\u301d', # reversed double prime quotation mark
        '\u301e', # double prime quotation mark
        '\u301f', # low double prime quotation mark
        
        # specifically left
        '\u00ab', # left-pointing double angle quotation mark
        '\u2018', # left single quotation mark
        '\u201b', # single high-reversed-9 quotation mark
        '\u201c', # left double quotation mark
        '\u201f', # double high-reversed-9 quotation mark
        '\u275b', # heavy single turned comma quotation mark ornament
        '\u275d', # heavy double turned comma quotation mark ornament

        # specifically left: Asian/angled style
        '\u00ab',  # left-pointing double-angle quotation mark
        '\u2039',  # single left-pointing angle quotation mark
        '\u300c',  # left corner bracket
        '\u300e',  # left white corner bracket
        '\uff62'   # halfwidth left corner bracket
    )

    SYMBOLS_RIGHTQUOTES = (
        # common
        '\u0022', # quotation mark
        '\uff02'  # fullwidth quotation mark
        '\u0027', # apostrophe
        '\uff07'  # fullwidth apostrophe
        '\U000E0022',  # tag quotation mark
        '\u301d', # reversed double prime quotation mark
        '\u301e', # double prime quotation mark
        '\u301f', # low double prime quotation mark
        
        # specifically right
        '\u00bb', # right-pointing double angle quotation mark
        '\u2019', # right single quotation mark
        '\u201a', # single low-9 quotation mark
        '\u201d', # right double quotation mark
        '\u201e', # double low-9 quotation mark
        '\u275c', # heavy single comma quotation mark ornament
        '\u275e', # heavy double comma quotation mark ornament

        # specifically right: Asian/angled style
        '\u00bb',  # right-pointing double-angle quotation mark
        '\u203a',  # single right-pointing angle quotation mark
        '\u300d',  # right corner bracket
        '\u300f',  # right white corner bracket
        '\uff63'   # halfwidth right corner bracket
    )

    SYMBOLS_GRAVE = (
        '\u0060', # grave accent (`)
        '\u02cb', # modifier letter grave accent
        '\u02ce', # modifier letter low grave accent
        '\u02f4', # modifier letter middle grave accent
        '\u02f5', # modifier letter middle double grave accent
        '\u0300', # combining grave accent
        '\u030f', # combining double grave accent
        '\u0316', # combining grave accent below
        '\u0340', # combining grave tone mark
        '\u1420', # canadian syllabics final grave
        '\uff40', # fullwidth grave accent
        '\U000e0060' # tag grave accent
    )

    SYMBOLS_LEFTPARENTHESES = (
        '\u0028', # left parenthesis
        '\u207d', # superscript left parenthesis
        '\u208d', # subscript left parenthesis
        '\u2768', # medium left parenthesis ornament
        '\u276a', # medium flattened left parenthesis ornament
        '\u2985', # left white parenthesis
        '\ufd3e', # ornate left parenthesis
        '\ufe59', # small left parenthesis
        '\uff08', # fullwidth left parenthesis
        '\uff5f', # fullwidth left white parenthesis
        '\u2772', # light left tortoise shell bracket ornament
        '\u2997', # left black tortoise shell bracket
        '\u3014', # left tortoise shell bracket
        '\u3018', # left white tortoise shell bracket
    )

    SYMBOLS_RIGHTPARENTHESES = (
        '\u0029', # right parenthesis
        '\u207e', # superscript right parenthesis
        '\u208e', # subscript right parenthesis
        '\u2769', # medium right parenthesis ornament
        '\u276b', # medium flattened right parenthesis ornament
        '\u2986', # right white parenthesis
        '\ufd3f', # ornate right parenthesis
        '\ufe5a', # small right parenthesis
        '\uff09', # fullwidth right parenthesis
        '\uff60', # fullwidth right white parenthesis
        '\u2773', # light right tortoise shell bracket ornament
        '\u2998', # right black tortoise shell bracket
        '\u3015', # right tortoise shell bracket
        '\u3019', # right white tortoise shell bracket
    )

    SYMBOLS_LEFTSQUAREBRACKET = (
        '\u005b', # left square bracket
        '\u2045', # left square bracket with quill
        #'\u23a1', # left square bracket upper corner
        #'\u23a3', # left square bracket lower corner
        '\u27e6', # mathematical left white square bracket
        '\u298b', # left square bracket with underbar
        '\u298d', # left square bracket with tick in top corner
        '\u298f', # left square bracket with tick in bottom corner
        '\u3010', # left black lenticular bracket
        '\u3016', # left white lenticular bracket
        '\u301a', # left white square bracket
    )

    SYMBOLS_RIGHTSQUAREBRACKET = (
        '\u005d', # right square bracket
        '\u2046', # right square bracket with quill
        #'\u23a4', # right square bracket upper corner
        #'\u23a6', # right square bracket lower corner
        '\u27e7', # mathematical right white square bracket
        '\u298c', # right square bracket with underbar
        '\u298e', # right square bracket with tick in top corner
        '\u2990', # right square bracket with tick in bottom corner
        '\u3011', # right black lenticular bracket
        '\u3017', # right white lenticular bracket
        '\u301b', # right white square bracket
    )

    SYMBOLS_LEFTCURLYBRACKET = (
        '\u007b', # left curly bracket
        #'\u23a7', # left curly bracket upper hook
        #'\u23a9', # left curly bracket lower hook
        '\u2774', # medium left curly bracket ornament
        '\u2983', # left white curly bracket
    )

    SYMBOLS_RIGHTCURLYBRACKET = (
        '\u007d', # right curly bracket
        #'\u23ab', # right curly bracket upper hook
        #'\u23ad', # right curly bracket lower hook
        '\u2775', # medium right curly bracket ornament
        '\u2984', # right white curly bracket
    )

    SYMBOLS_LEFTANGLEBRACKET = (
        '\u003c', # less-than sign
        '\u2039', # single left-pointing angle quotation mark
        '\u2329', # left-pointing angle bracket
        '\u276c', # medium left-pointing angle bracket ornament
        '\u276e', # heavy left-pointing angle quotation mark ornament
        '\u2770', # heavy left-pointing angle bracket ornament
        '\u27e8', # mathematical left angle bracket
        '\u27ea', # mathematical left double angle bracket
        '\u2991', # left angle bracket with dot
        '\u29fc', # left-pointing curved angle bracket
        '\u3008', # left angle bracket
        '\u300a', # left double angle bracket
    )

    SYMBOLS_RIGHTANGLEBRACKET = (
        '\u003e', # greater-than sign
        '\u203a', # single right-pointing angle quotation mark
        '\u232a', # right-pointing angle bracket
        '\u276d', # medium right-pointing angle bracket ornament
        '\u276f', # heavy right-pointing angle quotation mark ornament
        '\u2771', # heavy right-pointing angle bracket ornament
        '\u27e9', # mathematical right angle bracket
        '\u27eb', # mathematical right double angle bracket
        '\u2992', # right angle bracket with dot
        '\u29fd', # right-pointing curved angle bracket
        '\u3009', # right angle bracket
        '\u300b', # right double angle bracket
    )

    SYMBOLS_WHITESPACE = (
        '\u0009', # horizontal tabulation
        '\u0020', # space
        '\u00a0', # no-break space
        '\u2002', # en space
        '\u2003', # em space
        '\u2004', # three-per-em space
        '\u2005', # four-per-em space
        '\u2006', # six-per-em space
        '\u2007', # figure space
        '\u2008', # punctuation space
        '\u2009', # thin space
        '\u200a', # hair space
        '\u200b', # zero width space
        '\u202f', # narrow no-break space
        '\u205f', # medium mathematical space
        '\u3000', # ideographic space
        '\ufeff', # zero width no-break space
        '\U000e0020', # tag space
    )