import re


def extract_salaries(salary_str):
    # 正则表达式模式，匹配薪资范围中的两个整数
    pattern = r'(\d+)-(\d+)K'
    try:
        match = re.search(pattern, salary_str)
        if match:
            # 提取匹配到的两个整数
            min_salary, max_salary = map(int, match.groups())
            return min_salary, max_salary
    except Exception as e:
        print(e)

    return None, None


def is_salary_valid(min_salary, max_salary):
    if min_salary is None or max_salary is None:
        return False
    # 判断第一个数是否大于 10，第二个数是否大于等于 18
    return min_salary >= 8 and max_salary >= 15
