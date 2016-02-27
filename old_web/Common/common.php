<?php
define ( 'SESSION_NEW', 1 );
define ( 'SESSION_UPDATE', 2 );

//默认输出模板定义
define ( 'DEFAULT_DISPLAY', "Layout:default" );
define ( 'DEFAULT_ERROR', ":error" );
define ( 'DEFAULT_ADMIN', "Layout:admin_index" );

//角色定义
//中央服务器管理员ID
define ( 'ROLE_ROOT', 1 );
//企业管理员
define ( 'ROLE_ENT_ROOT', 2 );
//企业普通用户
define ( 'ROLE_ENT_USER', 3 );

//默认分页显示每页的记录数
define ( 'PAGE_NUM_DEFAULT', 24 );
load ( "extend" );
/**
 * 
 * 获取登录用户信息
 */
function getLoginUser() {
	
	if (isLogin ()) {
		$User = M ( "User" );
		$User->create ();
		$map ['id'] = $_SESSION ['UID'];
		
		$user = $User->where ( $map )
			->find ();
		if ($user != null)
			return $user;
	}
	return false;
}

/**
 * 
 * 设置登陆用户的SESSION
 * @param $name
 * @param $value
 */
function setSession($status=1, $user) {
	//用户登录
	if ($status == 1) {
		Session::set ( "nick", $user ['nick'] );
		Session::set ( "UID", $user ['id'] );
		if($user['status']==0){
			Session::set ( "active", $user ['id'] );
		}
		if($user['avatar']!=null&&trim($user['avatar'])!=""){
			Session::set("avatar",$user['avatar']);
		}
		if ($user ['id'] == ROLE_ROOT) {
			Session::set ( "RID", ROLE_ROOT );
		} else {
			//TODO 判断企业管理员及普通用户
			Session::set ( "RID", -1 );
		}
	
	} else if ($status == 2) { //用户更改自己信息时
		Session::set ( "nick", $user );
	}
}

function setOurCookie($uid, $eid, $isEntMaster, $lasttime) {
	Cookie::set ( "entusers_id", $uid );
	Cookie::set ( "ent_id", $eid );
	Cookie::set ( "isentmaster", $isEntMaster );
	Cookie::set ( "lasttime", $lasttime );
}
/**
 * 
 * 判断用户是否登录
 */
function isLogin() {
	if (isset ( $_SESSION ['UID'] )) {
		
		return true;
	}
	
	return false;
}

/**
 * 获取用户IP
 */
function get_user_ip() {
	$ip = get_client_ip ();
	return $ip;
}

function is_client_login() {
	if (Cookie::is_set("entusers_id")&&Cookie::is_set("ent_id")&&Cookie::is_set("isentmaster")&&Cookie::is_set("lasttime")){
		if(Cookie::get("entusers_id")>0&&Cookie::get("ent_id")>0&&Cookie::get("isentmaster")>=0)
			return true;
	}
	return false;
}

/**
 * 
 * 验证邮箱格式是否正确
 */
function check_email_format($email){
	if($email==null||trim($email)==""){
		return false;
	}
	$exp = "^[a-z'0-9]+([._-]*[a-z'0-9]+[._-]*)*@([a-z0-9]+([._-]*[a-z0-9]+[._-]*))+$";
	if(eregi($exp,$email)){
		return true;
	}		
	return false;
}
/**
 * 
 * 获取客户端登陆用户信息
 */
function get_clogin_user(){
	if(is_client_login()){
		$uid=get_cuser_id();
		$User=M("User");
		$user=$User->find($uid);
		if(isset($user['id'])&&$user['id']>0){
			return $user;
		}
	}
	return false;
}
/**
 * 
 * 客户端用户是否是企业管理员
 * 
 */
function is_ent_master(){
	if(is_client_login()){
		if(Cookie::get("isentmaster")==1)
			return true;
	}
	return false;
}

function get_cuser_id(){
	return Cookie::get("entusers_id");
}

