# pages/myprofile_page.py
import re
from playwright.sync_api import Page, Locator, expect
from config.settings import MYPROFILE_URL, SIGNIN_URL
from playwright_helpers.locators import (
    any_of, text_exact, text_like, has_class, attr_contains, by_role
)


class MyProfilePage:
    def __init__(self, page: Page):
        self.page = page

        # ==== LOCATORS ====
        self.followers_btn: Locator = page.locator(
                any_of(
                    has_class("_stat_1onfy_1"),
                    has_class("_clickable_1onfy_51")
                )
            ).filter(has_text="Followers")

        self.following_btn: Locator = page.locator(
                any_of(
                    has_class("_stat_1onfy_1"),
                    has_class("_clickable_1onfy_51")
                )
            ).filter(has_text="Following")
        self.share_btn: Locator = page.locator(
            any_of(
                by_role("button"),                 # <button role="button">…
                has_class("harmony-8iy9dm")
            )
        ).filter(has_text="Share").first

        # ==== MODALES ESPERADOS ====
        self.modal_dialog: Locator = page.locator(by_role("dialog"))
        self.modal_followers: Locator = page.locator(text_like("Followers|followers"))
        self.modal_following: Locator = page.locator(text_like("Following|following"))
        self.modal_share: Locator = page.locator(
            text_like("Share this profile|Copy link|Embed")
        )

        # ==== CAMPOS DE EDICIÓN DE CANCIÓN ====
        self.save_button_edit_track: Locator = page.locator(
            any_of(
                'button[type="submit"]:has-text("Save Changes")',
                'button:has-text("Save Changes")',
                has_class("harmony-o8n1vb")  # fallback por clase inestable
            )
        ).first



        self.song_name_input: Locator = self.page.locator(
            any_of(
                attr_contains("name", "trackMetadata"),   # p.ej. trackMetadata.0.title
                attr_contains("aria-label", "Track Name") # accesible/visible
            )
        ).first

        self.titulo_edit_track: Locator = page.locator(text_exact("Edit Your Track")
        )
        self.boton_edit_track = page.locator('[aria-label="Edit Track"]').first


        self.error_message_vacio: Locator = page.locator(
            any_of(
#                'span[class*="harmony-"]',
                text_like("Your track must have a name")  # clase observada en tu captura
            )
        )
        self.error_message_de_form_error: Locator = page.locator(
            any_of(
#                'span[class*="harmony-"]',
                text_like("Fix errors to continue your update.")  # clase observada en tu captura
            )
        )



        self.toast_success: Locator = page.locator(
            any_of(
                '[role="status"]',
                has_class("toast"),
                text_like("saved|changes saved|updated|success")
            )
        )

        self.remove_picture_button_track = page.locator('[aria-label="Remove artwork"]').first      # ==== FOTO DE PERFIL ====

        self.save_profile_btn: Locator = page.locator(
            any_of(text_exact("Save Changes"), 'button:has-text("Save")')
        )
        self.toast_error: Locator = page.locator(
            text_like("no image selected|cannot upload|error")
        )

        # ==== AVATAR / PERFIL ====
        self.avatar_button: Locator = page.locator(
            '[href*="/@"], [aria-label*="profile"], img[alt*="profile"]'
        )
         # ==== LOCATORS ====
        self.edit_button: Locator = page.locator("(//button[@type='button'])[6]")  # Botón Edit Page
        self.name_input: Locator = page.locator("css=.\_name_j8o6f_1 > input")      # Campo Nombre
        self.description_input: Locator = page.locator("css=textarea")             # Campo Descripción
        self.save_button: Locator = page.locator("button.harmony-9tt3ib")          # Botón Save Changes
        self.toast_success: Locator = page.locator("text=Changes saved successfully")
        self.avatar_icon: Locator = page.locator('[data-testid="avatar-test"]')  # Imagen de perfil
        self.username_link: Locator = page.locator('a[href*="/@"]')  
        self.edit_name_button: Locator = page.locator("css=.css-1xaj4qh")         # Botón para activar el campo de nombre

        # ================== HELPERS (esperar visibilidad) ==================
        

    def _wait_visible(self, locator: Locator, timeout: int = 10000):
        """Espera a que el locator sea visible."""
        expect(locator).to_be_visible(timeout=timeout)

    def _click_when_visible(self, locator: Locator, timeout: int = 10000):
        """Espera a que sea visible y hace click."""
        self._wait_visible(locator, timeout)
        locator.click()



    # ==== MÉTODOS ====

    def open(self, username: str):
        """Abre directamente el perfil por nombre de usuario."""
        self.page.goto(f"{BASE_URL}/{username}")
        expect(self.followers_btn).to_be_visible(timeout=8000)

    def open_followers_modal(self):
        """Abre el modal de followers."""
        self._click_when_visible(self.followers_btn, timeout=10000)
        self._wait_visible(self.modal_dialog, timeout=10000)
        print("✅ Modal de Followers visible correctamente.")
    def open_following_modal(self):
        """Abre el modal de following."""

        self._click_when_visible(self.following_btn, timeout=10000)
        self._wait_visible(self.modal_dialog, timeout=10000)

        print("✅ Modal de Following visible correctamente.")

    def open_share_modal(self):
        """Abre el modal de compartir perfil."""
        self._click_when_visible(self.share_btn, timeout=10000)
        self._wait_visible(self.modal_dialog, timeout=10000)
        print("✅ Modal de compartir visible correctamente.")

    def open_track_for_edit(self):
        """Abre el primer track del perfil y espera la carga dinámica de la vista de edición."""
        # 1️⃣ Clic en el botón "Edit Track"
        self._click_when_visible(self.boton_edit_track)
        print("🖱️ Click en 'Edit Track' ejecutado correctamente.")

        # 2️⃣ Esperar a que cambie la URL o contenga '/edit'
        try:
            expect(self.page).to_have_url(re.compile(".*/edit.*"), timeout=15000)
            print("🌐 URL cambió a vista de edición.")
        except AssertionError:
            # Si no cambia la URL (SPA), continuar con espera por el formulario
            print("⚠️ No hubo navegación detectada (SPA). Esperando formulario...")

        # 3️⃣ Esperar el campo del nombre o el título de edición
        titulo = self.page.locator('h1:has-text("Edit Your Track")')
        input_nombre = self.page.locator('[aria-label*="Track Name"], [name*="trackMetadata"]')

        # 4️⃣ Esperar a que alguno esté visible (con fallback progresivo)
        try:
            expect(titulo.or_(input_nombre)).to_be_visible(timeout=15000)
            print("🎵 Vista de edición cargada correctamente.")
        except AssertionError:
            # Último intento: esperar el botón "Save Changes"
            boton_save = self.page.locator('button:has-text("Save Changes")')
            expect(boton_save).to_be_visible(timeout=5000)
            print("✅ Confirmada carga del formulario de edición (por botón Save Changes).")











    def edit_song_name(self, new_name: str):
        """Simula la edición del nombre de una canción."""
        self._wait_visible(self.song_name_input, timeout=10000)
        self.song_name_input.fill(new_name)
        self._click_when_visible(self.save_button_edit_track, timeout=10000)


    def try_empty_song_name(self):
        """Intenta guardar con campo vacío."""
        self.edit_song_name("")
        self._wait_visible(self.error_message_vacio, timeout=10000)
        print("⚠️ No se permite guardar con nombre vacío.")

    def try_blank_song_name(self):
        """Intenta guardar con solo la tecla espacio."""
        self.edit_song_name("                                         ")
        self._wait_visible(self.error_message_vacio, timeout=10000)
        print("⚠️ No se permite guardar con espacios vacíos.")

    def try_save_empty_profile_picture(self):
        """Intenta guardar sin imagen cargada."""
        expect(self.remove_picture_button_track).to_be_visible(timeout=10000)
        expect(self.remove_picture_button_track).to_be_enabled(timeout=10000)
        self.remove_picture_button_track.click()
        self.save_button_edit_track.click()
        #self._wait_visible(self.error_message_de_form_error, timeout=10000)

        print("⚠️ Se guardó la foto de perfil vacía.")

    def go_to_my_profile(self):
        """Abre el perfil del usuario desde el avatar en 'Your Feed'."""
        expect(self.avatar_button).to_be_visible(timeout=8000)
        self.avatar_button.click()
        expect(self.page.locator('text=Followers')).to_be_visible(timeout=10000)
        print("✅ Navegación a 'My Profile' exitosa desde 'Your Feed'.")

    def open_edit_mode(self):
        """Abre el modo de edición de perfil."""
        expect(self.edit_button).to_be_visible(timeout=10000)
        self.edit_button.click()
        print("✏️ Modo edición activado.")

    def editar_nombre(self, nuevo_nombre: str):
        """Activa el campo de nombre y lo edita."""
        expect(self.edit_name_button).to_be_visible(timeout=10000)
        self.edit_name_button.click()
        print("🧩 Campo de nombre activado.")

        expect(self.name_input).to_be_visible(timeout=10000)
        self.name_input.fill("")
        self.name_input.type(nuevo_nombre)
        print(f"🧾 Nuevo nombre ingresado: {nuevo_nombre}")

    def editar_descripcion(self, nueva_descripcion: str):
        """Edita la descripción del perfil."""
        expect(self.description_input).to_be_visible(timeout=10000)
        self.description_input.fill("")
        self.description_input.type(nueva_descripcion)
        print(f"📝 Descripción actualizada a: {nueva_descripcion}")

    def guardar_cambios(self):
        """Hace clic en Save Changes y valida el resultado."""
        expect(self.save_button).to_be_visible(timeout=10000)
        self.save_button.click()
        print("💾 Clic en 'Save Changes' realizado.")    

    def open_profile(self):
    
        """Abre la página My Profile del usuario (USERNAME de .env) y maneja el modal si aparece."""
        self.page.goto(MYPROFILE_URL, wait_until="domcontentloaded")

        if self.page.url.startswith(SIGNIN_URL):
            raise RuntimeError("❌ No hay sesión iniciada. Inicia sesión antes de abrir My Profile.")

        self._wait_visible(self.edit_button, timeout=10000)


    def validar_mensaje(self, texto: str, timeout=5000) -> bool:
   
        try:
            locator = self.page.locator(f"text={texto}")
            expect(locator).to_be_visible(timeout=timeout)
            print(f"✅ Mensaje visible: '{texto}'")
            return True
        except Exception:
            print(f"❌ No se encontró el mensaje: '{texto}'")
            return False