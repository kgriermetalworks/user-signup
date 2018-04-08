from flask import Flask, request, redirect, render_template
import cgi



app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser



#call to display the original form with text and textarea
@app.route("/")
def index():

    return render_template('signup.html')

# create a function that will validate if any field is between 3 and 20 char in length #
# flask does nor like none values #
def validate(user_input):
    try:
        if len(user_input) <= 20 and len(user_input) >= 3:
            return True
    except ValueError:
        return False 

# validate all fields. POST request to avoid exposing sensitive information #
@app.route("/", methods=['POST'])
def validate_signup():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

# use validate function to test length. can not contain a space ' '. return error if needed #
    if not validate(username):
        username_error = 'Username must be between 3 and 20 characters in length'
        username = ''
    else:
        for char in username:
            if char == ' ':
                username_error = 'Username can not contain a space' 
                username = ''

# use validate function to test length. can not contain a space ' '. return error if needed #
    if not validate(password):
        password_error = 'Password must be between 3 and 20 characters in length'
        password = ''
    else:
        for char in password:
            if char == ' ':
                password_error = 'Password can not contain a space' 
                password = ''

# verify must match password. if not give error and re-enter #    
    if verify != password:
        verify_error = 'Verify Password does NOT match Password'
        verify = ''

# optional! if not empty, use validate function to test length. can not contain a space ' ' #
# can not contain more than a single (@) or (.) #
    if email != '':
        if not validate(email):
            email_error = 'Email must be between 3 and 20 characters in length'
            email = ''
        elif email.count('@') > 1 or email.count('.') > 1:
            email_error = 'Email can not contain more than a single "@" or "."'
            email = ''
        else:
            for char in email:
                if char == ' ':
                    email_error = 'Email can not contain a space' 
                    email = ''

# redirect if no errors and send username with GET request to welcome page #
# if errors, re-render index page with error prompts for user #
    if not username_error and not password_error and not verify_error and not email_error:
        user = username
        return redirect('/welcome?user={0}'.format(user))
    else:
        return render_template('signup.html', username_error=username_error , 
            password_error=password_error , verify_error=verify_error , email_error=email_error ,
            username=username , 
            password=password, verify=verify , email=email )


# welcome page for if no errors. only send username. Do not send sensitive information #
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    user = request.args.get('user')
    return render_template('welcome.html',user=user)


app.run()