# Grafo 1 — Relatório técnico final e auditoria

## 1. Fonte e rastreabilidade
Os dados utilizados são os arquivos JSON contidos em `nx_network_data (1).zip`, organizados em quatro diretórios: `gossipcop_fake`, `gossipcop_real`, `politifact_fake` e `politifact_real`. Foram encontrados e processados **11.257 arquivos JSON válidos**. O ZIP também contém 14 arquivos de metadados do macOS (`__MACOSX/._*`) que não são JSONs de notícias e foram excluídos. As datas internas do ZIP indicam 2020-04-12/13, mas **não comprovam a data de coleta dos eventos, a versão formal do dataset nem sua publicação**. O arquivo entregue não contém README, DOI, URL de download nem documentação da transformação original. A associação ao FakeNewsNet decorre da identificação do conjunto usado no projeto, e a procedência exata da versão processada deve ser registrada a partir do link de onde o arquivo foi obtido. Não atribuir a este ZIP metadados não verificáveis.

## 2. Definição do grafo
Cada notícia é uma árvore dirigida com raiz artificial (`type=1`), postagens (`type=2`), retuítes (`type=3`) e respostas (`type=4`). Cada aresta `pai → filho` é definida pelo aninhamento do campo `children` no JSON. Os atributos `time`, `user`, `tweet_id` e `id` são mantidos no registro original. A árvore representa **relações estruturais presentes no dataset**, não prova de exposição efetiva ou alcance dos usuários.

## 3. Métricas e fórmulas
- **Tamanho:** número de eventos excluindo a raiz artificial, `|V|-1`.
- **Profundidade máxima:** maior número de arestas da raiz artificial até um evento; a raiz está no nível zero.
- **Filhos da raiz:** grau de saída da raiz artificial, reportado separadamente.
- **Ramificação máxima:** maior número de filhos entre os vértices reais, excluindo a raiz artificial.
- **Ramificação média:** número de arestas cujo pai é um evento real dividido pelo número de eventos reais. Esta é a média de filhos por evento real e **não** a média condicionada a eventos que têm filhos.
- **Postagens, retuítes, respostas:** contagem dos tipos 2, 3 e 4.
- **Eventos temporizados:** eventos reais com valor numérico em `time`.
- **T10:** `(décimo menor timestamp - menor timestamp)/3600` horas, se houver pelo menos dez eventos com tempo válido. Não se usa o tempo da raiz artificial, que é nulo.
- **Duração observada:** `(maior timestamp - menor timestamp)/3600` horas.

## 4. Auditoria executada
Foi criado `extrair_metricas_grafo1.py`, que percorre diretamente os JSONs do ZIP, sem usar o CSV antigo como fonte. Foram reprocessadas 11.257 notícias. A comparação por chave `(source, label, filename)` com o CSV previamente entregue confirmou **zero divergências** nas 11 métricas (`size`, `depth`, `root_children`, `max_branch`, `mean_branch`, `retweets`, `replies`, `posts`, `timed`, `time10_hours`, `span_hours`). O script `validar_grafo1.py` também confronta os GEXFs dos dois estudos de caso com seus JSONs originais: coincidência exata de conjuntos de vértices e arestas, árvores dirigidas válidas, e coincidência exata dos dois subgrafos com as subárvores de descendentes.

Os estudos de caso são `gossipcop_fake/gossipcop-8463307904.json` (6.179 vértices, 6.178 arestas) e `gossipcop_real/gossipcop-955433.json` (3.903 vértices, 3.902 arestas). Os subgrafos partem, respectivamente, dos IDs `2621514926` (36 vértices, 35 arestas) e `1917835909` (42 vértices, 41 arestas). Os exemplos foram selecionados intencionalmente, não aleatoriamente.

