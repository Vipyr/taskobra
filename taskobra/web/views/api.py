from flask import Blueprint, render_template, request, redirect, url_for, current_app


blueprint = Blueprint('api', __name__, url_prefix='/api')

