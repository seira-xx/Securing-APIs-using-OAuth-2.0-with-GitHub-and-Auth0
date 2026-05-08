from flask import Flask, redirect, url_for, session, jsonify, render_template_string
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Secret key for session management
app.secret_key = "SECRET_KEY"

oauth = OAuth(app)

# GitHub OAuth Configuration
github = oauth.register(
    name='github',
    client_id='Ov23lic9OLBV6X3SKcDp',
    client_secret='2c15e97214275383ced3001816ed5afbd1e79c69',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Home Route
@app.route('/')
def home():
    return '<h1>OAuth 2.0 Lab Activity</h1><a href="/login">Login with GitHub</a>'

# Login Route
@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

# Callback Route
@app.route('/callback')
def callback():
    token = github.authorize_access_token()

    user = github.get('user').json()

    session['user'] = {
        "name": user.get("name"),
        "login": user.get("login"),
        "avatar": user.get("avatar_url"),
        "bio": user.get("bio"),
        "email": user.get("email"),
        "followers": user.get("followers"),
        "repos": user.get("public_repos"),
        "profile_url": user.get("html_url")
    }

    return redirect('/profile')

# Protected Route (HTML UI)
@app.route('/profile')
def profile():

    if 'user' not in session:
        return "Unauthorized", 401

    user = session['user']

    html = f"""
    <html>
    <head>
        <title>Profile</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f4f4;
                text-align: center;
                padding: 40px;
            }}
            
            img {{
                width: 120px;
                border-radius: 50%;
            }}
        </style>
    </head>
    <body>

        <div class="profile">
            <img src="{user['avatar']}">

            <h2>Welcome {user['name'] or user['login']}</h2>

            <p><b>Username:</b> {user['login']}</p>
            <p><b>Bio:</b> {user['bio'] or "No bio available"}</p>
            <p><b>Email:</b> {user['email'] or "Not public"}</p>
            <p><b>Followers:</b> {user['followers']}</p>
            <p><b>Public Repos:</b> {user['repos']}</p>

            <p>
                <a href="{user['profile_url']}" target="_blank">
                <button style="padding:10px; margin-top:15px; cursor:pointer;">
                    View GitHub Profile
                </button>
                </a>
            </p>
            <p>
            <a href="/api/secure-data" target="_blank">
                <button style="padding:10px; margin-top:15px; cursor:pointer;">
                    View Secure API Data
                </button>
            </a>
            </p>
            <p>
            <a href="/logout">
            <button style="padding:10px; margin-top:15px; cursor:pointer;">
            Logout
            </button>
            </a>
            </p>
        </div>

    </body>
    </html>
    """

    return render_template_string(html)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)

    return """
    <html>
        <head>
            <title>Logged Out</title>
        </head>
        <body style="font-family:Arial; text-align:center; padding:50px; background:#f4f4f4;">
            <div class="Logout">
                <h2>Logged Out Successfully</h2>
                <p>You have been safely logged out.</p>

                <a href="/">
                    <button style="padding:10px; cursor:pointer;">Go Home</button>
                </a>

                <br><br>

                <a href="/login">
                    <button style="padding:10px; cursor:pointer;">Login Again</button>
                    </a>
            </div>
        </body>
    </html>
    """

# BONUS Protected API Route
@app.route('/api/secure-data')
def secure_data():

    if 'user' not in session:
        return jsonify({
            "error": "Unauthorized access"
        }), 401

    return jsonify({
        "message": "This is a BONUS protected route 🎉",
        "user": session['user']['login'],
        "followers": session['user']['followers'],
        "repos": session['user']['repos']
    })

# Run Application
if __name__ == '__main__':
    app.run(debug=True)
