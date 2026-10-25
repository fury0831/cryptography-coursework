# Attribution and source context

Author: **Fengrui Zhang**.

The original materials are undergraduate learning notebooks. Standard algorithms and mathematical identities are not claimed as new inventions. Notebook filenames below are provenance labels, not downloadable inputs or claims of external authorship.

## RSA notebook

`Zhang.ipynb`, zero-based cell 3, contains exactly this heading:

> ## Starter algorithms

Cell 4 defines `fme`, `gcd`, `extended_gcd`, `mod_inverse`, `compute_d`, `decrypt_numbers_to_string`, and `smallest_prime_factor`. Neither the heading nor the cell states that these function bodies were supplied by an instructor or copied from an external implementation. It also does not explicitly describe an assignment instruction to implement them. The heading is therefore recorded as source context, not treated as proof of either external ownership or independent invention.

Cell 6 contains these algorithm references:

- [Wikipedia: Pollard's rho algorithm](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm)
- [cp-algorithms: Integer factorization, Pollard's rho](https://cp-algorithms.com/algebra/factorization.html#pollards-rho-algorithm)

The links alone do not establish that implementation text was copied. No external implementation or third-party source file is bundled on the basis of those links. Preserve this reference context when describing the coursework.

## ECC notebook

`ecc_project.ipynb`, zero-based cell 14, contains this exact comment inside `square_roots_mod_prime`:

> This follows the method in ecc_cycle.ipynb: p = 3 mod 4.

It points to a related local learning notebook. It does not say that an instructor supplied the implementation. The referenced method is the familiar modular square-root shortcut for primes congruent to 3 modulo 4. The related exploratory notebook is not copied into this repository.

The main ECC example's public-offset construction is intentionally described as nonconfidential. A separate incomplete ElGamal-style decryption draft is excluded; no security guarantee is inferred from that draft.

## Release boundary

The author expressly authorized public release of their self-written RSA/ECC code and selected MIT. The reviewed source did not identify a concrete externally copied implementation or a conflicting upstream license. A generic heading or mathematical reference is not being used to invent such a restriction.

The MIT text is provided unchanged in `LICENSE`. It does not relicense the external articles, reference PDFs, original assignment text, or original teaching inputs; none of those are included. If a specific externally owned implementation is subsequently identified, retain its applicable notice and resolve its inclusion separately.

The packaging, bounded demonstrations, documentation, and small checks were prepared with Codex assistance. The original algorithm function bodies were preserved; this is not a claim of independently invented mathematical algorithms.
