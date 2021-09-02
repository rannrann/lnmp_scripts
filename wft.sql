select s.employee_id, name, sum(basic+bonus) as total from salary as s
inner join employees as e
on s.employee_id=e.employee_id
where year(date)=2018
group by s.employee_id;

select date,name, basic+bonus as total
from salary as s
inner join employees as e
on s.employee_id = e.employee_id
where e.employee_id = 11 and year(date)=2018;

select s.employee_id,name,sum(basic+bonus) as total
from salary as s
inner join employees as e
on s.employee_id = e.employee_id
group by employee_id
having sum(basic+bonus) > 300000;


select grade,count(*) from salary as s
inner join wage_grade as w
on basic between w.low and w.high
where year(date) = 2018 and month(date) = 12
group by grade;

select name, grade from salary as s
inner join wage_grade as w
on basic between w.low and w.high
inner join employees as e
on s.employee_id = e.employee_id
where year(date) = 2018 and month(date) = 12;

select name, ,grade from salary as s
inner join wage_grade as w
on basic between w.low and w.high
inner join employees as e
on s.employee_id = e.employee_id
where year(date) = 2018 and month(date) = 12;

select name,dept_name,email from departments as d
inner join employees as e
on e.dept_id = d.dept_id
group by name;

select dept_id, min(birth_date) as t from employees
group by dept_id;

select concat(dept_id, '-->', dept_name) from departments

select dept_id,count(*) from employees group by dept_id
select dept_id from departments where dept_name='开发部';

select dept_id,count(*) from employees
group by dept_id
having count(*) < (select count(*) from employees where dept_id=(
select dept_id from departments where dept_name='开发部'
));

select e.dept_id, dept_name, count(*) from employees as e
inner join departments as d
on e.dept_id = d.dept_id
group by dept_id;

select e.dept_id, name, min(birth_date) from employees as e
inner join departments as d
on e.dept_id = d.dept_id
group by dept_id
having birth_date = min(birth_date);

select e.dept_id, dept_name, (
select count(*) from departments as d

)
group by dept_id;


select *  from departments d
right outer join employees

select * from employees where dept_id=(
select dept_id from departments where dept_name = "人事部"
)
or dept_id=(
select dept_id from departments where dept_name = "财务部"
);

select * from employees where dept_id=(
select dept_id from departments where dept_name = "人事部" or dept_name = "财务部"
);

select e.employee_id,name,dept_name,basic+bonus
from employees as e
inner join salary as s
on e.employee_id = s.employee_id
inner join departments as d
on e.dept_id = d.dept_id
where e.dept_id = (
select dept_id from departments where dept_name="人事部"
)
and date="20181210";

select e.employee_id, name, basic,bonus as total
from employees as e
inner join salary as s
on e.employee_id = s.employee_id
where date='20181210'

select e.employee_id, name, basic+bonus as total
from employees as e
inner join salary as s
on e.employee_id = s.employee_id
where basic = (
select max(basic) from salary where date='20181210'
)
and bonus=(
select max(bonus) from salary where date='20181210'
)
and date='20181210';

select e.employee_id, name, basic+bonus as total
from salary as s
inner join employees as e
on s.employee_id=e.employee_id
where date="20181210"
and having total=(
    select max(basic+bonus) from salary where date = '20181210'
);

select max(basic),max(bonus) from salary

select employee_id,dept_id, name, email
from employees as e
where dept_id =3;

select dept_id, dept_name, employees_id, name, email
from(
    select dept_name, e.*
    from departments as d
    inner join employees as e
    on d.dept_id=e.dept_id
)
where dept_id = 3;


(select name, birth_date from employees
where year(birth_date) < 1972)
union all
(select name, birth_date from employees
where year(birth_date) < 1972);

insert into employees values
(134, '张三', '2019-5-10', '2000-10-12', 'zhangsan@tedu.cn', '15088772354', 9),
(135, '李四', '2020-8-20', '1999-6-23', 'lisi@tedu.cn', '13323458734', 9);

update departments as d
inner join employees as e
on d.dept_id = e.dept_id
set dept_name='企划部'
where name = '李四';

delete e
from employees as e
inner join departments as d
on e.dept_id = d.dept_id
where dept_name = '企划部';