function update_ent_version($entId){
	$Ent=M("Ent");
	$data['id']=$entId;
	$data['version']=time();
	$Ent->save($data);
}

function getUserRole() {
	if (isLogin ()) {
		//TODO 查询用户角色
	}
}

function isRoot() {
	if (isLogin ()) {
		if (intval ( $_SESSION ['RID'] ) === ROLE_ROOT)
			return true;
		return false;
	}
	return false;
}

function isAdmin() {
	if (isLogin ()) {
		if (intval ( $_SESSION ['RID'] ) === ROLE_ADMIN)
			return true;
		return false;
	}
	return false;
}

function get_user_id() {
	if (isLogin ())
		return $_SESSION ['UID'];
	return false;
}
/**
 * 默认获取当前时间
 * 格式为：1970-01-01 11:30:45
 * $differ 单位秒，距离现在的时间，
 * 		        负数表示多少秒之前的时间
 * 		        正数表示多少秒之后的时间
 */
function get_date_time($differ=0) {
	//import ( "ORG.Util.Date" );
	//$date = new Date ();
	$format = "%Y-%m-%d %H:%M:%S";
	$date=time()+$differ;
	return strftime($format, $date);
	//return $date->format ( $format = "%Y-%m-%d %H:%M:%S" );
}
function get_date($differ=0) {
	//import ( "ORG.Util.Date" );
	//$date = new Date ();
	$format = "%Y-%m-%d";
	$date=time()+$differ;
	return strftime($format, $date);
	//return $date->format ( $format = "%Y-%m-%d %H:%M:%S" );
}

/**
 * 
 * 二进制流转化为字符串
 * @param $input
 */
function bin2bstr($input)
// Convert a binary expression (e.g., "100111") into a binary-string
{
  if (!is_string($input)) return null; // Sanity check
  // Pack into a string
  $input = str_split($input, 4);
  $str = '';
  foreach ($input as $v)
  {
   $str .= base_convert($v, 2, 16);
  }
 
  $str =  pack('H*', $str);
 
  return $str;
}

/**
 * 
 * 字符串转化为二进制流
 * @param $input
 */
function bstr2bin($input)
// Binary representation of a binary-string
{
  if (!is_string($input)) return null; // Sanity check
  // Unpack as a hexadecimal string
  $value = unpack('H*', $input);
 
  // Output binary representation
  $value = str_split($value[1], 1);
  $bin = '';
  foreach ($value as $v)
  {
   $b = str_pad(base_convert($v, 16, 2), 4, '0', STR_PAD_LEFT);
   
   $bin .= $b;
  }
 
  return $bin;
}


/**
 * 
 * 文件上传
 * @param $thum  是否生成缩略图
 * @param $thumMaxHeight  缩略图的最大高度
 * @param $thumbMaxWidth	缩略图的最大宽度
 * @param $domain	指定上传文件的主目录
 * @param $type  上传文件类型
 */
