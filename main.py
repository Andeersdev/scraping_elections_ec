import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_directory = "C:\\Users\\Dell Inspiron\\Downloads"
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'prefs', {
        'download.default_directory': download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
driver = webdriver.Chrome(options=options)
driver.get('https://app01.cne.gob.ec/Resultados20212V')


def bucles_selects(id_select, select, canton_value, name_dir_sup):
    try:
        select_canton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id_select))
        )
        # Obtener todas las opciones del select canton
        cantons = select_canton.find_elements(By.TAG_NAME, "option")
    except:
        print("Error, could not get select options")

    for canton in cantons:
        canton_value = canton.get_attribute("value")
        option_text = canton.text
        #
        if (canton_value.isdigit()):
            selection_canton = Select(select_canton)
            selection_canton.select_by_value(canton_value)
            dir_file_canton = name_dir_sup + \
                '/CANTONES/' + clean_name(option_text)
            time.sleep(2)
            btn_consult(dir_file_canton, option_text)

            try:
                # Obteniendo las opciones del select parroquia
                select_parishes = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ddlParroquia"))
                )
                parishes = select_parishes.find_elements(
                    By.TAG_NAME, "option")
            except:
                print("Error,could not get select options")
            for parish in parishes:
                parish_value = parish.get_attribute("value")
                text_parroquia = parish.text
                #
                if (parish_value.isdigit()):
                    selection_parroquia = Select(select_parishes)
                    selection_parroquia.select_by_value(
                        parish_value)
                    dir_file_parro = dir_file_canton + \
                        '/PARROQUIAS/' + clean_name(text_parroquia)
                    time.sleep(2)
                    btn_consult(dir_file_parro, text_parroquia)

                    try:
                        # Obteniendo opciones del select zonas
                        select_zones = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "ddlZona")))
                        zones = select_zones.find_elements(
                            By.TAG_NAME, "option")
                    except:
                        print("Error")

                    for zone in zones:
                        zone_value = zone.get_attribute("value")
                        zone_text = zone.text

                        if (zone_value.isdigit()):
                            selection_zone = Select(select_zones)
                            selection_zone.select_by_value(zone_value)
                            dir_file_zone = dir_file_parro + \
                                '/ZONAS/' + clean_name(zone_text)
                            time.sleep(2)
                            btn_consult(dir_file_zone, zone_text)

                            try:
                                # Esperar a que aparezca el select de juntas
                                select_junt = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.ID, "ddlJunta"))
                                )
                                junts = select_junt.find_elements(
                                    By.TAG_NAME, "option")
                            except:
                                print("Error, could not get select options")

                            for junt in junts:
                                junt_value = junt.get_attribute(
                                    "value")
                                junt_text = junt.text

                                if (junt_value.isdigit()):
                                    selection_junta = Select(select_junt)
                                    selection_junta.select_by_value(junt_value)
                                    dir_file_junta = dir_file_zone+'/JUNTAS/'
                                    time.sleep(1)
                                    btn_consult(dir_file_junta, junt_text)


def consult():
    time.sleep(3)
    while True:
        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'myButtonActive'))
            )
            if (element):
                print(f'Existe {element}')
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", element)
            element.click()
            break
        except:
            time.sleep(1)


def btn_consult(dir_r, text_file):

    consult()
    time.sleep(3)
    while True:
        try:
            btn_report = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="A1"]'))
            )
            driver.execute_script("arguments[0].click();", btn_report)
            break
        except:
            time.sleep(2)

    time.sleep(3)
    # Abriendo la nueva pestaña al dar click en anchor
    windown = driver.window_handles
    driver.switch_to.window(windown[-1])

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "preloader-content-accion-Template"))
            )
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'dxrd-preview-export-toolbar-item'))
            )
            elemento.click()
            break
        except:
            time.sleep(1)

    while True:
        try:
            # Esperar a que aparezcan las opciones del menú
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "dx-menu-items-container")))

            # Hacer clic en la opción de descarga
            element_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'PDF')]"))
            )
            element_div.click()
            break
        except:
            time.sleep(1)

    try:
        status_code = driver.execute_script(
            "return window.performance.getEntries()[0].response.status")
        if status_code == 500:
            print("Error 500 detectado. Volviendo a realizar la consulta.")
            driver.close()  # Cerrar la ventana actual
            driver.switch_to.window(windown[0])
            consult()
    except:
        pass

    time.sleep(3)

    organize_pdf(dir_r, text_file)
    # Cerrar la pestaña y volver a la pestaña original
    driver.close()
    driver.switch_to.window(windown[0])


