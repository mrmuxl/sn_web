<?php
/**
 * 
 * 用户模型
 * @author 莫柯明
 *
 */
class UserModel extends Model {

	
	protected $readonlyField = array('email');//只读字段 不允许修改

	
	
	protected $_auto = array (
		array ('status', '1' ), // 新增的时候把status字段设置为1
		//array ('password', 'md5', 1, 'function' ), // 对password字段在新增的时候使md5函数处理
		array ('create_time', 'get_date_time', 1, 'function' ), // 对create_time字段在新增的时候写入当前时间戳
		array ('last_login', 'get_date_time', 1, 'function'), //在新增时候都写入当前时间戳
		array ('update_time', 'get_date_time', 3, 'function' ),
	
		);
	
	protected $_validate = array (
		//array ('verify', 'require', '验证码必须！' ), //默认情况下用正则进行验证
		array('email','require','用户名必须！'),
		array('email','email','邮箱格式不正确！'),
		array ('email', 'require', '邮箱已经存在！', 0, unique, 1 ), // 在新增的时候验证name字段是否唯一
		array('nick','require','昵称必须！'),
		array('password','require','密码必须！'),
		array ('repassword', 'password', '确认密码不正确！', 0, 'confirm' ), // 验证确认密码是否和密码一致

	);

}
