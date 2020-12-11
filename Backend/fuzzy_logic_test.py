import unittest
from suchfunktion import fuzzy_logic


class MyTestCase(unittest.TestCase):
    def test_fuzzy_logic_found(self):
        """
        Test fuzzy_logic found
        """
        corpus = [
            ['The', 'competition', 'concerns', 'the', 'delivery', 'of', 'asphalt', 'works', 'on', 'municipal', 'roads', 'streets', 'foot', 'and', 'cycle', 'paths', 'pavements', 'squares', 'parking', 'places', 'some', 'private', 'roads', 'and', 'any', 'selected', 'new', 'installations', 'that', 'are', 'operated', 'and', 'maintained', 'by', 'the', 'individual', 'municipalities', 'The', 'annual', 'value', 'of', 'the', 'procurement', 'is', 'estimated', 'to', 'be', 'NOK', 'excluding', 'VAT', 'per', 'year', 'The', 'value', 'is', 'an', 'estimate', 'and', 'thus', 'not', 'binding', 'See', 'the', 'tender', 'documentation', 'for', 'further', 'information',
'The', 'establishment', 'of', 'a', 'provisional', 'cable', 'installations', 'at', 'Mosseporten', 'transformation', 'station',
'Construction', 'of', 'a', 'power', 'line', 'route', 'in', 'Moss',
'Building', 'and', 'ground', 'work', 'in', 'Mosseporten', 'transformer', 'station',
'The', 'contract', 'includes', 'all', 'work', 'that', 'needs', 'to', 'be', 'carried', 'out', 'with', 'an', 'excavator', 'or', 'similar', 'machinery', 'and', 'associated', 'necessary', 'works', 'in', 'connection', 'with', 'archaeological', 'records', 'surveys', 'and', 'excavations'
]
            ]

        substring = 'compatition'
        expected = 'competition'
        self.assertEqual(expected, fuzzy_logic(substring, corpus))

    def test_fuzzy_logic_notfound(self):
        """
        Test fuzzy_logic not found
        """
        corpus = [
            ['The', 'competition', 'concerns', 'the', 'delivery', 'of', 'asphalt', 'works', 'on', 'municipal', 'roads', 'streets', 'foot', 'and', 'cycle', 'paths', 'pavements', 'squares', 'parking', 'places', 'some', 'private', 'roads', 'and', 'any', 'selected', 'new', 'installations', 'that', 'are', 'operated', 'and', 'maintained', 'by', 'the', 'individual', 'municipalities', 'The', 'annual', 'value', 'of', 'the', 'procurement', 'is', 'estimated', 'to', 'be', 'NOK', 'excluding', 'VAT', 'per', 'year', 'The', 'value', 'is', 'an', 'estimate', 'and', 'thus', 'not', 'binding', 'See', 'the', 'tender', 'documentation', 'for', 'further', 'information',
'The', 'establishment', 'of', 'a', 'provisional', 'cable', 'installations', 'at', 'Mosseporten', 'transformation', 'station',
'Construction', 'of', 'a', 'power', 'line', 'route', 'in', 'Moss',
'Building', 'and', 'ground', 'work', 'in', 'Mosseporten', 'transformer', 'station',
'The', 'contract', 'includes', 'all', 'work', 'that', 'needs', 'to', 'be', 'carried', 'out', 'with', 'an', 'excavator', 'or', 'similar', 'machinery', 'and', 'associated', 'necessary', 'works', 'in', 'connection', 'with', 'archaeological', 'records', 'surveys', 'and', 'excavations'
             ]
        ]
        substring = 'idee'
        expected = ' '
        self.assertEqual(expected, fuzzy_logic(substring, corpus))

    def test_fuzzy_logic_empty(self):
        """
        Test fuzzy_logic empty
        """
        corpus = []
        substring = 'idee'
        expected = ' '
        self.assertEqual(expected, fuzzy_logic(substring, corpus))


if __name__ == '__main__':
    unittest.main()