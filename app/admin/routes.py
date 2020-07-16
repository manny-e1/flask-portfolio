from flask import (render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from app import db
from app.models import Blog, Project, Resume, User, HomePage
from app.admin.forms import BlogForm,ProjectForm,ResumeForm,HomepageForm
from cloudinary.uploader import upload
from app.decorators import isAdmin
from . import admin




@admin.route("/users", methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template('admin/userslist.html', users=users)


@admin.route("/blog/new", methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()   
    if request.method == 'POST':   
        if form.validate_on_submit():
            upload(form.picture.data)
            blog = Blog(title=form.title.data, description=form.description.data,
                 content=form.content.data,picture=picture['url'], author=current_user)
            db.session.add(blog)
            db.session.commit()
            flash('Your blog has been created!', 'success')
            return redirect(url_for('admin.index'))
    return render_template('admin/blogcrud.html', title='Add Blog',
                           form=form, legend='New Blog')


@admin.route("/blogs", methods=["GET"])
@login_required
def blogs():
    blogs = Blog.query.all()
    return render_template('admin/bloglist.html',title='Blogs', blogs=blogs)

@admin.route("/blog/<int:blog_id>", methods=["GET","POST"])
@login_required
def blog(blog_id):
    form = BlogForm()
    blog = Blog.query.get_or_404(blog_id)
    if request.method == 'POST':  
        if form.validate_on_submit():
            blog.title = form.title.data
            blog.content = form.content.data
            blog.description = form.description.data
            if form.picture.data:
                picture = upload(form.picture.data)
                blog.image = picture['url']
                flash('image has been updated.','info')
            db.session.commit()
            flash('Your blog has been updated!', 'success')
            return redirect(request.referrer)
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
        form.description.data = blog.description
    return render_template('admin/blogcrud.html', title='Update Blog', blog=blog,form=form)


@admin.route("/blog/delete/<int:blog_id>", methods=["GET","POST"])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('admin.blogs'))

@admin.route("/project/new", methods=['GET', 'POST'])
@login_required
@isAdmin
def new_project():
    form = ProjectForm()   
    if request.method == 'POST':
        if form.validate_on_submit():
            picture = upload(form.picture.data)
            project = Project(title=form.title.data, description=form.description.data,
                 link=form.link.data,image=picture['url'], author=current_user)
            db.session.add(project)
            db.session.commit()
            flash('Your blog has been created!', 'success')
            return redirect(url_for('admin.index'))
    return render_template('admin/projectcrud.html', title='Add Project',
                           form=form, legend='New Project')


@admin.route("/projects", methods=["GET"])
@login_required
def projects():
    projects = Project.query.all()
    return render_template('admin/projectlist.html', projects=projects)


@admin.route("/project/<int:project_id>", methods=["GET","POST"])
@login_required
def project(project_id):
    form = ProjectForm()
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':  
        if form.validate_on_submit():
            if form.picture.data:
                picture = upload(form.picture.data)
                project.image = picture['url']
                flash('Project\'s image has been updated.','info')
            project.username = form.title.data
            project.description = form.description.data 
            project.link = form.link.data
            flash('Project has been updated.','info')
            db.session.commit()
            return redirect(request.referrer)
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.link.data = project.link
    return render_template('admin/projectcrud.html', title='Update Project', project=project,form=form)

@admin.route("/project/delete/<int:project_id>", methods=["GET","POST"])
@login_required
@isAdmin
def delete_project(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('admin.projects'))



@admin.route("/resumes", methods=["GET"])
@login_required
def resumes():
    resumes = Resume.query.all()
    return render_template('admin/resumelist.html', resumes=resumes)


@admin.route("/resume/new", methods=['GET', 'POST'])
@login_required
@isAdmin
def new_resume():
    form = ResumeForm() 
    title = "Add"
    if request.method == 'POST':   
        if form.validate_on_submit():
            resume = Resume(name=form.name.data,content=form.content.data, author=current_user)
            db.session.add(resume)
            db.session.commit()
            flash('Your resume has been created!', 'success')
            return redirect(url_for('admin.index'))
    return render_template('admin/resumecrud.html', title=f'{title} Resume',
                           form=form, legend=f'{title} Resume')


@admin.route('/resume/update/<int:resume_id>', methods=['GET','POST'])
@login_required
@isAdmin
def update_resume(resume_id):
    title = "Update"
    resume = Resume.query.get_or_404(resume_id)
    form = ResumeForm() 
    if request.method == 'POST':  
        if form.validate_on_submit():
            if form.content.data != resume.content:
                resume.content = form.content.data
                db.session.commit()
                flash('Resume has been updated.','info')
            return redirect(request.referrer)
    elif request.method == 'GET':
        form.name.data = resume.name
        form.content.data = resume.content
    return render_template('admin/resumecrud.html', title=f'{title} Resume',
                           form=form, legend=f'{title} Resume', resume=resume)


@admin.route("/resume/delete/<int:resume_id>", methods=["GET","POST"])
@login_required
@isAdmin
def delete_resume(resume_id):
    resume = Resume.query.get(resume_id)
    db.session.delete(resume)
    db.session.commit()
    return redirect(url_for('admin.resumes'))

@admin.route("/resume/acitve/<int:resume_id>", methods=["GET","POST"])
@login_required
@isAdmin
def active_resume(resume_id):
    resume = Resume.query.get(resume_id)
    activated = Resume.query.filter_by(active=True).all()
    for res in activated:
        res.active = False
    resume.active = True
    db.session.commit()
    return redirect(url_for('admin.resumes'))

@admin.route('/for_homepage', methods=['GET', 'POST'])
@login_required
@isAdmin
def for_homepage():
    form = HomepageForm()
    homepage = HomePage.query.get(1)
    if homepage is None:
        if request.method == "POST" and form.validate_on_submit():
            picture = upload(form.picture.data)
            homepage = HomePage(name=form.name.data,
                        stack=form.stack.data,phone=form.phone.data,
                        email=form.email.data,picture=picture['url'])
            db.session.add(homepage)
            db.session.commit()
            flash('Homepage data has been created.','info')
            return redirect(request.referrer)
    if homepage is not None: 
        if request.method == "POST" and form.validate_on_submit():
            homepage.name = form.name.data
            homepage.stack = form.stack.data
            homepage.phone = form.phone.data
            homepage.email = form.email.data
            if form.picture.data:
                picture = upload(form.picture.data)
                homepage.image = picture['url']
                flash('image has been updated.','info')
            db.session.commit()
            return redirect(request.referrer)
        else:
            form.name.data = homepage.name
            form.stack.data = homepage.stack
            form.phone.data = homepage.phone
            form.email.data = homepage.email
    return render_template('admin/for_homepage.html', title='Homepage Data', homepage=homepage,form=form)
    
    