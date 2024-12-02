import sqlite3
import requests

def initialize_posts_database():
    connection = sqlite3.connect('user_posts.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_title TEXT,
        post_body TEXT
    )
    ''')
    
    connection.commit()
    connection.close()

def retrieve_posts_from_api():
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return []

def store_posts_in_database(posts):
    connection = sqlite3.connect('user_posts.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM user_posts')
    
    for post in posts:
        cursor.execute('''
        INSERT INTO user_posts (post_id, user_id, post_title, post_body)
        VALUES (?, ?, ?, ?)
        ''', (post['id'], post['userId'], post['title'], post['body']))
    
    connection.commit()
    connection.close()

def fetch_user_posts(user_id):
    connection = sqlite3.connect('user_posts.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_posts WHERE user_id = ?', (user_id,))
    user_posts = cursor.fetchall()
    connection.close()
    
    return user_posts

if __name__ == "__main__":
    initialize_posts_database()
    
    posts_data = retrieve_posts_from_api()
    store_posts_in_database(posts_data)
    
    target_user_id = 1
    user_specific_posts = fetch_user_posts(target_user_id)
    for post in user_specific_posts:
        print(post)