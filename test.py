from db_pg_work import get_full_list
from db_tables import avail

response = get_full_list(type_=avail.c.type_,
                         ty_l=['Кнопочные телефоны'],
                         brand=avail.c.type_,
                         br_l=['Кнопочные телефоны'])
print(response)