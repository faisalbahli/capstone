import os
from os import environ as env
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.utils import redirect
from models import Menu, setup_db, Drink
from auth import AuthError, requires_auth
from dotenv import load_dotenv

load_dotenv()

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
API_AUDIENCE = os.getenv('API_AUDIENCE')

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = os.getenv('ThisIsTheSecretKey')
app.debug = True

app = Flask(__name__)
setup_db(app)
CORS(app)


## ROUTES

@app.route('/')
def index():
  return""" <p><span style="font-size: 44px;">Welcome</span></p><p>There are two created accounts assigned with two roles in this project:</p>
<p><strong>1- Manager (Authorized to all actions and endpoints)</strong></p>
<ul>
    <li>Email : barista.role@gmail.com</li>
    <li>Password: Capstone@1</li>
</ul>
<p><br></p>
<p>Permissions for Manager:</p>
<table class="MuiTable-root" data-cosmos-key="table" style='box-sizing: inherit; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: inherit; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; border-spacing: 0px; border-collapse: collapse; width: 1000px; display: table; min-width: 400px; color: rgb(30, 33, 42); letter-spacing: 0.14994px; orphans: 2; text-align: start; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;'>
    <thead class="MuiTableHead-root" data-cosmos-key="table.header" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; display: table-header-group;">
        <tr class="MuiTableRow-root MuiTableRow-head" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss1972" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; width: 69.1649%; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42);'><span aria-disabled="false" class="MuiButtonBase-root MuiTableSortLabel-root MuiTableSortLabel-active" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); cursor: pointer; display: inline-flex; outline: 0px; position: relative; align-items: center; user-select: none; border-radius: 0px; justify-content: flex-start; text-decoration: none; background-color: transparent; appearance: none; -webkit-tap-highlight-color: transparent; flex-direction: inherit;" tabindex="0">Permission</span></th>
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss1973" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Description</th>
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss1974" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></th>
        </tr>
    </thead>
    <tbody class="MuiTableBody-root" data-cosmos-key="table.body" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; display: table-row-group;">
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss1926 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>delete:drinks</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Remove drinks</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss1926 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>get:drinks-detail</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Get details about drink</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss1926 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>patch:drinks</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Modify drinks</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss1926 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>post:drinks</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Create new drink</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss1926 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>post:menu</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>create new menu</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
    </tbody>
</table>
<p><br></p>
<p><br></p>
<p><strong>2- Barista (Authorized to only GET /drinks-detail endpoint)</strong></p>
<ul>
    <li>Email : barista.role@gmail.com</li>
    <li>Password: Capstone@1</li>
</ul>
<p>Permissions for Barista:</p>
<table class="MuiTable-root" data-cosmos-key="table" style='box-sizing: inherit; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: inherit; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; border-spacing: 0px; border-collapse: collapse; width: 1000px; display: table; min-width: 400px; color: rgb(30, 33, 42); letter-spacing: 0.14994px; orphans: 2; text-align: start; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;'>
    <thead class="MuiTableHead-root" data-cosmos-key="table.header" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; display: table-header-group;">
        <tr class="MuiTableRow-root MuiTableRow-head" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss2108" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; width: 69.1649%; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42);'><span aria-disabled="false" class="MuiButtonBase-root MuiTableSortLabel-root MuiTableSortLabel-active" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); cursor: pointer; display: inline-flex; outline: 0px; position: relative; align-items: center; user-select: none; border-radius: 0px; justify-content: flex-start; text-decoration: none; background-color: transparent; appearance: none; -webkit-tap-highlight-color: transparent; flex-direction: inherit;" tabindex="0">Permission</span></th>
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss2109" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Description</th>
            <th aria-sort="ascending" class="MuiTableCell-root MuiTableCell-head jss2 jss2110" scope="col" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 500; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 8px 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></th>
        </tr>
    </thead>
    <tbody class="MuiTableBody-root" data-cosmos-key="table.body" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; display: table-row-group;">
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 69.1649%;'><code class="MuiTypography-root jss58 jss2062 MuiTypography-colorTextPrimary" data-cosmos-key="code" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.5; font-family: "Roboto Mono", monospace; border: 0px; margin: 0px; padding: 2px 6px; font-size: 0.75rem; vertical-align: baseline; font-variant-numeric: slashed-zero; color: rgb(30, 33, 42); letter-spacing: 0.02083em; display: inline; border-radius: 4px; background-color: rgb(239, 240, 242);'>get:drinks-detail</code></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 22.9122%;'>Get details about drink</td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42); width: 7.9229%;'><br></td>
        </tr>
    </tbody>
</table>
<p><br></p>
<table class="MuiTable-root" data-cosmos-key="table" style='box-sizing: inherit; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: inherit; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; border-spacing: 0px; border-collapse: collapse; width: 1000px; display: table; min-width: 400px; color: rgb(30, 33, 42); letter-spacing: 0.14994px; orphans: 2; text-align: start; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;'>
    <tbody class="MuiTableBody-root" data-cosmos-key="table.body" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: baseline; font-variant-numeric: slashed-zero; display: table-row-group;">
        <tr class="MuiTableRow-root" data-cosmos-key="table.row" style="box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; border: 0px; margin: 0px; padding: 0px; font-size: 14px; vertical-align: middle; font-variant-numeric: slashed-zero; color: inherit; display: table-row; outline: 0px; transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;">
            <td class="MuiTableCell-root MuiTableCell-body " style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42);'><br></td>
            <td class="MuiTableCell-root MuiTableCell-body" style='box-sizing: inherit; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-east-asian: inherit; font-weight: 400; font-stretch: inherit; line-height: 1.6; font-family: Inter, fakt-web, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; border-width: 0px 0px 1px; border-top-style: initial; border-right-style: initial; border-bottom-style: solid; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: rgb(227, 228, 230); border-left-color: initial; border-image: initial; margin: 0px; padding: 16px; font-size: 0.875rem; vertical-align: inherit; font-variant-numeric: slashed-zero; display: table-cell; text-align: left; letter-spacing: 0.01071em; color: rgb(30, 33, 42);'><br></td>
        </tr>
    </tbody>
</table>
<p>The following endpoints are in the app:</p>
<ol>
    <li>/drinks (GET)</li>
    <li>/drinks (POST)</li>
    <li>/drinks-detail (GET)</li>
    <li>/drinks/&lt;id&gt; (PATCH)</li>
    <li>/drinks/&lt;id&gt; (DELETE)</li>
</ol>
<p>There is extra endpoint to get authorized and get the access token from the URL to test it if needed in Postman, which is:</p>
<ul>
    <li>authorization/url (GET)</li>
</ul>
<p><br></p>
  """

