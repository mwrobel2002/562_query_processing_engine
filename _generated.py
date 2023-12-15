
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
from datetime import *

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def initAllAttributes(mf_struct, F_VECT_COMPONENT_ARR=None, all_aggs=False):
    # Function to initialize mf_struct's aggregate values based on the case of either the query containing all aggregates in the select and no grouping variables, or containing grouping variables.
    for key in mf_struct.keys():
        # Initialization of base values for aggregate functions when there are no group by variables, and only aggregate functions in select statement
        if all_aggs:
            # e.g. key = 'count_2_quant'
            [agg_func, agg_table, agg_attr] = key.split('_')
            if agg_func == 'count':
                mf_struct[key] = 0
            elif agg_func == 'sum':
                mf_struct[key] = 0
            elif agg_func == 'min':
                mf_struct[key] = None
            elif agg_func == 'max':
                mf_struct[key] = None
            elif agg_func == 'avg':
                # avg is saved as {sum, count}
                # when completed with full loop to add aggregates: set mf_struct[key] = mf_struct[key]['average'] for all aggregates which agg_func == 'avg'
                mf_struct[key] = {'sum': 0, 'count': 0}
            else:
                raise Exception(f"Unknown aggregate function when initializing mf_struct aggregate values: {agg_func}")
        else:
            # Initialization of base values for aggregate functions for every unique combination of attributes
            for key in mf_struct.keys():
                for agg in F_VECT_COMPONENT_ARR:
                    # e.g. agg = 'count_2_quant'
                    [agg_func, agg_table, agg_attr] = agg.split('_')
                    if agg_func == 'count':
                        mf_struct[key][agg] = 0
                    elif agg_func == 'sum':
                        mf_struct[key][agg] = 0
                    elif agg_func == 'min':
                        mf_struct[key][agg] = None
                    elif agg_func == 'max':
                        mf_struct[key][agg] = None
                    elif agg_func == 'avg':
                        # avg is saved as {sum, count}
                        # when completed with full loop to add aggregates: set mf_struct[key][agg] = mf_struct[key][agg]['average'] for all aggregates which agg_func == 'avg'
                        mf_struct[key][agg] = {'sum': 0, 'count': 0}
                    else:
                        raise Exception(f"Unknown aggregate function when initializing mf_struct aggregate values: {agg_func}")
    return mf_struct
    
    

