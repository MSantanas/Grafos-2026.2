"""Gera tabelas e gráficos do Grafo 1 a partir de Metricas_Cascatas_FakeNewsNet.csv.
Uso: python gerar_graficos.py --csv Metricas_Cascatas_FakeNewsNet.csv --saida resultados
Dependências: pandas numpy matplotlib
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument('--csv', default='Metricas_Cascatas_FakeNewsNet.csv')
p.add_argument('--saida', default='resultados')
a = p.parse_args()
out = Path(a.saida); out.mkdir(parents=True, exist_ok=True)
d = pd.read_csv(a.csv)
for col in ('source','label'):
    d[col] = d[col].astype(str).str.lower()

summary = (d.groupby(['source','label']).agg(
    n=('size','size'), med_size=('size','median'),p90_size=('size',lambda s:s.quantile(.9)),
    med_depth=('depth','median'),p90_depth=('depth',lambda s:s.quantile(.9)),
    med_maxbranch=('max_branch','median'),p90_maxbranch=('max_branch',lambda s:s.quantile(.9)),
    time10_available=('time10_hours','count')).reset_index())
summary.to_csv(out/'Resumo_Comparativo_Grafo1.csv', index=False)

for col, title, xlabel, filename in [
 ('size','Tamanho das cascatas','Eventos reais por cascata','Comparacao_Grafo1_Tamanho.png'),
 ('depth','Profundidade das cascatas','Profundidade máxima','Comparacao_Grafo1_Profundidade.png'),
 ('max_branch','Ramificação máxima','Maior grau de saída (excluindo raiz artificial)','Comparacao_Grafo1_Ramificacao.png')]:
    fig, axs=plt.subplots(1,2,figsize=(13,5),sharey=True)
    for ax,src in zip(axs,['gossipcop','politifact']):
        for label in ['falsa','verdadeira']:
            x=np.sort(d.loc[(d.source==src)&(d.label==label),col].dropna().to_numpy())
            if len(x)==0: continue
            # Função de sobrevivência: fração com valor >= x
            xx=np.unique(x)
            yy=1-np.searchsorted(x,xx,side='left')/len(x)
            ax.step(xx,yy,where='post',label=label.capitalize())
        if col in ('size','max_branch'): ax.set_xscale('symlog',linthresh=1)
        ax.set_title(src.capitalize());ax.set_xlabel(xlabel);ax.grid(alpha=.25);ax.legend()
    axs[0].set_ylabel('Proporção de cascatas com valor ≥ x')
    fig.suptitle(title);fig.tight_layout();fig.savefig(out/filename,dpi=190,bbox_inches='tight');plt.close(fig)

temporal=(d.groupby(['source','label']).agg(
    cascatas=('size','size'),t10_disponivel=('time10_hours','count'),
    mediana_t10_h=('time10_hours','median'),
    p25_t10_h=('time10_hours',lambda s:s.quantile(.25)),
    p75_t10_h=('time10_hours',lambda s:s.quantile(.75)),
    p90_t10_h=('time10_hours',lambda s:s.quantile(.9)),
    mediana_duracao_observada_h=('span_hours','median')).reset_index())
temporal['cobertura_t10_pct']=100*temporal.t10_disponivel/temporal.cascatas
temporal.to_csv(out/'Resumo_Temporal_Grafo1.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(13,5),sharey=True)
for ax,src in zip(axs,['gossipcop','politifact']):
    for label in ['falsa','verdadeira']:
        x=np.sort(d.loc[(d.source==src)&(d.label==label),'time10_hours'].dropna().to_numpy())
        x=x[x>0] # escala logarítmica exige valores positivos
        if len(x)==0:continue
        ax.plot(x,np.arange(1,len(x)+1)/len(x),label=label.capitalize(),linewidth=2)
    ax.set_xscale('log');ax.set_title(src.capitalize());ax.set_xlabel('T10 (horas; escala logarítmica)');ax.grid(alpha=.25);ax.legend()
axs[0].set_ylabel('Proporção acumulada entre T10 positivos')
fig.suptitle('Tempo até o décimo evento registrado')
fig.tight_layout();fig.savefig(out/'Comparacao_Grafo1_Tempo_Decimo_Evento.png',dpi=190,bbox_inches='tight');plt.close(fig)
print(f'Processadas {len(d)} cascatas. Resultados em: {out.resolve()}')
