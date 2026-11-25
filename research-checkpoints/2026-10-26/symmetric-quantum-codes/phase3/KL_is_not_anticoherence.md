# A checked obstacle to an overly strong generalization

The three-error code certified by `code37_root_certificate.json` and all98 KL identities is **not2-anticoherent**. This is a concrete counterexample to replacing unrestricted error correction by vanishing low spin moments.

Let j=37/2 and let the even-weight codeword have coefficients sqrt(C(37,2i))q_i, with q0=1 and the other q_i in the certified rational root box. Write B=Σ_i C(37,2i)q_i². The polynomial

    F=Σ_i C(37,2i)[3(37−4i)²−37·39]q_i²

satisfies F=12B(〈Jz²〉−j(j+1)/3). Exact rational interval evaluation of the root box proves F<0. The normalized moment difference is approximately−27.02717; this approximation is not needed for the sign proof. See `check_non_anticoherence37.py` and `non_anticoherence37.json`. The advisor independently obtained the same sign and a root-box uncertainty below8.1e−46 relative to the center value.

Error correction requires PTP=λ_T P for all detected T. It does **not** require λ_T=0 for traceless spin tensors. Anticoherent-subspace bounds are therefore not automatically unrestricted code bounds. A general lower-bound argument must retain the allowed common scalar moments, or independently prove that the particular code under consideration has zero moments.

This does not refute the conjectured minimum-length formula3t²+3t+1. It refutes one stronger, tempting reduction of the problem. Neither the phenomenon nor this calculation is claimed novel.