def updateAggregateValue(mf_struct, typecast_dict, row=None, row_agg_func=None, row_attr_str=None, row_aggregate=None, row_agg_attr=None, all_aggs=False):
    if all_aggs:
        # Increment/Update aggregate values in mf_struct, doing a single pass over the data table. Check which aggregate function is currently being updated in mf_struct.keys(), then update accordingly.
            for key in mf_struct.keys():
                [agg_func, agg_table, agg_attr] = key.split('_')
                if agg_func == 'sum':
                    # For sum, increment by the attribute value from the database table row.
                    mf_struct[key] = mf_struct[key] + int(row[agg_attr])
                elif agg_func == 'count':
                    # For count, simply increment the aggregate value by 1.
                    mf_struct[key] = mf_struct[key] + 1
                elif agg_func == 'avg':
                    # For average, store both the count and sum to compute later after all aggregates have been looped through
                    mf_struct[key]['count'] =  mf_struct[key]['count'] + 1
                    mf_struct[key]['sum'] = mf_struct[key]['sum'] + int(row[agg_attr])
                elif agg_func == 'max':
                    # For max, only replace the aggregate value if the value from the database table row is greater than than the currently stored aggregate in mf_struct.
                    if typecast_dict[agg_attr] == 'string':
                        if mf_struct[key] == None:
                            mf_struct[key] = str(row[agg_attr])
                        elif str(row[agg_attr]) > mf_struct[key]:
                            mf_struct[key] = str(row[agg_attr])
                    elif typecast_dict[agg_attr] == 'int':
                        if mf_struct[key] == None:
                            mf_struct[key] = int(row[agg_attr])
                        elif int(row[agg_attr]) > mf_struct[key]:
                            mf_struct[key] = int(row[agg_attr])
                    elif typecast_dict[agg_attr] == 'date':
                        if mf_struct[key] == None:
                            mf_struct[key] = row[agg_attr]
                        elif row[agg_attr] > mf_struct[key]:
                            mf_struct[key] = row[agg_attr]       
                elif agg_func == 'min':
                    # For min, only replace the aggregate value if the value from the database table row is less than the currently stored aggregate in mf_struct.
                    if typecast_dict[agg_attr] == 'string':
                        if mf_struct[key] == None:
                            mf_struct[key] = str(row[agg_attr])
                        elif str(row[agg_attr]) < mf_struct[key]:
                            mf_struct[key] = str(row[agg_attr])
                    elif typecast_dict[agg_attr] == 'int':
                        if mf_struct[key] == None:
                            mf_struct[key] = int(row[agg_attr])
                        elif int(row[agg_attr]) < mf_struct[key]:
                            mf_struct[key] = int(row[agg_attr])
                    elif typecast_dict[agg_attr] == 'date':
                        if mf_struct[key] == None:
                            mf_struct[key] = row[agg_attr]
                        elif row[agg_attr] < mf_struct[key]:
                            mf_struct[key] = row[agg_attr]  
    else:
        # Increment/Update aggregate values in mf_struct, doing a single pass over the data table. Check which aggregate function is currently being updated by looping over the aggregates arr
        # then update accordingly.
        if row_agg_func == 'count':
            # For count, simply increment the aggregate value by 1.
            mf_struct[row_attr_str][row_aggregate] =  mf_struct[row_attr_str][row_aggregate] + 1
        elif row_agg_func == 'sum':
            # For sum, increment by the attribute value from the database table row.
            mf_struct[row_attr_str][row_aggregate] =  mf_struct[row_attr_str][row_aggregate] + int(row[row_agg_attr])
        elif row_agg_func == 'min':
            # For min, only replace the aggregate value if the value from the database table row is less than the currently stored aggregate in mf_struct.
            if typecast_dict[row_agg_attr] == 'string':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
                elif str(row[row_agg_attr]) < mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
            elif typecast_dict[row_agg_attr] == 'int':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
                elif int(row[row_agg_attr]) < mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
            elif typecast_dict[row_agg_attr] == 'date':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
                elif row[row_agg_attr] < mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
                    
        elif row_agg_func == 'max':
            # For max, only replace the aggregate value if the value from the database table row is greater than than the currently stored aggregate in mf_struct.
            if typecast_dict[row_agg_attr] == 'string':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
                elif str(row[row_agg_attr]) > mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
            elif typecast_dict[row_agg_attr] == 'int':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
                elif int(row[row_agg_attr]) > mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
            elif typecast_dict[row_agg_attr] == 'date':
                if mf_struct[row_attr_str][row_aggregate] == None:
                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
                elif row[row_agg_attr] > mf_struct[row_attr_str][row_aggregate]:
                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
        elif row_agg_func == 'avg':
            # For average, store both the count and sum to compute later after all aggregates have been looped through
            mf_struct[row_attr_str][row_aggregate]['count'] =  mf_struct[row_attr_str][row_aggregate]['count'] + 1
            mf_struct[row_attr_str][row_aggregate]['sum'] = mf_struct[row_attr_str][row_aggregate]['sum'] + int(row[row_agg_attr])
        pass
    return mf_struct

