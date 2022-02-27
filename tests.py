import unittest
import SubnetMaker
from SubnetMaker import IncorectDataError
def broken_function():
    raise Exception('This is broken')
class MyTestCase(unittest.TestCase):
    def test_get_correct_data(self):
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/wronglastoctet.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/wrong3octet.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/wrong2octet.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/wrongFirstoctet.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/wrongNnumber.txt')

    def test_not_2_string_intxt(self):
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/3_lines_ends_with_slash_n.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/more_than_2_lines.txt')
        with self.assertRaises(IncorectDataError):
            SubnetMaker.get_valid_data('TestData/testInTxt/less_than_2_lines.txt')

    def test_autogen_not_finded(self):
        # Not finded -> return 0.0.0.0/0
        self.assertEqual(SubnetMaker.get_min_subnet('1.2.3.4', 'TestData/testOuttxt/case1.txt'), '0.0.0.0/0')
    def test_autogen_cases(self):
        self.assertEqual(SubnetMaker.get_min_subnet('100.100.100.100', 'TestData/testOuttxt/case2.txt'), '0.0.0.0/1')
        self.assertEqual(SubnetMaker.get_min_subnet('193.0.0.3', 'TestData/testOuttxt/case3.txt'), '192.0.0.0/2')
        self.assertEqual(SubnetMaker.get_min_subnet('200.0.128.3', 'TestData/testOuttxt/case4.txt'), '192.0.0.0/3')
        self.assertEqual(SubnetMaker.get_min_subnet('255.255.255.254', 'TestData/testOuttxt/case5.txt'), '240.0.0.0/4')



if __name__ == '__main__':
    unittest.main()