function saveFile($thumb = false, $thumbMaxWidth = 160, $thumbMaxHeight = 160, $domain,$type=false) {
	import ( "ORG.Net.UploadFile" );
	
	$upload = new UploadFile (); // 实例化上传类
	

	$upload->maxSize = C ( 'UPLOAD_SIZE' ); // 设置附件上传大小
	
	if($type===false){
		$upload->allowExts = array ('jpg', 'gif', 'png', 'jpeg', 'swf' ); // 设置附件上传类型
	}else{
		$upload->allowExts =$type;
	}
	$date = date ( "Y/m/d" );
	//print "date===" . $date;
	$upload->savePath = C ( 'UPLOAD_PATH' ) . '/' . $domain . '/' . $date . '/'; // 设置附件上传目录
	//print "savePath----" . $upload->savePath;
	muti_mkdir ( $upload->savePath );
	//设置是否生成缩略图及其最大宽、高
	if ($thumb === true) {
		$upload->thumb = $thumb;
		$upload->thumbMaxWidth = $thumbMaxWidth;
		$upload->thumbMaxHeight = $thumbMaxHeight;
		$upload->thumbPrefix = "snap_" . $thumbMaxWidth . "X" . $thumbMaxHeight . "_";
	}
	$upload->saveRule = "uniqid"; //文件名生成规则
	

	if (! $upload->upload ()) { // 上传错误提示错误信息
		exit ( $upload->getErrorMsg () . "  " );
		//$this->error($upload->getErrorMsg());
		return false;
	} else { // 上传成功获取上传文件信息
		

		$info = $upload->getUploadFileInfo ();
		//print "上传信息：" . $info [0] ['savepath'];
		$start = strlen ( C ( 'UPLOAD_PATH' ) ) + 1;
		for($i = 0; $i < count ( $info ); $i ++) {
			$str = $info [$i] ['savepath'];
			//print "path---" . $str;
			$picPath = msubstr ( $str, $start, (strlen ( $str ) - $start - 1) );
			$picSaveName = msubstr ( $info [$i] ['savename'], 0, 13 );
			//保存上传文件信息至DB
			$info [$i] ['saveContent'] = "folder=" . $picPath . ",uid=" . $picSaveName . ",ext=" . $info [$i] ['extension'] . ",swidth=" . $thumbMaxWidth . ",sheight=" . $thumbMaxHeight . ",name=" . $info [$i] ['name'] . ",size=" . $info [$i] ['size'];
		}
		//print "real====".$info[0]['realsavepath'];
		return $info;
	}
}

/**
 * 
 * 上传文件所在位置
 * @param $picMsg
 */
function getPicUri($picMsg) {
	if(null==$picMsg||""==trim($picMsg)){
		return "";
	}
	$array = explode ( ",", $picMsg );
	$folder = msubstr ( $array [0], 7, strlen ( $array [0] ) );
	return $folder;
}

/**
 * 
 * 上传文件保存后的名称
 * @param  $picMsg
 */
function getPicName($picMsg) {
	if(null==$picMsg||""==trim($picMsg)){
		return "";
	}
	$array = explode ( ",", $picMsg );
	$uid = msubstr ( $array [1], 4, strlen ( $array [1] ) );
	$ext = msubstr ( $array [2], 4, strlen ( $array [2] ) );
	return $uid . "." . $ext;
}


/**
 * 创建多级目录
 */
function muti_mkdir($dir) {
	if (! is_dir ( $dir )) {
		if (! muti_mkdir ( dirname ( $dir ) )) {
			return false;
		}
		if (! mkdir ( $dir, 0777 )) {
			return false;
		}
	}
	return true;
}

/**
 * 
 * 获取前几位的IP
 * @param $ip
 */
function getBeforeIp($ip){
	if($ip==null||trim($ip)==""){
		return "*.*.*.*";
	}
	$ipList=explode(".", $ip);
	return $ipList[0].".".$ipList[1].".*.*";
}

/** 
 * 批量删除文件
 * @param $files
 */
function del_files($files) {
	if (! empty ( $files )) {
		//print count($files);
		for($i = 0; $i < count ( $files ); $i ++) {
			if (file_exists ( $files [$i] )) {
				//print $files[$i];//."===i=".$i;
				unlink ( $files [$i] );
			}
		}
	}
}

/**
 * 删除被取代的用户头像
 */
function delUserAvatar($picMsg){
	$all_path = array ();
	$folder = getPicUri ( $picMsg );
	$name = getPicName ( $picMsg );
	$project = C ( 'PROJECT_HOME' ) . msubstr ( C ( 'UPLOAD_PATH' ), 1, strlen ( C ( 'UPLOAD_PATH' ) ) );
	$all_path [0] = $project . "/" . $folder . "/" . $name;
	$all_path [1] = $project . "/" . $folder . "/snap_50X50_" . $name;
	del_files($all_path);

}