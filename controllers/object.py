@auth.requires_login()
def update():
	db.object.description.widget = SQLFORM.widgets.text.widget
	record = db(db.object.id == request.args[0]).select().first()
	db.object.id.readable  = False
	db.object.owner.readable = False
	updateobjectform = SQLFORM(db.object, record, fields = ['name', 'collection', 'price', 'category', 'quantity', 'tradable_quantity', 'wanted_quantity','description', 'image'])

	if updateobjectform.process(onvalidation = checking_quantity).accepted:
		response.flash = "Your object is updated."

	elif updateobjectform.errors:
		response.flash = "One or more errors in your form field. Please see below for more information."

	else:
		response.flash = "Please complete the form to update your object."

	return dict(updateobjectform = updateobjectform)

@auth.requires_login()
def create():
	response.collection = db(db.collection.id == request.vars['collection']).select().first()
	response.owner = db(db.auth_user.id == auth.user_id).select().first()

	form = SQLFORM(db.object, fields = ['name', 'collection', 'price', 'category', 'quantity', 'tradable_quantity', 'wanted_quantity','description', 'image'], submit_button='Create')
	form.vars.owner = auth.user_id
	if form.process(onvalidation = checking_quantity).accepted:
		redirect(URL('object', 'view', args=[form.vars.id], vars=dict(message='object_created')))
	elif form.errors:
		response.flash = "One or more errors in your form field. Please see below for more information."

	return dict(form = form)

#check the quantity and tradable_quantity to ensure that tradable_quantity is less than quantity.
def checking_quantity(form):
	if (form.vars.quantity  < form.vars.tradable_quantity):
		form.errors.tradable_quantity = "Tradable quantity cannot be greater than quantity of the object."
	else:
		form.vars.tradable_quantity = form.vars.tradable_quantity


def view():
	response.result = db(db.object.id == request.args[0]).select().first()
	response.collection = db(db.collection.id == response.result.collection).select().first()
	response.owner = db(db.auth_user.id == response.collection.owner).select().first()
	return dict()
