from selenium.webdriver.common.by import By # type:ignore
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException # type:ignore
import time

def get_submit_button(driver, input_element, delay):
    while True:
        try:
            time.sleep(delay)
            submit_container = driver.execute_script("return arguments[0].parentNode.parentNode.parentNode.parentNode;", input_element)
            submit_button = submit_container.find_elements(By.XPATH, './*')[2].find_elements(By.XPATH, './*')[0]
            return submit_button
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"[INFO] Botón de enviar credenciales aún no está disponible. Reintentando en {delay} segundos...")
            time.sleep(delay)

def get_stats_button(driver, delay):
    while True:
        try:
            time.sleep(delay)

            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            print("[SUCCESS] Elemento 'css-sp0pf4' encontrado.")
            
            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            print("[SUCCESS] Primer iframe encontrado.")
            
            second_iframe = first_iframe.find_element(By.TAG_NAME, "iframe")
            print("[SUCCESS] Segundo iframe encontrado.")
            
            third_iframe = second_iframe.find_element(By.TAG_NAME, "iframe")
            print("[SUCCESS] Tercer iframe encontrado.")
            
            root_element = third_iframe.find_element(By.ID, "root")
            print("[SUCCESS] Elemento 'root' encontrado.")
            
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo de 'root' obtenido.")
            
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo del primer hijo obtenido.")
            
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            print("[INFO] Segundo hijo obtenido.")
            
            ninend_common_ui_element = second_content_6d02a.find_elements(By.XPATH, "./*")[9]
            print("[INFO] Décimmo hijo obtenido.")
            
            fourth_bottom_right_7663b = ninend_common_ui_element.find_elements(By.XPATH, "./*")[3]
            print("[INFO] Cuarto hijo obtenido.")
            
            first_box_4ecd6 = fourth_bottom_right_7663b.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo del cuarto nivel obtenido.")
            
            first_item_wrapper_7891b_right_ac8e8 = first_box_4ecd6.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo del contenedor de resultados obtenido.")
            
            first_unnamed = first_item_wrapper_7891b_right_ac8e8.find_element(By.XPATH, "./*")
            print("[INFO] Primer elemento desde el ítem envuelto.")
            
            stats_button = first_unnamed.find_element(By.XPATH, "./*")
            print("[SUCCESS] Botón de estadísticas encontrado.")
            return stats_button
        
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"[INFO] Botón de estadísticas aún no está disponible. Reintentando en {delay} segundos...")
            time.sleep(delay)

def get_data(driver, delay):
    numbers = []
    while True:
        try:
            print("esperando 10 segundos")
            time.sleep(delay)

            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            print("[SUCCESS] Elemento 'css-sp0pf4' encontrado.")

            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(first_iframe)
            print("[SUCCESS] Primer iframe encontrado.")
            
            second_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(second_iframe)
            print("[SUCCESS] Segundo iframe encontrado.")
            
            third_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(third_iframe)
            print("[SUCCESS] Tercer iframe encontrado.")
            
            root_element = driver.find_element(By.ID, "root")
            print("[SUCCESS] Elemento 'root' encontrado.")
            
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo de 'root' obtenido.")

            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            print("[INFO] Primer hijo del primer hijo obtenido.")

            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            print("[INFO] Segundo hijo obtenido.")

            thirteenth_desktopDrawerContainer_f0216 = second_content_6d02a.find_element(By.CLASS_NAME, "desktopDrawerContainer--f0216")
            print("[INFO] Décimo tercer hijo obtenido.")

            first_desktopDrawer_ff97b_visible_1c4a1 = thirteenth_desktopDrawerContainer_f0216.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")
            driver.execute_script("arguments[0].classList.add('visible--1c4a1');", first_desktopDrawer_ff97b_visible_1c4a1)

            first_desktopDrawerCard_2bc56 = first_desktopDrawer_ff97b_visible_1c4a1.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_content_1a8af = first_desktopDrawerCard_2bc56.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            second_contentContainer_f5d2a = first_content_1a8af.find_elements(By.XPATH, "./*")[1]
            print("[INFO] Segundo hijo obtenido.")

            first_statisticsDrawer_4bfec = second_contentContainer_f5d2a.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_wrapper_3f4b5 = first_statisticsDrawer_4bfec.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            second_list_72361 = first_wrapper_3f4b5.find_elements(By.XPATH, "./*")[1]
            print("[INFO] Segundo hijo obtenido.")

            first_active_f0a91_muteAnimation_3f915 = second_list_72361.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_body_036f5_landscape_6c853 = first_active_f0a91_muteAnimation_3f915.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_div_unknow = first_body_036f5_landscape_6c853.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_widthWrap_1c118 = first_div_unknow.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            first_recentNumbers_141d3_immersive2_e3d37 = first_widthWrap_1c118.find_elements(By.XPATH, "./*")[0]
            print("[INFO] Primer hijo obtenido.")

            second_numbers_ca008_recent_number_d9e03_desktop_80ae3 = first_recentNumbers_141d3_immersive2_e3d37.find_elements(By.XPATH, "./*")[1]
            print("[INFO] Primer hijo obtenido.")

            list_number_container_8752e_recent_number_7cf3a_desktop_377f7 = second_numbers_ca008_recent_number_d9e03_desktop_80ae3.find_elements(By.XPATH, "./*")
            print("[INFO] lista de hijos obtenida.")
            
            for child in list_number_container_8752e_recent_number_7cf3a_desktop_377f7:
                number_container = child.find_elements(By.XPATH, "./*")[0]
                number_span = number_container.find_elements(By.XPATH, "./*")[0]
                number = number_span.text
                numbers.append(number)
            
            driver.switch_to.default_content()
            return numbers
        
        except (NoSuchElementException, StaleElementReferenceException) as e:
            driver.switch_to.default_content()
            print(f"[INFO] No se pudo obtener la data. Reintentando en {delay} segundos...")
            time.sleep(delay)