@app.route('/authorization/url', methods=['GET'])
def generate_auth_url():
  url = f'https://{AUTH0_DOMAIN}/authorize' \
    f'?audience={API_AUDIENCE}' \
    f'&response_type=token&client_id=' \
    f'{AUTH0_CLIENT_ID}&redirect_uri=' \
    f'{AUTH0_CALLBACK_URL}'
  return redirect(url, code=302)

@app.route('/drinks')
def get_drinks_with_short_info():
    
    drinks = list(map(Drink.long, Drink.query.all()))
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200



@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_with_long_info(jwt):

    drinks = list(map(Drink.long, Drink.query.all()))
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200



@app.route('/drinks', methods =['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = dict(request.json)
    print("body: ", body)
    try:
            drink_data = json.loads(request.data.decode('utf-8'))
            drink = Drink(
                title=drink_data['title'],
                recipe=json.dumps(drink_data['recipe'])
                )
            drink.insert()
            drinks = Drink.query.all()
            formatted_drinks = [drink.long() for drink in drinks]
            return jsonify({
                "success" : True,
                "drinks": [formatted_drinks]
            }), 200
       
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<id>', methods =['PATCH'])
@requires_auth('patch:drinks')
def modify_drink(jwt, id):
    body = dict(request.json)
    try:
        if body.get('title') or body.get('recipe'):
            drink_data = json.loads(request.data.decode('utf-8'))
            
            title = drink_data['title'],
            recipe = json.dumps(drink_data['recipe'])
                
            drink = Drink.query.get(id)
            if drink is None:
                abort(404)
            
            drink.title = title
            drink.recipe = recipe

            drink.update()
            drinks = Drink.query.all()
            formatted_drinks = [drink.long() for drink in drinks]
            return jsonify({
                "success" : True,
                "drinks": [formatted_drinks]
            }), 200
        else:
            abort(422)
    except Exception as e:
        print(e)
        abort(422)

@app.route('/drinks/<id>', methods =['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)
            
        drink.delete()
        return jsonify({
         'success': True,
         'delete': id,
        }), 200
    except Exception as e:
        print(e)
        abort(422)


@app.route('/menus', methods =['POST'])
@requires_auth('post:menu')
def create_menu(jwt):
  body = dict(request.json)
  print("body: ", body)
  try:
      menu_data = json.loads(request.data.decode('utf-8'))
      print("menu data: ", menu_data )
      print(menu_data['name'])
      menu = Menu(name=menu_data['name'])
      menu.insert()
      menus = Menu.query.all()
      formatted_menus = [menu.get_menu_name() for menu in menus]
      return jsonify({
              "success" : True,
              "menus": [formatted_menus]
          }), 200
      
  except Exception as e:
      print(e)
      abort(422)

## Error Handling
@app.errorhandler(404)
def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found',
          }), 404

@app.errorhandler(422)
def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable',
          }), 422
          
@app.errorhandler(400)
def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request',
          }), 400

@app.errorhandler(405)
def method_not_found(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed',
          }), 405    

## AUTH Error
@app.errorhandler(AuthError)
def auth_error(AuthError):
    return jsonify({
          'success': False,
          'error': AuthError.status_code,
          'message': AuthError.error['code'],
          }),    

