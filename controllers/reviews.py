@auth.requires_login()
def index():
    t = db.Review
    q = (t.receiver == auth.user.id)
    reviewsFrom = SQLFORM.grid(q
                ,searchable = True
                ,fields=[t.sender]
                ,csv = False
                ,details = False
                ,create = False
                ,editable = False
                ,deletable = False
                ,links = []
                )
    q = (t.sender == auth.user.id)
    reviewsTo = SQLFORM.grid(q
            ,searchable = True
            ,fields=[t.receiver]
            ,csv = False
            ,details = False
            ,create = False
            ,editable = False
            ,deletable = False
            ,links = []
            )
    return dict(rFrom = reviewsFrom, rTo = reviewsTo)