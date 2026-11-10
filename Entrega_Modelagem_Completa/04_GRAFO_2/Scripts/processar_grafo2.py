import zipfile,json,collections,csv,time,os
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
zpath=BASE/'02_DADOS/Dataset_Original/nx_network_data (1).zip'
out=BASE/'04_GRAFO_2/Redes_Usuarios/Reprocessamento';out.mkdir(parents=True,exist_ok=True)
counts=collections.defaultdict(collections.Counter); nodes=collections.defaultdict(set);news=collections.Counter(); events=collections.Counter(); skipped=collections.Counter();seen_news=collections.defaultdict(lambda:collections.Counter())
t=time.time()
with zipfile.ZipFile(zpath) as z:
 for ix,name in enumerate(z.namelist()):
  if not name.endswith('.json') or '__MACOSX' in name:continue
  parts=name.split('/');grp=parts[-2];news[grp]+=1
  root=json.loads(z.read(name)); stack=[(root,None)];users_in_news=set()
  while stack:
   obj,parent=stack.pop();typ=obj.get('type');usr=obj.get('user');events[(grp,typ)]+=1
   if typ!=1 and usr is not None:
    usr=str(usr);nodes[grp].add(usr);users_in_news.add(usr)
   if typ==3:
    pu=parent.get('user') if parent else None
    if parent is None or parent.get('type')==1 or pu is None or usr is None:skipped[(grp,'parent_missing')]+=1
    elif str(pu)==str(usr):skipped[(grp,'self_loop')]+=1
    else:counts[grp][(str(pu),str(usr))]+=1
   stack.extend((c,obj) for c in obj.get('children',[]))
  for u in users_in_news:seen_news[grp][u]+=1
  if (ix+1)%2000==0:print('processed',ix+1,'elapsed',round(time.time()-t,1),flush=True)
for grp, edges in counts.items():
 with open(out/f'arestas_{grp}.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['Source','Target','Weight']);w.writerows((a,b,n) for (a,b),n in edges.items())
 indeg=collections.Counter();outdeg=collections.Counter();instr=collections.Counter();outstr=collections.Counter()
 for (a,b),n in edges.items():outdeg[a]+=1;indeg[b]+=1;outstr[a]+=n;instr[b]+=n
 with open(out/f'usuarios_{grp}.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['Id','Label','InDegree','OutDegree','InStrength','OutStrength','NewsCount'])
  for u in nodes[grp]:w.writerow([u,u,indeg[u],outdeg[u],instr[u],outstr[u],seen_news[grp][u]])
 with open(out/f'top_usuarios_{grp}.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['UserId','OutStrength','OutDegree','InStrength','InDegree','NewsCount'])
  for u,n in outstr.most_common(100):w.writerow([u,n,outdeg[u],instr[u],indeg[u],seen_news[grp][u]])
with open(out/'resumo_grafo2.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['Grupo','Noticias','Usuarios','ArestasUnicas','RetuitesRepresentados','RetuitesSemPaiValido','AutolacosExcluidos'])
 for grp in sorted(news):w.writerow([grp,news[grp],len(nodes[grp]),len(counts[grp]),sum(counts[grp].values()),skipped[(grp,'parent_missing')],skipped[(grp,'self_loop')]])
print('DONE',round(time.time()-t,1));print((out/'resumo_grafo2.csv').read_text())
