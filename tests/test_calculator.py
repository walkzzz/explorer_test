import pytest
import allure


@allure.feature("数学运算")
@allure.story("四则运算")
class TestCalculator:
    """四则运算测试"""

    @allure.title("测试加法运算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_addition(self):
        """验证加法运算结果正确"""
        with allure.step("执行加法运算"):
            result = 1 + 1
        
        with allure.step("验证结果"):
            assert result == 2

    @allure.title("测试减法运算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_subtraction(self):
        """验证减法运算结果正确"""
        with allure.step("执行减法运算"):
            result = 5 - 2
        
        with allure.step("验证结果"):
            assert result == 3

    @allure.title("测试乘法运算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiplication(self):
        """验证乘法运算结果正确"""
        with allure.step("执行乘法运算"):
            result = 3 * 4
        
        with allure.step("验证结果"):
            assert result == 12

    @allure.title("测试除法运算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_division(self):
        """验证除法运算结果正确"""
        with allure.step("执行除法运算"):
            result = 10 / 2
        
        with allure.step("验证结果"):
            assert result == 5

    @allure.title("测试除法运算（小数结果）")
    @allure.severity(allure.severity_level.MINOR)
    def test_division_decimal(self):
        """验证除法运算小数结果正确"""
        with allure.step("执行除法运算"):
            result = 7 / 3
        
        with allure.step("验证结果"):
            assert abs(result - 2.3333333333333335) < 0.0000000001

    @allure.title("测试四则混合运算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mixed_operations(self):
        """验证四则混合运算结果正确"""
        with allure.step("执行混合运算"):
            result = (1 + 2) * 3 - 4 / 2
        
        with allure.step("验证结果"):
            assert result == 7
