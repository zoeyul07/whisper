import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.exten([BASE_DIR])

import pymysql
import flask import Blueprint, request, jsonify

series_app = Blueprint("series_app", __name__)