def clean_name(name):
    illegal_characters = ['/', '\\', '?',
                          '%', '*', ':', '|', '"', '<', '>', '.']
    for character in illegal_characters:
        if character == '/':
            name = name.replace(character, '')  # Reemplazar '/' con ''
        else:
            # Eliminar otros caracteres no permitidos
            name = name.replace(character, '')
    return name.strip()  # Eliminar espacios al principio y al final


def organize_pdf(dir_r, text_file):

    i = 0
    while i < 3:
        try:
            name_file_clean = clean_name(text_file)
            dir_folder = os.path.join('./downloads/2021-2V', dir_r)

            # Crear la carpeta si no existe
            if not os.path.exists(dir_folder):
                os.makedirs(dir_folder)

            # Buscar archivos PDF en el directorio de descarga
            pdf_files = [f for f in os.listdir(
                download_directory) if f.endswith('.pdf')]

            # Filtrar archivos PDF específicos (puedes usar condiciones más específicas)
            target_pdf = [
                f for f in pdf_files if 'REPORTE DE RESULTADOS FINALES' in f]

            if len(target_pdf) == 1:
                # Renombrar y mover el archivo PDF
                new_name_file = name_file_clean + '.pdf'
                dir_origin = os.path.join(download_directory, target_pdf[0])
                dir_final = os.path.join(dir_folder, new_name_file)

                # Mover y renombrar el archivo
                shutil.move(dir_origin, dir_final)
                time.sleep(1)
                break
            else:
                print(
                    f"tener en cuenta este archivo {dir_r + ' ' +name_file_clean}")

        except Exception as e:
            time.sleep(2)
            i += 1


# LOGICA PARA ACCEDER A LA OPCION PRESIDENTE
while True:
    try:
        option_btn_first_load = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'myButtonDig'))
        )
        option_btn_first_load[0].click()
        break
    except:
        time.sleep(2)
time.sleep(3)

while True:
    try:
        select_province = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ddlProvincia')))
        provinces = select_province.find_elements(
            By.TAG_NAME, "option")
        break
    except:
        time.sleep(1)

for province in provinces:
    province_value = province.get_attribute("value")
    province_text = province.text

    if (province_value.isdigit()):
        select = Select(select_province)
        select.select_by_value(province_value)
        time.sleep(3)
        btn_consult(province_text, province_text)

        while True:
            try:
                select_cir = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "ddlCircunscripcion"))
                )
                break
            except:
                time.sleep(1)
        if select_cir.is_enabled():
            circumscriptions = select_cir.find_elements(
                By.TAG_NAME, "option")

            for circumscription in circumscriptions:
                cir_value = circumscription.get_attribute("value")
                cir_text = circumscription.text
                if (cir_value.isdigit()):
                    select = Select(select_cir)
                    select.select_by_value(cir_value)

                    dir_file_cir = province_text + \
                        '/CIRCUNSCRIPCION/' + clean_name(cir_text)
                    time.sleep(2)
                    btn_consult(dir_file_cir, cir_text)
                    time.sleep(1)
                    bucles_selects(
                        'ddlCanton', select_cir, cir_value, dir_file_cir)

        else:
            bucles_selects('ddlCanton', select_province,
                           province_value, province_text)

input("Presiona Enter para cerrar el navegador...")
driver.quit()
