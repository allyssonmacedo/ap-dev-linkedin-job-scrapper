import connectmongo

client = connectmongo.connectServer()

db_connection = client['jobs-in']

collection = db_connection.get_collection('jobs')

#posts = collection.posts
post_id = collection.insert_one(post).inserted_id
post_id
