"""Extrai métricas estruturais e temporais do ZIP nx_network_data do FakeNewsNet.
Uso: python extrair_metricas_grafo1.py --zip 'nx_network_data (1).zip' --saida Metricas_Cascatas_FakeNewsNet.csv
Cada arquivo JSON é uma árvore com raiz artificial type=1 e children aninhados.
"""
import argparse, csv, json, zipfile
from collections import Counter
from pathlib import Path

FIELDS=['source','label','filename','size','depth','root_children','max_branch','mean_branch','retweets','replies','posts','timed','time10_hours','span_hours']

def extrair(root):
    stack=[(root,0)]
    size=0; depth=0; root_children=len(root.get('children') or []); max_branch=0
    counts=Counter(); times=[]; total_children_nonroot=0
    while stack:
        node,level=stack.pop()
        children=node.get('children') or []
        if level>0:
            size+=1; depth=max(depth,level)
            counts[node.get('type')]+=1
            max_branch=max(max_branch,len(children))
            total_children_nonroot+=len(children)
            t=node.get('time')
            if isinstance(t,(int,float)) and not isinstance(t,bool):times.append(t)
        stack.extend((child,level+1) for child in children)
    times.sort()
    return dict(size=size,depth=depth,root_children=root_children,max_branch=max_branch,
        mean_branch=(total_children_nonroot/size if size else 0),
        retweets=counts[3],replies=counts[4],posts=counts[2],timed=len(times),
        time10_hours=((times[9]-times[0])/3600 if len(times)>=10 else None),
        span_hours=((times[-1]-times[0])/3600 if times else None))

def run(zip_path,out_path):
    count=0
    with zipfile.ZipFile(zip_path) as z,open(out_path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
        for member in z.namelist():
            if not member.endswith('.json') or member.startswith('__MACOSX/') or Path(member).name.startswith('._'):continue
            parts=Path(member).parts
            folder=parts[-2]
            source,klass=folder.rsplit('_',1)
            if source not in ('gossipcop','politifact') or klass not in ('fake','real'):
                raise ValueError(f'Pasta desconhecida: {folder}')
            data=json.loads(z.read(member))
            metrics=extrair(data)
            w.writerow(dict(source=source,label=('falsa' if klass=='fake' else 'verdadeira'),filename=parts[-1],**metrics))
            count+=1
    print(f'{count} cascatas processadas em {out_path}')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--zip',default='nx_network_data (1).zip');p.add_argument('--saida',default='Metricas_Cascatas_FakeNewsNet.csv');a=p.parse_args()
    run(a.zip,a.saida)
