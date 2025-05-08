## Análise Base Whois

Urls distintos (isso aqui seria o host da tabela e-commerce): 1856679

Hosts (isso aqui seria o domínio da tabela e-commerce):
Distintos: 1823423
* Quantos hosts se repetem: 33256
* Quantos hosts não se repetem: 1790167

Distribuição das probabilidades:

| interval 	| count 	| percent 	|
|:---:	|:---:	|:---:	|
| (0.0, 0.1) 	| 798828 	| 0.4302 	|
| (0.3, 0.4) 	| 462518 	| 0.2491 	|
| (0.1, 0.2) 	| 287849 	| 0.155 	|
| (0.2, 0.3) 	| 114910 	| 0.0619 	|
| (0.9, 1.0) 	| 87350 	| 0.047 	|
| (0.4, 0.5) 	| 47369 	| 0.0255 	|
| (0.5, 0.6) 	| 19550 	| 0.0105 	|
| (0.6, 0.7) 	| 13584 	| 0.0073 	|
| (0.8, 0.9) 	| 12938 	| 0.007 	|
| (0.7, 0.8) 	| 11783 	| 0.0063 	|

Maior que o novo threshold (0.6): 125655 (aprox. 6,767%)

Menor que o novo threshold (0.6): 1731024 (aprox. 93,23%)

## Análise Tabela de e-commerce (sites.ecommerce)

* Quantidade de domínios distintos na tabela (05/05/2025): 1425972

* Quantidade de hosts distintos na tabela (05/05/2025): 1457982

* Quantidade de valores nulos na coluna de probabilidade (05/05/2025): 277091

Distribuição das probabilidades (considerando somente os que não são nulos):

| interval 	| count 	| percent 	|
|:---:	|:---:	|:---:	|
| (0.0, 0.1) 	| 538635 	| 0.4561 	|
| (0.1, 0.2) 	| 174017 	| 0.1474 	|
| (0.9, 1.0) 	| 151458 	| 0.1283 	|
| (0.2, 0.3) 	| 86523 	| 0.0733 	|
| (0.4, 0.5) 	| 82080 	| 0.0695 	|
| (0.3, 0.4) 	| 51419 	| 0.0435 	|
| (0.5, 0.6) 	| 27148 	| 0.023 	|
| (0.8, 0.9) 	| 25038 	| 0.0212 	|
| (0.7, 0.8) 	| 22417 	| 0.019 	|
| (0.6, 0.7) 	| 22156 	| 0.0188 	|

## Comparação com a tabela de e-commerce

Domínios (hosts do whois e domínios do e-commerce):

* Disponíveis tanto na tabela de e-commerce quanto nos dados do Whois: 555895

* Disponíveis apenas no Whois: 1267528

* Disponíveis apenas na tabela de e-commerce: 870077

* Total (domínios distintos na tabela de e-commerce + hosts distintos nos dados do Whois): 2693500

### Distribuição das probabilidades apenas dos domínios que estão na base Whois

| interval 	| count 	| percent 	|
|:---:	|:---:	|:---:	|
| (0.0, 0.1) 	| 458426 	| 0.3617 	|
| (0.3, 0.4) 	| 403738 	| 0.3185 	|
| (0.1, 0.2) 	| 214075 	| 0.1689 	|
| (0.2, 0.3) 	| 90661 	| 0.0715 	|
| (0.4, 0.5) 	| 38366 	| 0.0303 	|
| (0.9, 1.0) 	| 26752 	| 0.0211 	|
| (0.5, 0.6) 	| 13344 	| 0.0105 	|
| (0.6, 0.7) 	| 8562 	| 0.0068 	|
| (0.7, 0.8) 	| 6853 	| 0.0054 	|
| (0.8, 0.9) 	| 6751 	| 0.0053 	|

### Comparação das probabilidades (considerando somente os 555895 domínios disponíveis em ambas bases) em porcentagem

fórmula => (probabilidade_novo_modelo - probabilidade_modelo_antigo) / probabilidade_modelo_antigo

| interval 	| count 	| percent 	|
|:---:	|:---:	|:---:	|
| (-100, -75] 	| 226305 	| 0.4071 	|
| (-75, -50] 	| 94010 	| 0.1691 	|
| (-25, 0] 	| 66001 	| 0.1187 	|
| (-50, -25] 	| 57571 	| 0.1036 	|
| (-inf, -100] 	| 42640 	| 0.0767 	|
| (0, 25] 	| 28417 	| 0.0511 	|
| (100, inf] 	| 25903 	| 0.0466 	|
| (25, 50] 	| 7150 	| 0.0129 	|
| (50, 75] 	| 4559 	| 0.0082 	|
| (75, 100] 	| 3339 	| 0.006 	|

### Comparação das predições (considerando somente os 555895 domínios disponíveis em ambas as bases)

Threshold (limiar de decisão) utilizado nas probabilidades do modelo antigo = 0.5

Threshold (limiar de decisão) utilizado nas probabilidades do modelo novo = 0.6

Análise:

* Eram classificados como True pelo modelo antigo e agora é classificado como False pelo novo modelo: 44465

* Eram classificados como False pelo modelo antigo e agora é classificado como True pelo novo modelo: 2530

* A predição não mudou (continua sendo a mesma classe): 466260