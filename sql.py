import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv


def query():
    """
    Used for testing standard queries in SQL.
    """
    load_dotenv()

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    dbname = os.getenv('DBNAME')

    conn = psycopg2.connect("dbname="+dbname+" user="+user+" password="+password,
                            cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor()
    cur.execute( '''
        With t1 as (
	select month, max(quant) as max_1_quant
	from sales
	where prod = 'Ice'
	group by month
), t2 as (
	select month, max(quant) as max_2_quant
	from sales
	where prod = 'Cherry'
	group by month
), t3 as (
	select month, max(quant) as max_3_quant
	from sales
	where prod = 'Butter'
	group by month
)
select t1.month, t1.max_1_quant, t2.max_2_quant, t3.max_3_quant
from t1
join t2 on t1.month = t2.month
join t3 on t1.month = t3.month;
''')

    return tabulate.tabulate(cur.fetchall(),
                             headers="keys", tablefmt="psql")


def main():
    print(query())


if "__main__" == __name__:
    main()
