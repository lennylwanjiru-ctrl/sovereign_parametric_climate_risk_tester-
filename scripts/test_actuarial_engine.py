import os
import unittest
import pandas as pd

class TestActuarialSolvencyEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up diagnostic connection paths before running tests."""
        self.metrics_path = 'data/stochastic_solvency_metrics.csv'
        self.data_available = os.path.exists(self.metrics_path)
        if self.data_available:
            self.df = pd.read_csv(self.metrics_path).set_index('metric_name')

    def test_metrics_file_exists(self):
        """Test 1: Verify the simulation script outputted the metrics ledger."""
        self.assertTrue(self.data_available, "❌ Error: stochastic_solvency_metrics.csv is missing!")

    def test_depletion_probability_bounds(self):
        """Test 2: Ensure the simulated fund depletion probability falls within logical 0-100% limits."""
        if self.data_available:
            prob = self.df.loc['FUND_DEPLETION_PCT', 'metric_value']
            self.assertTrue(0.0 <= prob <= 100.0, f"❌ Actuarial Error: Probability bounds ruptured ({prob}%)!")

    def test_var_tvar_relationship(self):
        """Test 3: Mathematically verify that TVaR is equal to or greater than VaR (Tail Coherence)."""
        if self.data_available:
            var_val = self.df.loc['VAR_99_USD', 'metric_value']
            tvar_val = self.df.loc['TVAR_99_USD', 'metric_value']
            self.assertTrue(tvar_val >= var_val, f"❌ Actuarial Error: Incoherent tail risk metric (TVaR {tvar_val} < VaR {var_val})!")

if __name__ == '__main__':
    print("\n🧪 Running Automated Actuarial Integration Unit Tests...")
    unittest.main()