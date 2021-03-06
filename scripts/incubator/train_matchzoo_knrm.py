#!/usr/bin/env python
import os, sys
import pickle
import matchzoo as mz
from matchzoo.data_pack import pack, DataPack

from matchzoo.models.knrm import KNRM

BATCH_SIZE=64
WORKERS_QTY=1
USE_MULTI_PROC=True

print("loading embeddings ...")
gloveEmbedding = mz.datasets.embeddings.load_glove_embedding(dimension=300)
print("embedding loaded")

sys.path.append('.')

from scripts.data_convert.matchzoo_reader \
    import readWhiteSpacedMatchZooData, WhiteSpacePreprocessor

colName = sys.argv[1]
modelFile = sys.argv[2]
epochQty = int(sys.argv[3])

dataTranFile = os.path.join('collections', 'derived_data', colName,  'match_zoo_train', 'data_transform.bin')
dataFileTrain = os.path.join('collections', 'derived_data', colName, 'match_zoo_train', 'tran_neg10.tsv')
dataFileTest = os.path.join('collections', 'derived_data', colName,  'match_zoo_train', 'dev1_allCand.tsv')

print(f'Collection: {colName} # of epochs: {epochQty} model file: {modelFile} data transform file: {dataTranFile}')

if os.path.exists(modelFile):
  # Stupid hack for now, b/c save will fail if the model exists
  print('Model already exists, exiting!')
  sys.exit(1)

# Note dtype! don't let Pandas guess column data types!
dataTrainPacked = pack(readWhiteSpacedMatchZooData(dataFileTrain))
dataTestPacked = pack(readWhiteSpacedMatchZooData(dataFileTest))

#prep = mz.preprocessors.BasicPreprocessor()
prep = WhiteSpacePreprocessor()

import pdb, sys

#try:
if True:

  rankingTask = mz.tasks.Ranking(loss=mz.losses.RankHingeLoss())
  rankingTask.metrics = [
    mz.metrics.NormalizedDiscountedCumulativeGain(k=3),
    mz.metrics.NormalizedDiscountedCumulativeGain(k=5),
    mz.metrics.MeanAveragePrecision()
  ]
  print("rankingTask initialized with metrics", rankingTask.metrics)

  if os.path.exists(dataTranFile):
    print(f'Loading existing preprocessor from {dataTranFile}')
    with open(dataTranFile, 'rb') as f:
      prep = pickle.load(f) 
  else:
    print(f'Fitting a new preprocessor')

    # For some reason, we fit the preprocessor to packed data
    prep.fit(dataTrainPacked)

  print('Preprocessor context:')
  print(prep.context)

  with open(dataTranFile, 'wb') as of:
    pickle.dump(prep, of) 

  print('Data transformer is fitted and saved!')

  dataTrainProc = prep.transform(dataTrainPacked)
  dataTestProc = prep.transform(dataTestPacked)

  model=KNRM()
  model.params.update(prep.context)

  model.params['embedding_output_dim'] = gloveEmbedding.output_dim
  model.params['embedding_trainable'] = True
  model.params['task'] = rankingTask
  model.params['kernel_num'] = 21
  model.params['sigma'] = 0.1
  model.params['exact_sigma'] = 0.001
  model.params['optimizer'] = 'adadelta'

  model.guess_and_fill_missing_params(verbose=1)
  print("Params completed",model.params.completed())
  model.build()
  model.compile()
  model.backend.summary()

  print('Building the embedding matrix!')
  embeddingMatrix = gloveEmbedding.build_matrix(prep.context['vocab_unit'].state['term_index'])
  model.load_embedding_matrix(embeddingMatrix)

  print('Unpacking test data')
  
  xTest, yTest = dataTestProc.unpack()
  evaluate = mz.callbacks.EvaluateAllMetrics(model, x=xTest, y=yTest, batch_size=len(xTest))

  print('Generating training data!')

  # This needs to use the processed data!
  trainGenerator = mz.DataGenerator(
    dataTrainProc,
    mode='pair',
    num_dup=5,
    num_neg=1,
    batch_size=BATCH_SIZE
  )
  print('num batches:', len(trainGenerator))
  history = model.fit_generator(trainGenerator, epochs=epochQty, callbacks=[evaluate], workers=WORKERS_QTY, use_multiprocessing=USE_MULTI_PROC)

  model.save(modelFile)
  print(model.evaluate(xTest, yTest, batch_size=128))
  
#except:
   # tb is traceback
  #type, value, tb = sys.exc_info()
  #pdb.post_mortem(tb)

