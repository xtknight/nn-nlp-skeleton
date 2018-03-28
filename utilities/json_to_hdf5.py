'''
Separate json stream(s) into hdf5 array format for far more efficient processing

Example:

$ python3 json_to_hdf5.py /tmp/jsonfile1.json.gz /tmp/jsonfile2.json.gz
    /tmp/jsonfile3.json.gz

'''
import os
import json
import psutil
import sys
import h5py
import gzip
import bz2
import logging
import argparse

process = psutil.Process(os.getpid())

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
    level=logging.INFO)

logger = logging.getLogger('JsonToHDF5')

parser = argparse.ArgumentParser(description='Separate large json stream(s) \
    into hdf5 array format')

# Required positional argument
parser.add_argument('input_files', type=str, nargs='+',
                    help='Input json file(s) in order (bz2 or gz also \
                    possible)')
parser.add_argument('--encoding', type=str, default='UTF-8',
                    help='Input text file encoding (default: "UTF-8")')
parser.add_argument('--dataset-name', type=str, default='vlen_dataset',
                    help='HDF5 dataset output name (default: "vlen_dataset")')

#parser.add_argument('output_file', type=str,
#                    help='Output filename for hdf5 file')

args = parser.parse_args()

assert len(args.input_files) > 0

outputFn = args.input_files[0] + '.hdf5'

lastData = ''
lastPrintedProgress = 0
dataCount = 0

# nothing special: just return the data string as-is for now
processData = lambda doc: doc

logger.info('Creating HDF5 file %s' % (outputFn))
f = h5py.File(outputFn, 'w')
logger.info('Creating HDF5 dataset %s:%s' % (outputFn, args.dataset_name))
dset = f.create_dataset(args.dataset_name, (0,), \
    dtype=h5py.special_dtype(vlen=str), chunks=True, maxshape=(2**32,))

file_count = len(args.input_files)

logger.info('Beginning input file iteration...')

for file_idx, input_file in enumerate(args.input_files):
    #logger.info('Open input file: %s' % input_file)

    if input_file.lower().endswith('.bz2'):
        infile = bz2.open(input_file, 'rt', encoding=args.encoding)
    elif input_file.lower().endswith('.gz'):
        infile = gzip.open(input_file, 'rt', encoding=args.encoding)
    else:
        infile = open(input_file, 'r', encoding=args.encoding)

    try:
        infilename = input_file.split('/')[-1]
    except:
        infilename = input_file.split('\\')[-1]

    #logger.info('Decoding JSON...')
    jsondata = json.loads(infile.read())

    rss = process.memory_info().rss / 1048576.0
    sys.stderr.write( \
        '\rDump data: FILE=%s, IDX=%d, COUNT=%d/%d (%.2f%%), ' \
        'MEM=%.2fMB' % \
        (infilename, dataCount+1, file_idx+1, \
        file_count, 100.0 * (file_idx+1)/file_count, rss))

    for record_idx, record in enumerate(jsondata):
        #if dataCount % 100 == 0:
            if dset.size <= dataCount:
                dset.resize((dataCount+128, ))

            dset[dataCount] = json.dumps(record)
            dataCount += 1

        #if dataCount >= 100: # stop early for testing
        #    break

sys.stderr.write('\n')
sys.stderr.flush()

logger.info('File iteration complete.')

# eventually resize down to actual data count
dset.resize((dataCount, ))

f.close()

logger.info('Output %d objects to %s:%s' % (dataCount, outputFn, \
    args.dataset_name))
