import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
pares=[("Bach → Chopin","steering_forte"),("Chopin → Bach","steering_forte_Chopin_Bach"),
       ("Mozart → Debussy","steering_forte_Mozart_Debussy"),("Joplin → Chopin","steering_forte_Joplin_Chopin")]
conds=[("nenhum","nenhum","#8a8a8a"),("aleatorio","aleatório","#d08c3a"),("centrado","centrado","#2a6f97")]
fig,ax=plt.subplots(figsize=(9,5.4))
w=0.22
for i,(nome,f) in enumerate(pares):
    d=pd.read_csv(f+".csv")
    for j,(c,lab,col) in enumerate(conds):
        s=d[d.cond==c].groupby("seed").progresso.mean()
        m,e=s.mean(),s.std(ddof=1)/np.sqrt(len(s))
        x=i+(j-1)*w
        ax.errorbar(x,m,yerr=e,fmt="o",color=col,capsize=4,ms=7,label=lab if i==0 else None)
        ax.annotate(f"{m:.2f}".replace(".",","),(x,m+e),xytext=(0,5),textcoords="offset points",ha="center",fontsize=8,color=col)
ax.set_xticks(range(4)); ax.set_xticklabels([p[0] for p in pares],fontsize=11)
ax.axhline(0,color="#bbb",lw=.8); ax.axhline(1,color="#bbb",lw=.8,ls="--")
ax.text(3.45,1.01,"alvo = 1",ha="right",fontsize=8,color="#777")
ax.set_ylim(-0.05,1.05); ax.set_yticks([0,.2,.4,.6,.8,1]); ax.set_yticklabels(["0","0,2","0,4","0,6","0,8","1"]); ax.set_xlim(-0.5,3.5)
ax.set_ylabel("Progresso no eixo origem → alvo\n(média por semente ± erro padrão)")
ax.legend(title="Vetor somado",loc="upper right",bbox_to_anchor=(1,0.93),frameon=False)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.suptitle("O vetor do compositor desloca a música entre estilos distantes, mas não em todo par",fontsize=12.5,x=0.02,ha="left",y=0.97)
fig.text(0.02,0.905,"7 sementes por par, α = 1. Centrado > aleatório em 7/7, 7/7, 6/7 e 5/7 sementes (o último, p = 0,69).",fontsize=9,color="#444",ha="left")
fig.text(0.02,0.015,"Haydn → Mozart omitido: os centróides estão a 0,10 de distância, o eixo não é definido e o progresso sai de 0–1 (não interpretável).",fontsize=8,color="#555",ha="left")
fig.tight_layout(rect=(0,0.04,1,0.89))
fig.savefig("figs/steering_pares.png",dpi=150)
