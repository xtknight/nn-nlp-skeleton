# -*- coding: utf-8 -*-
import sys
import argparse
import logging
import json
import konlpy
#import copy

from konlpy.tag import Komoran
from os import listdir
from os.path import isfile, join
from multiprocessing import Pool
from normalizer import Normalizer
from tokenizer import Tokenizer

"""
Preprocess several files in parallel, and then write them to a single HDF5 file
"""


'''
print(Tokenizer.tokenize('hello (this is a test) string and I\'ve run this '
                         'program thirty-three times...',
                         keep_punctuation=False,
                         keep_symbols=True))
print(Tokenizer.tokenize('다 522 정통 ‘모피아’(재무부+마피아 합성어)다.',
                         keep_punctuation=False,
                         keep_symbols=False))
#
sys.exit(1)
'''

# remove non-semantic tags
#omit_tags = set(['SS', 'SW', 'ETM', 'JKO', 'JKB', 'JKS', 'JX', 'EP', 'EF',
# 'SF', 'EC', 'XSA', 'VCP'])

omit_tags = set(['SF','SE','SS','SP','SO','SW','EF','EP','EC','ETM','JKS','JKC',
            'JKG','JKO','JKB', 'JKV','JKQ','JC','JX','VCP','XSA'])

def get_tagged_output(komoran: Komoran, input_sentence: str) -> str:
    # normalize punctuation, etc...
    #print('In:', ln)
    ln = Normalizer.normalize(input_sentence)
    tk = Tokenizer.tokenize(ln,
                            keep_punctuation=False,
                            keep_symbols=False)
    pos_tags = komoran.pos(' '.join(tk))
    filtered_pos_tags = list(filter(lambda t: t[1] not in omit_tags,
                                    pos_tags))
    #print('Out:', filtered_pos_tags)
    return filtered_pos_tags

'''
Pre-process the entries in the specified json file and output
to same filename + .stage0
'''
def json_process(json_fn: str):
    logging.info('Processing %s...' % json_fn)

    file_title = json_fn.rsplit('/', 1)[-1]
    komoran = Komoran()
    json_data = None
    with open(json_fn, 'r', encoding='utf-8') as fd:
        json_data = json.load(fd)

    cnt = len(json_data)
    out_data = []
    for i, json_entry in enumerate(json_data):
        if i % 100 == 0:
            logging.info('Progress[%s]: %d/%d (%.2f%%)' % (file_title, i, cnt,
                                                           100.0 *
                                                           float(i) \
                                                           / float(cnt)))

        out_entry = {}
        #out_entry = copy.deepcopy(json_entry)

        summary_sentences = []
        for ln in json_entry['subtitles']:
            ln = ln.strip()
            if ln:
                t_o = get_tagged_output(komoran, ln)
                summary_sentences.append((ln, t_o))

        body_sentences = []
        for ln in json_entry['body'].split('\n'):
            ln = ln.strip()
            if ln:
                t_o = get_tagged_output(komoran, ln)
                body_sentences.append((ln, t_o))

        out_entry['body'] = body_sentences
        out_entry['summary'] = summary_sentences

        out_data.append(out_entry)

    with open(json_fn + '.stage0', 'w', encoding='utf-8') as fd:
        json.dump(out_data, fd)

if __name__ == '__main__':
    # necessary for seeing logs
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Preprocess json input for '
                                                 'summarization task')
    # Required positional argument
    parser.add_argument('input_dir', type=str,
                        help='Input json bucket files directory (UTF-8)')
    parser.add_argument('output_file', type=str,
                        help='Base output filename of word2vec/doc2vec model (gensim)')
    '''
    parser.add_argument('--doc2vec', action='store_true', default=False,
                        help='Generate a doc2vec model instead of a word2vec model')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Training epochs (default 10). Shuffle sentences and re-train during each training epoch.')
    parser.add_argument('--limit-documents', type=int, default=0,
                        help='Limit model generation to first N documents of corpus')
    parser.add_argument('--min-sentence-length', type=int, default=5,
                        help='If sentence is shorter than N Eojeols (full words), it will not be processed for inclusion in the word2vec model (default 5)')
    parser.add_argument('--dimension', type=int, default=100,
                        help='word2vec: dimensionality of feature vectors (default 100). doc2vec mode may demand a higher value.')
    parser.add_argument('--window', type=int, default=5,
                        help='word2vec: maximum distance between current and predicted word (default 5). doc2vec mode may demand a higher value.')
    parser.add_argument('--workers', type=int, default=4,
                        help='word2vec: use this many worker threads to train the model (default 4)')
    parser.add_argument('--min-word-occurrence', type=int, default=5,
                        help='word2vec: ignore all words with total frequency lower than this (default 5)')
    parser.add_argument('--ignore-eojeol-boundaries', action='store_true', default=False,
                        help='Ignore eojeol boundaries: make all constituent parts words themselves')
    parser.add_argument('--only-train-titles', action='store_true', default=False,
                        help='Only train doc2vec on titles rather than Wiki categories')
    parser.add_argument('--only-train-articles-with-categories', action='store_true', default=False,
                        help='Only train on articles that have categories (applicable for category training)')
    parser.add_argument('--exclude-tags', type=str, default='',
                        help='Exclude certain POS tags from the model (comma-delimited list). Works even if hybrid-sense2vec is off.')
    parser.add_argument('--train-entire-documents', action='store_true', default=False,
                        help='Train entire documents with one tag rather than iterating through all individual sentences and labeling with the same tag. Based on testing, doesn\'t seem to matter. Only compatible with doc2vec mode.')
    parser.add_argument('--hybrid-sense2vec', action='store_true', default=False,
                        help='Include POS tags in the word vectors for each sentence')
    parser.add_argument('--use-skipgram', action='store_true', default=False,
                        help='Use skip-gram instead of the default CBOW. Incompatible with doc2vec.')
    parser.add_argument('--use-pvdbow', action='store_true', default=False,
                        help='Use PV-DBOW instead of the default PV-DM. Incompatible with word2vec.')
    parser.add_argument('--min-word-length', type=int, default=0,
                        help='word2vec: ignore all words with a length lower than this (default 0).')
    parser.add_argument('--input-words-sense-tagged', action='store_true', default=False,
                        help='Assume that input words are tagged with senses __nn. Helps min-word-length calculation.')
    '''

    args = parser.parse_args()
    input_files = sorted([join(args.input_dir, f) for f in listdir(args.input_dir)
                   if isfile(join(args.input_dir, f)) and f.endswith('.json')])

    with Pool(5) as p:
        p.map(json_process, input_files)

        #for f in input_files:
        #    logging.info('Processing %s...' % f)
        #    json_process(f)
        #    break