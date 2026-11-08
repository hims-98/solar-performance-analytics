import unittest
import pandas as pd

from src.solar_analytics import analyse_daily_data, create_monthly_summary


class SolarAnalyticsTests(unittest.TestCase):
    def test_pr_and_cuf_calculation(self):
        data = pd.DataFrame({
            "date": ["2026-01-01"],
            "energy_kwh": [1800],
            "poa_kwh_m2": [5],
            "installed_capacity_kwp": [400],
        })
        result = analyse_daily_data(data)
        self.assertAlmostEqual(result.loc[0, "pr_pct"], 90.0)
        self.assertAlmostEqual(result.loc[0, "cuf_pct"], 18.75)

    def test_missing_column_is_rejected(self):
        data = pd.DataFrame({"date": ["2026-01-01"], "energy_kwh": [100]})
        with self.assertRaises(ValueError):
            analyse_daily_data(data)

    def test_monthly_summary(self):
        data = pd.DataFrame({
            "date": ["2026-01-01", "2026-01-02"],
            "energy_kwh": [1800, 1600],
            "poa_kwh_m2": [5, 4],
            "installed_capacity_kwp": [400, 400],
        })
        daily = analyse_daily_data(data)
        monthly = create_monthly_summary(daily)
        self.assertEqual(len(monthly), 1)
        self.assertEqual(monthly.loc[0, "days_reported"], 2)


if __name__ == "__main__":
    unittest.main()
