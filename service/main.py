from flask import request, jsonify, render_template
from config import app, db
from models import Contact


@app.route('/')
def index():
    return render_template('/templates/index.html')


@app.route("/read", methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        json_contacts = list(map(lambda x: x.to_json(), contacts))
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        print("Something went wrong: " + e)
        return jsonify({"message:": str(e)})


@app.route("/create", methods=["POST"])
def create_contact():

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
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not fount"}), 404

    data = requset.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contat.email)

    try:
        db.session.commit
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": "User updated"}), 200


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not fount"}), 404

    try:
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
