from django.db.models import Q
from django.utils.text import smart_split, unescape_string_literal


def construct_search_query(search_term, search_fields):
    # Construct the ORM lookups
    orm_lookups = [f"{field}__icontains" for field in search_fields]
    term_queries = []

    for bit in smart_split(search_term):
        if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
            bit = unescape_string_literal(bit)
        or_queries = Q.create(
            [(orm_lookup, bit) for orm_lookup in orm_lookups],
            connector=Q.OR,
        )
        term_queries.append(or_queries)

    query = Q.create(term_queries, connector=Q.AND)

    return query


def construct_date_query(start_date, end_date, date_field):
    queries = []
    if start_date and end_date:
        queries.append((f"{date_field}__range", [start_date, end_date]))
    elif start_date:
        queries.append((f"{date_field}__gte", start_date))
    elif end_date:
        queries.append((f"{date_field}__lte", end_date))

    return Q.create(queries, connector=Q.AND) if queries else Q()
