from flask import (render_template, url_for,
                   redirect,Response, request, current_app)
from app import db
from app.models import HomePage, Project,Resume, Blog
from . import visitor
import pdfcrowd
import sys

@visitor.route("/", methods=["GET"])
def index():
    homepage = HomePage.query.one()
    projects = Project.query.all()
    image = homepage.picture
    return render_template(
        "visitor/home.html", 
        name=homepage.name,
        stack=homepage.stack,
        email=homepage.email,
        phone=homepage.phone,
        image=image,
        projects = projects
        )

@visitor.route("/resume", methods=["GET","POST"])
def resume():
    resume = Resume.query.filter_by(active=True).one()
    content = resume.content
    if request.method == "POST":
        render = render_template('visitor/resume.html', content=content)
        try:
            client = pdfcrowd.HtmlToPdfClient('mannye',current_app.config["PDFCROWD_API_KEY"])
            pdf = client.convertString(render)
            response = Response(pdf)
            response.headers['Content-Disposition'] = 'inline; filename="amanuel-ewnetu-resume.pdf"'
            response.headers['Content-Type'] = 'application/pdf'
            return response 
        except pdfcrowd.Error as why:
            return Response(why.getMessage(), status=why.getCode(), mimetype='text/plain')
    return render_template('visitor/resume.html',content=content)

@visitor.route('/blogs', methods=['GET'])
def blogs():
    blogs = Blog.query.all()
    return render_template('visitor/blog.html', blogs=blogs)
