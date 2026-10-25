# Provenance and exclusions

`source-map.json` records the filenames, SHA-256 hashes and zero-based notebook cell indices of the two primary source notebooks. The hashes identify the reviewed versions without publishing notebook content or private filesystem paths.

The local primary notebooks matched their supplied attachment counterparts byte-for-byte. Function definitions were extracted in full; original module-level inputs, notebook execution cells and saved outputs were excluded. All 38 extracted function ASTs were compared with the source versions and match.

The original RSA input was found after the initial attachment-only review. Safe static parsing found three records of the expected tuple structure, and each modulus matched the product of its corresponding saved factors. That check did not decrypt a message. The original input is deliberately absent here; the runnable examples use new numeric configurations instead.

Related notebooks explored real/finite-field curve arithmetic, group orders and an ElGamal-style decryption formula. The ElGamal-style draft had no saved executions, depended on inputs not defined within the same notebook, and included no encryption or random-k implementation. It is excluded rather than represented as a tested implementation.

Excluded from this release:

- Original course input files, original ciphertext, recovered messages and stored private exponents/keys.
- Complete notebooks and notebook outputs.
- Course questions, reference PDFs, textbook extracts, schedules and unrelated material.
- The incomplete ElGamal-style draft and its separate scratch input area.
- Private absolute paths and downloaded attachment metadata.

See `../ATTRIBUTION.md` for the exact “Starter algorithms” heading, local ECC method reference, external algorithm links and release authorization context. See `../VALIDATION.md` for the limited checks actually run.
