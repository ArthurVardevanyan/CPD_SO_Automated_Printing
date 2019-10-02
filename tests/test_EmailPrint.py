import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import EmailPrint


class Testing(unittest.TestCase):
    def test_Email_Printer(self):
        self.assertTrue(EmailPrint.Email_Printer("tests/SO", "11344-2704 First Last - Test 1", ""))
        self.assertTrue(EmailPrint.Email_Printer("tests/SO", "11345-3704 First Last - Test 2", ""))

    def test_Email_Print(self):
        self.assertTrue(EmailPrint.Email_Print("tests/SO",
                                      "11344-2704 First Last - Test 1", "False", [], "stacker"))
        self.assertTrue(EmailPrint.Email_Print("tests/SO",
                                      "11345-3704 First Last - Test 2", "False", [], "stacker"))

    def test_Email_Html(self):
        self.assertTrue(EmailPrint.Email_Html(
            "11344-2704 First Last - Test 1",
            "tests/SO/11344-2704 First Last - Test 1", 
            '<b>Bill To: First Last</b><br>11344-2704 First Last - Test 1<br>',
            ["File 1: -2704.01 Test File.pdf', 'Page Count': '9'"]))
        self.assertTrue(EmailPrint.Email_Html(
            "11345-3704 First Last - Test 2",
            "tests/SO/11345-3704 First Last - Test 2", 
            '<b>Bill To: First Last</b><br>11345-3704 First Last - Test 2<br>',
            ["File 1: -3704.01 Test File.pdf', 'Page Count': '9'"]))



if __name__ == '__main__':
    unittest.main()
