#!/usr/bin/env python3
"""Reproduz concentração e remoção de usuários do Grafo 2 a partir dos CSVs agregados.
Execução: python 04_GRAFO_2/Scripts/reproduzir_analises_grafo2.py
Não modifica os CSVs originais. Usa apenas a biblioteca padrão.
"""
import csv, math
from pathlib import Path
BASE = Path(__file__).resolve().parents[2]
G2 = BASE/'04_GRAFO_2'
OUT = G2/'Metricas'/'Reproducao'
OUT.mkdir(parents=True,exist_ok=True)
GROUPS=['gossipcop_fake','gossipcop_real','politifact_fake','politifact_real']

def load_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        yield from csv.DictReader(f)

def run(group):
    strengths={}
    for row in load_csv(G2/'Redes_Usuarios'/'Usuarios'/f'usuarios_{group}.csv'):
        if int(row['OutStrength'])>0: strengths[row['Id']]=int(row['OutStrength'])
    active=set(strengths)
    n=len(active)
    k=math.ceil(n*.01)
    # Empate na posição limite: desempate por identificador, para resultado determinístico.
    top=set(sorted(strengths,key=lambda u:(-strengths[u],u))[:k])
    total=0; targeted=0; lost_unique=0; count_edges=0
    # Baseline analítica: amostragem uniforme de k usuários dentre n origens ativas.
    # Uma aresta é perdida se ao menos uma ponta é selecionada.
    expected=0.0
    p=k/n
    p_two=1-((n-k)*(n-k-1)/(n*(n-1))) if n>1 else 1.0
    for row in load_csv(G2/'Redes_Usuarios'/'Arestas'/f'arestas_{group}.csv'):
        src,tgt,w=row['Source'],row['Target'],int(row['Weight'])
        count_edges+=1;total+=w
        if src in top or tgt in top:targeted+=w;lost_unique+=1
        expected+=w*(p_two if tgt in active else p)
    # Concentração: soma das forças de saída dos top k / total de relações.
    concentration=100*sum(strengths[u] for u in top)/total
    return dict(Grupo=group,UsuariosOrigemAtivos=n,Removidos1pct=k,RetuitesTotais=total,
                ConcentracaoTop1pct=round(concentration,4),PerdaTop1pct=round(100*targeted/total,4),
                PerdaAleatoriaEsperada=round(100*expected/total,4),
                Razao=round(targeted/expected,4),ArestasUnicasPerdidasPct=round(100*lost_unique/count_edges,4))

if __name__=='__main__':
    rows=[run(g) for g in GROUPS]
    path=OUT/'analises_recalculadas_grafo2.csv'
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    for row in rows:print(row)
    print('Resultado:',path)
