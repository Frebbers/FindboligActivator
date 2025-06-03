from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Setup Firefox WebDriver
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://findbolig.nu/da-dk/profile/my-waiting-lists")

# Wait for login if needed (you may need to handle login manually)
input("Please login if needed, then press Enter to continue...")

# Process all "Meld mig aktiv" buttons one by one
button_count = 0
while True:
    try:
        # Find the first "Meld mig aktiv" button
        active_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Meld mig aktiv')]"))
        )

        button_count += 1
        print(f"Clicking 'Meld mig aktiv' button #{button_count}")

        # Scroll button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", active_button)
        time.sleep(1)  # Wait for scroll to complete

        # Click the "Meld mig aktiv" button
        active_button.click()

        # Wait for and click the confirmation popup
        try:
            ja_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".o-button--inverted"))
            )
            print("Clicking 'Ja' button to confirm")
            ja_button.click()

            print(f"Successfully activated item #{button_count}")

            # Wait for page to refresh/update
            time.sleep(3)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Could not find confirmation button: {e}")

    except (TimeoutException, NoSuchElementException):
        print("No more 'Meld mig aktiv' buttons found. Process completed.")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

print(f"Process completed. Successfully signed up for {button_count} listings.")

# Keep the browser open for inspection
input("Press Enter to close the browser...")
driver.quit()
