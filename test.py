
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
from datetime import *

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py
def query():
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []
    
    f = open("q4.txt", "r")
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
        #Assume '*' is transposed to every attribute in the table in the arguments of phi already
        temp_row = []
        
        # loop through rows in the database
        for row in cur:
            temp_row = []
            for attr in SELECT_ARR:
                temp_row.append(row[attr])
            _global.append(temp_row)
        
        return tabulate.tabulate(_global,
                        headers=SELECT_ARR, tablefmt="psql")
    else:

        PRED_ARR = PRED_LIST.split(';')

        # {
        #     1: ['1.quant_!=_100', '1.state_=_NY', '1.quant_>_10', '1.quant>_2.quant']
        #     2: {}
        #     3: {}
        # }

    # [2,1,3]
        # Initialize dictionary for predicates
        PRED_KEYS = []
        for pred in PRED_ARR:
            grp_var = pred[:pred.find('.')]
            comparison = pred[(pred.find('.') + 1):]
            if grp_var in PRED_KEYS:
                pass
            else:
                PRED_KEYS.append(grp_var)
                pred_dict[grp_var] = []

        for pred in PRED_ARR:
            grp_var = pred[:pred.find('.')]
            comparison = pred[(pred.find('.') + 1):]
            pred_attr = ''
            pred_symbol = ''
            pred_value = ''
            temp_index = 0
            for letter in comparison:
                if (letter not in possible_comparisons):
                    temp_index += 1
                    pred_attr += letter
                else:
                    break

            for letter in comparison[temp_index:]:
                if letter in possible_comparisons:
                    temp_index += 1
                    pred_symbol += letter
                else:
                    break

            pred_value = comparison[temp_index:]
            
            pred_str = f"{pred_attr}_{pred_symbol}_{pred_value}"
            pred_dict[grp_var].append(pred_str)
            
            
            
        GROUP_BY_ATTRS = V.split(',')
        GROUP_BY_STR = ""
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
                    
        #Creates dictionary of unique grouping attributes and empty dictionary which will eventually contain the agg. vals
        for key in GBKEYS_LIST:
            mf_struct[key] = {}

        # Initialization of base values for aggregate functions for every unique combination of attributes
        F_VECT_COMPONENT_ARR = F_VECT.split(',')
        for key in mf_struct.keys():
            for agg in F_VECT_COMPONENT_ARR:
                # agg = 'count_2_quant'
                [agg_func, agg_table, agg_attr] = agg.split('_')
                if agg_func == 'count':
                    # e.g. key = 'joe_fruit', agg = 'count_2_quant'
                    mf_struct[key][agg] = 0
                elif agg_func == 'sum':
                    # e.g. key = 'joe_fruit', agg = 'count_2_quant'
                    mf_struct[key][agg] = 0
                elif agg_func == 'min':
                    # e.g. key = 'joe_fruit', agg = 'count_2_quant'
                    # Highest 
                    mf_struct[key][agg] = None
                elif agg_func == 'max':
                    # e.g. key = 'joe_fruit', agg = 'count_2_quant'
                    mf_struct[key][agg] = None
                elif agg_func == 'avg':
                    # e.g. key = 'joe_fruit', agg = 'count_2_quant'
                    # avg saved as {sum, count}
                    # when completed with full loop to add aggregates: set mf_struct[key][agg] = mf_struct[key][agg]['average'] for all aggregates which agg_func == 'avg'
                    mf_struct[key][agg] = {'sum': 0, 'count': 0}
                else:
                    raise Exception(f"Unknown aggregate function when initializing mf_struct aggregate values: {agg_func}")
        
        # return mf_struct
        # mf_struct has been initialized with the initial values correspoding to the aggregate functions

        cur.scroll(0, 'absolute')
        for row in cur:
            row_attr_str = ""
            # For eaceh row, create a string consisting of the values of each group by attribute, separated by _'s.
            for attr in GROUP_BY_ATTRS:
                attr_str = attr.strip()
                if attr == GROUP_BY_ATTRS[0]:
                    row_attr_str += str(row[attr_str])
                else:
                    row_attr_str += "_" + str(row[attr_str])
            if row_attr_str.strip() in GBKEYS_LIST:
                row_aggregates = mf_struct[row_attr_str].keys()
                # row_aggregate e.g. = 'count_1_quant'
                fits_table_flag = True
                for row_aggregate in row_aggregates:
                    fits_table_flag = True
                    [row_agg_func, row_agg_table, row_agg_attr] = row_aggregate.split('_')

                    #Returns a list of all the conditions
                    # example is quant_>_100 (attr_symbol_value)
                    conditions_array = pred_dict[row_agg_table]
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
                        if row_agg_func == 'count':
                            mf_struct[row_attr_str][row_aggregate] =  mf_struct[row_attr_str][row_aggregate] + 1
                        elif row_agg_func == 'sum':
                            mf_struct[row_attr_str][row_aggregate] =  mf_struct[row_attr_str][row_aggregate] + int(row[row_agg_attr])
                        elif row_agg_func == 'min':
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
                            # print('Im in max')
                            if typecast_dict[row_agg_attr] == 'string':
                                # print('type = string')
                                if mf_struct[row_attr_str][row_aggregate] == None:
                                    # print('mf struct row attr = None')
                                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
                                elif str(row[row_agg_attr]) > mf_struct[row_attr_str][row_aggregate]:
                                    # print('mf struct row attr exists')
                                    mf_struct[row_attr_str][row_aggregate] = str(row[row_agg_attr])
                            elif typecast_dict[row_agg_attr] == 'int':
                                # print('type = int')
                                if mf_struct[row_attr_str][row_aggregate] == None:
                                    # print('mf struct row attr = None')
                                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
                                elif int(row[row_agg_attr]) > mf_struct[row_attr_str][row_aggregate]:
                                    # print('mf struct row attr exists')
                                    mf_struct[row_attr_str][row_aggregate] = int(row[row_agg_attr])
                            elif typecast_dict[row_agg_attr] == 'date':
                                # print('type = date')
                                if mf_struct[row_attr_str][row_aggregate] == None:
                                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
                                elif row[row_agg_attr] > mf_struct[row_attr_str][row_aggregate]:
                                    mf_struct[row_attr_str][row_aggregate] = row[row_agg_attr]
                        elif row_agg_func == 'avg':
                            mf_struct[row_attr_str][row_aggregate]['count'] =  mf_struct[row_attr_str][row_aggregate]['count'] + 1
                            mf_struct[row_attr_str][row_aggregate]['sum'] = mf_struct[row_attr_str][row_aggregate]['sum'] + int(row[row_agg_attr])            
            else:
                raise Exception("Key not in list: " + row_attr_str)

        # Convert values in mf_struct into rows in _global for returning purposes.
        for non_aggregates, aggregates_dict in mf_struct.items():
            # non_aggregates = 'Boo_Cherry', aggregates_dict = {
                                                            #    'count_1_quant': 235,
                                                            #    'avg_2_quant': {'sum': 23492, 'count': 49},
                                                            #  }
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
                    for pred in HAVING_ARR:
                        for comp in comparison_check:
                            if comp in pred:
                                comparison = comp
                                break
                        [having_agg, having_val] = pred.split(comparison)

                        #Cast having_val
                        
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
                            # non_aggregates = 'Boo_Cherry', aggregates_dict = {
                                                            #    'count_1_quant': 235,
                                                            #    'avg_2_quant': 523,
                                                            #  }

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
            # here
            if passes_conditions_flag:
                _global.append(temp_row)
    
    return _global, tabulate.tabulate(_global,
                        headers=SELECT_ARR, tablefmt="psql")

def main():
    returned_array, pretty_str = query()
    print(pretty_str)
    
if "__main__" == __name__:
    main()
    