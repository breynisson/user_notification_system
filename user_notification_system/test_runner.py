# user_notification_system/test_runner.py

import subprocess
import sys

def run_tests_allure():
    """
    Run pytest with Allure output.
    """
    cmd = ["pytest", "-v", "--alluredir=reports/allure-results"]
    # Use subprocess to call pytest within this function.
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
