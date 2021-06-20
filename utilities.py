import os
from datetime import date, datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId


def get_post(user_pronouns, username, user_id):
    post_type = request.form['post_type']

    if post_type == "general":
        post = general_post(user_pronouns, username, user_id, post_type)
        return post

    elif post_type == "code":
        post = code_post(user_pronouns, username, user_id, post_type)
        return post

    elif post_type == "review":
        post = review_post(user_pronouns, username, user_id, post_type)
        return post

    else:
        flash("Ops that type is unknown please try")


def general_post(user_pronouns, username, user_id, post_type):

    post_date = datetime.now().strftime('%d/%m/%y, %H:%M')
    post_input = request.form['post_input']
    post_title = request.form['post_title']
    post_id = ObjectId()

    post = {
        '_id': post_id,
        'date': post_date,
        'post_title': post_title,
        'author': username + " " + user_pronouns,
        'user_id': user_id,
        'username': username,
        'post_input': post_input,
        'post_type': post_type,
        'comments': []
    }
    return post


def code_post(user_pronouns, username, user_id, post_type):

    post_date = datetime.now().strftime('%d/%m/%y, %H:%M')
    post_input = request.form['post_input']
    post_title = request.form['post_title']
    code_pen = request.form['code_pen']
    post_id = ObjectId()

    post = {
        '_id': post_id,
        'date': post_date,
        'post_title': post_title,
        'author': username + " " + user_pronouns,
        'user_id': user_id,
        'username': username,
        'post_input': post_input,
        'post_type': post_type,
        'code_pen': code_pen,
        'comments': []
    }
    return post


def review_post(user_pronouns, username, user_id, post_type):

    post_date = datetime.now().strftime('%d/%m/%y, %H:%M')
    post_input = request.form['post_input']
    post_title = request.form['post_title']
    github = request.form['github']
    deployed = request.form['deployed']
    post_id = ObjectId()

    post = {
        '_id': post_id,
        'date': post_date,
        'post_title': post_title,
        'author': username + " " + user_pronouns,
        'username': username,
        'user_id': user_id,
        'post_input': post_input,
        'post_type': post_type,
        'deployed': deployed,
        'github': github,
        'comments': []
    }
    return post


def update_post():
    post_type = request.form['post_type']

    if post_type == "general":
        post_edit = edit_general_post()
        return post_edit

    elif post_type == "code":
        post_edit = edit_code_post()
        return post_edit

    elif post_type == "review":
        post_edit = edit_review_post()
        return post_edit

    else:
        flash("Ops that type is unknown please try")


def edit_general_post():

    post_input = request.form['post_input']
    post_title = request.form['post_title']

    edit_post = {
        'post_title': post_title,
        'post_input': post_input,
    }
    return edit_post


def edit_code_post():
    post_input = request.form['post_input']
    post_title = request.form['post_title']
    code_pen = request.form['code_pen']

    edit_post = {
        'post_title': post_title,
        'post_input': post_input,
        'code_pen': code_pen,

    }
    return edit_post


def edit_review_post():

    post_input = request.form['post_input']
    post_title = request.form['post_title']
    github = request.form['github']
    deployed = request.form['deployed']
    
    edi_post = {
        'post_title': post_title,
        'post_input': post_input,
        'deployed': deployed,
        'github': github,
    }
    return edit_post

