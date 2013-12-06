def index():
    t = db.Contact
    q = ((not t.blocked) & ((t.sender == auth.user.id) | (t.receiver == auth.user.id)))
    contacts = SQLFORM.grid(q
            ,searchable = True
            ,fields=[t.sender, t.receiver, t.accepted]
            ,csv = False
            ,details = False
            ,create = False
            ,editable = False
            ,deletable = False
            ,links = []
            )
    return dict(contacts=contacts)

def getContactStatus(user):
    t = db.Contact
    q = ((t.sender == auth.user.id) | (t.receiver == auth.user.id))
    
    return "none"

@auth.requires_signature()
def add():
    user = db.auth_user(request.args(0))
    message = "Confirm contact with "+user.first_name+" "+user.last_name+"?"
    if user is None: 
        session.flash = 'Invalid contact request.'
        redirect(URL('contacts', 'index'))
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('default', 'index'))
    if form.process().accepted:
        
    return dict(user = user, message = message, actions=actions)