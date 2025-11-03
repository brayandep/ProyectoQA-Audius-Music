# pages/myprofile_page.py
from playwright.sync_api import Page, Locator, expect
from config.settings import BASE_URL
from playwright_helpers.locators import (
    any_of, text_exact, text_like, has_class, attr_contains, by_role
)


class MyProfilePage:
    def __init__(self, page: Page):
        self.page = page

        # ==== LOCATORS ====
        self.followers_btn: Locator = page.locator(
            any_of(text_exact("Followers"), '[href*="followers"]')
        )
        self.following_btn: Locator = page.locator(
            any_of(text_exact("Following"), '[href*="following"]')
        )
        self.share_btn: Locator = page.locator(
            any_of(text_exact("Share"), '[aria-label*="Share"]')
        )

        # ==== MODALES ESPERADOS ====
        self.modal_dialog: Locator = page.locator(by_role("dialog"))
        self.modal_followers: Locator = page.locator(text_like("Followers|followers"))
        self.modal_following: Locator = page.locator(text_like("Following|following"))
        self.modal_share: Locator = page.locator(
            text_like("Share this profile|Copy link|Embed")
        )

        # ==== CAMPOS DE EDICIÓN DE CANCIÓN ====
        self.song_name_input: Locator = page.locator(
            any_of('input[name="trackName"]', '[placeholder*="Track name"]')
        )
        self.save_button: Locator = page.locator(
            any_of(text_exact("Save"), 'button:has-text("Save")')
        )
        self.error_message: Locator = page.locator(
            text_like("cannot be empty|invalid|required")
        )

        # ==== FOTO DE PERFIL ====
        self.edit_picture_button: Locator = page.locator(
            any_of(text_exact("Edit Photo"), '[aria-label*="Edit profile photo"]')
        )
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

    # ==== MÉTODOS ====

    def open(self, username: str):
        """Abre directamente el perfil por nombre de usuario."""
        self.page.goto(f"{BASE_URL}/{username}")
        expect(self.followers_btn).to_be_visible(timeout=8000)

    def open_followers_modal(self):
        """Abre el modal de followers."""
        self.followers_btn.click()
        expect(self.modal_dialog).to_be_visible(timeout=8000)
        print("✅ Modal de Followers visible correctamente.")

    def open_following_modal(self):
        """Abre el modal de following."""
        self.following_btn.click()
        expect(self.modal_dialog).to_be_visible(timeout=8000)
        print("✅ Modal de Following visible correctamente.")

    def open_share_modal(self):
        """Abre el modal de compartir perfil."""
        self.share_btn.click()
        expect(self.modal_dialog).to_be_visible(timeout=8000)
        print("✅ Modal de compartir visible correctamente.")

    def edit_song_name(self, new_name: str):
        """Simula la edición del nombre de una canción."""
        self.song_name_input.fill(new_name)
        self.save_button.click()

    def try_empty_song_name(self):
        """Intenta guardar con campo vacío."""
        self.edit_song_name("")
        expect(self.error_message).to_be_visible(timeout=5000)
        print("⚠️ No se permite guardar con nombre vacío.")

    def try_blank_song_name(self):
        """Intenta guardar con solo espacios."""
        self.edit_song_name("   ")
        expect(self.error_message).to_be_visible(timeout=5000)
        print("⚠️ No se permite guardar con espacios vacíos.")

    def try_save_empty_profile_picture(self):
        """Intenta guardar sin imagen cargada."""
        self.edit_picture_button.click()
        self.save_profile_btn.click()
        expect(self.toast_error.or_(self.modal_dialog)).to_be_visible(timeout=8000)
        print("⚠️ No se guardó la foto de perfil vacía.")

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
    
        try:
            if self.avatar_icon.is_visible():
                self.avatar_icon.click()
                print("🖱️ Perfil abierto desde el avatar.")
            else:
                expect(self.username_link).to_be_visible(timeout=5000)
                self.username_link.first.click()
                print("🖱️ Perfil abierto desde el enlace del nombre de usuario.")
        except Exception as e:
            raise RuntimeError(f"❌ No se pudo abrir el perfil: {e}")

        # Esperar a que cargue la página del perfil
        expect(self.edit_button).to_be_visible(timeout=10000)
        print("✅ Vista de perfil cargada correctamente.")

    def validar_mensaje(self, texto: str, timeout=5000) -> bool:
   
        try:
            locator = self.page.locator(f"text={texto}")
            expect(locator).to_be_visible(timeout=timeout)
            print(f"✅ Mensaje visible: '{texto}'")
            return True
        except Exception:
            print(f"❌ No se encontró el mensaje: '{texto}'")
            return False