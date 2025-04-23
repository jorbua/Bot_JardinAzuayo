
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
##from selenium.webdriver.firefox.service import Service as FirefoxService
##from selenium.webdriver.firefox.options import Options

##CHROME
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import chromedriver_autoinstaller
from autopylogger import init_logging
from pathlib import Path
from datetime import timedelta,datetime
import os
import time
import configparser
import requests
import subprocess
import multiprocessing


def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False

#INSTRUCCIONES
#BANCO PIDE REGISTRO DE PC, registrar desde el robot

url="https://javirtual.jardinazuayo.fin.ec/jaweb/login/organizacion"
##user_name = "BROADNETGALMEIDA1"
##password = "Broadnet2022*"
user_name = "JBustamante1"
password = "Broad2025."
#urlcuenta="https://bancavirtual.bancoguayaquil.com/CashMultidispositivosBG/Aplicaciones/index.html#/trans/BV/Cuentas/ESTADOCUENTA/?PATH=BancaEmpresas%2Fview%2FCuentas%2FEstadoCuenta.html"
logs_dir="C:\RobotEC\Archivos\{fecha}\JardinAzuayo"
ruta_archivo_clave="C:\\RobotEC\\BroadnetBot\\webjardinazuayo\\token.txt"
download_dir="C:\RobotEC\Archivos\{fecha}\JardinAzuayo\\"

hora=datetime.today().strftime('%H:%M:%S')
hora=hora.replace(":","")
fecha=datetime.today().strftime('%Y-%m-%d')
fecha=fecha.replace("-","")
download_dir=download_dir.replace("{fecha}",fecha)
logs_dir=download_dir.replace("{fecha}",fecha)


if hora>="050000" and hora<="230000":
    try:
        #verifica carpeta de trabajo
        #crea carpeta solo fecha
        try:
            path = Path(download_dir)
            path.mkdir(parents=True)
        except:
            print("Carpeta ya existe")

        mylogger = init_logging(log_name="logjardinazuayo", log_directory=logs_dir)

        
##        from selenium import webdriver
##        from webdriver_manager.chrome import ChromeDriverManager
##        from webdriver_manager.core.os_manager import ChromeType
##
##        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        
##         ##FIREFOX
##        mylogger.info('Inicializa FIREFOX')
##        from webdriver_manager.firefox import GeckoDriverManager
##        options = Options()
##        options.set_preference("browser.download.folderList", 2)
##        #options.set_preference("browser.download.manager.showWhenStarting", False)
##        options.set_preference("browser.download.dir", download_dir)
##        #options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
####        fp = webdriver.FirefoxProfile()
####        fp.set_preference("browser.download.folderList", 2)
####        fp.set_preference("browser.download.dir", download_dir)
##        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

        ##CHROME
        mylogger.info('Inicializa CHROME')
        from webdriver_manager.chrome import ChromeDriverManager
        Options = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : download_dir,"download.folderList":2}
        Options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(service=ChromeService(),options=Options)

        
##        ##OPERA
##        mylogger.info('Inicializa OPERA')
##        webdriver_service = service.Service('C:\\RobotEC\\BroadnetBot\\webprodubanco\\operadriver_win32\\operadriver.exe')
##        webdriver_service.start()
##
##        android_caps = {}
##        android_caps['operaOptions'] = {
##            'androidPackage': 'com.opera.browser',
##        }
##
##        driver = webdriver.Remote(webdriver_service.service_url, desired_capabilities=android_caps)

        
        driver.maximize_window()
        driver.delete_all_cookies()  
        driver.get(url)        

        #carga url de inicio
        mylogger.info(url)
        while not page_is_loading(driver):
            continue
        try:
            os.remove(ruta_archivo_clave)
        except:
            mylogger.info("No hay archivo de token")
        time.sleep(1)
        #segunda carga
        driver.refresh()
        while not page_is_loading(driver):
            continue
        #escoge organizacion
        mylogger.info("escoge organizacion")
        WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div/a[2]/div/div/div'))
            ).click()
        while not page_is_loading(driver):
            continue
        #usuario
        mylogger.info("Ingresa usuario")
        element = driver.find_element(By.XPATH, '//*[@id="usuario"]')
        element.send_keys(user_name)
        #espera clave
        time.sleep(0.5)    
        #clave
        mylogger.info("Ingresa clave")
        element = driver.find_element(By.XPATH, '//*[@id="clave"]')
        element.send_keys(password)
        #espera clave
        #time.sleep(1000000)
        time.sleep(1)
        #boton ingresar
        WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="login"]/div/div/div[5]/button'))
            ).click()
        #element.send_keys(Keys.RETURN)
        mylogger.info("Boton ingresar")
        while not page_is_loading(driver):
            continue
        existe_archivo=0
        contador_espera_archivo=0
        mylogger.info("Espero archivo de clave")
        print ("Espero archivo de clave")
        while (existe_archivo==0):
          existe_archivo=os.path.isfile(ruta_archivo_clave)
          time.sleep(1)
          contador_espera_archivo=contador_espera_archivo+1
          if (contador_espera_archivo>240):
              mylogger.info("Termino tiempo, NO* hay archivo de clave")
              print("Termino tiempo, NO* hay archivo de clave")
              existe_archivo=0
              break
        if (existe_archivo==1):
          mylogger.info("SI* hay archivo de clave")
          print("SI* hay archivo de clave")
          token=open(ruta_archivo_clave).read()
          #token=token[0:6] #leo sin salto de linea
          #mylogger.info(token)
          os.remove(ruta_archivo_clave)
          mylogger.info(token)
          print(token)       
        element = WebDriverWait(driver, 30).until(
           EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[1]'))
        )
        element.send_keys(token[0:1])
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[2]')
        element.send_keys(token[1:2])
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[3]')
        element.send_keys(token[2:3])
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[4]')
        element.send_keys(token[3:4])
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[5]')
        element.send_keys(token[4:5])
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[2]/div/input[6]')
        element.send_keys(token[5:6])
        time.sleep(0.5)
        #otp
        #clic boton aceptar otp
        WebDriverWait(driver,10).until(
          EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div[2]/div[1]/form/div/div/div[4]/div[2]/button'))
        ).click()
        while not page_is_loading(driver):
            continue
        WebDriverWait(driver,10).until(
           EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/section/section/section/main/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/a/span[2]'))
        ).click()
        #descargar excel
        WebDriverWait(driver,60).until(
           EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/section/section/section/main/div/div[2]/div/div[3]/div/div[3]/div/div/div/div/div/button[2]'))
        ).click()
        mylogger.info("DESCARGA OK !!!")
        time.sleep(20) # seconds
        #time.sleep(180)
    except Exception as e:
        mylogger.info ("excepcion")
        mylogger.info (type(e))     # the exception instance
        mylogger.info (e.args)      # arguments stored in .args
        mylogger.info (e)           # __str__ allows args to printed directly
    mylogger.info("Termina sesion")
    driver.close()
    driver.quit()
    ##mylogger.info("EJECUTA DE NUEVO")
    ##subprocess.Popen(["C:\RobotEC\BroadnetBot\webpichincha\dist\webpichincha\webpichincha.exe"])
else:
    mylogger.info("FUERA DE HORARIO !!!")


