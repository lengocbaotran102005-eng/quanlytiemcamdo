import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://127.0.0.1:5000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin@123"
OUTPUT_DIR = Path("screenshots_admin")


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1600,900")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def wait_for(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def capture_login_page(driver):
    driver.get(f"{BASE_URL}/login")
    wait_for(driver, By.NAME, "username")
    capture(driver, "00_login")


def login_as_admin(driver):
    driver.get(f"{BASE_URL}/login")
    wait_for(driver, By.NAME, "username")
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    user_input.clear()
    user_input.send_keys(ADMIN_USERNAME)
    pass_input.clear()
    pass_input.send_keys(ADMIN_PASSWORD)
    pass_input.submit()
    wait_for(driver, By.TAG_NAME, "h1")


def capture(driver, name: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.png"
    time.sleep(1)
    driver.save_screenshot(str(path))
    print(f"Saved {path}")


def open_dashboard(driver):
    driver.get(f"{BASE_URL}/")
    wait_for(driver, By.TAG_NAME, "h1")
    capture(driver, "01_dashboard")


def open_transactions_list(driver):
    driver.get(f"{BASE_URL}/transactions")
    try:
        wait_for(driver, By.TAG_NAME, "table")
    except TimeoutException:
        print("Timeout waiting for transactions table, capturing current page.")
    capture(driver, "02_transactions_list")


def open_first_transaction_detail(driver):
    driver.get(f"{BASE_URL}/transactions")
    try:
        link = wait_for(driver, By.CSS_SELECTOR, "tbody tr td a")
        href = link.get_attribute("href") or ""
        tx_id = href.rstrip("/").split("/")[-1]
        link.click()
        wait_for(driver, By.TAG_NAME, "h1")
        capture(driver, "03_transaction_detail")
        return tx_id
    except Exception:
        print("No transaction to capture detail")
        return None


def open_customers_list_and_detail(driver):
    driver.get(f"{BASE_URL}/customers")
    try:
        wait_for(driver, By.TAG_NAME, "table")
    except TimeoutException:
        print("Timeout waiting for customers table, capturing current page.")
    capture(driver, "04_customers_list")
    try:
        link = wait_for(driver, By.CSS_SELECTOR, "tbody tr td a")
        link.click()
        wait_for(driver, By.TAG_NAME, "h1")
        capture(driver, "05_customer_detail")
    except Exception:
        print("No customer to capture detail")


def open_items_list(driver):
    driver.get(f"{BASE_URL}/items")
    try:
        wait_for(driver, By.TAG_NAME, "table")
    except TimeoutException:
        print("Timeout waiting for items table, capturing current page.")
    capture(driver, "06_items_list")


def open_reports(driver):
    driver.get(f"{BASE_URL}/reports")
    try:
        wait_for(driver, By.TAG_NAME, "canvas")
    except TimeoutException:
        print("Timeout waiting for reports chart, capturing current page.")
    capture(driver, "07_reports")


def open_users_list(driver):
    driver.get(f"{BASE_URL}/users")
    try:
        wait_for(driver, By.TAG_NAME, "table")
    except TimeoutException:
        print("Timeout waiting for users table, capturing current page.")
    capture(driver, "08_users_list")


def open_profile(driver):
    driver.get(f"{BASE_URL}/profile")
    try:
        wait_for(driver, By.TAG_NAME, "h1")
    except TimeoutException:
        print("Timeout waiting for profile header, capturing current page.")
    capture(driver, "09_profile")


def open_qr_interest(driver, tx_id: str):
    if not tx_id:
        return
    driver.get(f"{BASE_URL}/transactions/{tx_id}/interest/qr")
    try:
        wait_for(driver, By.TAG_NAME, "img")
    except TimeoutException:
        print("Timeout waiting for QR interest image, capturing current page.")
    capture(driver, "10_qr_interest")


def open_qr_redeem(driver, tx_id: str):
    if not tx_id:
        return
    driver.get(f"{BASE_URL}/transactions/{tx_id}/redeem/qr")
    try:
        wait_for(driver, By.TAG_NAME, "img")
    except TimeoutException:
        print("Timeout waiting for QR redeem image, capturing current page.")
    capture(driver, "11_qr_redeem")


def open_print_ticket(driver, tx_id: str):
    if not tx_id:
        return
    driver.get(f"{BASE_URL}/transactions/{tx_id}/print")
    try:
        wait_for(driver, By.TAG_NAME, "h1")
    except TimeoutException:
        print("Timeout waiting for print ticket page, capturing current page.")
    capture(driver, "12_print_ticket")


def open_print_redeem(driver, tx_id: str):
    if not tx_id:
        return
    driver.get(f"{BASE_URL}/transactions/{tx_id}/print-redeem")
    try:
        wait_for(driver, By.TAG_NAME, "h1")
    except TimeoutException:
        print("Timeout waiting for print redeem page, capturing current page.")
    capture(driver, "13_print_redeem")


def main():
    driver = create_driver()
    try:
        capture_login_page(driver)
        login_as_admin(driver)
        open_dashboard(driver)
        open_transactions_list(driver)
        tx_id = open_first_transaction_detail(driver)
        open_qr_interest(driver, tx_id)
        open_qr_redeem(driver, tx_id)
        open_print_ticket(driver, tx_id)
        open_print_redeem(driver, tx_id)
        open_customers_list_and_detail(driver)
        open_items_list(driver)
        open_reports(driver)
        open_users_list(driver)
        open_profile(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
