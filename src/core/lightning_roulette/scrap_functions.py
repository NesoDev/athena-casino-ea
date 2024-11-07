from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

def get_submit_button(driver, input_element, delay, logger):
    logger.log("Buscando 'submit_button'...", "SCRAPPER")
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            f1_password_input = driver.execute_script("return arguments[0].parentNode;", input_element)
            f2_password_input = driver.execute_script("return arguments[0].parentNode;", f1_password_input)
            f3_password_input = driver.execute_script("return arguments[0].parentNode;", f2_password_input)
            f4_password_input = driver.execute_script("return arguments[0].parentNode;", f3_password_input)
            f5_password_input = driver.execute_script("return arguments[0].parentNode;", f4_password_input)
            f1_submit_button = f5_password_input.find_elements(By.XPATH, './*')[2]
            submit_button = f1_submit_button.find_elements(By.XPATH, './*')[0]
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
            if submit_button is not None:
                return submit_button
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("'submit_button' no se encontró. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None

def get_root_element(driver, delay, logger):
    max_retries = 20
    retry_count = 0
    while retry_count < max_retries:
        try:
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_iframe = css_sp0pf4.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(first_iframe)
            second_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(second_iframe)
            third_iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(third_iframe)
            root_element = driver.find_element(By.ID, "root")
            if root_element is not None:
                return root_element
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            driver.switch_to.default_content()
            retry_count += 1
            logger.log("'root_element' no se encontró. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None

def get_stats_button(driver, delay, logger):
    logger.log("Buscando 'stats_button'...", "SCRAPPER")
    root_element = get_root_element(driver, delay, logger)
    if root_element is None:
        return None
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            tenth_common_ui_element = second_content_6d02a.find_elements(By.XPATH, "./*")[9]
            fourth_bottom_right_7663b = tenth_common_ui_element.find_elements(By.XPATH, "./*")[3]
            first_box_4ecd6 = fourth_bottom_right_7663b.find_element(By.XPATH, "./*")            
            first_item_wrapper_7891b_right_ac8e8 = first_box_4ecd6.find_element(By.XPATH, "./*")            
            stats_button = first_item_wrapper_7891b_right_ac8e8.find_elements(By.XPATH, "./*")[1]
            if stats_button is not None:
                return stats_button
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            driver.switch_to.default_content()
            retry_count += 1
            logger.log("'stats_button' no se encontró. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None

def get_data(driver, delay, logger):
    root_element = get_root_element(driver, delay, logger)
    if root_element is None:
        return None
    max_retries = 5
    retry_count = 0
    first_desktopDrawerCard_2bc56 = None
    while True:
        try:
            #logger.log("Extrayendo resultados...", "SCRAPPER")
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            thirteenth_desktopDrawerContainer_f0216 = second_content_6d02a.find_element(By.CLASS_NAME, "desktopDrawerContainer--f0216")
            first_desktopDrawer_ff97b_visible_1c4a1 = thirteenth_desktopDrawerContainer_f0216.find_elements(By.XPATH, "./*")[0]
            class_first_desktopDrawer_ff97b_visible_1c4a1 = first_desktopDrawer_ff97b_visible_1c4a1.get_attribute("class")
            if len(class_first_desktopDrawer_ff97b_visible_1c4a1.split(" ")) < 2:
                continue
            if class_first_desktopDrawer_ff97b_visible_1c4a1.split(" ")[1] != "visible--1c4a1":
                continue
            #driver.execute_script("arguments[0].classList.add('visible--1c4a1');", first_desktopDrawer_ff97b_visible_1c4a1)
            first_desktopDrawerCard_2bc56 = first_desktopDrawer_ff97b_visible_1c4a1.find_elements(By.XPATH, "./*")[0]
            if first_desktopDrawer_ff97b_visible_1c4a1.is_displayed() and len(first_desktopDrawerCard_2bc56.find_elements(By.XPATH, "./*")) == 0:
                if retry_count > max_retries:
                    return None
                retry_count += 1
                continue
            break
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            logger.log("'first_desktopDrawerCard_2bc56' no se encontró. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    retry_count = 0
    numbers = []
    while retry_count < max_retries:
        try:
            #logger.log("Extrayendo resultados...", "SCRAPPER")
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
            for child in list_number_container_8752e_recent_number_7cf3a_desktop_377f7:
                number_container = child.find_elements(By.XPATH, "./*")[0]
                number_span = number_container.find_elements(By.XPATH, "./*")[0]
                number = number_span.text
                numbers.append(number)
            numbers = list(filter(lambda x: x != "", numbers))
            driver.switch_to.default_content()
            #logger.log("Retornando resultados extraidos.", "SCRAPPER")
            if numbers:
                break
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            numbers = []
            retry_count += 1
            logger.log("Extracción de datos falló. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    if retry_count >= max_retries:
        return None
    return numbers

def check_session_expired(driver, delay, max_retries, logger):
    root_element = get_root_element(driver, delay, logger)
    if root_element is None:
        return None
    retry_count = 0
    while retry_count < max_retries:
        try:
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            twelfth_popup_container_140f0 = second_content_6d02a.find_elements(By.XPATH, "./*")[11]
            class_twelfth_popup_container_140f0 = twelfth_popup_container_140f0.get_attribute("class")
            driver.switch_to.default_content()
            # logger.log("Retornando resultado de la revisión de sesión expirada.", "SCRAPPER")
            if class_twelfth_popup_container_140f0 == "popupContainer--140f0 blocking--0ef8a highestPriority--13a6e":
                return True
            elif (class_twelfth_popup_container_140f0 is not None) and class_twelfth_popup_container_140f0 != "":
                return False
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("Verificación de sesión expirada falló. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None

def check_session_duplicate(driver, delay, max_retries, logger):
    root_element = get_root_element(driver, delay, logger)
    if root_element is None:
        return None
    retry_count = 0
    while retry_count < max_retries:
        try:
            first_app_7c603 = root_element.find_element(By.XPATH, "./*")
            first_container_55875 = first_app_7c603.find_element(By.XPATH, "./*")
            second_content_6d02a = first_container_55875.find_elements(By.XPATH, "./*")[1]
            twelfth_popup_container_140f0 = second_content_6d02a.find_elements(By.XPATH, "./*")[11]
            class_twelfth_popup_container_140f0 = twelfth_popup_container_140f0.get_attribute("class")
            first_popupWrapper_f73e8  = twelfth_popup_container_140f0.find_elements(By.XPATH, "./*")[0]
            class_first_popupWrapper_f73e8 = first_popupWrapper_f73e8.get_attribute("class")
            driver.switch_to.default_content()
            if class_twelfth_popup_container_140f0 == "popupContainer--140f0 blocking--0ef8a" and class_first_popupWrapper_f73e8 == "popupWrapper--f73e8 ":
                return True
            elif (class_twelfth_popup_container_140f0 is not None and class_twelfth_popup_container_140f0 != "") or (class_first_popupWrapper_f73e8 is not None and class_first_popupWrapper_f73e8 != ""):
                return False
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("Verificación de sesión duplicada falló. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None

def need_refresh_for_blocking(driver, delay, max_retries, logger):
    is_session_expired = check_session_expired(driver, delay, max_retries, logger)
    if is_session_expired is None:
        logger.log("Se agotaron los intentos para la detección de sesión expirada", "CHECK SESSION")
        return None
    #is_session_duplicated = check_session_duplicate(driver, delay, logger)
    #if is_session_duplicated is None:
    #    logger.log("Se agotaron los intentos para la detección de sesión duplicada", "CHECK SESSION")
    #    return None
    if is_session_expired == False:
        return False
    #if is_session_expired == False and is_session_duplicated == False:
    #    return False
    if is_session_expired:
        logger.log("Estado de la sesión -> Expirada", "SCRAPPER")
        return True
    #if is_session_duplicated:
    #    logger.log("Estado de la sesión -> Duplicada", "SCRAPPER")
    #    return True

def get_funplay_button(driver, delay, logger):
    logger.log("Buscando botón FunPlay", "SCRAPPER")
    max_retries = 30
    retry_count = 0
    first_roo186 = None
    while retry_count < max_retries:
        try:
            css_sp0pf4 = driver.find_element(By.CLASS_NAME, "css-sp0pf4")
            first_son = css_sp0pf4.find_element(By.XPATH, "./*")
            first_unnamed = first_son.find_element(By.XPATH, "./*")
            first_muiBox_root_css_btne3 = first_unnamed.find_element(By.XPATH, "./*")
            first_muiBox_root_css_13hwmkc = first_muiBox_root_css_btne3.find_element(By.XPATH, "./*")
            first_roo186 = first_muiBox_root_css_13hwmkc.find_element(By.XPATH, "./*")
            if first_roo186 is not None:
                break
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("'first_roo186' no encontrado. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    if retry_count >= max_retries:
        return None
    retry_count = 0
    first_roo195 = None
    found_text = False
    while retry_count < max_retries:
        try:     
            first_roo191 = first_roo186.find_element(By.XPATH, "./*")
            first_roo192 = first_roo191.find_element(By.XPATH, "./*")
            first_roo195 = first_roo192.find_element(By.XPATH, "./*")
            first_roo196 = first_roo195.find_elements(By.XPATH, "./*")[0]
            if first_roo196.text == "You're playing for fun, login to play for real." or first_roo196.text == "Estás jugando por diversión, inicia sesión para jugar de verdad.":
                found_text = True
                break
            elif first_roo196.text is None or first_roo196.text == "":
                found_text = False
                break
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("'first_roo195' no encontrado. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    if retry_count >= max_retries or found_text == False:
        return None
    retry_count = 0
    button = None
    while retry_count < max_retries:
        try: 
            second_roo201_roo202 = first_roo195.find_elements(By.XPATH, "./*")[1]
            button = second_roo201_roo202.find_element(By.XPATH, "./*")
            if button is not None:
                return button
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError) as e:
            retry_count += 1
            logger.log("Botón FunPlay no encontrado. Reintentando en {} segundos...".format(delay), "ERROR")
            time.sleep(delay)
    return None