# Validation record

Release preparation date: 2026-10-25.

## Checks actually performed

- Parsed and syntax-compiled every Python source file.
- Compared all 11 RSA and 27 ECC function ASTs with the primary source notebooks: all function bodies match. Only packaging and new wrappers were added; the original algorithms were not rewritten.
- Ran `python3 -B -m unittest discover -s tests -v` with the available Python 3.13 interpreter: **12 tests passed**.
- The suite ran both CLI examples as separate processes, parsed their JSON output, and verified `round_trip_equal` was true with no stderr output.
- Checked release text for private absolute filesystem paths: none found.

The small checks cover modular exponentiation against Python's independent built-in `pow`, invertible and noninvertible residues, small trial division and Pollard rho, an invented RSA record, point identity and inverse behavior, zero and negative scalars, point closure, public-offset recovery without a secret, a tiny field enumeration/order example, a two-character synthetic mapping, and invalid toy input rejection.

## Scope and limits

Only newly created toy inputs and small arithmetic cases were executed. The largest direct Pollard rho check used 91; no large-factorization experiment was run. The group enumeration check used a field modulo 7.

The original `Zhang.txt` input, original ciphertext or recovered messages, saved private-key records, and original notebook demonstrations were not executed or included. Existing historical notebook outputs were not reproduced.

Passing these checks supports the small demonstrated behavior and packaging. It does not establish correctness for every input, cryptographic security, constant-time execution, production readiness, or performance. The public-offset example is expressly nonconfidential.

No remote repository was created or uploaded as part of these local checks.
