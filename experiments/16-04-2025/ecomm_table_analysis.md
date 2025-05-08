## Análise Base Whois

Urls distintos (isso aqui seria o host da tabela e-commerce): 1856679

Hosts (isso aqui seria o domínio da tabela e-commerce):
Distintos: 1823423
* Quantos hosts se repetem: 33256
* Quantos hosts não se repetem: 1790167

Distribuição das probabilidades:

| intervalo 	| quantidade 	| porcentagem (%) 	|
|:---:	|:---:	|:---:	|
| [0.0, 0.1) 	| 798828 	| 43,02 	|
| [0.3, 0.4) 	| 462518 	| 24,91 	|
| [0.1, 0.2) 	| 287849 	| 15,5 	|
| [0.2, 0.3) 	| 114910 	| 6,19 	|
| [0.9, 1.0) 	| 87350 	| 4,7 	|
| [0.4, 0.5) 	| 47369 	| 2,55 	|
| [0.5, 0.6) 	| 19550 	| 1,05 	|
| [0.6, 0.7) 	| 13584 	| 0,73 	|
| [0.8, 0.9) 	| 12938 	| 0,7 	|
| [0.7, 0.8) 	| 11783 	| 0,63 	|

Maior que o novo threshold (0.6): 125655 (aprox. 6,768%)

Menor que o novo threshold (0.6): 1731024 (aprox. 93,232%)

## Análise Tabela de e-commerce (sites.ecommerce)

* Quantidade de domínios distintos na tabela (05/05/2025): 1425972

* Quantidade de hosts distintos na tabela (05/05/2025): 1457982

* Quantidade de valores nulos na coluna de probabilidade (05/05/2025): 277091

Distribuição das probabilidades (considerando somente os que não são nulos):

| intervalo 	| quantidade 	| porcentagem (%) 	|
|:---:	|:---:	|:---:	|
| [0.0, 0.1) 	| 538635 	| 45,61 	|
| [0.1, 0.2) 	| 174017 	| 14,74 	|
| [0.9, 1.0) 	| 151458 	| 12,83 	|
| [0.2, 0.3) 	| 86523 	| 7,33 	|
| [0.4, 0.5) 	| 82080 	| 6,95 	|
| [0.3, 0.4) 	| 51419 	| 4,35 	|
| [0.5, 0.6) 	| 27148 	| 2,3 	|
| [0.8, 0.9) 	| 25038 	| 2,12 	|
| [0.7, 0.8) 	| 22417 	| 1,9 	|
| [0.6, 0.7) 	| 22156 	| 1,88 	|

## Comparação com a tabela de e-commerce

Domínios (considerando a coluna host do Whois e as colunas host e domínio da tabela de e-commerce):

* Disponíveis tanto na tabela de e-commerce quanto nos dados do Whois: 555895

* Disponíveis apenas no Whois: 1267528

* Disponíveis apenas na tabela de e-commerce: 903136

* Total (domínios distintos na tabela de e-commerce + hosts distintos nos dados do Whois): 2726559

Obs: nesse caso, eu peguei somei a lista de valores únicos da coluna host e da coluna domínio da tabela de e-commerce e comparei com os valores da coluna host do Whois.

### Distribuição das probabilidades apenas dos domínios que estão na base Whois

| intervalo 	| quantidade 	| porcentagem (%) 	|
|:---:	|:---:	|:---:	|
| [0.0, 0.1) 	| 458630 	| 36,17 	|
| [0.3, 0.4) 	| 403809 	| 31,85 	|
| [0.1, 0.2) 	| 214117 	| 16,89 	|
| [0.2, 0.3) 	| 90693 	| 7,15 	|
| [0.4, 0.5) 	| 38372 	| 3,03 	|
| [0.9, 1.0) 	| 26769 	| 2,11 	|
| [0.5, 0.6) 	| 13352 	| 1,05 	|
| [0.6, 0.7) 	| 8565 	| 0,68 	|
| [0.7, 0.8) 	| 6855 	| 0,54 	|
| [0.8, 0.9) 	| 6753 	| 0,53 	|

Total: 1267915

Obs: nesse caso, eu fiz um join com a base do Whois e da tabela de e-commerce usando a coluna host de ambos, depois fiz outro join com a base do Whois e da tabela de e-commerce considerando a coluna host e domínio, respectivamente. Por fim, uni as duas tabelas e dei um drop_duplicates na coluna host. O total deu um pouco a mais do que antes, mas a porcentagem não foi afetada.

### Comparação das probabilidades (considerando somente os 555895 domínios disponíveis em ambas bases) em porcentagem

fórmula => (probabilidade_novo_modelo - probabilidade_modelo_antigo) / probabilidade_modelo_antigo

| intervalo 	| quantidade 	| porcentagem (%) 	|
|:---:	|:---:	|:---:	|
| (-100, -75] 	| 227669 	| 40,96 	|
| (-75, -50] 	| 94572 	| 17,01 	|
| (-25, 0] 	| 67046 	| 12,06 	|
| (-50, -25] 	| 58086 	| 10,45 	|
| (-inf, -100] 	| 39703 	| 7,14 	|
| (0, 25] 	| 28755 	| 5,17 	|
| (100, inf] 	| 25121 	| 4,52 	|
| (25, 50] 	| 7135 	| 1,28 	|
| (50, 75] 	| 4511 	| 0,81 	|
| (75, 100] 	| 3297 	| 0,59 	|

### Comparação das predições (considerando somente os 555895 domínios disponíveis em ambas as bases)

Threshold (limiar de decisão) utilizado nas probabilidades do modelo antigo = 0.5

Threshold (limiar de decisão) utilizado nas probabilidades do modelo novo = 0.6

Análise dos que não estão nulos (516192):

* Eram classificados como True pelo modelo antigo e agora é classificado como False pelo novo modelo: 44852 (8,689%)

* Eram classificados como False pelo modelo antigo e agora é classificado como True pelo novo modelo: 1926 (0,373%)

* A predição não mudou (continua sendo a mesma classe em ambos modelos): 469414 (90,938%)