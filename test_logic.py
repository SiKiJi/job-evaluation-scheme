import unittest
from logic import calculate_total_points, determine_grade
from data_models import FACTOR_SCORES_MSS

class TestJobEvaluation(unittest.TestCase):
    def test_scores_structure(self):
        """Verify the data model structure matches the table."""
        self.assertEqual(FACTOR_SCORES_MSS["Education"][1], 11)
        self.assertEqual(FACTOR_SCORES_MSS["Education"][5], 110)
        self.assertEqual(FACTOR_SCORES_MSS["Experience"][1], 12)
        
    def test_grading_operatives(self):
        """Test grading ranges for Operatives based on user text."""
        # Job Grade O 01 – 230 or lower
        self.assertEqual(determine_grade(153.25, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 01")
        self.assertEqual(determine_grade(230, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 01")
        
        # Job Grade O 02 – from 231 to 307
        self.assertEqual(determine_grade(231, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 02")
        self.assertEqual(determine_grade(306.55, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 02") # Boundary check
        
        # Job Grade O 03 – from 308 to 385
        self.assertEqual(determine_grade(310, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 03")
        
        # Job Grade O 04 – from 386 to 462
        self.assertEqual(determine_grade(400, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 04")
        
        # Job Grade O 05 – 463 upwards
        self.assertEqual(determine_grade(508.75, "Operatives", "Managerial/Supervisory/Specialist (MSS)"), "O 05")

    def test_grading_admin(self):
        """Test grading ranges for Administrators based on user text."""
        # Job Grade MS 01 – 319 or lower
        self.assertEqual(determine_grade(237.25, "Administrator", "Managerial/Supervisory/Specialist (MSS)"), "MS 01")
        
        # Job Grade MS 02 – from 320 to 401
        self.assertEqual(determine_grade(334.00, "Administrator", "Managerial/Supervisory/Specialist (MSS)"), "MS 02")
        
        # Job Grade MS 03 – 402 upwards
        self.assertEqual(determine_grade(432.55, "Administrator", "Managerial/Supervisory/Specialist (MSS)"), "MS 03")
        self.assertEqual(determine_grade(482.95, "Administrator", "Managerial/Supervisory/Specialist (MSS)"), "MS 03")

    def test_calculation_registrar_example(self):
        """
        Attempt to reconstruct 'Registrar' (237.25) or similar.
        Note: The manual tables only show integers. 
        The prompt examples have decimals.
        This test checks if the INTEGER logic holds for integer inputs.
        """
        # Minimum possible score (Level 1 for all)
        # 11+12+14+10+7+8+6+7+25+11+5 = 116
        min_score = sum([f[1] for f in FACTOR_SCORES_MSS.values()])
        self.assertEqual(calculate_total_points({k: v[1] for k, v in FACTOR_SCORES_MSS.items()}), 116)
        
        # Max score (Level 5/6/3)
        # Education 5 (110) + Exp 5 (120) + Comp 5 (140) + Err 5 (100) + Rel 3 (70) + Line 5 (80) + Scope 6 (60) + Conf 5 (70) + Contact 5 (90) + Ing 5 (110) + Work 3 (50)
        # Sum = 1000? Let's check maxes.
        max_score = 0
        for f, levels in FACTOR_SCORES_MSS.items():
            max_level = max(levels.keys())
            max_score += levels[max_level]
        
        # Expected max based on manual addition:
        # 110+120+140+100+70+80+60+70+90+110+50 = 1000
        self.assertEqual(max_score, 1000)

if __name__ == '__main__':
    unittest.main()
