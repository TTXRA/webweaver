from WebWeaverWOS import ww_wos
from WebWeaverELS import ww_els
from WebWeaverBDTD import ww_bdtd


def webweaver(db, query, query_type="0", query_date="0"):
    if db == 1:
        ww_wos(query, query_type, query_date)
    elif db == 2:
        ww_els(query, query_type, query_date)
    elif db == 3:
        ww_bdtd(query, query_type, query_date)
    else:
        ww_wos(query, query_type, query_date)
        ww_els(query, query_type, query_date)
        ww_bdtd(query, query_type, query_date)


query = "data"
webweaver(3, query,  "0", "2023")
