# E-commerce Website Classifier

Um classificador de [e-commerce | não e-commerce] para sites

O projeto de classificação de e-commerce foi desenvolvido e está em produção no ILUM. Na pasta modelos, encontra-se os modelos e vetorizadores já treinados.

Na pasta scripts, possui os arquivos do desenvolvimento do modelo. O mais importante é o feature_engineering.ipynb, onde tem a engenharia de features e treinamento do modelo. Para rodar, hoje utiliza-se ILUM dado o volume dos dados, mas anteriormente era rodado com ecomm_predict_countries e ecomm_predict_spiderweb.

Para classificar os sites, é necessário ter o html deles. Com isso, é necessário um pré-processamento de limpeza dos htmls para remover entradas nulas e diferente de status 200. Em seguida, os htmls passam por NLP onde é limpado, normalizado e tokenizado. As features finais são presença de preços e valores no html, presença de cnpj no site, e o TF-IDF do córpus dos sites.