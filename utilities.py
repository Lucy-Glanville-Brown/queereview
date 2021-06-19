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
        'post_input': post_input,
        # 'img_url': user_session['image_url'],
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
        'post_input': post_input,
        # 'img_url': user_session['image_url'],
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
        'user_id': user_id,
        'post_input': post_input,
        # 'img_url': user_session['image_url'],
        'post_type': post_type,
        'deployed' : deployed,
        'github' : github,
        'comments': []
    }

    return post
