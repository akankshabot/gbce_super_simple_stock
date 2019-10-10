import unittest
import mystock as sm

class StockMarketTests(unittest.TestCase):

    def test_calculate_dividend(self):
        result = sm.StockMarket().calculate_dividend('POP',10)
        self.assertEqual(result,0.8)

    def test_calculate_pe_ration(self):
        result = sm.StockMarket().calculate_pe_ration('GIN',10)
        self.assertEqual(result,50.0)

    def test_add_record(self):
        result = sm.StockMarket().add_record('GIN', 22, True)
        self.assertEqual(result,None)

if __name__ == '__main__': 
    unittest.main() 