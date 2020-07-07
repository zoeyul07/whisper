import os
import sys
import pymysql

from flask import Blueprint, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

user_app = Blueprint('user', __name__)
