from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

def get_submit_button(driver, input_element, delay):
    while True:
        try:
            #print("[SCRAPPER] Buscando 'botón enviar credenciales'.")
            f1_password_input = driver.execute_script("return arguments[0].parentNode;", input_element)
            f2_password_input = driver.execute_script("return arguments[0].parentNode;", f1_password_input)
            f3_password_input = driver.execute_script("return arguments[0].parentNode;", f2_password_input)
            f4_password_input = driver.execute_script("return arguments[0].parentNode;", f3_password_input)
            f5_password_input = driver.execute_script("return arguments[0].parentNode;", f4_password_input)
            f1_submit_button = f5_password_input.find_elements(By.XPATH, './*')[2]
            submit_button = f1_submit_button.find_elements(By.XPATH, './*')[0]
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
            #print("[SCRAPPER] Retornando 'botón enviar credenciales' encontrado.")
            return submit_button
        except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
            print(f"[ERROR] 'Botón enviar credenciales' no se encontró. Reintentando en {delay} segundos...")
            time.sleep(delay)

def get_stats_button(driver, delay):
    while True:
        try:
            #print("[SCRAPPER] Buscando 'botón estadísticas'.")
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(first_iframe)
            second_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(second_iframe)
            third_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(third_iframe)
            root_element = driver.find_element(By.ID, "root")
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            tenth_common_ui_element = second_content_6d02a.find_elements(By.XPATH, "./*")[9]
            fourth_bottom_right_7663b = tenth_common_ui_element.find_elements(By.XPATH, "./*")[3]
            first_box_4ecd6 = fourth_bottom_right_7663b.find_element(By.XPATH, "./*")            
            first_item_wrapper_7891b_right_ac8e8 = first_box_4ecd6.find_element(By.XPATH, "./*")            
            stats_button = first_item_wrapper_7891b_right_ac8e8.find_elements(By.XPATH, "./*")[1]
            #print("[SCRAPPER] Retornando 'botón estadísticas' encontrado.")
            return stats_button
        except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
            driver.switch_to.default_content()
            print(f"[ERROR] 'Botón estadísticas' no se encontró. Reintentando en {delay} segundos...")
            time.sleep(delay)

def get_data(driver, delay):
    while True:
        try:
            #print("[SCRAPPER] Extrayendo resultados'.")
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(first_iframe)
            second_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(second_iframe)        
            third_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(third_iframe)        
            root_element = driver.find_element(By.ID, "root")
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            thirteenth_desktopDrawerContainer_f0216 = second_content_6d02a.find_element(By.CLASS_NAME, "desktopDrawerContainer--f0216")
            first_desktopDrawer_ff97b_visible_1c4a1 = thirteenth_desktopDrawerContainer_f0216.find_elements(By.XPATH, "./*")[0]
            driver.execute_script("arguments[0].classList.add('visible--1c4a1');", first_desktopDrawer_ff97b_visible_1c4a1)
            first_desktopDrawerCard_2bc56 = first_desktopDrawer_ff97b_visible_1c4a1.find_elements(By.XPATH, "./*")[0]
            if len(first_desktopDrawerCard_2bc56.find_elements(By.XPATH, './*')) == 0:
                return None
            first_content_1a8af = first_desktopDrawerCard_2bc56.find_elements(By.XPATH, "./*")[0]
            second_contentContainer_f5d2a = first_content_1a8af.find_elements(By.XPATH, "./*")[1]
            first_statisticsDrawer_4bfec = second_contentContainer_f5d2a.find_elements(By.XPATH, "./*")[0]
            first_wrapper_3f4b5 = first_statisticsDrawer_4bfec.find_elements(By.XPATH, "./*")[0]
            second_list_72361 = first_wrapper_3f4b5.find_elements(By.XPATH, "./*")[1]
            first_active_f0a91_muteAnimation_3f915 = second_list_72361.find_elements(By.XPATH, "./*")[0]
            first_body_036f5_landscape_6c853 = first_active_f0a91_muteAnimation_3f915.find_elements(By.XPATH, "./*")[0]
            first_div_unknow = first_body_036f5_landscape_6c853.find_elements(By.XPATH, "./*")[0]
            first_widthWrap_1c118 = first_div_unknow.find_elements(By.XPATH, "./*")[0]
            first_recentNumbers_141d3_immersive2_e3d37 = first_widthWrap_1c118.find_elements(By.XPATH, "./*")[0]
            second_numbers_ca008_recent_number_d9e03_desktop_80ae3 = first_recentNumbers_141d3_immersive2_e3d37.find_elements(By.XPATH, "./*")[1]
            list_number_container_8752e_recent_number_7cf3a_desktop_377f7 = second_numbers_ca008_recent_number_d9e03_desktop_80ae3.find_elements(By.XPATH, "./*")
            numbers = []
            for child in list_number_container_8752e_recent_number_7cf3a_desktop_377f7:
                number_container = child.find_elements(By.XPATH, "./*")[0]
                number_span = number_container.find_elements(By.XPATH, "./*")[0]
                number = number_span.text
                numbers.append(number)
            numbers = list(filter(lambda x: x != "", numbers))
            driver.switch_to.default_content()
            #print("[SCRAPPER] Retornando resultados extraidos.")
            return numbers
        except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
            driver.switch_to.default_content()
            print(f"[ERROR] Extracción de datos falló. Reintentando en {delay} segundos...")
            time.sleep(delay)

