'''
Output Little-Endian bytes and labels file from gensim model
Also outputs necessary json config file portion
For use with TensorBoard
'''

import os
import sys
import struct
import logging
import argparse
from gensim.models import Word2Vec, Doc2Vec
# necessary for seeing logs

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
    level=logging.INFO)

parser = argparse.ArgumentParser(description='Convert gensim Word2Vec model to \
    TensorBoard visualization format')

# Required positional argument
parser.add_argument('input_file', type=str,
                    help='Input word2vec model file')
#parser.add_argument('output_file', type=str,
#                    help='Base output filename of TensorBoard data files')

args = parser.parse_args()

w2vmodel = Word2Vec.load(args.input_file)

try:
    vocab = w2vmodel.vocab
except:
    vocab = w2vmodel.wv.vocab

num_rows = len(vocab)

dim = w2vmodel.vector_size

try:
    base_fn = args.input_file.split('/')[-1]
except:
    base_fn = args.input_file.split('\\')[-1]

assert len(base_fn) > 0

tensor_bytes_out_fn = '%s_%d_%dd_tensors.bytes' % (base_fn, num_rows, dim)
tensor_tsv_out_fn = '%s_%d_%dd_tensors.tsv' % (base_fn, num_rows, dim)
labels_out_fn = '%s_%d_%dd_labels.tsv' % (base_fn, num_rows, dim)

tensor_bytes_out = open(tensor_bytes_out_fn, 'wb')

try:
    labels_out = open(labels_out_fn, 'w', encoding='utf-8')
except:
    labels_out = open(labels_out_fn, 'w')

try:
    tensor_tsv_out = open(tensor_tsv_out_fn, 'w', encoding='utf-8')
except:
    tensor_tsv_out = open(tensor_tsv_out_fn, 'w')

labels_out.write('word\tcount\n')

for i, wd in enumerate(vocab):
    if i % 100 == 0:
        sys.stderr.write('\rDump vocabulary: %d/%d (%.2f%%)' % \
            (i+1, num_rows, 100.0 * (i+1) / num_rows))

    floatvals = w2vmodel[wd].tolist()
    assert dim == len(floatvals)
    assert '\t' not in wd

    if i > 0:
        tensor_tsv_out.write('\n')

    for f_i, f in enumerate(floatvals):
        tensor_bytes_out.write(struct.pack('<f', f))
        
        if f_i > 0:
            tensor_tsv_out.write('\t%.8f' % f)
        else:
            tensor_tsv_out.write('%.8f' % f)

    try:
        labels_out.write('%s\t%s\n' % (wd, vocab[wd].count))
    except:
        labels_out.write(('%s\t%s\n' % (wd, vocab[wd].count)).encode('utf-8'))

sys.stderr.write('\n')
sys.stderr.flush()

tensor_bytes_out.close()
tensor_tsv_out.close()
labels_out.close()

# projector file

print('''{
  "embeddings": [
    {
      "tensorName": "%s",
      "tensorShape": [%d, %d],
      "tensorPath": "%s",
      "metadataPath": "%s"
    }
  ],
  "modelCheckpointPath": "Demo datasets"
}''' % (base_fn, num_rows, dim, tensor_bytes_out_fn, labels_out_fn))
