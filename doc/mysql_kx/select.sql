insert into print(email,is_print,print_num,used_print_num,create_at,expire)select email,1,999,0,now(),'2013-12-30 00:00:00' from  vipuser;
insert into shared(email,is_shared,shared_num,used_shared_num,create_at,expire)select email,1,999,0,now(),'2013-12-30 00:00:00' from  vipuser;

update publish_user set ver= 31 where email !='simplenect@simplenect.com' and email != 'update@simplenect.com';
