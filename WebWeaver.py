from WebWeaverWOS import ww_wos
from WebWeaverELS import ww_els
from WebWeaverBDTD import ww_bdtd


def webweaver(db, query, query_type, query_date, query_id):
    match db:
        case "1":
            total = ww_wos(query, query_type, query_date, query_id)
        case "2":
            total = ww_els(query, query_type, query_date, query_id)
        case "3":
            total = ww_bdtd(query, query_type, query_date, query_id)
        case _:
            total = int(ww_wos(query, query_type, query_date, query_id))
            total += int(ww_els(query, query_type, query_date, query_id))
            total += int(ww_bdtd(query, query_type, query_date, query_id))

    return total
