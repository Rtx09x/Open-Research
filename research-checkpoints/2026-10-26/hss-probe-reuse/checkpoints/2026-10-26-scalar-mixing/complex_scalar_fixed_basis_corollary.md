# Complex scalar corollary by phase gauging and complexification

**Status:** elementary corollary of the audited real scalar theorem;
independent analytic advisor audit PASS (26 October 2026). No new unitary-Haar moment argument is needed.
Same binary hierarchy with scalar active spaces and2-coordinate leaves.

For prescribed COMPLEX scalar nested row and column bases, there are known
physical diagonal unitary matrices D_U,D_V that turn the two hierarchies into
real nonnegative scalar transfer hierarchies, up to harmless active-basis
phases. To see this, fix phases at the two root active vectors and descend.
If a parent has transfer b=(b_1,b_2)^T and phase eta, assign its child's phase
eta_i=eta b_i/|b_i| (arbitrary if b_i=0). The new transfer coefficients are
conj(eta_i)b_i eta=|b_i|. Each child has only one parent, so these choices are
consistent. The final coordinate phases form the physical diagonal unitary.
Prescribed active subspaces are unchanged by their scalar basis phases;
arbitrary coupling coefficients absorb them. Thus the fixed complex class
is carried exactly to the complexification of the real class with transfer
magnitudes, not to a free coordinate-support enlargement.

Let Atilde=D_U^* A D_V. Its fixed-class orthogonal projection and Frobenius
residual transform unitarily. Run the real width3 probe construction for the
real transfer hierarchies, retaining complex samples. The same real linear
coefficient map acts separately on Re Atilde and Im Atilde, so

    E||R(Atilde)||_F²
      =E||R(Re Atilde)||_F²+E||R(Im Atilde)||_F²
      <=800||Atilde||_F².

Exactness and range in the complex fixed class yield the same801 relative
squared-Frobenius factor, independently of depth. Query count is exactly
three complex A products and three complex A^* products. Known unitary
pre/post multiplication costs no extra oracle call. For a real test psi,
conj(Atilde^* psi)=Atilde^T psi, so one may reuse the real-coefficient transpose
formulas by conjugating the adjoint sample; equivalently write their complex
adjoint version directly. A bilinear transpose query is not assumed available.
The output is pulled back as D_U R(Atilde) D_V^*.

This is a complex scalar fixed-basis corollary only. It does not extend the
proof to arbitrary rank, change the prescribed-before-probes requirement,
or make a finite-precision guarantee. The query unit is one complex matvec;
no conversion to a real-only oracle is implicit. Standard unbiased averaging
also complexifies unchanged.
