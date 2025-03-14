import unittest

from garminworkouts.models.power import Power


class PowerTestCase(unittest.TestCase):
    def test_valid_power_to_watts_conversion(self) -> None:
        ftp = 200
        valid_powers: list = [
            ("0", 0),
            ("0%", 0),
            ("0.10", 20),
            ("10%", 20),
            ("100%", 200),
            ("120%", 240),
            ("150%", 300),
            ("0W", 0),
            ("0w", 0),
            ("100W", 100),
            ("100w", 100),
            ("1000W", 1000),
            ("1000w", 1000)
        ]

        for power, watts in valid_powers:
            with self.subTest(msg="Expected %d watts for '%s' (ftp=%s)" % (watts, power, ftp)):
                self.assertEqual(Power(power).to_watts(ftp), watts)

    def test_invalid_power_to_watts_conversion(self) -> None:
        ftp = 200
        invalid_powers: list[str] = ["-1", "-1%", "2500", "2500%", "-1W", "5000W", "foo", "foo%", "fooW"]

        for power in invalid_powers:
            with self.subTest(msg="Expected ValueError for '%s" % power):
                with self.assertRaises(ValueError):
                    Power(power).to_watts(ftp)

    def test_power_to_watts_conversion_with_invalid_ftp(self) -> None:
        power = "100"
        invalid_ftps = [-1, 1000, "foo"]
        for ftp in invalid_ftps:
            with self.subTest(msg="Expected ValueError for '%s" % ftp):
                with self.assertRaises(ValueError):
                    Power(power).to_watts(ftp)

    def test_power_zones(self):
        rftp = Power("200W")
        cftp = Power("250W")
        zones, rpower_zones, cpower_zones, data = Power.power_zones(rftp, cftp)
        self.assertEqual(zones, [0.65, 0.8, 0.9, 1.0, 1.15, 1.3, 1.5, 1.7, 2.0])
        self.assertEqual(rpower_zones, [130, 160, 180, 200, 229, 260, 300, 340, 400])
        self.assertEqual(cpower_zones, [162, 200, 225, 250, 287, 325, 375, 425, 500])
        self.assertEqual(len(data), 2)
