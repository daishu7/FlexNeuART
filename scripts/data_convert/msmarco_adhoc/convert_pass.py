#!/usr/bin/env python
import sys
import json
import argparse
import multiprocessing

sys.path.append('scripts')
from data_convert.text_proc import *
from data_convert.convert_common import *

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc documents.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--max_doc_size', metavar='max doc size bytes', help='the threshold for the document size, if a document is larger it is truncated',
                    type=int, default=MAX_DOC_SIZE)
# Number of cores minus one for the spaning process
parser.add_argument('--proc_qty', metavar='# of processes', help='# of NLP processes to span',
                    type=int, default=multiprocessing.cpu_count()-1)


args = parser.parse_args()
print(args)

inpFile = FileWrapper(args.input)
outFile = FileWrapper(args.output, 'w')
maxDocSize = args.max_doc_size

stopWords = readStopWords(STOPWORD_FILE, lowerCase=True)
print(stopWords)

class PassParseWorker:
  def __init__(self, stopWords, spacyModel):
    self.nlp = SpacyTextParser(spacyModel, stopWords, keepOnlyAlphaNum=True, lowerCase=True)

  def __call__(self, line):

    if not line:
      return None

    line = line[:maxDocSize] # cut documents that are too long!
    fields = line.split('\t')
    if len(fields) != 2:
      return None

    pid, body = fields

    text, text_unlemm = self.nlp.procText(body)

    doc = {DOCID_FIELD : pid,
         TEXT_FIELD_NAME : text,
         TEXT_UNLEMM_FIELD_NAME : text_unlemm,
         TEXT_RAW_FIELD_NAME : body.lower()}
    return json.dumps(doc) + '\n'


proc_qty=args.proc_qty
print(f'Spanning {proc_qty} processes')
pool = multiprocessing.Pool(processes=proc_qty)
ln = 0
for docStr in pool.imap(PassParseWorker(stopWords, SPACY_MODEL), inpFile, IMAP_PROC_CHUNK_QTY):
  ln = ln + 1
  if docStr is not None:
    outFile.write(docStr)
  else:
    print('Ignoring misformatted line %d' % ln)

  if ln % REPORT_QTY == 0:
    print('Processed %d passages' % ln)

print('Processed %d passages' % ln)

inpFile.close()
outFile.close()
