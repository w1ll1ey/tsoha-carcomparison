from app import app
import qry
import json
from flask import redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    email = session["email"]
    user_id = qry.get_user_id(email)
    comparisons = qry.get_comparison_data(user_id)
    return render_template("index.html", comparisons = comparisons)

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if not qry.get_userdata(email):
        return "Sähköpostiosoitteeseen ei ole liitetty tiliä!"
    else:
        hash_value = qry.get_userdata(email).password
        if check_password_hash(hash_value, password):
            session["email"] = email
            return redirect("/")
        else:
            return "Väärä salasana!"

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    qry.add_userdata(email, hash_value)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["email"]
    return redirect("/")

@app.route("/createcar")
def createcar():
    return render_template("createcar.html")

@app.route("/submit", methods=["POST"])
def submit():
    manufacturer = request.form["manufacturer"]
    model = request.form["model"]
    gen = request.form["generation"]
    type = request.form["type"]
    qry.add_car(manufacturer, model, gen, type)
    return redirect("/createcar")

#@app.route("/result", methods=["POST"])
#def result():
#    return render_template("createcarresult.html", manufacturer=request.form["manufacturer"], model=request.form["model"], type=request.form["type"])

@app.route("/createcomparison", methods=["POST"])
def createcomparison():
    email = session["email"]
    name = request.form["name"]
    userid = qry.get_user_id(email)
    qry.add_comparison(name, userid)
    value = qry.get_comparisonid(name)
    session["comparisonid"] = value
    return redirect("/editcomparison")

@app.route("/editcomparison")
def editcomparison():
    return render_template("selection.html")

@app.route("/addcar", methods=["POST"])
def addcar():
    manufacturer = request.form["manufacturer"]
    model = request.form["model"]
    gen = request.form["generation"]
    type = request.form["type"]
    carid = qry.get_carid(manufacturer, model, gen, type)
    comparisonid = session["comparisonid"]
    qry.update_comparison(comparisonid, carid)
    return redirect("/editcomparison")

@app.route("/comparison", methods=["POST"])
def comparison():
    comparison = request.form["comparison"]
    carids = qry.get_comparison_cars(comparison)
    session["comparisonid"] = comparison
    if carids:
        cardata = qry.get_car_data(carids)
        return render_template("comparison.html", cardata = cardata, carids = carids)
    else:
        return render_template("comparison.html")






@app.route("/registered", methods=["POST"])
def registered():
    return "Vahvistussähköposti lähetetty osoitteeseen " + request.form["email"] + "."

@app.route("/signin")
def signin():
    return render_template("signin.html", username=request.form["username"])
