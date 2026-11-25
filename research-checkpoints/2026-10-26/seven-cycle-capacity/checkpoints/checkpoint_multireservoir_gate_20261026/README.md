# Local-only verified multi-reservoir gate

I0² ∪ Z ∪ T(Z) has273778 physical length10 words and an explicit135033-clique
partition. Its restricted normalized capacity is below3.258698 at every macro
length, excluding3.258841. This is not a globalC7 upper bound or a new lower
bound. Exact finitealpha is only bracketed134753…135033.

Run from this directory, standard library only:

    python physical_iteration/verify_multireservoir_final.py
    python advisor/check_c7_multireservoir_portable.py

The portable advisor checker differs from its preserved original only in the
workspace-root path. The final certificate and literal published base arrays
are the only mathematical data dependencies. SourceLICENSE/NOTICE retained.
See physical_iteration/multireservoir_gate_proof.md for proof, scope and search
provenance. Antecedent search files referenced there live in the working tree,
not this minimal packet; they are not needed to verify the result.

Frozen locally under the parent's packaging hold. No git/upload/publication.
Priority is not established; published constructions remain attributed.
