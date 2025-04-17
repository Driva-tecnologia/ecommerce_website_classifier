# %%
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import FloatType, BooleanType, StructField, StructType, DoubleType, ArrayType
import pickle
import math
import time
import re
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# %%
conf = SparkConf().setAppName("Spark com S3").setMaster("local[*]")

conf.set("spark.driver.memory", "70g")
conf.set("spark.executor.memory", "70g")
conf.set("spark.executor.pyspark.memory", "70g")

# conf.set("spark.driver.cores", "20")
# conf.set("spark.executor.cores", "20")

# conf.set("spark.memory.offHeap.enabled", "true")
# conf.set("spark.memory.offHeap.size", "20g")

# conf.set("spark.sql.shuffle.partitions", "2000")
# conf.set("spark.sql.parquet.columnarReaderBatchSize", "2048") 
conf.set("spark.sql.parquet.enableVectorizedReader", "false")
conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
conf.set("spark.sql.repl.eagerEval.enabled", "true")
conf.set("spark.sql.repl.eagerEval.truncate", 100)

conf.set("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY)
conf.set("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY)
conf.set("spark.hadoop.fs.s3a.endpoint", AWS_ENDPOINT_URL)
conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.2")
conf.set("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")

spark = SparkSession.builder.config(conf=conf).getOrCreate()

# %%
import logging
logger = spark._jvm.org.apache.log4j
logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
logging.getLogger("py4j").setLevel(logging.ERROR)

# %%
import boto3
# Inicialize o cliente boto3 para listar os objetos na pasta S3
s3 = boto3.client('s3', endpoint_url='https://s3.bhs.io.cloud.ovh.net')
bucket_name = 'drivalake'
prefix = 'sites/bronze/spiderwebv4/countries_'

# Função para listar todos os arquivos no bucket/prefix
def list_s3_files(bucket, prefix):
    files = []
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for content in response.get('Contents', []):
        files.append(content['Key'])
    while 'NextContinuationToken' in response:
        continuation_token = response['NextContinuationToken']
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        for content in response.get('Contents',  []):
            files.append(content['Key'])
    return files

# Listar todos os arquivos
files = list_s3_files(bucket_name, prefix)

# %% [markdown]
# # Model helper functions

# %%
def check_integrity(dataframe):
    try:
        columns_expected = [
            'domain',
            'html',
            ]
        
        if not all(item in dataframe.columns.tolist() for item in columns_expected):
            raise Exception('Missing required columns. Columns expected:\n' + str(columns_expected))
        
        dataframe['html'] = dataframe['html'].astype(str)

        dataframe_filtered = dataframe[(dataframe['html'] != '[]') & 
                                (dataframe['html'] != '') & 
                                (dataframe['domain'].str.endswith('.br'))]
        if len(dataframe) != len(dataframe_filtered):
            count = len(dataframe) - len(dataframe_filtered)
            print(f"WARNING: dataframe has {count} entries with empty HTML and/or does not ends with '.br'. Removing those entries.")
            dataframe = dataframe_filtered

        dataframe_filtered = dataframe.drop_duplicates()
        if len(dataframe) != len(dataframe_filtered):
            count = len(dataframe) - len(dataframe_filtered)
            print(f"WARNING: dataframe has {count} entries with duplicates values. Removing those entries.")
            dataframe = dataframe_filtered
    
    
        nulls = dataframe['domain'].isnull().sum()
        if nulls > 0:
            print(f"WARNING: column 'domain' has {nulls} empty values. Removing those entries.")
            dataframe = dataframe.dropna(subset=['domain'])

        nulls = dataframe['html'].isnull().sum()
        if nulls > 0:
            print(f"WARNING: column 'html' has {nulls} empty values. Removing those entries.")
            dataframe = dataframe.dropna(subset=['html'])
        
        return dataframe
    except Exception as e:
        raise Exception('Failed in integrity check.\nError:\n' + str(e))

# %%
def build_lemmatizer_pt_dict():
    try:
        import os
        import requests
        
        url = "https://github.com/michmech/lemmatization-lists/raw/master/lemmatization-pt.txt"
        file_name = "lemmatization-pt.txt"

        # Verificar se o arquivo já existe
        if not os.path.exists(file_name):
            response = requests.get(url)
            with open(file_name, 'wb') as f:
                f.write(response.content)

        # Processar o arquivo
        lemmatizer_pt_dict = {}
        with open(file_name, 'r') as dic:
            for line in dic:
                txt = line.split()
                if len(txt) == 2:
                    lemmatizer_pt_dict[txt[1]] = txt[0]

        return lemmatizer_pt_dict
    except Exception as e:
        file_name = "lemmatization-pt.txt"
        if os.path.exists(file_name):
            os.remove(file_name)
        raise Exception('An error occurred on custom_lemmatizer.\nError:\n' + str(e))

    finally:
        file_name = "lemmatization-pt.txt"
        # if os.path.exists(file_name):
        #     os.remove(file_name)

# %%
def custom_lemmatizer(tokens, lemmatizer_pt_dict):
    try:
      from nltk.stem.wordnet import WordNetLemmatizer
  
      lemmatizer = WordNetLemmatizer()
      tokens_lemmatized = []
      for token in tokens:
        if token in lemmatizer_pt_dict.keys():
          tokens_lemmatized.append(lemmatizer_pt_dict.get(token))
        else:
          tokens_lemmatized.append(lemmatizer.lemmatize(token))

      return tokens_lemmatized
    except Exception as e:
        raise Exception('An error occurred on custom_lemmatizer.\nError:\n' + str(e))

# %%
def get_html_body(html_str):
    from bs4 import BeautifulSoup
    try:
        # Tentar usar diferentes parsers
        for parser in ['html.parser', 'html5lib', 'lxml']:
            try:
                soup = BeautifulSoup(html_str, parser)
                text = soup.body.get_text() if soup.body else ''
                return text
            except Exception as parser_e:
                continue
        
    except Exception as e:
        return ''

# %%
def process_html_for_vectorizer(html_text, lemmatizer_pt_dict):
    import nltk
    from nltk.corpus import stopwords
    import unicodedata
    from bs4 import BeautifulSoup
    import re
    
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)

    try:              
        STOP_WORDS = (set(stopwords.words('portuguese'))).union(set(stopwords.words('english')))

        # pegar somente o body do HTML
        text = get_html_body(html_text)

        preprocessed_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

        # Remover espaços em branco e quebras de linha desnecessárias
        preprocessed_text = re.sub(r'\s+', ' ', preprocessed_text).strip()

        # substitui tudo que não é letra ou espaço por um espaço
        preprocessed_text = re.sub(r"[^a-zA-Z\s]", " ", preprocessed_text)

        # Regex para identificar palavras
        pattern = re.compile(r'([A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+)')

        # Substituir as correspondências por elas mesmas precedidas por um espaço
        preprocessed_text = pattern.sub(r' \1', preprocessed_text)

        # lowercase
        preprocessed_text = preprocessed_text.lower()

        # remover possives espaços repetidos
        preprocessed_text = re.sub(r"\s+", " ", preprocessed_text).strip()

        # tokenizar
        tokens = nltk.word_tokenize(preprocessed_text)

        # remover stopwords
        tokens = [
            token for token in tokens if token not in STOP_WORDS and len(token) > 2
        ]

        # Aplicar lemmatizer
        tokens = custom_lemmatizer(tokens, lemmatizer_pt_dict)

        return tokens
    except Exception as e:
        raise Exception('An error occurred while processing HTMLs for vectorizer.\nError:\n' + str(e))

# %%
def process_html_for_how_many_prices(text):
    import re
    try:              
        regex_precos = re.compile(r'\$|R\$')
        precos = regex_precos.findall(text)
        return len(precos)
    except Exception as e:
        raise Exception('An error occurred while processing HTMLs for prices.\nError:\n' + str(e))

# %%
def only_number(text):
    text = re.sub(r'[^\d]', '', text)
    return text

def remove_invalid_company(company_id):
    company_id = re.sub(r'(\d)\1{12}', '', company_id)
    if len(company_id) == 14:
        return company_id
    return None 

def order_by_common(data):
    from collections import Counter
    data_output = Counter(data)
    return [k for k, v in data_output.most_common()]

def extract_and_process_cnpjs(text):
    pattern = re.compile(r'\d{2}\.\d{3}\.\d{3}[\/ ]\d{4}[- ]\d{2}')
    matches = pattern.findall(text)
    processed_matches = []
    for match in matches:
        cleaned = only_number(match)
        valid_company = remove_invalid_company(cleaned)
        if valid_company:
            processed_matches.append(valid_company)
    return processed_matches

# %%
def generate_features(dataframe):
    try:
        dataframe = check_integrity(dataframe)

        lem_dict = build_lemmatizer_pt_dict()        
        dataframe.loc[:, 'tokens'] = dataframe.loc[:, 'html'].apply(lambda x: process_html_for_vectorizer(x, lem_dict))

        dataframe.loc[:, 'processed_cnpjs'] = dataframe.loc[:, 'html'].apply(extract_and_process_cnpjs)
        dataframe.loc[:, 'has_cnpj'] = dataframe.loc[:, 'processed_cnpjs'].apply(bool)

        html_body = dataframe.loc[:,'html'].apply(get_html_body)
        dataframe.loc[:, 'count_prices'] = html_body.apply(process_html_for_how_many_prices)
        dataframe['has_prices'] = dataframe['count_prices'] > 1

        return dataframe
    except Exception as e:
        raise Exception('An error occured while trying to generate features.\nError:\n' + str(e))

# %%
def predict_proba_with_domain(domains: list, HTML_raw: list, estimator, vectorizer):

    df = pd.DataFrame({'domain': domains, 'html': HTML_raw})
    df = generate_features(df)
    df = df.reset_index(drop=True)

    token_strings = [' '.join(doc) for doc in df['tokens']]
    tfidf_matrix = vectorizer.transform(token_strings)

    features = ['has_cnpj', 'has_prices']
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    other_features = df[features]
    features_df = pd.concat([other_features, tfidf_df], axis=1)
    
    model_predictions_prob = estimator.predict_proba(features_df)

    y_probs_0 = []
    y_probs_1 = []
    y_preds = []

    for prob_tuple in model_predictions_prob:
        y_probs_0.append(prob_tuple[0])
        y_probs_1.append(prob_tuple[1])

        if prob_tuple[1] >= 0.5:
            y_preds.append(1)
        else:
                y_preds.append(0)

    return y_preds, y_probs_0, y_probs_1

# %% [markdown]
# # Load model and process!

# %%
batch_size = 5
batches = [files[i:i + batch_size] for i in range(0, len(files), batch_size)]

# Carregar e processar cada parte separadamente
for i, batch in enumerate(batches):
    if i < 9: continue # 74+
    
    print(f"Processing batch {i+1}/{len(batches)}")
    file_paths = [f"s3a://{bucket_name}/{file}" for file in batch]
    df_spider_br = spark.read.parquet(*file_paths)
    
    # Fazer o processamento necessário com df_batch
    print('preprocessing...')
    df_spider_br = df_spider_br.select('domain', 'html', 'status')
    df_spider_br = df_spider_br.withColumn('html', col('html').cast('string'))
    df_spider_br = df_spider_br.filter((col('status') == 200.0) & (col('html') != '[]') & (col('html') != '') & (col('domain').endswith('.br')))
    df_spider_br = df_spider_br.select('domain', 'html')
    df_spider_br = df_spider_br.dropDuplicates()

    ###########################################################3

    print('loading model...')
    # Open picked model
    serialized_model = open('../models/MODEL_v1_ecommerce_tfidf_vectorizer_multinomial_nb_custom_lemmatizer_3_True_42_1000_spiderwebv4_dataset_html.pkl', "rb")
    model = pickle.load(serialized_model)
    serialized_model.close()
    # Open picked vectorizer
    serialized_vectorizer = open('../models/VECTORIZER_v1_ecommerce_tfidf_vectorizer_multinomial_nb_custom_lemmatizer_3_True_42_1000_spiderwebv4_dataset_html.pkl', "rb")
    vectorizer = pickle.load(serialized_vectorizer)
    serialized_vectorizer.close()

    # Broadcast model to spark executors
    spark.sparkContext.broadcast(model)
    spark.sparkContext.broadcast(vectorizer)

    # prediction method
    def predictor(domain, html):
        y_preds, y_probs_0, y_probs_1 = predict_proba_with_domain([domain], [html], model, vectorizer)
        return (float(y_probs_1[0]), bool(y_preds[0]))

    result_schema = StructType([
        StructField("probability", DoubleType()),
        StructField("prediction", BooleanType())
    ])

    #register python method as spark UDF
    udf_predictor = udf(predictor, result_schema)

    ###########################################################
    print('predicting...')
    df_with_predictions = df_spider_br.withColumn('results', udf_predictor(df_spider_br.domain, df_spider_br.html))
    
    # Criar colunas separadas para probability e prediction
    df_with_predictions = df_with_predictions.withColumn("probability", col("results.probability")) \
                                             .withColumn("prediction", col("results.prediction")) \
                                             .drop('results')


    print('writing...')
    file_path = '../data/ecommerce/countries_filtered_with_predictions_v2'
    df_with_predictions.write.parquet(file_path, mode='append')

spark.stop()

# %%
i

# %%
spark.stop()

# %%
# df_spider_br.write.parquet('./data/spider_br/brazil_filtered.parquet', mode='error')
# df_test = spark.read.parquet('./data/spider_br/brazil_filtered.parquet')
# df_spider_br = spark.read.parquet('./data/spider_br/brazil_filtered.parquet')


