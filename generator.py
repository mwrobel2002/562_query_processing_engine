import subprocess

# avg_2_quant, avg_3_quant
# {'avg_2_quant':(sum, count), 'avg_3_quant':(sum, count)} 
# {'avg_2_quant':(1000, 6), 'avg_3_quant':(50, 1)}
# aggregates [avg_2_quant, avg_3_quant, sum_2_quant]
# for row in table
    # get row values
    # hashmap.push('customer_name', [0, 0, 50])
    # average_dict['customer_name']['avg_2_quant'][0] += row.value (SUM)
    # average_dict['customer_name']['avg_2_quant'][0] += 1 (COUNT)
# after the for loop concludes
# hashmap[customer_name].avg_2_quant = average_dict[customer_name][avg_2_quant][0] / average_dict[customer_name][avg_2_quant][1]


    # average_dict.
def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    f = open("q1.txt", "r")
    phi_arr = f.readlines()
    print('------------------------')
    print(phi_arr)
    S = phi_arr[0].strip('\n')
    n = phi_arr[1].strip('\n')
    V = phi_arr[2].strip('\n')
    F_VECT = phi_arr[3].strip('\n')
    PRED_LIST = phi_arr[4].strip('\n')
    HAVING = phi_arr[5].strip('\n')
    print(S)
    print(n)
    print(V)
    print(F_VECT)
    print(PRED_LIST)
    print(HAVING)
    print('------------------------')

    F_VECT_COMPONENT_ARR = F_VECT.split(',').split


    # Flags to determine if this exists among any of the aggregates after looping through each individually
    count_flag = False
    sum_flag = False
    max_flag = False
    min_flag = False
    avg_flag = False

    for agg in F_VECT_COMPONENT_ARR:
        current_aggregate = agg.split('_')
    
    print('------------------------')
   
    mf_struct = {}

    body = """
    for row in cur:
        if row['quant'] > 10:
            _global.append(row)
    """


    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv

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
    {body}
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code to a file
    open("_generated.py", "w").write(tmp)
    # Execute the generated code
    subprocess.run(["python", "_generated.py"])


if "__main__" == __name__:
    main()
