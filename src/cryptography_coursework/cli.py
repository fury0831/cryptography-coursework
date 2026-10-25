"""Bounded, newly created numeric demos for the coursework modules."""

import argparse
import json
from pathlib import Path


def integer(value, label, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be an integer in [{minimum}, {maximum}].")
    return value


def read_input(path, keys):
    if path.stat().st_size > 4096:
        raise ValueError("Only small numeric example files are accepted.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != set(keys):
        raise ValueError("Example fields must be exactly: " + ", ".join(keys))
    return data


def rsa_demo(data):
    p = integer(data["p"], "p", 3, 10000)
    q = integer(data["q"], "q", 3, 10000)
    if p == q:
        raise ValueError("This exercise requires two distinct primes.")
    from . import rsa as course
    if course.smallest_prime_factor(p) != p or course.smallest_prime_factor(q) != q:
        raise ValueError("Both toy factors must be prime.")
    modulus = p * q
    phi = (p - 1) * (q - 1)
    exponent = integer(data["e"], "e", 2, phi - 1)
    message = integer(data["message_integer"], "message_integer", 0, modulus - 1)
    if course.gcd(exponent, phi) != 1:
        raise ValueError("The public exponent must be coprime to phi.")
    cipher = course.fme(message, exponent, modulus)
    found_p, found_q = course.factor_n(modulus)
    private_exponent = course.compute_d(found_p, found_q, exponent)
    if private_exponent is None:
        raise ValueError("The toy private exponent could not be computed.")
    recovered = course.fme(cipher, private_exponent, modulus)
    return {
        "study": "RSA numeric teaching example",
        "source": "new toy input; no original course message",
        "modulus": modulus,
        "public_exponent": exponent,
        "message_integer": message,
        "generated_cipher_integer": cipher,
        "recovered_factors": [found_p, found_q],
        "recovered_integer": recovered,
        "round_trip_equal": recovered == message,
        "security_claim": "none",
    }


def ecc_offset_demo(data):
    prime = integer(data["p"], "p", 5, 10000)
    a = integer(data["a"], "a", 0, prime - 1)
    b = integer(data["b"], "b", 0, prime - 1)
    values = data["message_point"]
    if not isinstance(values, list) or len(values) != 2:
        raise ValueError("message_point must contain two integer coordinates.")
    point = tuple(integer(v, "point coordinate", 0, prime - 1) for v in values)
    scalar = integer(data["public_offset_scalar"], "public_offset_scalar", 1, 100)
    from . import ecc as course
    if not course.check_curve(a, b, prime):
        raise ValueError("Invalid teaching curve parameters.")
    if not course.is_on_curve(point, a, b, prime):
        raise ValueError("The toy message point is not on the curve.")
    public_offset = course.scalar_mult(scalar, point, a, prime)
    if public_offset is None:
        raise ValueError("Choose a toy offset that is not the identity.")
    cipher_point = course.point_add(point, public_offset, a, prime)
    recovered = course.point_add(cipher_point, course.point_neg(public_offset, prime), a, prime)
    return {
        "study": "Public elliptic-curve offset counterexample",
        "source": "new toy input; no original message or ciphertext",
        "curve": {"a": a, "b": b, "p": prime},
        "message_point": point,
        "public_offset": public_offset,
        "transformed_point": cipher_point,
        "recovered_without_secret": recovered,
        "round_trip_equal": recovered == point,
        "security_claim": "none: a public offset provides no confidentiality",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Small numeric coursework demonstrations; not secure cryptographic products.")
    parser.add_argument("study", choices=("rsa", "ecc-offset"))
    parser.add_argument("--input", type=Path, required=True, help="A newly created toy JSON input.")
    args = parser.parse_args(argv)
    try:
        if args.study == "rsa":
            data = read_input(args.input, ("p", "q", "e", "message_integer"))
            result = rsa_demo(data)
        else:
            data = read_input(args.input, ("a", "b", "p", "message_point", "public_offset_scalar"))
            result = ecc_offset_demo(data)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0
