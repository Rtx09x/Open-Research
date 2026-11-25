# Seven-checksum-class necessity theorem

Every binary length-12 single-deletion-correcting code of size at least 317 uses at least seven VT checksum classes. Therefore an improving trade from VT0 introduces at least six nonzero syndromes. This does **not** improve the global integer interval 316–320 or prove VT optimality.

Read [checksum_support_theorem.md](checksum_support_theorem.md). The selected self-contained archive has 868 exact dual records covering all 1,716 supports, 2,352 required cliques, and a stdlib checker. To keep individual repository transfers bounded, its unchanged bytes are stored in 47 ordered parts, each at most 256 KiB. The manifest binds every part and the complete ZIP, SHA-256 `d3fd5337d50c5ec13bfd672a0169c175aef03c2133efeabd709c19ede8aad8b4`.

From this directory, `python -I -S replay_k6.py --independent` verifies hashes, reassembles/extracts only into a disposable temporary directory, then runs both the primary and independent checkers. `python -I -S replay_k6.py --negative` deliberately removes one required certificate and requires rejection. No external data or solver is needed.

The separate [global dual checkpoint](../continuation/release_20261025/README.md) and [fractional 26-coordinate obstruction](../continuation/barrier26_release_20261025/README.md) do not construct a code.
