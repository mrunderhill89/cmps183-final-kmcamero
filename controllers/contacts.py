def index():
    t = db.Contact
    #Get grid of the user's contacts
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
