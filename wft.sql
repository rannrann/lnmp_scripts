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

create view emp_view
as
    select name, email, dept_name
    from employees as e
    inner join departments as d
    on e.dept_id = d.dept_id;

create view emp_sal_view
as
    select name, date, basic+bonus as total
    from employees as e
    inner join salary as s
    on e.employee_id = s.employee_id;

create or replace view emp_view
as
    select name, email, d.dept_id, dept_name
    from employees as e
    inner join departments as d
    on e.dept_id = d.dept_id;

alter view emp_sal_view
as
    select date, e.employee_id, name, basic, bonus, basic+bonus as total
    from employees as e
    inner join salary as s
    on e.employee_id = s.employee_id;


delimiter //
create procedure empcount_pro(inout dept_no int)
begin
    select count(*) from employees
    where dept_id=dept_no;
end //
delimiter ;

call empcount_pro(4);

delimiter //
create procedure insdep_pro(in dname varchar(10))
begin
    insert into mydb.departments set dept_name = dname;
end//
delimiter;

call insdep_pro('运维部');
call insdep_pro('开发部');

delimiter //
create procedure empemail_pro(in emp_name varchar(10), out mail varchar(25))
begin
    select email into mail
    from nsd2021.employees
    where name = emp_name;
end//

delimiter ;
call empemail_pro('刘倩', @m);
select @m;

delimiter //
create procedure myadd(INOUT i int)
begin
    set i = i+100;
end //

delimiter ;
set @n=8;
call myadd(@n);

select @n;

delimiter //
create procedure aaa(in i int, in j int, out result int)
begin
    select i+j into result;
end //
delimiter ;
set @i=1;
set @j=2;
call aaa(@i,@j,@re);
select @re;


delimiter //
create procedure deptype_pro(in no int, out dept_type varchar(5))
begin
    declare name varchar(5);
    select dept_name into name from departments
    where dept_id = no;
    if name='运维部' then
        set dept_type = '技术部';
    elseif name = '开发部' then
        set dept_type = '技术部';
    elseif name = '测试部' then
        set dept_type = '技术部';
    else
        set dept_type = '非技术部';
    end if;
end //

delimiter ;
call deptype_pro(1, @t);
select @t;

delimiter //
create procedure deptype_pro2(in no int, out dept_type varchar(5))
begin
    declare name varchar(5);
    select dept_name into name from departments
    where dept_id = no;
    case name
    when '运维部' then set dept_type = '技术部';
    when '开发部' then set dept_type = '技术部';
    when '测试部' then set dept_type = '技术部';
    else set dept_type='非技术部';
    end case;
end //

delimiter ;
call deptype_pro2(1, @tt);
select @tt;

delimiter //
create procedure while_pro(in i int)
begin
    declare j int default 1;
    while j<i do
        insert into departments(dept_name) values(concat('hr',j));
        set j=j+1;
    end while;
end //
delimiter ;
call while_pro(2);
select dept_name from departments;

delimiter //
create procedure while_pro2(in i int)
begin
    declare j int default 1;
    a:while j<i do
        insert into departments(dept_name) values('hr');
        if j>=2 then
            leave a;
        end if;
        set j=j+1;
    end while a;
end //

delimiter ;
call while_pro2(10);
