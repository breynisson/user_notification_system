# user_notification_system/report_generator.py

import subprocess
import sys

def generate_allure_report():
    """
    Use Allure CLI to generate the HTML report from the results.
    """
    cmd = ["allure", "generate", "reports/allure-results", "-o", "reports/allure-report", "--clean"]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
