# Numeric toy inputs

Both examples were assembled for this release and do not contain original coursework ciphertext or recovered messages.

- `rsa_toy.json`: factors 11 and 17, exponent 7, invented integer message 42. The CLI generates the corresponding ciphertext when run.
- `ecc_offset_toy.json`: curve coefficients 2 and 3 over the field modulo 103, point `(2,18)`, and public offset scalar 3. The demo illustrates removal of a public offset without a secret.

These are small correctness examples, not benchmark data. They do not establish security or behavior on large inputs. Validation results are recorded in `../VALIDATION.md`.
