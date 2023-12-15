/*Query 1*/
select cust, prod, quant
from sales;

/*Query 2*/
With t1 as (
	select cust, prod, sum(quant) as sum_1_quant
	from sales
	where state = 'NY'
	group by cust, prod
), t2 as (
	select cust, prod, sum(quant) as sum_2_quant
	from sales
	where state = 'NJ'
	group by cust, prod
), t3 as (
	select cust, prod, sum(quant) as sum_3_quant
	from sales
	where state = 'CT'
	group by cust, prod
)
select t1.cust, t1.prod, t1.sum_1_quant, t2.sum_2_quant, t3.sum_3_quant
from t1
join t2 on t1.cust = t2.cust and t1.prod = t2.prod
join t3 on t1.cust = t3.cust and t1.prod = t3.prod;

/*Query 3*/
With t1 as (
	select cust, prod, min(date) as min_1_date, sum(quant) as sum_1_quant
	from sales
	where state = 'NY'
	group by cust, prod
), t2 as (
	select cust, prod, count(quant) as count_2_quant
	from sales
	where state = 'NJ'
	group by cust, prod
)
select t1.cust, t1.prod, t1.min_1_date, t1.sum_1_quant, t2.count_2_quant 
from t1
join t2 on t1.cust = t2.cust and t1.prod = t2.prod
where t1.min_1_date < '2018-01-01' and t2.count_2_quant > 50;

/*Query 4*/
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


/*Query 5*/
select cust, prod, month, avg(quant), min(date), max(date)
from sales
group by cust, prod, month;

/*Current Query*/