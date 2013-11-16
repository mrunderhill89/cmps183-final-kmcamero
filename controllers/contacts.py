def index():
    t = db.Contact
    #Get grid of projects owned by user
    q = ((auth.user.id == t.fromUser) | (auth.user.id == t.toUser))
    form = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.fromUser, t.toUser]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    )
    return dict(form= form)

def add():
    return dict()

def addByEmail():
    form = SQLFORM.factory(
                            Field('email', requires=IS_NOT_EMPTY()),
                            Field('relationship', requires=IS_NOT_EMPTY())
                           )
    if form.process().accepted:
        session.flash = 'Contact posted'
        redirect(URL('contacts', 'index'))
    return dict(form = form)