def check_session_expired(driver, delay):
    while True:
        try:
            #print("[SCRAPPER] Revisando si la sesión ha expirado.")
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(first_iframe)
            second_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(second_iframe)
            third_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(third_iframe)
            root_element = driver.find_element(By.ID, "root")
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            twelfth_popup_container_140f0 = second_content_6d02a.find_elements(By.XPATH, "./*")[11]
            class_twelfth_popup_container_140f0 = twelfth_popup_container_140f0.get_attribute("class")
            driver.switch_to.default_content()
            #print("[SCRAPPER] Retornando resultado de la revisión de sesión expirada.")
            if  class_twelfth_popup_container_140f0 == "popupContainer--140f0 blocking--0ef8a highestPriority--13a6e":
                return True
            return False
        except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
            driver.switch_to.default_content()
            #print(f"[INFO] Números no obtenidos. Reintentando en {delay} segundos...")
            print(f"[ERROR] Verificación de sesión expirada falló. Reintentando en {delay} segundos...")
            time.sleep(delay)

def get_funplay_button(driver, delay):
    while True:
        try:
            #print("[SCRAPPER] Buscando botón 'fun play'.")
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_son = css_sp0pf4.find_element(By.XPATH, "./*")
            first_unnamed = first_son.find_element(By.XPATH, "./*")
            first_muiBox_root_css_btne3 = first_unnamed.find_element(By.XPATH, "./*")
            first_muiBox_root_css_13hwmkc = first_muiBox_root_css_btne3.find_element(By.XPATH, "./*")
            first_roo186 = first_muiBox_root_css_13hwmkc.find_element(By.XPATH, "./*")
            if first_roo186.get_attribute('class') != 'roo186':
                return None
            first_roo191 = first_roo186.find_element(By.XPATH, "./*")
            first_roo192 = first_roo191.find_element(By.XPATH, "./*")
            first_roo195 = first_roo192.find_element(By.XPATH, "./*")
            first_roo196 = first_roo195.find_elements(By.XPATH, "./*")[0]
            if first_roo196.text != "You're playing for fun, login to play for real.":
                continue
            second_roo201_roo202 = first_roo195.find_elements(By.XPATH, "./*")[1]
            button = second_roo201_roo202.find_element(By.XPATH, "./*")
            return button 
        except (NoSuchElementException, StaleElementReferenceException, TimeoutError, TimeoutException, IndexError) as e:
            print(f"[ERROR] Boton FunPlay no encontrado. Reintentando en {delay} segundos...")
            time.sleep(delay)