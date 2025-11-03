import pytest
from pages.upload_page import UploadPage


@pytest.mark.functional
def test_TC001_subir_archivo_valido(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    # define ruta del archivo que subirás
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    page_with_session.wait_for_timeout(5000)
    upload.assert_file_uploaded()
    page_with_session.wait_for_timeout(5000)

@pytest.mark.functional
def test_TC002_poner_en_el_TracKName_menor_a_65_caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    upload.assert_file_uploaded()
    upload.BotonSiguiente()
    upload.CamposObligatorios(
        nuevo_nombre="Tema con Artwork QA",
        genero_primera_opcion=True,
        artwork_busqueda="rock",
        tag_valor="juegos",
    )
    page_with_session.wait_for_timeout(5000)
    upload.Save()

@pytest.mark.functional
def test_TC003_Verificar_que_no_permita_poner_en_el_TracKName_caracteres_vacios_(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    upload.assert_file_uploaded()
    upload.BotonSiguiente()
    upload.CamposObligatorios(
        nuevo_nombre="",
        genero_primera_opcion=True,
        artwork_busqueda="rock",
        tag_valor="juegos",
    )
    page_with_session.wait_for_timeout(5000)
    upload.Save()
    assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"

@pytest.mark.functional
@pytest.mark.xfail(reason="Bug conocido: el mensaje de error al ingresar campos vacios")
def test_TC004_Verificar_que_no_permita_ingresar_espacios_vacios_al_campo_de_Name_validando_como_Caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    upload.assert_file_uploaded()
    upload.BotonSiguiente()
    upload.CamposObligatorios(
        nuevo_nombre="",
        genero_primera_opcion=True,
        artwork_busqueda="rock",
        tag_valor="juegos",
    )
    page_with_session.wait_for_timeout(5000)
    upload.Save()
    assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"

@pytest.mark.functional
def test_TC005_Verificar_que_al_subir_con_espacios_vacios_en_el_campo_Name_se_quite_automaticamente_mostrando_solo_caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    upload.assert_file_uploaded()
    upload.BotonSiguiente()
    upload.CamposObligatorios(
        nuevo_nombre="The Rock - Beatles",
        genero_primera_opcion=True,
        artwork_busqueda="rock",
        tag_valor="juegos",
    )
    page_with_session.wait_for_timeout(5000)
    upload.Save()

@pytest.mark.functional
@pytest.mark.xfail(reason="Permite Ingresar caracteres alfanumericos e incluso simbolso en el campo de Track Name")
def test_TC006_Verificar_no_permita_ingresar_con_caracteres_alfanumericos_o_simbolos_en_el_campo_Name(page_with_session):
    upload = UploadPage(page_with_session)
    upload.open()
    file_path = "resources/audio/demo.mp3"
    upload.upload_audio_file(file_path)
    upload.assert_file_uploaded()
    upload.BotonSiguiente()
    upload.CamposObligatorios(
        nuevo_nombre="The Rock 123123113@@@e112412!#$%&/",
        genero_primera_opcion=True,
        artwork_busqueda="rock",
        tag_valor="juegos",
    )
    page_with_session.wait_for_timeout(5000)
    upload.Save()