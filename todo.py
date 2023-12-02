"""

TODO LIST:

1. Ask professor about uncommon aggregates such VARIANCE, MEDIAN. Do we need to handle them?
2. Ask how an EMF query would impact phi operator

hashmap h

for row in cursor.rows
    if h.contains(row.groupby_vars):

    else:
        h.insert(groupby_vars, row(F_VECT[1]), row(F_VECT[2])) 

        
3. How to show in the phi operator "and" VS "or" in the predicate list of comparisons from SQL 
"""