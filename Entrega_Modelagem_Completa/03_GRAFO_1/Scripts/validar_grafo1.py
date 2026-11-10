"""Valida GEXFs dos casos contra os JSONs originais e métricas CSV recalculadas."""
import json,zipfile,networkx as nx,pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'02_DADOS/Dataset_Original/nx_network_data (1).zip'
GEXF=ROOT/'03_GRAFO_1/Modelos_Gephi'
METRICAS=ROOT/'03_GRAFO_1/Metricas'
CASOS=[
 ('nx_network_data/gossipcop_fake/gossipcop-8463307904.json','Grafo_1_Falsa_Radial_Hierarquico_Gephi.gexf','Subgrafo_2621514926_Descendentes_Gephi.gexf','2621514926'),
 ('nx_network_data/gossipcop_real/gossipcop-955433.json','Grafo_1_Verdadeira_Radial_Hierarquico_Gephi.gexf','Grafo1_NoticiaVerdadeira_SubgrafoDetalhado.gexf','1917835909')]

def original(root):
    nodes={};edges=set();stack=[root]
    while stack:
        p=stack.pop();pid=str(p['id']);nodes[pid]=p
        for c in p.get('children') or []:
            edges.add((pid,str(c['id'])));stack.append(c)
    return nodes,edges

def main():
    with zipfile.ZipFile(DATA) as z:
        for member,gfile,sfile,selected in CASOS:
            nodes,edges=original(json.loads(z.read(member)))
            g=nx.read_gexf(GEXF/gfile)
            assert set(g.nodes)==set(nodes),f'{gfile}: vértices divergentes'
            assert set(g.edges)==edges,f'{gfile}: arestas divergentes'
            assert nx.is_arborescence(g),f'{gfile}: não é arborescência'
            s=nx.read_gexf(GEXF/sfile)
            desc=nx.descendants(g,selected)|{selected}
            assert set(s.nodes)==desc,f'{sfile}: nós divergentes'
            assert set(s.edges)==set(g.subgraph(desc).edges),f'{sfile}: arestas divergentes'
            print(f'OK {member}: {len(g)} vértices, {g.number_of_edges()} arestas; subárvore {len(s)} vértices, {s.number_of_edges()} arestas')
    old=pd.read_csv(METRICAS/'Metricas_Cascatas_FakeNewsNet.csv')
    new=pd.read_csv(METRICAS/'Metricas_Cascatas_Recalculadas.csv')
    cols=[c for c in old if c not in ('source','label','filename')]
    m=old.merge(new,on=['source','label','filename'],suffixes=('_anterior','_recalculado'),validate='one_to_one')
    assert len(m)==len(old)==len(new)==11257
    import numpy as np
    for c in cols:
        assert np.allclose(m[c+'_anterior'],m[c+'_recalculado'],equal_nan=True,rtol=1e-9,atol=1e-8),f'Diferença: {c}'
    print('OK 11.257 cascatas: todas as 11 métricas conferem com CSV anterior')
if __name__=='__main__':main()
