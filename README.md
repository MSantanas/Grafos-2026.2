# Propagação de Desinformação em Redes Sociais

**Projeto acadêmico de Teoria dos Grafos — Cenário 2: Propagação de Desinformação em Redes Sociais.**

Este repositório reúne o desenvolvimento de um protótipo de análise de redes voltado ao estudo de como notícias falsas (*fake*) e verdadeiras (*real*) se propagam em redes sociais. A proposta utiliza **grafos dirigidos**, métricas estruturais e representações visuais para comparar cascatas de disseminação e investigar a participação dos usuários na circulação das informações.

## Informações acadêmicas

| Informação | Descrição |
| --- | --- |
| **Universidade** | Universidade Federal de Itajubá (UNIFEI) |
| **Unidade acadêmica** | Instituto de Matemática e Computação (IMC) |
| **Disciplina** | SMAC03 — Grafos |
| **Professor** | Rafael Frinhani |
| **Cenário do projeto** | Propagação de Desinformação em Redes Sociais |

## Equipe

| Integrante | Papel no projeto 
| --- | --- |
| **Maria Eduarda de Jesus Santana** | Coordenadora | 
| **Maria Alice Moraes Batista** | Modeladora A |
| **Manuela de Cássia Silva Santos** | Modeladora B | 
| **Matheus Motta Soriano** | Desenvolver A |
| **Sofia Nogueira Batista** | Desenvolvedora B |

## Objetivo

Analisar e comparar os padrões de propagação de notícias falsas e verdadeiras por meio de modelos fundamentados na Teoria dos Grafos, observando:

- O **tamanho**, a **profundidade**, a **ramificação** e a **duração** das cascatas de disseminação.
- As diferenças entre as cascatas associadas às classes `fake` e `real`, considerando separadamente as fontes de dados.
- A participação de usuários na rede agregada de interações e a concentração de interações associadas a notícias falsas.
- A sensibilidade da estrutura da rede a **remoções hipotéticas de vértices**, quando empregadas como experimento complementar.

## Base de dados

O projeto utiliza cascatas de propagação de notícias associadas às fontes **GossipCop** e **PolitiFact**, com rótulos de notícias falsas (`fake`) e verdadeiras (`real`). O conjunto de dados de referência indicado na disciplina é o **FakeNewsNet**.

- [FakeNewsNet — Kaggle](https://www.kaggle.com/datasets/mdepak/fakenewsnet)

O notebook trabalha com um arquivo ZIP de **JSONs estruturados como árvores de propagação**, contendo eventos e relações `children` entre eles. O arquivo deve ser disponibilizado no formato esperado pelo código; dependendo da origem do download, pode ser necessária uma etapa de preparação dos dados.

## Tecnologias utilizadas

- **Python 3** — implementação do protótipo.
- **NetworkX** — construção e análise dos grafos.
- **Pandas** — organização, agregação e comparação das métricas.
- **Matplotlib** — gráficos e visualizações.
- **Jupyter Notebook / Google Colab** — execução e documentação interativa das análises.
- **JSON e ZIP** — armazenamento e leitura dos dados de propagação.
- **Gephi** - recurso auxiliar na modelagem.

## Limitações

- A análise depende da qualidade, completude e classificação dos dados disponíveis.
- A direção das arestas representa relações registradas no dataset, não necessariamente influência causal entre pessoas.
- Os pesos de interação não equivalem automaticamente ao número de pessoas alcançadas ou ao impacto social de uma notícia.
- Os resultados observados nas fontes GossipCop e PolitiFact não podem ser generalizados indiscriminadamente para todas as redes sociais.
- A remoção hipotética de usuários não reproduz as respostas comportamentais de uma rede social real.

## Referências e créditos

- **UNIFEI — SMAC03: Grafos.** Diretrizes do Projeto, 2º semestre de 2026, Prof. Rafael Frinhani.
- **FakeNewsNet.** Base pública de notícias e dados sociais, disponível no [Kaggle](https://www.kaggle.com/datasets/mdepak/fakenewsnet).
- **Fake News Propagation.** [Repositório de referência](https://github.com/mdepak/fake-news-propagation) para estruturas de propagação.
- **NetworkX.** [Documentação oficial](https://networkx.org/documentation/stable/).

## Como executar

### 1. Preparar o ambiente

Clone ou baixe este repositório e instale as bibliotecas principais:

```bash
python -m pip install jupyter networkx pandas matplotlib
```

Se estiver utilizando uma versão ampliada do notebook, com análises estatísticas adicionais, podem ser necessárias também `numpy` e `scipy`:

```bash
python -m pip install numpy scipy
```

No Google Colab, parte dessas bibliotecas pode já estar disponível.

### 2. Executar o notebook

Abra o arquivo `.ipynb` deste repositório no Jupyter Notebook ou Google Colab e execute as células na ordem apresentada. Para iniciar o Jupyter localmente:

```bash
jupyter notebook
```

O processamento poderá produzir tabelas de métricas, gráficos de comparação, ilustrações de cascatas e análises do grafo de usuários. Os arquivos específicos gerados dependem das células executadas; entre os previstos no código estão `metricas_cascatas.csv` e `grafo1_comparacao.png`.

---

**Projeto desenvolvido para fins acadêmicos na Universidade Federal de Itajubá (UNIFEI), na disciplina SMAC03 — Grafos, 2026/2.**
