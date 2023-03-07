from flask import flash,request,session,url_for,redirect
from ideas_app.config.mysqlconnection import connectToMySQL
from ideas_app.controllers import users

db_name ="users"
class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def getId(cls, data):
        query = f"select * from ideas where id = %(id)s;"
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        print("\n\n\ngetID from Post result:",result)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    @classmethod
    def save(cls, data):
        #content = request.form['content']
        #content = f'{content}'
        #print(content)
        user_id = session.get("id")
        print("\n\nUSER_ID",user_id)
        query = "insert into ideas (content,user_id) values "\
                f"(%(content)s,{user_id});"
        mysql = connectToMySQL(db_name)
        result = mysql.query_db(query, data)
        print("\nRESULT",result)
        data_usuario = {'id': result}
        return cls.getId(data_usuario)
    @classmethod
    def getPosts(cls):
        query = "select * from ideas;"
        results = connectToMySQL(db_name).query_db(query)
        print(results)
        ideas = []
        for i  in results:
            ideas.append( cls(i) )
            print("\n\nI D E A S",ideas)
        return ideas
    @classmethod
    def get_posts_with_user(cls):
        query = "select users.name,users.alias,users.id,users.email,ideas.user_id, ideas.id, ideas.content from users left join ideas on users.id = ideas.user_id;"

        results = connectToMySQL(db_name).query_db(query)
        print("\n\nPosts by user RESULTS",results)
        print("\nResults",type(results))
        posts = []
        for result  in results:
            posts.append( result)
            print("\n\nI D E A S",posts)
        return posts
    @classmethod
    def get_posts_by_users(cls,data):
        query = "select users.name, users.alias ideas.content from users left join ideas on users.id = ideas.user_id;"
        results = connectToMySQL(db_name).query_db(query)
        print(results)
        posts = cls(results[0])
        for row in results:
            p = {
                'id': row['id'],
                'users.name': row['users.name'],
                'users.alias': row['users.alias'],
                'ideas.content': row['content']

                
            }
            posts.append( Post(p) )
            print("\n\n\n",posts['id'],"\n")
            print(type(posts))
        return posts
    
    @classmethod
    def destroy(cls,data):
        query  = f"DELETE FROM ideas WHERE id = {data};"
        
        return connectToMySQL(db_name).query_db(query,data)
    
    @classmethod
    def getLikes(cls):
        query = "select * from likes"
        results = connectToMySQL(db_name).query_db(query)
        print("\n\nLikes",results)
        print("\Likes type",type(results))
        likes = []
        for result  in results:
            likes.append(result)
            print("\n\nLIKES",likes)
        return likes
    
    @classmethod
    def like(cls,data):
        query = "insert into likes (user_id,idea_id,amount) values (%(user_id)s,%(idea_id)s,1);"
        result = connectToMySQL(db_name).query_db(query,data)
        print("\n\n\n\nINSERT_LIKE RESULT: ",result)
        return result
    @classmethod
    def get_likes_by_id(cls,data):
        query = f"select * from likes where user_id={data}"
        results = connectToMySQL(db_name).query_db(query)
        print("\n\nLikes",results)
        print("\nLikes type",type(results))
        likes = []
        for result  in results:
            likes.append(result)
            print("\n\nLIKES",likes)
        return likes
    @classmethod
    def get_amount_of_likes(cls,data):
        query = f"select count(user_id) from likes where user_id={data}"
        results = connectToMySQL(db_name).query_db(query)
        print("\n\nAMOUNT OF LIKES RESULTS",results)
        print("\nRESULTS type",type(results))
        return results
    @classmethod
    def update_like(cls,idea_id):
        query = f"update likes set amount = %(amount)+1 where (user_id = {session.get('id')} AND idea_id={idea_id})"
        results = connectToMySQL(db_name).query_db(query)
        print("\nUPDATE LIKES RESULTS",results)
        print("\nRESULTS type",type(results))
        return results
    @classmethod
    def get_amount_of_likes_by_post(cls):
        query = f"select count(idea_id) from likes where idea_id = %(idea_id)s;"
        results = connectToMySQL(db_name).query_db(query)
        print("\n\nAMOUNT OF LIKES BY POST RESULTS",results)
        print("\nRESULTS type",type(results))
        return results
    @classmethod
    def get_alias_name(cls,id):
        query=f"select users.alias,users.name,users.id from users left join likes on users.id = likes.user_id where likes.idea_id={id};"
        results = connectToMySQL(db_name).query_db(query)
        return results