def query():
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')
    
    try:
        conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password, cursor_factory=psycopg2.extras.DictCursor)
    except:
        raise Exception("Database connection unsuccessful")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []
    
    f = open("q5.txt", "r")
    phi_arr = f.readlines()
    S = phi_arr[0].strip()
    n = phi_arr[1].strip()
    V = phi_arr[2].strip()
    F_VECT = phi_arr[3].strip()
    PRED_LIST = phi_arr[4].strip()
    HAVING = phi_arr[5].strip()

    mf_struct = {}
    pred_dict = {}
    possible_comparisons = ['!', '<', '>', '=']
    SELECT_ARR = S.split(',')

    typecast_dict = {
        'cust' : 'string',
        'prod' : 'string',
        'day'  : 'int',
        'month': 'int',
        'year' : 'int',
        'state': 'string',
        'quant': 'int',
        'date' : 'date'
    }

    if (V == 'NONE'):
        # No grouping variables in the query
        # Assume '*' is transposed to every attribute in the table in the arguments of phi already
        temp_row = []
        allAggs_flag = True
        # Must check if all select attributes are aggregates or all attributes are simple data columns.
        for proj in SELECT_ARR:
            if not 'sum' in proj and not 'count' in proj and not 'avg' in proj and not 'min' in proj and not 'max' in proj:
                allAggs_flag = False
                break
        
        if allAggs_flag:
            # All select attributes in the query are aggregate functions.
            for key in SELECT_ARR:
                mf_struct[key] = {}

            F_VECT_COMPONENT_ARR = F_VECT.split(',')
            # Initialization of attributes in mf_struct, and pass through data table to update aggregate values in mf_struct.
            mf_struct = initAllAttributes(mf_struct, F_VECT_COMPONENT_ARR=F_VECT_COMPONENT_ARR, all_aggs=True)
            for row in cur:
                mf_struct = updateAggregateValue(mf_struct, typecast_dict, row=row, all_aggs=True)

            # Compute average values in mf_struct from the stored sum and count (In initAllAttributes and updateAggregateValue)
            for key, value in mf_struct.items():
                [agg_func, agg_table, agg_attr] = key.split('_') 
                if agg_func == 'avg':
                    if int(value['count']) != 0:
                        mf_struct[key] = (int(value['sum'])/int(value['count']))
                    else:
                        mf_struct[key] = 0
                temp_row.append(mf_struct[key])

            # Append all rows of mf_struct to global (output array) and print the tabulation (prettily formatted table string) of output array.
            _global.append(temp_row)

            print("Number of Rows: ", len(_global))
            return tabulate.tabulate(_global,
                            headers=SELECT_ARR, tablefmt="psql")
        else:
            # No aggregates
            # loop through rows in the database
            for row in cur:
                temp_row = []
                for attr in SELECT_ARR:
                    temp_row.append(row[attr])
                # Append all rows of table with correct attributes selected to global (output array) and print the tabulation (prettily formatted table string) of output array.
                _global.append(temp_row)

            print("Number of Rows: ", len(_global))
            return tabulate.tabulate(_global,
                            headers=SELECT_ARR, tablefmt="psql")
    else:
        # There are grouping variables. Handle accordingly.

        # Initialize dictionary for predicates
        PRED_ARR = PRED_LIST.split(';')
        PRED_KEYS = []
        for pred in PRED_ARR:
            # For each predicate (e.g. 1.state='NY'), initialize a key for each grouping variable.
            grp_var = pred[:pred.find('.')]
            comparison = pred[(pred.find('.') + 1):]
            if grp_var in PRED_KEYS:
                pass
            else:
                PRED_KEYS.append(grp_var)
                pred_dict[grp_var] = []

        # For each predicate, append a string to its corresponding grouping variable table array containing the condition string of the predicate.
        for pred in PRED_ARR:
            grp_var = pred[:pred.find('.')]
            comparison = pred[(pred.find('.') + 1):]
            # Initialize empty variables
            pred_attr = ''
            pred_symbol = ''
            pred_value = ''
            temp_index = 0
            # Loop until comparison operator is found - this is the predicate attribute e.g. state
            for letter in comparison:
                if (letter not in possible_comparisons):
                    temp_index += 1
                    pred_attr += letter
                else:
                    break
            # Loop until comparison operator is no longer found found - this is the operator e.g. >=
            for letter in comparison[temp_index:]:
                if letter in possible_comparisons:
                    temp_index += 1
                    pred_symbol += letter
                else:
                    break
            # Remaining string is what the predicate attribute must be compared to - e.g. 'NY' in 1.state='NY'
            pred_value = comparison[temp_index:]
            
            # Append this value as a string to pred_dict separated by underscores e.g. 1.state_>=_'NY'
            pred_str = f"{pred_attr}_{pred_symbol}_{pred_value}"
            pred_dict[grp_var].append(pred_str)
            
            
            
        GROUP_BY_ATTRS = V.split(',')
        GROUP_BY_STR = ""
        # Initialize group by attributes string e.g. cust,prod -> cust_prod
        for attr in GROUP_BY_ATTRS:
            if attr == GROUP_BY_ATTRS[0]:
                GROUP_BY_STR += attr.strip()
            else:
                GROUP_BY_STR += "_" + attr.strip()
        

        GBKEYS_LIST = []
        for row in cur:
            row_attr_str = ""
            # For each row, create a string consisting of the values of each group by attribute, separated by _'s.
            for attr in GROUP_BY_ATTRS:
                attr_str = attr.strip()
                if attr == GROUP_BY_ATTRS[0]:
                    row_attr_str += str(row[attr_str])
                else:
                    row_attr_str += "_" + str(row[attr_str])
            if row_attr_str in GBKEYS_LIST:
                pass
            else:
                GBKEYS_LIST.append(row_attr_str)
                    
        # Creates dictionary of unique grouping attributes and empty dictionary which will eventually contain the agg. vals
        for key in GBKEYS_LIST:
            mf_struct[key] = {}

        # Initialization of base values for aggregate functions for every unique combination of attributes e.g. setting avg_1_quant = {'sum': 0, 'count': 0}, or min_2_quant = None
        F_VECT_COMPONENT_ARR = F_VECT.split(',')
        mf_struct = initAllAttributes(mf_struct, F_VECT_COMPONENT_ARR=F_VECT_COMPONENT_ARR, all_aggs=False)


        # mf_struct has now been initialized with the initial values correspoding to the aggregate functions

        # For each row in the table, begin the process of checking which group by key the row fits, which conditions for each aggregate function/table it fits, and update those aggregate values.
        cur.scroll(0, 'absolute')
        for row in cur:
            row_attr_str = ""
            # For each row, create a string consisting of the values of each group by attribute, separated by _'s.
            for attr in GROUP_BY_ATTRS:
                attr_str = attr.strip()
                if attr == GROUP_BY_ATTRS[0]:
                    row_attr_str += str(row[attr_str])
                else:
                    row_attr_str += "_" + str(row[attr_str])
            # Make sure row's group by string matches up with one in GBKEYS_LIST -> Should always be true, else something went wrong.
            if row_attr_str.strip() in GBKEYS_LIST:
                row_aggregates = mf_struct[row_attr_str].keys()
                # row_aggregate e.g. = 'count_1_quant'
                fits_table_flag = True
                # For each aggregate string, determine if the row fits the conditions of said aggregate (correct table), table conditions are valid e.g. 1.state='NY' checks if row's state is NY.
                for row_aggregate in row_aggregates:
                    fits_table_flag = True
                    [row_agg_func, row_agg_table, row_agg_attr] = row_aggregate.split('_')

                    # Returns a list of all conditions for the grouping variable table.
                    if row_agg_table == '0':
                        conditions_array = []
                    else: 
                        conditions_array = pred_dict[row_agg_table]
                    
                    # For each condition, determine if the row's value correctly compares to the condition requirement.
                    # row_condition = e.g. state='NY', or e.g. quant>100
                    for row_condition in conditions_array:
                        [cond_attr, symbol, value] = row_condition.split('_')
                        value = value.replace("'", "")
                        if symbol == '>':
                            if not row[cond_attr] > value:
                                fits_table_flag = False
                        elif symbol == '>=':
                            if not row[cond_attr] >= value:
                                fits_table_flag = False
                        elif symbol == '<':
                            if not row[cond_attr] < value:
                                fits_table_flag = False
                        elif symbol == '<=':
                            if not row[cond_attr] <= value:
                                fits_table_flag = False
                        elif symbol == '=':
                            if not row[cond_attr] == value:
                                fits_table_flag = False
                        elif symbol == '!=':
                            if not row[cond_attr] != value:
                                fits_table_flag = False

                    # Conditions for the table have been checked. If the row fits the conditions of the table:
                    if fits_table_flag:
                        mf_struct = updateAggregateValue(mf_struct, typecast_dict, row=row, row_agg_func=row_agg_func, row_attr_str=row_attr_str, row_aggregate=row_aggregate, row_agg_attr=row_agg_attr, all_aggs=False)
            else:
                raise Exception("Key not in list: " + row_attr_str)

        # Convert values in mf_struct into rows in _global for returning purposes.
        for non_aggregates, aggregates_dict in mf_struct.items():
            temp_row = []
            passes_conditions_flag = True
            # SELECT cust, prod, avg(2.quant), date
            NON_AGGREGATE_ARR = non_aggregates.split('_')
            for attr in NON_AGGREGATE_ARR:
                temp_row.append(attr.strip())

            # First pass on aggregates_dict to calculate any averages based on sum/count
            for key, value in aggregates_dict.items():
                # key = 'count_1_quant'
                [row_agg_func, row_agg_table, row_agg_attr] = key.split('_')
                if row_agg_func == 'avg':
                    if int(value['count']) != 0:
                        aggregates_dict[key] = (int(value['sum'])/int(value['count']))
                    else:
                        aggregates_dict[key] = 0
            comparison_check = ['>=', '<=', '!=', '>', '<', '=']

            # Check Having Clause here in second pass, and append to _global for return if it passes having clause conditions
            for key, value in aggregates_dict.items():
                # key = 'count_1_quant'
                if HAVING == 'NONE':
                    temp_row.append(value)
                else:
                    HAVING_ARR = HAVING.split(';')
                    comparison = ''
                    # For each predicate in the having array, correctly split based on the comparison operator (and save comparison operator for later).
                    for pred in HAVING_ARR:
                        for comp in comparison_check:
                            if comp in pred:
                                comparison = comp
                                break
                        [having_agg, having_val] = pred.split(comparison)

                        # Cast having_val to correct type based on attribute
                        [havingAggFunc, havingAggTable, havingAggAttr] = having_agg.split('_')
                        havingType = typecast_dict[havingAggAttr]
                        if havingType == 'string':
                            having_val = str(having_val)
                        elif havingType == 'int':
                            having_val = int(having_val)
                        elif havingType == 'date':
                            having_val = datetime.strptime(having_val, "%Y-%m-%d")
                            having_val = having_val.date()

                        else:
                            raise Exception(f"No dictionary entry for the having clause type: {havingType}")

                        if having_agg in aggregates_dict.keys():
                            # aggregates_dict[having_agg] will grab value of the thing e.g. will grab value of count_2_quant (115)
                            if aggregates_dict[having_agg] == None:
                                passes_conditions_flag = False
                            else:
                                if comparison == '>':
                                    if aggregates_dict[having_agg] > having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                                elif comparison == '<':
                                    if aggregates_dict[having_agg] < having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                                elif comparison == '=':
                                    if aggregates_dict[having_agg] == having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                                elif comparison == '>=':
                                    if aggregates_dict[having_agg] >= having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                                elif comparison == '<=':
                                    if aggregates_dict[having_agg] <= having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                                elif comparison == '!=':
                                    if aggregates_dict[having_agg] != having_val:
                                        pass
                                    else:
                                        passes_conditions_flag = False
                                        break
                            
                        else:
                            raise Exception(f"Aggregate {having_agg} not found in aggregate keys list during check for Having clause")
                    if passes_conditions_flag:
                        temp_row.append(value)
            # If aggregate conditions pass, append output to global array.
            if passes_conditions_flag:
                _global.append(temp_row)

    # Return tabulated (formatted string of array) version of output.
    print("Number of Rows: ", len(_global))
    return tabulate.tabulate(_global,
                        headers=SELECT_ARR, tablefmt="psql")
def main():
    print(query())
    
if "__main__" == __name__:
    main()    
        