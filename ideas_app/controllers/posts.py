from ideas_app import app
from ideas_app.models.user import *
from ideas_app.models.post import *
from ideas_app.models import *
from ideas_app.controllers import users
from flask import render_template, redirect, request, session,url_for

@app.route('/bright_ideas/delete/<int:id>')
def delete_post(id):
    data ={
        'id': id
    }
    Post.destroy(data)
    flash(f"Post #{id} has been deleted succesfully :D")
    return redirect('/bright_ideas')

@app.route('/bright_ideas/like/<int:id>')
def like_post(id):
    data ={
        'user_id': session.get("id"),
        'idea_id':id
    }
    print("POST GET AMOUNT OF LIKES ", Post.get_amount_of_likes(id))
    if Post.get_likes_by_id(id) is tuple:
        Post.like(data)
    else:
        amount = Post.get_amount_of_likes(id)
        print("\nAMOUNT",amount)
        Post.update_like(id)
    print("POST LIKE DATAAAAAA",Post.like(data))

    return redirect('/bright_ideas')

@app.route('/bright_ideas/<int:id>')
def like_status(id):
    
    #usuario = Usuario.getId(session)
    #user = Usuario.get_all()
    ideas = Post.get_posts_with_user()
    likes = Post.getLikes()
    #print("\n\n\nUSUARIOS",usuario)
    print("\n\n\n",ideas)
    alias = Post.get_alias_name(id)
    #total = Usuario.total_posts(id)
    cantLikes = 0
    return render_template("like_status.html",ideas=ideas,likes=likes,id=id,alias=alias)

