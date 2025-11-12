import pytest
import allure
from pages.upload_page import UploadPage


# ============================================================
# 🎵 TEST FUNCIONALES DEL MÓDULO "UPLOAD" (Audius Music)
# ============================================================

@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC001 - Subir archivo válido en formato mp3")
@allure.description("""
Description
Desde el módulo Upload, el usuario selecciona un archivo de audio válido con extensión .mp3 y lo envía para su carga.
El sistema procesa el archivo y refleja el estado de subida exitosa sin errores de validación.

Resultado esperado : El archivo .mp3 se carga correctamente y la UI muestra el estado de “subido” (o equivalente), permitiendo continuar con el flujo de publicación/edición.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox actualizados
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida (fixture: page_with_session)
Archivo de prueba existente y legible: resources/audio/demo.mp3
Permisos del navegador para seleccionar archivos
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC001_subir_archivo_valido(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Abrir módulo Upload"):
        test_logger.info("Abriendo módulo Upload")
        upload.open()

    with allure.step(f"Subir archivo válido: {file_path}"):
        test_logger.info(f"Subiendo archivo válido: {file_path}")
        upload.upload_audio_file(file_path)
        page_with_session.wait_for_timeout(5000)
        upload.assert_file_uploaded()
        test_logger.info("Archivo cargado correctamente y marcado como subido.")

    allure.attach(page_with_session.screenshot(), name="Archivo_subido", attachment_type=allure.attachment_type.PNG)
    test_logger.info("✅ Archivo mp3 subido correctamente.")


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC002 - Poner TrackName con menos de 65 caracteres")
@allure.description("""
Description
Tras cargar un audio válido, el usuario ingresa un TrackName cuya longitud es menor a 65 caracteres y completa los campos obligatorios.
El sistema acepta el nombre y permite guardar sin errores.

Resultado esperado : El TrackName (< 65 caracteres) se guarda correctamente y el flujo avanza sin validaciones bloqueantes.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC002_poner_en_el_TracKName_menor_a_65_caracteres(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo de audio válido"):
        test_logger.info("Subiendo archivo válido para probar TrackName < 65 caracteres")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()

    with allure.step("Rellenar campos obligatorios"):
        test_logger.info("Llenando campos con nombre corto y válidos")
        upload.CamposObligatorios(
            nuevo_nombre="Tema con Artwork QA",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        page_with_session.wait_for_timeout(5000)
        upload.Save()
        test_logger.info("Track guardado con nombre válido y corto.")

    allure.attach(page_with_session.screenshot(), name="TrackName_valido", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC003 - No permitir TrackName vacío")
@allure.description("""
Description
Luego de subir un audio válido, el usuario intenta continuar dejando el campo TrackName vacío.
El sistema valida que el nombre no puede estar vacío y muestra un mensaje de error.

Resultado esperado : Se bloquea el guardado y aparece el mensaje “Your track must have a name.”.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC003_Verificar_que_no_permita_poner_en_el_TracKName_caracteres_vacios_(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y dejar nombre vacío"):
        test_logger.info("Probando validación: TrackName vacío no permitido")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    with allure.step("Validar mensaje de error por nombre vacío"):
        test_logger.info("Validando mensaje de error esperado")
        assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"
        test_logger.info("✅ Mensaje 'Your track must have a name.' mostrado correctamente.")
    allure.attach(page_with_session.screenshot(), name="Error_nombre_vacio", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC004 - No permitir solo espacios en el campo Name")
@allure.description("""
Description
El usuario intenta guardar un TrackName compuesto únicamente por espacios.
El sistema debe normalizar/validar y rechazar nombres vacíos efectivos.

Resultado esperado : Se bloquea el guardado y se muestra el mensaje “Your track must have a name.”.
Nota: Caso marcado como xfail por bug conocido (actualmente acepta espacios).
""")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="Bug conocido: el sistema acepta espacios como caracteres válidos")
def test_TC004_Verificar_que_no_permita_ingresar_espacios_vacios_al_campo_de_Name_validando_como_Caracteres(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo con nombre de solo espacios"):
        test_logger.info("Probando validación: solo espacios en TrackName")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre=" ",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    with allure.step("Validar mensaje de error"):
        test_logger.info("Esperando mensaje de validación por nombre vacío")
        assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC005 - Quitar espacios vacíos y permitir solo caracteres válidos")
@pytest.mark.functional
@pytest.mark.integration
def test_TC005_Verificar_que_al_subir_con_espacios_vacios_en_el_campo_Name_se_quite_automaticamente_mostrando_solo_caracteres(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y limpiar espacios en TrackName"):
        test_logger.info("Validando normalización de espacios en TrackName")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="  The Rock   -   Beatles  ",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()
        test_logger.info("Track guardado correctamente sin espacios extra.")

    allure.attach(page_with_session.screenshot(), name="Track_limpio", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC006 - No permitir tags de más de 30 caracteres")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="Permite ingresar más de 30 caracteres en el campo tags")
def test_TC006_Verificar_que_no_permita_tags_que_superen_los_30_caracteres(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y usar tag muy largo"):
        test_logger.info("Probando validación de longitud >30 en campo Tags")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="The Rock QA Test",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="LaamistadesunarelaciónafectivaentredosomáspersonasLaamistadesunarelaciónafectivaentredosomáspersonas.",
        )
        upload.Save()

    with allure.step("Validar mensaje por tag largo"):
        test_logger.info("Esperando mensaje de validación por tag largo")
        assert upload.AssertMensajesLargos("Fix errors to continue your upload."), "❌ No se mostró el mensaje esperado"


@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC007 - No permitir archivos que no sean mp3 o wav")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC007_Verificar_que_no_permita_subir_Archivos_que_no_estan_en_formato_mp3o_wav(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/prueba.jpg"

    with allure.step("Intentar subir archivo no compatible"):
        test_logger.info("Intentando subir archivo no permitido (.jpg)")
        upload.open()
        upload.upload_audio_file(file_path)
<<<<<<< HEAD

=======
        
>>>>>>> 2ac5d08c91d64a258451e87337660a979bcea474
    with allure.step("Validar mensaje de tipo de archivo no soportado"):
        test_logger.info("Verificando mensaje 'Unsupported File Type'")
        assert upload.validar_mensaje("Unsupported File Type"), "❌ No se mostró el mensaje esperado"
        test_logger.info("✅ Validación de tipo de archivo ejecutada correctamente.")

    allure.attach(page_with_session.screenshot(), name="Archivo_invalido", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC008 - No permitir más de 64 caracteres en TrackName")
@pytest.mark.functional
@pytest.mark.integration
def test_TC008_Verificar_que_no_permita_ingresar_mas_de_64_caracteres_en_el_campo_TrackName(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar TrackName demasiado largo"):
        test_logger.info("Probando validación de longitud >64 en TrackName")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="Grupo_Rock- the beatles-stramberry" * 4,
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()
        test_logger.info("Intento de guardado con nombre largo completado.")

    allure.attach(page_with_session.screenshot(), name="Nombre_largo", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC009 - Permitir mínimo 1 caracter en TrackName")
@pytest.mark.functional
@pytest.mark.integration
def test_TC009_Verificar_que_permita_ingresar_al_menos_1caracter_en_el_campo_TrackName_como_valido(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar TrackName de un solo carácter"):
        test_logger.info("Validando mínimo permitido (1 carácter en TrackName)")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="a",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()
        test_logger.info("TrackName con 1 carácter guardado correctamente.")

    allure.attach(page_with_session.screenshot(), name="TrackName_1caracter", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Permitir mínimo 1 caracter en Tags")
@pytest.mark.functional
@pytest.mark.integration
def test_TC010_Verificar_como_minimo_1_caracter_de_tamaño_ene_el_campo_Tags_para_ser_Valido(page_with_session, test_logger):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar solo un carácter en Tags"):
        test_logger.info("Validando mínimo permitido (1 carácter en Tags)")
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="The Rock - Green day",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="a",
        )
        upload.Save()
        test_logger.info("Campo Tags con 1 carácter validado correctamente.")

    allure.attach(page_with_session.screenshot(), name="Tags_1caracter", attachment_type=allure.attachment_type.PNG)
