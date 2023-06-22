import flet as ft
from app_layout import AppLayout
from flet import (
    AlertDialog,
    AppBar,
    Column,
    Container,
    ElevatedButton,
    Icon,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    TemplateRoute,
    Text,
    TextField,
    UserControl,
    View,
    colors,
    icons,
    margin,
    padding,
    theme,
)
from user import User


class CloudflareD1(UserControl):
    def __init__(self, page: Page,):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change
        self.login_profile_button = PopupMenuItem(
            text="Log in", )
        # on_click=self.login
        self.appbar_items = [
            self.login_profile_button,
            PopupMenuItem(),  # divider
            PopupMenuItem(text="XXXX"),
        ]
        self.appbar = AppBar(
            leading=Icon(ft.icons.CLOUD_CIRCLE_OUTLINED, size=32),
            leading_width=100,
            title=Text(f"cloudflare Workers&D1 Tutorial"  # font_family="Pacifico"
                       , size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.colors.ORANGE_300,
            actions=[
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        return self.layout

    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [self.appbar, self.layout],
                padding=padding.all(0),
                bgcolor=colors.BLUE_GREY_200,
            )
        )
        self.page.update()
        self.page.go("/")

    def login(self, e):
        def close_dlg(e):
            if user_name.value == "" or password.value == "":
                user_name.error_text = "Please provide username"
                password.error_text = "Please provide password"
                self.page.update()
                return
            else:
                user = User(user_name.value, password.value)
                if user not in self.store.get_users():
                    self.store.add_user(user)
                self.user = user_name.value
                self.page.client_storage.set("current_user", user_name.value)

            dialog.open = False
            self.appbar_items[0] = PopupMenuItem(
                text=f"{self.page.client_storage.get('current_user')}'s Profile"
            )
            self.page.update()

        user_name = TextField(label="User name")
        password = TextField(label="Password", password=True)
        dialog = AlertDialog(
            title=Text("Please enter your login credentials"),
            content=Column(
                [
                    user_name,
                    password,
                    ElevatedButton(text="Login", on_click=close_dlg),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/boards")
        elif troute.match("/boards"):
            self.layout.set_all_boards_view()
        elif troute.match("/members"):
            self.layout.set_members_view()
        self.page.update()


def main(page: Page):

    page.title = "cloudflare Workers&D1 Tutorial"
    page.padding = 0
    page.theme = theme.Theme(font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    # page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    page.bgcolor = colors.BLUE_GREY_200
    app = CloudflareD1(page)
    page.add(app)
    page.update()
    app.initialize()


# ft.app(target=main, assets_dir="../assets")
# ft.app(target=main, assets_dir="../assets")
ft.app(target=main, port=8080, view=ft.WEB_BROWSER)
