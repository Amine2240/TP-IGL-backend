from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCreateDPI:
    def __init__(self, driver_path, app_url, data):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.app_url = app_url
        self.data = data

    def open_application(self):
        """Open the Angular application."""
        self.driver.get(self.app_url)

    def fill_patient_form(self):
        """Fill out the patient details form."""
        patient = self.data["patient"]["user"]
        self.driver.find_element(By.ID, 'nom').send_keys(patient["nom"])
        self.driver.find_element(By.ID, 'prenom').send_keys(patient["prenom"])
        self.driver.find_element(By.ID, 'dateNaissance').send_keys(patient["date_naissance"])
        self.driver.find_element(By.ID, 'telephone').send_keys(patient["telephone"])
        self.driver.find_element(By.ID, 'email').send_keys(patient["email"])
        #self.driver.find_element(By.ID, 'role').send_keys(patient["role"])
        self.driver.find_element(By.ID, 'NSS').send_keys(str(self.data["patient"]["NSS"]))
        

    def fill_contact_urgence_form(self):
        """Fill out the emergency contact details form."""
        contact = self.data["contact_urgence"]
        self.driver.find_element(By.ID, 'contact_nom').send_keys(contact["nom"])
        self.driver.find_element(By.ID, 'contact_prenom').send_keys(contact["prenom"])
        self.driver.find_element(By.ID, 'contact_telephone').send_keys(contact["telephone"])
        self.driver.find_element(By.ID, 'contact_email').send_keys(contact["email"])

    def fill_mutuelle(self):
        self.driver.find_element(By.ID, 'mutuelle').send_keys(self.data.get("mutuelle").get("nom"))
        self.driver.find_element(By.ID, 'mutuelleID').send_keys(self.data.get("mutuelle").get("id"))

    def fill_antecedants(self):
        """Fill out antecedants."""
        for antecedant in self.data["antecedants"]:
            self.driver.find_element(By.ID, 'antecedant_nom').send_keys(antecedant["nom"])
            self.driver.find_element(By.ID, 'antecedant_type').send_keys(antecedant["type"])
            self.driver.find_element(By.ID, 'add_antecedant').click()
      
            
    def select_image(self):
        """Select the image to upload."""
        self.driver.find_element(By.ID, 'imageInput').send_keys(self.data["image_path"])

    def select_checkboxes(self, checkbox_list, field_name):
        """Select multiple checkboxes."""
        for checkbox in checkbox_list:
            checkbox_elem = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field_name}'][value='{checkbox}']")
            if not checkbox_elem.is_selected():
                checkbox_elem.click()


    def submit_form(self):
        """Submit the form."""
        self.driver.find_element(By.ID, 'submit').click()

    def wait_for_success(self):
        """Wait for the success message to appear."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'success_message'))
        )
        print("Test Passed: DPI created successfully!")
    def upload_image(self):
        """Upload the image."""
        self.driver.find_element(By.ID, 'imageInput').send_keys(self.data["image_path"])
    def select_radio(self, field_name, value):
        """Select a radio button based on value."""
        radio_button = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field_name}'][value='{value}']")
        radio_button.click()
    def run_test(self):
        """Run the entire test."""
        try:
            self.open_application()
            self.fill_patient_form()
            self.fill_contact_urgence_form()
            self.fill_mutuelle()
            self.fill_antecedants()
            self.submit_form()
            self.wait_for_success()
        except Exception as e:
            print(f"Test Failed: {e}")
        finally:
            self.driver.quit()

# Test Data
test_data = {
    "patient": {
        "user": {
            "nom": "Doe",
            "prenom": "John",
            "date_naissance": "1980-05-15",
            "telephone": "0221237890",
            "email": "john.doe@example.com",
            "role": "patient"
        },
        "NSS": 45
    },
    "contact_urgence": {
        "nom": "Smith",
        "prenom": "Jane",
        "telephone": "0221237810",
        "email": "jane.smith@example.com"
    },
    "hopital_initial_id": 1,
    "mutuelle": {
        "nom":"Health Mutual",
        "id": 123
        },
    "antecedants": [
        {"nom": "Doe", "type": "Type A"},
        {"nom": "Doe", "type": "Type B"}
    ]
}

# Run the test
if __name__ == "__main__":
    #adjust the path to the chromedriver executable
    test = TestCreateDPI(driver_path='C:\chromedriver\chromedriver-win64', app_url='http://localhost:4200', data=test_data)
    test.run_test()
