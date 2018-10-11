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
    if not validate(username) or " " in username:
        username_error = 'Username must be between 3 and 20 characters in length and can NOT contain a space'
        username = ''

# use validate function to test length. can not contain a space ' '. return error if needed #
    if not validate(password) or " " in password:
        password_error = 'Password must be between 3 and 20 characters in length'
        password = ''
    

# verify must match password. if not give error and re-enter #    
    if verify != password:
        verify_error = 'Verify Password does NOT match Password'
        verify = ''

# optional! if not empty, use validate function to test length. can not contain a space ' ' #
# can not contain more or less than a single (@) and (.) #
    if email != '' and not validate(email):
        email_error = 'Email must be between 3 and 20 characters in length'
        email = ''
    elif email !='' and (" " in email):
        email_error = 'Email can NOT contain a space'
        email = ''
    elif email != '' and not(email.count("@") == 1):
        email_error = "Email must contain a single '@'"
        email = ''
    elif email != '' and not(email.count(".") == 1):
        email_error = "Email must contain a single '.'"
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