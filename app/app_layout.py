# import ssl
from time import sleep
from flet import (
    ButtonStyle,
    Column,
    Container,
    Control,
    Page,
    Row,
    Text,
    padding,
)
import requests
from sidebar import Sidebar
import urllib3
import flet as ft
import json
import os
from dotenv import load_dotenv
load_dotenv()


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.sidebar = Sidebar(self, page)

        self._active_view: Control = self.fetch_data()

        # event when changed textfield values
        def textfield_change(e):
            if company_name_textfield.value == "" or contract_name_textfield.value == "":
                submit_button.disabled = True
            else:
                submit_button.disabled = False
            self.page.update()

        # display Message to fail create new customer
        msg_failed_add_customer = Row(
            [
                ft.Text("Sorry... Failed to send new customer. Retry Access few minutes Later.",
                        size=24, color=ft.colors.RED_500
                        )
            ],
            visible=False
        )

        # display Message to success create new customer
        msg_success_add_customer = Row(
            [
                ft.Text("Success to create new customer!",
                        size=24, color=ft.colors.BLUE_900,
                        )
            ],
            visible=False
        )

        # click submit button
        def button_clicked(e):
            if (len(company_name_textfield.value) == 0 or len(contract_name_textfield.value) == 0):
                page.update()
                return
            # create POST request
            try:
                url = os.getenv('WORKERS_URL')
                data = {
                    'CompanyName': company_name_textfield.value,
                    'ContactName': contract_name_textfield.value,
                }
                data_encode = json.dumps(data)
                requests.post(url, data=data_encode)
                # clear input values
                company_name_textfield.value = ""
                contract_name_textfield.value = ""
                submit_button.disabled = True
                msg_failed_add_customer.visible = False
                msg_success_add_customer.visible = True
                page.update()
                sleep(1)
                page.go('/')
                msg_success_add_customer.visible = False
            except Exception as e:
                print(e)
                msg_failed_add_customer.visible = True
                page.update()

        # text fields
        company_name_textfield = ft.TextField(
            label="Company Name", on_change=textfield_change)
        contract_name_textfield = ft.TextField(
            label="Contract Name", on_change=textfield_change)

        # button to add customer
        submit_button = ft.ElevatedButton(
            disabled=True,
            text="Submit", on_click=button_clicked)

        # define layout
        self.members_view = Column([
            Container(
                Text
                (
                    value="Add New Customers",
                    style=ft.FontWeight.W_500,
                    size=28
                ),
                expand=False,
                padding=padding.only(top=15),
            ),
            Row(
                [
                    Container(
                        Text(value="Company Name"),
                        width=150,
                        expand=False,
                        padding=padding.only(left=10),
                    ),
                    company_name_textfield
                ]
            ),
            Row(
                [
                    Container(
                        Text(value="Contract Name"),
                        width=150,
                        expand=False,
                        padding=padding.only(left=10),
                    ),
                    contract_name_textfield
                ]
            ),
            msg_failed_add_customer,
            msg_success_add_customer,
            Row(
                [
                    submit_button
                ]
            ),
        ]
        )

        self.controls = [self.sidebar, self.active_view]

    @ property
    def active_view(self):
        return self._active_view

    @ active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.sidebar.sync_board_destinations()
        self.update()

    def fetch_data(self):
        # display Error Message to fail get customers
        data_rows = []
        msg_failed_get_customers = Row(
            [
                ft.Text("Sorry... Failed to get customers. Retry Access few minutes Later.",
                        size=20, color=ft.colors.RED_500
                        )
            ],
            visible=False
        )
        # cloudflare workersからデータ取得
        try:
            msg_failed_get_customers.visible = False
            url = os.getenv('WORKERS_URL')
            response = requests.get(url)
            result = response.json()
            for customer in result:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(customer['CustomerId']))),
                        ft.DataCell(ft.Text(customer['CompanyName'])),
                        ft.DataCell(ft.Text(customer['ContactName'])),
                    ],
                )
                data_rows.append(row)
        except Exception as e:
            print(e)
            msg_failed_get_customers.visible = True

        return Column([
              Row(
                [Container(
                    Text(value="Current Customers",
                        style="headlineMedium"),
                    expand=True,
                    padding=padding.only(top=15),
                )],
            ),
            msg_failed_get_customers,
            Container(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(
                            ft.Text("CompanyId")),
                        ft.DataColumn(ft.Text("CompanyName")),
                        ft.DataColumn(ft.Text("ContactName")),
                    ],
                    rows=list(data_rows),
                    visible=len(data_rows) > 0,
                ),
                expand=False
            )])

    def set_all_boards_view(self):
        # 初回と2回名
        self.active_view = self.fetch_data()
        self.hydrate_all_boards_view()
        self.sidebar.top_nav_rail.selected_index = 0
        self.sidebar.bottom_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    # add member view
    def set_members_view(self):
        self.active_view = self.members_view
        self.sidebar.top_nav_rail.selected_index = 1
        self.sidebar.bottom_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    def hydrate_all_boards_view(self):
        self.sidebar.sync_board_destinations()
