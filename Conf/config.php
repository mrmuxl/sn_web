<?php
return array (

//'配置项'=>'配置值'

'APP_DEBUG' => true, 

'DB_TYPE' => 'mysql', 

'DB_HOST' => '127.0.0.1', 

'DB_NAME' => 'kx', 

'DB_USER' => 'root', 

'DB_PWD' => 'mysql123', 

'DB_PORT' => '3306', 

'DB_PREFIX' => 'kx_', 


'LOG_RECORD' => true, // 开启日志记录   

'LOG_RECORD_LEVEL'  =>  array('EMERG','ALERT','CRIT','ERR','WARN','NOTICE','INFO','DEBUG','SQL'), 
//'LOG_RECORD_LEVEL'  =>  array('EMERG','ALERT','CRIT','ERR'), 
//自动导入工具类
'AUTO_LOAD_PATH'=> 'Think.Util.,ORG.Util.',
'TMPL_ACTION_ERROR'     => 'Public:error', // 默认错误跳转对应的模板文件
'TMPL_ACTION_SUCCESS'   => 'Public:success', // 默认成功跳转对应的模板文件
'DB_FIELDTYPE_CHECK'=>true,  // 开启字段类型验证


'COOKIE_EXPIRE'=> 31104000,
'COOKIE_DOMAIN'=>'local-dev.cn',
'COOKIE_PATH'=>'/',
'COOKIE_PREFIX'=> 'qianmo_',

'ALI_CONFIG'=>array(
	//合作身份者id，以2088开头的16位纯数字
	'partner'      => '2088701946824441',
	
	//安全检验码，以数字和字母组成的32位字符
	'key'          => '6g03a2iveow0iy9wy00n8y0y8jt3xspt',
	
	//签约支付宝账号或卖家支付宝帐户
	'seller_email' => '437061179@qq.com',
	
	//页面跳转同步通知页面路径，要用 http://格式的完整路径，不允许加?id=123这类自定义参数
	//return_url的域名不能写成http://localhost/create_direct_pay_by_user_php_utf8/return_url.php ，否则会导致return_url执行无效
	'return_url'   => 'http://www.local-dev.cn/Pay/return_url',
	
	//服务器异步通知页面路径，要用 http://格式的完整路径，不允许加?id=123这类自定义参数
	'notify_url'   => 'http://www.local-dev.cn/Pay/notify_url',
	
	//↑↑↑↑↑↑↑↑↑↑请在这里配置您的基本信息↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
	
	
	//签名方式 不需修改
	'sign_type'    => 'MD5',
	
	//字符编码格式 目前支持 gbk 或 utf-8
	'input_charset'=> 'utf-8',
	
	//访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
	'transport'    => 'http'
),

//自定义配置

'UPLOAD_PATH'=>'./Public/Upload',

'UPLOAD_SIZE' =>  3145728 ,

'PROJECT_HOME'=>'E:\\workspace\\php\\kx\\trunk\\src\\server',

'WWW'=>'http://www.local-dev.cn',
'IMG'=>'http://img.local-dev.cn',
'STATIC'=> 'http://static.local-dev.cn',
'DOWNLOAD'=> 'http://static.local-dev.cn',
'DOMAIN'=> 'local-dev.cn',

);
