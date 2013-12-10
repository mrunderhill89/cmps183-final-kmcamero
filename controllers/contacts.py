@auth.requires_login()
def index():
    t = db.Contact
    q = ((t.blocked == False) & ((t.sender == auth.user.id) | (t.receiver == auth.user.id)))
    contacts = SQLFORM.grid(q
            ,searchable = True
            ,fields=[t.sender, t.receiver, t.accepted]
            ,csv = False
            ,details = False
            ,create = False
            ,editable = False
            ,deletable = False
            ,links = [dict(header=T('Status'), body = getContactStatusR),
                      dict(header=T('Actions'), body = getContactActions)]
            )
    return dict(contacts=contacts)

def getContactActions(r):
    accept = A('Accept', _href=URL('contacts','accept', args = [r.id], user_signature = True), _class='btn')
    block = A('Block', _href=URL('contacts','block', args = [r.id],user_signature = True), _class='btn')
    withdraw = A('Withdraw', _href=URL('contacts','withdraw', args = [r.id],user_signature = True), _class='btn')
    if (r.accepted or r.receiver != auth.user.id):
        return withdraw + block
    return accept + withdraw + block

def getContactStatus(user):
    t = db.Contact
    contacts = db((t.sender == auth.user.id) | (t.receiver == auth.user.id))
    if (contacts.count() > 0):
        contact = contacts.select().first() or None
        if (contact is not None):
            if (contact.accepted):
                return "accepted"
            if (contact.blocked):
                return "blocked"
            if (contact.sender == auth.user.id):
                return "pending receiver's approval"
            return "pending your approval"
    return "none"

def getContactStatusR(r):
    if (r.receiver == auth.user.id):
        return getContactStatus(r.sender)
    return getContactStatus(r.receiver)

@auth.requires_signature()
def add():
    user = db.auth_user(request.args(0))
    message = "Confirm contact with "+user.first_name+" "+user.last_name+"?"
    if user is None: 
        session.flash = 'Invalid contact request.'
        redirect(URL('contacts', 'index'))
    status = getContactStatus(user)
    if (status != "none"):
        if (status == "blocked"):
            session.flash = 'The other user has blocked you. You can no longer add them as a contact.'
        else:
            session.flash = 'You cannot have more than one contact with the same person.'
        redirect(URL('contacts', 'index'))
    else:
        form = SQLFORM.factory()
        form.add_button('Cancel', URL('contacts', 'index'))
        if form.process().accepted:
            db.Contact.insert(sender = auth.user.id, receiver = user, accepted = False, blocked = False)
            redirect(URL('contacts', 'index'))
    return dict(user = user, message = message, form=form)

@auth.requires_signature()
def accept():
    contact = db.Contact(request.args(0))
    user = contact.sender
    message = "Confirm contact with "+user.first_name+" "+user.last_name+"?"
    if user is None: 
        session.flash = 'Sender is not an active user'
        redirect(URL('contacts', 'index'))
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('contacts', 'index'))
    if form.process().accepted:
        contact.update_record(accepted = True)
        redirect(URL('contacts', 'index'))
    return dict(user = user, message = message, form=form)

@auth.requires_signature()
def block():
    contact = db.Contact(request.args(0))
    user = contact.sender
    message = "Block contact with "+user.first_name+" "+user.last_name+"? This will prevent them from trying to contact you again."
    if user is None: 
        session.flash = 'Other party is not an active user'
        redirect(URL('contacts', 'index'))
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('contacts', 'index'))
    if form.process().accepted:
        contact.update_record(accepted = False, blocked = True)
        redirect(URL('contacts', 'index'))
    return dict(user = user, message = message, form=form)

@auth.requires_signature()
def withdraw():
    contact = db.Contact(request.args(0))
    user = contact.sender
    if (contact.sender == auth.user.id):
        user = contact.receiver
    message = "Remove contact with "+user.first_name+" "+user.last_name+"? This won't prevent them from trying to contact you again."
    if user is None: 
        session.flash = 'Other party is not an active user'
        redirect(URL('contacts', 'index'))
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('contacts', 'index'))
    if form.process().accepted:
        contact.delete_record()
        redirect(URL('contacts', 'index'))
    return dict(user = user, message = message, form=form)