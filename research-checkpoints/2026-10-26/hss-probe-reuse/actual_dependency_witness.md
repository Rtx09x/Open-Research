# Actual reused-sketch dependence at every fixed oversampling size

**Status:** complete proof; independent algebra audit passed. This refutes a proof shortcut, not the compression algorithm or RE-02.

Consider k=1,L=1,N=4 and A=[[0,I₂],[I₂,0]]. Use the Levitt–Martinsson top-singular-vector basis selection with any integer sketch width s≥3. The forward and transpose test families are independent.

Condition on G=Ω[first leaf,:] and the transpose-derived bases V₁,V₂. The latter depend only on Ψ and are therefore independent of Ω. Let N be any fixed orthonormal basis of ker G, with r=s−2 columns, H=Ω[second leaf,:], and v=V₂. Conditional on G,V₁,V₂,

    M=HN

is a2-by-r standard Gaussian matrix. The algorithm's first leaf basis u is a top left singular vector of M. The exact projected core that the carried data is intended to sketch is UᵀAV, since the discrepancy factors satisfy UᵀDV=0. This is not a claim that the noisy root least-squares estimate already equals that core. Its offdiagonal entry from first to second leaf is h=uᵀv. The compressed forward test in the second leaf is vᵀH. Define two gauge-invariant statistics

    X=h²,       W=||vᵀHN||².

Let λ₁≥λ₂ be the eigenvalues of MMᵀ. By rotational invariance, its principal eigendirection is uniform on the circle and independent of the eigenvalues. Hence X=cos²θ with θ uniform moduloπ, so E X=1/2 and Var(X)=1/8. In the principal-eigenvector coordinates,

    W = λ₂ + (λ₁−λ₂) X.

Therefore

    Cov(X,W | G,V₁,V₂) = (Eλ₁−Eλ₂)/8 > 0.

The gap is strictly positive almost surely and has finite positive mean, including r=1 where λ₂=0. Thus the compressed forward test and the compressed matrix are dependent, even though the test itself is marginally Gaussian conditional on the transpose bases. This remains true for every larger fixed s, so oversampling does not restore the naive independence argument.

To avoid conditioning on retained G altogether, let R span row(G), so [N,R] is orthogonal. The additional variable W_row=||vᵀHR||² is independent of M, hence of X, conditional on G,V. Thus W_total=||vᵀH||²=W+W_row has the same strictly positive covariance with X. Moreover E[X|G,V]=1/2 and E[W_total|G,V]=s are constant in G. Averaging over G preserves the covariance conditional only on V. W_total is directly measurable from the compressed second-leaf test row. Therefore the dependence is intrinsic to the compressed objects, not only to an enlarged conditioning σ-field.

The invalid step is: “V is independent of Ω, hence VᵀΩ is Gaussian, hence it can be analyzed as an independent Gaussian sketch of UᵀAV.” The first two statements are correct; the last is false because U was selected using Ω. The example establishes exactly that barrier and makes no assertion that the desired approximation bound is false.
