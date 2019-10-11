from flask import render_template, request, redirect, Blueprint, session, url_for, flash, Markup,Request

main = Blueprint('main',__name__)

@main.route("/") 
@main.route("/home") 
def home(): 
	return render_template('index.html',)

