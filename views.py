from flask import render_template, redirect, url_for, flash
from app import app, db
from models import User, ColumnInfo, UsageEntry
from forms import UsageEntryForm, UserForm, ColumnInfoForm

@app.route('/usage_entry', methods=['GET', 'POST'])
def usage_entry():
    form = UsageEntryForm()
    form.user_id.choices = [(user.id, user.name) for user in User.query.all()]
    form.column_id.choices = [(column.sn) for column in ColumnInfo.query.all()]
    
    if form.validate_on_submit():
        # If the form is submitted and validated, process the data
        user_id = form.user_id.data
        column_id = form.column_id.data
        project = form.project.data
        technique = form.technique.data
        mobile_phase_a = form.mobile_phase_a.data
        mobile_phase_b = form.mobile_phase_b.data

        # Create a new UsageEntry object and add it to the database
        usage_entry = UsageEntry(
            user_id=user_id,
            column_id=column_id,
            project=project,
            technique=technique,
            mobile_phase_a=mobile_phase_a,
            mobile_phase_b=mobile_phase_b
        )
        db.session.add(usage_entry)
        db.session.commit()
        # Redirect to a success page or another route
        flash('Usage Entry Successful!', 'success')
        return redirect(url_for('register_user'))
    return render_template('usage_entry.html', form=form)

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = UserForm()

    if form.validate_on_submit():
        # If the form is submitted and validated, process the data
        name = form.name.data

        # Create a new User object and add it to the database
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        # Redirect to a success page or another route
        flash('User Entry Successful!', 'success')
        return redirect(url_for('register_user'))

    # If the form is not submitted or is invalid, render the form template
    return render_template('user_registration.html', form=form)

@app.route('/register_column_info', methods=['GET', 'POST'])
def register_column_info():
    form = ColumnInfoForm()

    if form.validate_on_submit():
        # If the form is submitted and validated, process the data
        sn = form.sn.data
        supplier = form.supplier.data
        dimension = form.dimension.data
        date = form.date.data

        # Create a new ColumnInfo object and add it to the database
        column_info = ColumnInfo(sn=sn, supplier=supplier, dimension=dimension, date=date)
        db.session.add(column_info)
        db.session.commit()

        # Redirect to a success page or another route
        flash('Column Registration Successful!', 'success')
        return redirect(url_for('register_user'))

    # If the form is not submitted or is invalid, render the form template
    return render_template('column_info_registration.html', form=form)

@app.route('/product_details')
def product_details():
    # Query all column information from the database
    columns = ColumnInfo.query.all()
    return render_template('product_details.html', columns=columns)

@app.route('/last_product_usage')
def last_product_usage():
    # Query the last usage entry for each column
    last_usages = []
    for column in ColumnInfo.query.all():
        last_usage = UsageEntry.query.filter_by(column_id=column.sn).order_by(UsageEntry.id.desc()).first()
        if last_usage:
            last_usages.append(last_usage)
    return render_template('last_product_usage.html', last_usages=last_usages)