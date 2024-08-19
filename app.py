from flask import request, jsonify, render_template, Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai


app = Flask(__name__,  template_folder='templates')
CORS(app)


# Replace with your actual Gemini API details

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    """
    A class used to represent a contact in the application.

    Attributes
    ----------
    id : int
        The unique identifier for the contact.
    first_name : str
        The first name of the contact.
    last_name : str
        The last name of the contact.
    email : str
        The email address of the contact.

    Methods
    -------
    to_json():
        Returns a dictionary representation of the contact in JSON format.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_json(self):
        """
        Returns a dictionary representation of the contact in JSON format.

        Returns
        -------
        dict
            A dictionary with keys 'id', 'firstName', 'lastName', and 'email'
            corresponding to the contact's attributes.
        """
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }

@app.route('/')
def index():
    """
    This function is a route handler for the root URL of the application.
    It renders the index.html template.

    Parameters:
    None

    Returns:
    A rendered HTML template for the index page.
    """
    return render_template('index.html')


@app.route("/read", methods=["GET"])
def get_contacts():
    """
    Retrieves all contacts from the database and returns them as a JSON response.

    Parameters:
    None

    Returns:
    JSON response containing a list of contacts. Each contact is represented as a dictionary with keys:
    'id', 'firstName', 'lastName', and 'email'. If an error occurs during the retrieval process,
    a JSON response with a 'message' key containing the error details is returned.
    """
    try:
        contacts = Contact.query.all()
        json_contacts = list(map(lambda x: x.to_json(), contacts))
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        print("Something went wrong: " + e)
        return jsonify({"message:": str(e)})


@app.route("/create", methods=["POST"])
def create_contact():
    """
    Creates a new contact in the database using the provided first name, last name, and email.

    Parameters:
    first_name (str): The first name of the contact.
    last_name (str): The last name of the contact.
    email (str): The email address of the contact.

    Returns:
    JSON response with a 'message' key indicating the outcome of the operation.
    If the operation is successful, the 'message' key will contain "User Created!".
    If the operation fails due to missing parameters, the 'message' key will contain "empty"
    and a 400 status code will be returned.
    If an error occurs during the database operation, the 'message' key will contain the error details
    and a 400 status code will be returned.
    """

    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (jsonify({"message": "empty"}), 400)
    
    new_contact = Contact(
        first_name=first_name, last_name=last_name, email=email
    )

    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        print("Something went wrong: " + e)
        return jsonify({"message:": str(e)}), 400

    return jsonify({"message": "User Created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    """
    Updates an existing contact in the database using the provided user ID.

    Parameters:
    user_id (int): The unique identifier of the contact to be updated.

    Returns:
    JSON response with a 'message' key indicating the outcome of the operation.
    If the operation is successful, the 'message' key will contain "User updated!".
    If the operation fails due to the contact not being found, the 'message' key will contain "User not found"
    and a 404 status code will be returned.
    If an error occurs during the database operation, the 'message' key will contain the error details
    and a 400 status code will be returned.
    """
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User updated"}), 200


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    """
    Deletes a contact from the database using the provided user ID.

    Parameters:
    user_id (int): The unique identifier of the contact to be deleted.

    Returns:
    JSON response with a 'message' key indicating the outcome of the operation.
    If the operation is successful, the 'message' key will contain "User deleted!".
    If the operation fails due to the contact not being found, the 'message' key will contain "User not found"
    and a 404 status code will be returned.
    If an error occurs during the database operation, the 'message' key will contain the error details
    and a 500 status code will be returned.
    """
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    try:
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
