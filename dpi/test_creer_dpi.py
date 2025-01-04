from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

class TestCreateDPI:
    def __init__(self, driver_path, app_url, data):
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service,
                                       keep_alive=True)
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
        self.driver.find_element(By.ID, 'mutuelleId').send_keys(self.data.get("mutuelle").get("id"))
             
    def select_image(self , image_path):
        """Select the image to upload."""
        self.driver.find_element(By.ID, 'imageInput').send_keys(image_path)

    def select_checkboxes(self, checkbox_list, field_name):
        """Select multiple checkboxes."""
        for checkbox in checkbox_list:
            checkbox_value = checkbox.get("nom")
            checkbox_elem = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field_name}'][id='{checkbox_value}']")
            self.driver.execute_script("arguments[0].click();", checkbox_elem)


    def submit_form(self):
        """Submit the form."""
        self.driver.find_element(By.ID, 'submit').click()

    def wait_for_success(self):
        """Wait for the success message to appear."""
        # Wait for the success message to appear you can change this 
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'success_message'))
        )
        print("Test Passed: DPI created successfully!")

    def select_radio(self, field_name, value):
        """Select a radio button based on value."""
        radio_button = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field_name}'][id='{value}']")
        radio_button.click()
    def run_test(self):
        """Run the entire test."""
        try:
            self.open_application()
            self.fill_patient_form()
            self.fill_contact_urgence_form()
            self.fill_mutuelle()
            self.select_radio(
                field_name="sousTraitement",
                value=self.data.get("sous_traitement")
            )
            self.select_checkboxes(
                checkbox_list=self.data.get("antecedants"),
                field_name="Diabète"
            )
          
            self.select_radio(
                field_name="vaccine",
                value=self.data.get("vaccine")
            )
           # self.fill_antecedants()
            self.select_image(self.data.get("image_path"))
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
            "nom": "John",
            "prenom": "Doe",
            "date_naissance": "1985-03-15",
            "telephone": "123456789",
            "email": "johndoe@example.com",
        },
        "NSS": 123456789
    },
    "contact_urgence": {
        "nom": "Jane",
        "prenom": "Smith",
        "telephone": "987654321",
        "email": "janesmith@example.com"
    },
    "mutuelle": {
        "nom": "HealthPlus",
        "id": "12345"
    },
    "antecedants": [
        {"nom": "Diabète", "type": "Chronic"},
        
    ],
    "image_path": r"C:\Users\GEEK\Pictures\adidas.jpg",  
    "sous_traitement": "Oui",
    
    "vaccine": "Oui"
}


# Run the test
if __name__ == "__main__":
    #adjust the path to the chromedriver executable
    test = TestCreateDPI(driver_path='C:\chromedriver\chromedriver-win64\chromedriver.exe', app_url='http://localhost:4200/formPatient', data=test_data)
    try:
        test.run_test()
    except Exception as e:
        print(f"Test Failed: {e}")