## 5. Resultados estruturais
| Fonte | Classe | Notícias | Mediana de eventos | P90 eventos | Mediana profundidade | Mediana ramificação máxima |
|---|---|---:|---:|---:|---:|---:|
| GossipCop | Falsa | 3.684 | 30 | 1.335 | 2 | 3 |
| GossipCop | Verdadeira | 6.945 | 73 | 181 | 2 | 2 |
| PolitiFact | Falsa | 351 | 239 | 1.863 | 5 | 20 |
| PolitiFact | Verdadeira | 277 | 184 | 3.454,8 | 5 | 19 |

As medianas de tamanho se invertem entre as fontes: maior para notícias verdadeiras no GossipCop e para notícias falsas no PolitiFact. As medianas de profundidade coincidem entre classes dentro de cada fonte. A heterogeneidade e as caudas longas impedem uma generalização simples.

## 6. Resultados temporais
| Fonte | Classe | T10 calculável | Cobertura | Mediana T10 (horas) |
|---|---|---:|---:|---:|
| GossipCop | Falsa | 2.960 | 80,35% | 11,03 |
| GossipCop | Verdadeira | 6.845 | 98,56% | 0,36 |
| PolitiFact | Falsa | 336 | 95,73% | 7,97 |
| PolitiFact | Verdadeira | 252 | 90,97% | 291,02 |

T10 está disponível para **10.393 de 11.257** cascatas (92,3%). As **864** restantes têm menos de dez eventos. Há **565** cascatas com T10 acima de 365 dias, evidenciando caudas temporais muito longas. Essas observações foram mantidas nas tabelas, não descartadas silenciosamente. Os gráficos usam escala logarítmica e T10 é interpretado como intervalo entre registros, não velocidade de alcance. Os dados não estabelecem a data real da primeira exposição nem janelas de observação equivalentes.

## 7. Figuras e legendas
1. **Cascata geral falsa:** árvore radial com 6.179 vértices. Fonte: elaboração própria a partir dos JSONs processados.
2. **Cascata geral verdadeira:** árvore radial com 3.903 vértices, mesma codificação de tipos. Fonte: elaboração própria.
3. **Subárvore falsa:** 36 vértices, 35 arestas, um post e 35 retuítes. Fonte: elaboração própria.
4. **Subárvore verdadeira:** 42 vértices, 41 arestas, um post, 19 retuítes e 22 respostas. Fonte: elaboração própria.
5. **Tamanho:** função de sobrevivência empírica por fonte e classe.
6. **Profundidade:** função de sobrevivência empírica por fonte e classe.
7. **Ramificação máxima:** função de sobrevivência empírica por fonte e classe.
8. **T10:** função de distribuição acumulada empírica, apenas cascatas com T10 calculável.

As posições radiais e hierárquicas são recursos de apresentação, não escalas temporais. As figuras não permitem inferir visualizações por usuário, causalidade ou representatividade estatística dos dois casos.

## 8. Limitações e conclusão
O conjunto é uma versão processada sem documentação de proveniência no próprio ZIP. A relação de propagação é a relação `children` registrada no arquivo, e não uma reconstrução independente de eventos da plataforma. Os dois estudos de caso não são amostras representativas. Não foram realizados testes inferenciais ou ajustes por fatores de confusão. A comparação foi estratificada por fonte e permanece descritiva. O modelo mostra padrões distintos de tamanho, profundidade, ramificação e intervalos entre eventos, sem sustentar a afirmação universal de que notícias falsas sempre se propagam mais ou mais rapidamente.

## 9. Como reproduzir
Na pasta raiz do pacote, instalar `pandas numpy matplotlib networkx` e executar, nesta ordem:

```bash
python extrair_metricas_grafo1.py --zip "nx_network_data (1).zip" --saida Metricas_Cascatas_Recalculadas.csv
python validar_grafo1.py
python gerar_graficos.py --csv Metricas_Cascatas_Recalculadas.csv --saida Resultados_Reproduzidos
```

O primeiro comando lê todos os JSONs e calcula as métricas; o segundo compara CSVs e grafos; o terceiro recria as figuras estatísticas e tabelas de resumo. O pacote também contém os SVGs finais exportados do Gephi e seus GEXFs correspondentes.
