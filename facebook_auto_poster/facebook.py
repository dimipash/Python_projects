from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def login_to_facebook(driver, email, password):
    driver.get("https://facebook.com")

    email_element = driver.find_element(By.ID, "email")
    email_element.send_keys(email)

    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()


def post_status(driver, status_message):
    try:
        # Wait for the status input field to be clickable
        status_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Create a post']"))
        )
        status_element.click()

        # Wait for the status text area to be visible and send the message
        status_text_area = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        status_text_area.send_keys(status_message)

        # Find and click the Post button
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Post']"))
        )
        post_button.click()

        print("Status posted successfully!")
    except TimeoutException:
        print("Timed out waiting for element to be available")


def main():
    email = "your_email@example.com"
    password = "your_password"
    status_message = "Hello, World!"

    driver = webdriver.Firefox()
    try:
        login_to_facebook(driver, email, password)
        post_status(driver, status_message)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
