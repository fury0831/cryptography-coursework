"""Small independent arithmetic checks; never reads original coursework inputs."""

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cryptography_coursework import cli, ecc, rsa


class RSAToyChecks(unittest.TestCase):
    def test_modular_power_matches_builtin(self):
        for value in (0, 1, 42, 186):
            for exponent in (0, 1, 7, 23):
                with self.subTest(value=value, exponent=exponent):
                    self.assertEqual(rsa.fme(value, exponent, 187), pow(value, exponent, 187))

    def test_modular_inverse_and_missing_inverse(self):
        self.assertEqual((7 * rsa.mod_inverse(7, 160)) % 160, 1)
        self.assertIsNone(rsa.mod_inverse(2, 160))

    def test_small_factorization_methods(self):
        self.assertEqual(rsa.factor_n(187), (11, 17))
        factor = rsa.pollard_rho_factor(91)
        self.assertGreater(factor, 1)
        self.assertLess(factor, 91)
        self.assertEqual(91 % factor, 0)

    def test_new_numeric_record_and_recovery(self):
        cipher = pow(42, 7, 187)
        record = rsa.read_one_record(f"(187, 7, [{cipher}])")
        self.assertEqual(record, [187, 7, [cipher]])
        p, q, private_exponent, recovered = rsa.decrypt_rsa_message(*record)
        self.assertEqual(p * q, 187)
        self.assertEqual((7 * private_exponent) % 160, 1)
        self.assertEqual(recovered, chr(42))

    def test_wrapper_rejects_invalid_toy_inputs(self):
        for changes in ({"p": True}, {"q": 11}, {"p": 9}, {"e": 2}, {"message_integer": 187}):
            data = {"p": 11, "q": 17, "e": 7, "message_integer": 42}
            data.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                cli.rsa_demo(data)


class ECCToyChecks(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.p = 2, 3, 103
        self.point = (2, 18)

    def test_identity_inverse_and_zero(self):
        self.assertTrue(ecc.is_on_curve(self.point, self.a, self.b, self.p))
        self.assertEqual(ecc.point_add(None, self.point, self.a, self.p), self.point)
        self.assertIsNone(ecc.point_add(self.point, ecc.point_neg(self.point, self.p), self.a, self.p))
        self.assertIsNone(ecc.scalar_mult(0, self.point, self.a, self.p))

    def test_scalar_multiplication_and_closure(self):
        twice = ecc.point_add(self.point, self.point, self.a, self.p)
        self.assertEqual(ecc.scalar_mult(2, self.point, self.a, self.p), twice)
        self.assertEqual(ecc.scalar_mult(-1, self.point, self.a, self.p), ecc.point_neg(self.point, self.p))
        self.assertTrue(ecc.is_on_curve(twice, self.a, self.b, self.p))

    def test_public_offset_recovered_without_secret(self):
        offset = ecc.scalar_mult(3, self.point, self.a, self.p)
        cipher = ecc.point_add(self.point, offset, self.a, self.p)
        recovered = ecc.point_add(cipher, ecc.point_neg(offset, self.p), self.a, self.p)
        self.assertEqual(recovered, self.point)

    def test_small_root_enumeration_and_order(self):
        self.assertEqual(set(ecc.square_roots_mod_prime(2, 7)), {3, 4})
        self.assertEqual(ecc.square_roots_mod_prime(0, 7), [0])
        points = ecc.find_points_by_roots(2, 3, 7)
        group_size = ecc.count_curve_points_by_roots(2, 3, 7)
        self.assertEqual(group_size, len(points) + 1)
        order = ecc.point_order_from_group_order((3, 6), 2, 7, group_size, ecc.factor_number(group_size))
        self.assertEqual(group_size % order, 0)
        self.assertIsNone(ecc.scalar_mult(order, (3, 6), 2, 7))

    def test_small_character_mapping(self):
        points = ecc.message_to_points("BA", "AB", 1, self.point, self.a, self.p)
        self.assertEqual(ecc.points_to_message(points, "AB", 1, self.point, self.a, self.p), "BA")

    def test_wrapper_rejects_invalid_point(self):
        with self.assertRaises(ValueError):
            cli.ecc_offset_demo({"a": 2, "b": 3, "p": 103, "message_point": [2, 19], "public_offset_scalar": 3})


class CLIToyChecks(unittest.TestCase):
    def test_both_examples_run_without_external_inputs(self):
        for study, filename in (("rsa", "rsa_toy.json"), ("ecc-offset", "ecc_offset_toy.json")):
            with self.subTest(study=study):
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / "run_demo.py"), study, "--input", str(ROOT / "examples" / filename)],
                    check=True, capture_output=True, text=True, timeout=10, env=env,
                )
                data = json.loads(result.stdout)
                self.assertTrue(data["round_trip_equal"])
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
