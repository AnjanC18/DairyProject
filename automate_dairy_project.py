from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Setup driver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Test Data
vendor_name = f"Vendor_{random.randint(1000, 9999)}"
vendor_contact = f"{random.randint(6000000000, 9999999999)}"
milk_price_update = "57.0"
milk_type = "Cow"
quantity = "10"
latest_bill_no = None  # We'll set this after bill is generated

def login():
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    print("✅ Logged in")

def add_vendor():
    driver.get("http://127.0.0.1:5000/vendor_details")
    driver.find_element(By.NAME, "name").send_keys(vendor_name)
    driver.find_element(By.NAME, "contact").send_keys(vendor_contact)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    print(f"✅ Vendor added: {vendor_name} / {vendor_contact}")

def update_milk_price():
    driver.get("http://127.0.0.1:5000/milk_details")
    time.sleep(1)

    try:
        rows = driver.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            if "Cow" in row.text:
                milk_id = row.find_element(By.TAG_NAME, "td").text.strip()

                # Click "Edit"
                edit_btn = driver.find_element(By.ID, f"edit-{milk_id}")
                edit_btn.click()
                time.sleep(0.5)

                # Update price
                price_input = driver.find_element(By.ID, f"price-{milk_id}")
                price_input.clear()
                price_input.send_keys(milk_price_update)

                # Click "Save"
                save_btn = driver.find_element(By.ID, f"save-{milk_id}")
                save_btn.click()
                time.sleep(1)

                print("✅ Milk price updated")
                return
        print("❌ Cow milk row not found")
    except Exception as e:
        print("❌ Failed to update milk price:", e)

def generate_bill():
    global latest_bill_no

    driver.get("http://127.0.0.1:5000/bill")
    driver.find_element(By.NAME, "vendor_id").send_keys("1")  # Update if needed
    driver.find_element(By.NAME, "milk_type").send_keys(milk_type)
    driver.find_element(By.NAME, "quantity").send_keys(quantity)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    # Try to extract bill number from flash message
    try:
        flash_divs = driver.find_elements(By.CLASS_NAME, "alert")
        for div in flash_divs:
            if "Bill" in div.text and "generated" in div.text:
                parts = div.text.split()
                for word in parts:
                    if word.startswith("BILL"):
                        latest_bill_no = word
                        break
        print(f"✅ Bill generated: {latest_bill_no}")
    except:
        print("✅ Bill generated (bill number not extracted)")

def generate_pdf():
    if not latest_bill_no:
        print("⚠️ Cannot generate PDF: Bill number not available")
        return

    driver.get("http://127.0.0.1:5000/bill_details")
    bill_input = driver.find_element(By.NAME, "bill_no")

    bill_input.clear()
    bill_input.send_keys(latest_bill_no)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    # Trigger PDF generation
    driver.find_element(By.NAME, "bill_no").send_keys(latest_bill_no)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    print("✅ PDF generated (check D:\\Vs)")

def logout():
    try:
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)
        if "login" in driver.current_url or "Login" in driver.page_source:
            print("✅ Logged out successfully")
        else:
            print("⚠️ Logout redirect failed")
    except Exception as e:
        print("❌ Logout failed:", e)

def run_all():
    try:
        login()
        add_vendor()
        update_milk_price()
        generate_bill()
        generate_pdf()
        logout()
        print("✅ Full flow executed")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_all()
