'''
Separate text stream into hdf5 array format for far more efficient processing

Memory-efficient

Example:

$ python3 text_to_hdf5.py /tmp/wikicomp-2014_arko.xml.bz2 "<articlePair id"
    --split-token-end "</articlePair>"

'''
import os
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

logger = logging.getLogger('TextToHDF5')

parser = argparse.ArgumentParser(description='Separate large text stream \
    delimited by arbitrary tokens into hdf5 array format')

# Required positional argument
parser.add_argument('input_file', type=str,
                    help='Input text file (bz2 or gz also possible)')
parser.add_argument('--encoding', type=str, default='UTF-8',
                    help='Input text file encoding (default: "UTF-8")')
parser.add_argument('--dataset-name', type=str, default='vlen_dataset',
                    help='HDF5 dataset output name (default: "vlen_dataset")')
# for example: "<articlePair id"
parser.add_argument('split_token_start', type=str,
                    help='Start split token (can be XML tag). Example: " \
                    <articlePair id"')

# for example: "</articlePair>"
parser.add_argument('--split-token-end', type=str, default=None,
                    help='Start split token (can be ending XML tag \
                     or nothing if only splitting by start token). Example: \
                     "</articlePair>"')
parser.add_argument('--disable-progress', action='store_true', default=False,
                    help='Disable progress bar (helps when reading large \
                    compressed file where file needs to be decompressed \
                    to determine progress bar denominator)')

#parser.add_argument('output_file', type=str,
#                    help='Output filename for hdf5 file')

args = parser.parse_args()

outputFn = args.input_file + '.hdf5'

assert args.split_token_end != None, 'blank end token not implemented'

lastData = ''
lastPrintedProgress = 0
dataCount = 0

# nothing special: just return the data string as-is for now
processData = lambda doc: doc

if args.input_file.lower().endswith('.bz2'):
    infile = bz2.open(args.input_file, 'rt', encoding=args.encoding)
elif args.input_file.lower().endswith('.gz'):
    infile = gzip.open(args.input_file, 'rt', encoding=args.encoding)
else:
    infile = open(args.input_file, 'r', encoding=args.encoding)

logger.info('Creating HDF5 file %s' % (outputFn))
f = h5py.File(outputFn, 'w')
logger.info('Creating HDF5 dataset %s:%s' % (outputFn, args.dataset_name))
dset = f.create_dataset(args.dataset_name, (0,), \
    dtype=h5py.special_dtype(vlen=str), chunks=True, maxshape=(2**32,))

if not args.disable_progress:
    logger.info('Computing input file length. If this takes too long or causes \
issues (in the case of a compressed input file), use \
--disable-progress')

    infile.seek(0, os.SEEK_END)
    file_len = infile.tell()
    infile.seek(0, os.SEEK_SET)

logger.info('Beginning input file iteration...')

#for ln in infile: (breaks .tell())

ln = infile.readline()
while ln:
    if dataCount % 100 == 0:
        rss = process.memory_info().rss / 1048576.0
        if not args.disable_progress:
            sys.stderr.write( \
                '\rDump data: IDX=%d, POS=%d/%d (%.2f%%), MEM=%.2fMB' % \
                (dataCount+1, infile.tell(), \
                file_len, 100.0 * infile.tell()/file_len, rss))
        else:
            sys.stderr.write('\rDump data: IDX=%d, MEM=%.2fMB' % \
                (dataCount+1, rss))

    if lastData=='':
        if args.split_token_start in ln:
            lastData = args.split_token_start + \
                ln.split(args.split_token_start)[1].split( \
                    args.split_token_end)[0]
            if args.split_token_end in ln:
                lastData += args.split_token_end
                results = processData(lastData)
                if results:
                    if dset.size <= dataCount:
                        dset.resize((dataCount+128, ))

                    dset[dataCount] = results
                    dataCount += 1
                lastData = ''
        else:
            if lastData!='':
                lastData += ln
    else:
        if args.split_token_end in ln:
            lastData += ln.split(args.split_token_end)[0].strip() + \
                args.split_token_end
            results = processData(lastData)
            if results:
                if dset.size <= dataCount:
                    dset.resize((dataCount+128, ))

                dset[dataCount] = results
                dataCount += 1
            lastData = ''
        else:
            lastData += ln

    #if dataCount >= 100: # stop early for testing
    #    break

    ln = infile.readline()

sys.stderr.write('\n')
sys.stderr.flush()

logger.info('File iteration complete.')

# eventually resize down to actual data count
dset.resize((dataCount, ))

f.close()

logger.info('Output %d objects to %s:%s' % (dataCount, outputFn, \
    args.dataset_name))
