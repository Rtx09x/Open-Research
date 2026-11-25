"""Small physical-probe controls for the restricted path LS theorem."""
import json
import numpy as np
from test_path_global_ls_inverse import bank


def main():
    rng=np.random.default_rng(997352);out=[]
    for n in [4,8,16,32]:
        support=[(i,i) for i in range(n)]+[(i,i+1) for i in range(n-1)]+[(i+1,i) for i in range(n-1)]
        d=len(support);aa=np.zeros((d,n,n))
        for a,(i,j) in enumerate(support):aa[a,i,j]=1
        sums=np.zeros(n*n);second=np.zeros(d);exacterr=0.;trials=200
        for _ in range(trials):
            om,ps=bank(n,5,rng),bank(n,5,rng)
            gradients=aa@(om@om.T)+(ps@ps.T)@aa
            gram=gradients.reshape(d,-1)@aa.reshape(d,-1).T
            inv=np.linalg.inv(gram)
            decode=inv@gradients.reshape(d,-1)
            leakage=decode-aa.reshape(d,-1)
            exacterr=max(exacterr,float(np.max(np.abs(leakage@aa.reshape(d,-1).T))))
            sums+=np.sum(leakage*leakage,axis=0)/trials
            second+=np.sum(inv*inv,axis=0)/trials
        out.append(dict(n=n,trials=trials,total_scalar_queries=10,
                        max_on_model_error=exacterr,
                        max_empirical_unit_input_error_factor=1+float(max(sums)),
                        max_empirical_inverse_square_diagonal=float(max(second)),
                        proven_error_factor=85,proven_inverse_square_diagonal=7/3))
    result=dict(status='NUMERICAL_CONTROLS_NOT_PROOF',results=out)
    print(json.dumps(result,indent=2))
    with open('path_global_ls_robustness_results.json','w') as f:json.dump(result,f,indent=2)

if __name__=='__main__':main()
