from WebWeaverWOS import ww_wos
from WebWeaverELS import ww_els
from WebWeaverBDTD import ww_bdtd


def webweaver(db, query, query_type, query_date, query_id):
    if db == "1":
        ww_wos(query, query_type, query_date, query_id)
    elif db == "2":
        ww_els(query, query_type, query_date, query_id)
    elif db == "3":
        ww_bdtd(query, query_type, query_date, query_id)
    else:
        ww_wos(query, query_type, query_date, query_id)
        ww_els(query, query_type, query_date, query_id)
        ww_bdtd(query, query_type, query_date, query_id)
