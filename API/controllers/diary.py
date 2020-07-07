import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pymysql
from flask import Blueprint, jsonify, request

diary_app = Blueprint("diary", __name__)

