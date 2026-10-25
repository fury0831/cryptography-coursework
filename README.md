# Cryptography coursework

Two undergraduate studies connecting mathematical ideas to readable Python implementations: RSA factorization and decryption, and finite-field elliptic-curve arithmetic.

The repository includes the complete function definitions from the two primary notebooks, a command-line entry point, newly created numeric examples, and small correctness checks. Original assignment inputs, notebook outputs, recovered messages, and reference PDFs are excluded.

**Educational scope:** these are small mathematical exercises, not secure cryptographic products. The elliptic-curve public-offset demonstration specifically shows a construction that provides no confidentiality.

## Quick start

Python **3.11+**, standard library only. No package installation is required.

```bash
python3 run_demo.py rsa --input examples/rsa_toy.json
python3 run_demo.py ecc-offset --input examples/ecc_offset_toy.json
python3 -B -m unittest discover -s tests -v
```

Run from the repository root. The CLI bounds its inputs to small examples and prints numeric JSON. It does not read the original coursework data or contact a network service.

## RSA: from factors to a recovered integer

The module connects trial division, a basic Pollard rho loop, extended Euclid, modular inversion, and repeated squaring. It retains the original record parser and decryption functions, while the CLI uses a newly created input rather than the assignment file.

The example starts with `p=11`, `q=17`, `e=7`, and the invented integer message `42`. The CLI constructs a toy ciphertext, factors the modulus, derives the private exponent, and recovers the integer. It is intentionally small and does not demonstrate an attack on modern RSA.

The original implementation routes moduli below `10^10` to trial division. This is an implementation choice, not a measured performance boundary. Its Pollard rho loop has no iteration budget; do not use the raw function for unbounded or untrusted inputs. The totient formula assumes two distinct prime factors, and the notebook-level functions have limited input validation. The CLI validates its small toy inputs separately.

## Elliptic curves: arithmetic and a public-offset counterexample

The module includes point addition, doubling, double-and-add scalar multiplication, point enumeration, point-order calculation, and character-to-point mapping.

The primary demonstration forms `C = M + T` where `T` is public. Anyone can calculate `M = C - T`, so the construction offers **no confidentiality**. The new numeric example uses the curve `y² = x³ + 2x + 3 mod 103`, message point `(2,18)`, and public offset `3M`. It prints the recovered point without using a secret.

Point enumeration and trial division are intended for small parameters. The modular square-root helper supports its documented `p ≡ 3 (mod 4)` shortcut rather than every prime. The character mapping is a custom finite lookup, not a standard hash-to-curve encoding.

A separate exploratory notebook describes an ElGamal-style recovery formula. It has no saved execution results and is missing self-contained inputs and an encryption/randomness implementation. It is **not** merged into this repository as a completed encryption system.

## Layout

```text
src/cryptography_coursework/rsa.py    11 original function definitions
src/cryptography_coursework/ecc.py    27 original function definitions
src/cryptography_coursework/cli.py    New bounded numeric demonstrations
run_demo.py                         Entry point without installation
examples/                           Newly created toy inputs
tests/                              Small arithmetic and CLI checks
provenance/source-map.json           Notebook hashes and cell-to-function mapping
ATTRIBUTION.md                      Source context and references
VALIDATION.md                       What was checked and what was not
```

## Evidence and attribution

The primary notebooks were checked against the supplied attachments and are byte-identical. All function bodies were preserved during extraction; original top-level inputs and execution cells were replaced by the new CLI. The original RSA input was found locally and its format and saved factor products were checked, but it is not part of this release.

Historical notebook outputs are not presented as freshly reproduced results. Release checks use only newly created or tiny mathematical examples, not original course messages or large factorizations. See [VALIDATION.md](VALIDATION.md).

These implementations use standard mathematical algorithms. The RSA notebook has a section titled “Starter algorithms” and cites Pollard rho references; its title alone does not establish that implementation text was supplied by the course. The ECC square-root comment points to the author's related `ecc_cycle.ipynb` learning notebook. See [ATTRIBUTION.md](ATTRIBUTION.md) for the exact evidence and references. This repository does not claim the mathematical algorithms are novel or that every conceptual method was independently invented.

The repository organization, new examples, and tests were prepared with Codex assistance. Publication of the author's self-written code and use of MIT were expressly authorized. [MIT](LICENSE) covers the code the author has the right to license; linked external works retain their own terms and are not bundled here.
