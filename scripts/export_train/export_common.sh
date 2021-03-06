#@IgnoreInspection BashAddShebang


checkVarNonEmpty "DEV1_SUBDIR"
checkVarNonEmpty "BITEXT_SUBDIR"

# This default is set by a calling script
checkVarNonEmpty "outSubdir"

threadQty=1
hardNegQty=10
sampleMedNegQty=20
sampleEasyNegQty=10
candTrainQty=500
candTestQty=10
randSeed=0
maxDocWhitespaceQty=-1 # means no truncation

boolOpts=("h" "help" "print help")

paramOpts=(
"thread_qty"             "threadQty"           "# of threads"
"out_subdir"             "outSubdir"           "output sub-directory (default $outSubdir)"
"hard_neg_qty"           "hardNegQty"          "A max. # of *HARD* negative examples (all K top-score candidates) per query (default $hardNegQty)"
"sample_med_neg_qty"     "sampleMedNegQty"     "A max. # of *MEDIUM* negative samples (negative candidate and QREL samples) per query (default $sampleMedNegQty)"
"sample_easy_neg_qty"    "sampleEasyNegQty"    "A max. # of *EASY* negative samples (sampling arbitrary docs) per query (default $sampleEasyNegQty)"
"cand_train_qty"         "candTrainQty"        "A max. # of candidate records to generate training data (default $candTrainQty)"
"cand_test_qty"          "candTestQty"         "A max. # of candidate records to generate test data (default $candTestQty)"
"max_num_query_train"    "maxNumQueryTrain"    "Optional max. # of train queries"
"max_num_query_test"     "maxNumQueryTest"     "Optional max. # of test/dev queries"
"max_doc_whitespace_qty" "maxDocWhitespaceQty" "Optional max. # of whitespace separated tokens to keep in a document"
"seed"                   "randSeed"            "A random seed (default $randSeed)"
)

usageMain="<collection> <name of the index field> \
<train subdir, e.g., $DEFAULT_TRAIN_SUBDIR> \
<test subdir, e.g., $DEV1_SUBDIR>"

parseArguments $@

if [ "$maxNumQueryTrain" != "" ] ; then
  maxNumQueryTrainParam=" -max_num_query_train $maxNumQueryTrain "
fi

if [ "$maxNumQueryTest" != "" ] ; then
  maxNumQueryTestParam=" -max_num_query_test $maxNumQueryTest "
fi

if [ "$help" = "1" ] ; then
  genUsage "$usageMain"
  exit 1
fi

collect=${posArgs[0]}
if [ "$collect" = "" ] ; then
  genUsage "$usageMain" "Specify $SAMPLE_COLLECT_ARG (1st arg)"
  exit 1
fi

indexFieldName=${posArgs[1]}
if [ "$indexFieldName" = "" ] ; then
  genUsage "$usageMain" "Specify the name of the index field (2d arg)"
  exit 1
fi

partTrain=${posArgs[2]}
if [ "$partTrain" = "" ] ; then
  genUsage "$usageMain" "Specify the training sub-dir, e.g., $DEFAULT_TRAIN_SUBDIR (3d arg)"
  exit 1
fi

partTest=${posArgs[3]}
if [ "$partTest" = "" ] ; then
  genUsage "$usageMain" "Specify the training sub-dir, e.g., $DEV1_SUBDIR (4th arg)"
  exit 1
fi


checkVarNonEmpty "COLLECT_ROOT"
checkVarNonEmpty "FWD_INDEX_SUBDIR"
checkVarNonEmpty "INPUT_DATA_SUBDIR"
checkVarNonEmpty "DERIVED_DATA_SUBDIR"
checkVarNonEmpty "QUERY_FIELD_NAME"
checkVarNonEmpty "QREL_FILE"

inputDataDir="$COLLECT_ROOT/$collect/$INPUT_DATA_SUBDIR"
fwdIndexDir="$COLLECT_ROOT/$collect/$FWD_INDEX_SUBDIR/"
luceneIndexDir="$COLLECT_ROOT/$collect/$LUCENE_INDEX_SUBDIR/"

outDir="$COLLECT_ROOT/$collect/$DERIVED_DATA_SUBDIR/$outSubdir/$indexFieldName"

if [ ! -d "$outDir" ] ; then
  mkdir -p "$outDir"
fi

echo "========================================================"
echo "Train split: $partTrain"
echo "Eval split: $partTest"
echo "Random seed: $randSeed"
echo "Output directory: $outDir"
echo "# of threads: $threadQty"
echo "A # of hard/medium/easy samples per query: $hardNegQty/$sampleMedNegQty/$sampleEasyNegQty"
echo "A max. # of candidate records to generate training data: $candTrainQty"
echo "A max. # of candidate records to generate test data: $candTestQty"
echo "Max train query # param.: $maxNumQueryTrainParam"
echo "Max test/dev query # param.: $maxNumQueryTestParam"
echo "========================================================"
