from flask import render_template, redirect, url_for, flash, jsonify
from app import app, db
from models import User, ColumnInfo, UsageEntry
from forms import UsageEntryForm, UserForm, ColumnInfoForm
from jinja2 import TemplateNotFound

@app.route('/usage_entry', methods=['GET', 'POST'])
def usage_entry():
    form = UsageEntryForm()
    form.user_id.choices = [(user.id, user.name) for user in User.query.all()]
    form.column_id.choices = [(column.sn, column.reference) for column in ColumnInfo.query.all()]
    
    if form.validate_on_submit():
        # If the form is submitted and validated, process the data
        user_id = form.user_id.data
        column_id = form.column_id.data
        project = form.project.data
        technique = form.technique.data
        mobile_phase_a = form.mobile_phase_a.data
        mobile_phase_b = form.mobile_phase_b.data
        date = form.date.data

        # Create a new UsageEntry object and add it to the database
        usage_entry = UsageEntry(
            user_id=user_id,
            column_id=column_id,
            project=project,
            technique=technique,
            mobile_phase_a=mobile_phase_a,
            mobile_phase_b=mobile_phase_b,
            date = date
        )
        db.session.add(usage_entry)
        db.session.flush()
        id_= usage_entry.id
        db.session.commit()
        # Redirect to a success page or another route
        flash('Usage Entry Successful!', 'success')
        return redirect( url_for('product_last_usage', id=id_) )
    return render_template('usage_entry.html', form=form)
    
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    Userform = UserForm()

    if Userform.validate_on_submit():
        # If the form is submitted and validated, process the data
        name = Userform.name.data
        employee_id = Userform.employee_id.data

        # Create a new User object and add it to the database
        user = User(name=name, employee_id=employee_id)
        db.session.add(user)
        db.session.commit()

        # Redirect to a success page or another route
        flash('User Entry Successful!', 'success')
        return redirect(url_for('registration'))
    
    form = ColumnInfoForm()

    if form.validate_on_submit():
        # If the form is submitted and validated, process the data
        sn = form.sn.data
        reference = form.reference.data
        supplier = form.supplier.data
        dimension = form.dimension.data

        # Create a new ColumnInfo object and add it to the database
        column_info = ColumnInfo(sn=sn, reference=reference, supplier=supplier, dimension=dimension)
        db.session.add(column_info)
        db.session.commit()

        # Redirect to a success page or another route
        flash('Column Registration Successful!', 'success')
        return redirect(url_for('registration'))
    
    return render_template('Registration.html', Userform=Userform, form=form)


@app.route('/get_product_columns')
def get_product_columns():
     # Query all column values from the database
    columns = ColumnInfo.query.all()

    # Serialize the data into JSON format
    column_values = [{'sn': column.sn, 'reference': column.reference, 'supplier': column.supplier, 'dimension': column.dimension} for column in columns]

    # Return the JSON response
    return jsonify(column_values)


@app.route('/product_details', defaults={'column_id': None})
@app.route('/product_details/<string:column_id>')
def product_details(column_id):
    # Query all column information from the database
    products=[]
    if column_id: 
        columns = ColumnInfo.query.filter_by(sn=column_id).first()
        products.append(columns)
        return render_template('product_details.html', columns=products)
    else:
        columns = ColumnInfo.query.all()
        products.append(columns)
        print(products)
        return render_template('product_details.html', columns=columns)


@app.route('/product_last_usage', defaults={'id': None})
@app.route('/product_last_usage/<int:id>')
def product_last_usage(id):
    last_usage=[]
    if id:
        # Query last usage of the product from the database
        last_usage.append(UsageEntry.query.get(id))
        # Render template to display last usage of the product
        print(last_usage)
        return render_template('last_product_entry.html', usage=last_usage)
    else:
        print(last_usage)
        return render_template('last_product_entry.html', usage = [])


@app.route('/product_usage', defaults={'column_id': None})
@app.route('/product_usage/<string:column_id>')
def product_usage(column_id):
    last_usage=[]
    if column_id:
        # Query last usage of the product from the database
        last_usage=UsageEntry.query.filter_by(column_id=column_id).order_by(UsageEntry.date.desc()).all()
        # Render template to display last usage of the product
        print(last_usage)
        return render_template('product_usage.html', usage=last_usage)
    else:
        return render_template('product_usage.html', usage = [])

    