from flask import render_template, redirect, url_for, flash, request
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
        db.session.commit()
        # Redirect to a success page or another route
        flash('Usage Entry Successful!', 'success')
        return redirect( url_for('product_last_usage', column_id=column_id) )
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
        date = form.date.data

        # Create a new ColumnInfo object and add it to the database
        column_info = ColumnInfo(sn=sn, reference=reference, supplier=supplier, dimension=dimension, date=date)
        db.session.add(column_info)
        db.session.commit()

        # Redirect to a success page or another route
        flash('Column Registration Successful!', 'success')
        return redirect(url_for('registration'))
    
    return render_template('Registration.html', Userform=Userform, form=form)


@app.route('/product_details')
def product_details():
    # Query all column information from the database
    columns = ColumnInfo.query.all()
    return render_template('product_details.html', columns=columns)

# @app.route('/last_product_usage')
# def last_product_usage():
#     # Query the last usage entry for each column
#     last_usages = []
#     for column in ColumnInfo.query.all():
#         last_usage = UsageEntry.query.filter_by(column_id=column.sn).order_by(UsageEntry.id.desc()).first()
#         if last_usage:
#             last_usages.append(last_usage)
#     return render_template('last_product_usage.html', last_usages=last_usages)

@app.route('/product_last_usage', defaults={'column_id': None})
@app.route('/product_last_usage/<string:column_id>')
def product_last_usage(column_id):
    if column_id:
        # Query last usage of the product from the database
        last_usage = UsageEntry.query.filter_by(column_id=column_id).order_by(UsageEntry.date.desc()).first()
        # Render template to display last usage of the product
        return render_template('last_product_usage.html', usage=last_usage)
    else:
        last_usage_entries = []
        columns = ColumnInfo.query.all()
        for column in columns:
            last_usage_entry = UsageEntry.query.filter_by(column_id=column.sn).order_by(UsageEntry.date.desc()).first()
            if last_usage_entry:
                last_usage_entries.append(last_usage_entry)
        print(last_usage_entries)
        return render_template('last_usage_entries.html', last_usage_entries=last_usage_entries)
       
