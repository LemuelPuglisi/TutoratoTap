""" Usage: python remote_wordcount.py <url> """

import sys

from pyspark import RDD, SparkFiles
from pyspark.sql import SparkSession

NN_DATA_MINING_NOTES = \
    'https://github.com/LemuelPuglisi/DiveIntoDataMining/blob/main/10_Reti_neurali.md'


CLASSIFICATION_DATA_MINING_NOTES = \
    'https://github.com/LemuelPuglisi/DiveIntoDataMining/blob/main/3_Classificazione.md'


def wordcount(spark: SparkSession, url: str, minlen=5) -> RDD:
    """ Given an remote file, returns the word count as an RDD. 
    """
    # lambda functions used for computing wordcount. 
    extract_words = lambda line: line.split(' ') 
    only_alpha_minlen = lambda word: word.isalpha() and len(word) >= minlen
    to_key_val = lambda word: (word, 1)
    sum_by_key = lambda ca, cb: ca + cb
    # retrieve the remote file using the URL
    spark.sparkContext.addFile(url)
    filename = url.split('/')[-1] 
    fileURI  = 'file://' + SparkFiles.get(filename) 
    text = spark.sparkContext.textFile(fileURI)
    words = text.flatMap(extract_words).filter(only_alpha_minlen)
    wcount = words.map(to_key_val).reduceByKey(sum_by_key)
    return wcount


if __name__ == '__main__':

    url = CLASSIFICATION_DATA_MINING_NOTES
    if len(sys.argv) > 1: url = sys.argv[1]

    # WARNING: set files.overwrite to true in order to re-run
    # the script without problems (the file is kept inside our cluster).  
    spark = SparkSession.builder \
        .config("spark.files.overwrite", "true") \
        .getOrCreate()

    wc = wordcount(spark, url)
    top10 = wc.sortBy(lambda x: x[1], ascending=False).take(10)
    for wc in top10: print(wc)