<?php
/**
 * 
 * 用户功能模块
 * @author 
 *
 */

class UserAction extends CommonAction {
	
	/**
	 * 
	 * 用户列表
	 */
	public function ulist(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$map=array();
		$con="1=1 ";
		if(isset($_GET['search_key'])&&intval($_GET['search_key'])>0){
			$skey=intval($_GET['search_key']);
			$map['search_key']=$skey;
			if(isset($_GET['search_value'])&&trim($_GET['search_value'])!=""){
				$sval=trim($_GET['search_value']);
				$map['search_value']=$sval;
				switch ($skey){
					case 1:{$con.=" and id='".$sval."'";break;}
					case 2:{$con.=" and nick='".$sval."'";break;}
					case 3:{$con.=" and email='".$sval."'";break;}
					default:;
				}
			}
		}
		$p=1;
		if(isset($_GET['p'])&&intval($_GET['p'])>0){
			$p=intval($_GET['p']);
		}
		$User=M("User");
		$count=$User->where($con)->count();
		$Page=new Page($count, PAGE_NUM_DEFAULT);
		foreach($map as $key=>$val) {
			$Page->parameter   .=   "$key=".urlencode($val)."&";
	   	}
	   	$page=$Page->show();
		$uList=$User->where($con)->order("create_time desc")->field("id,nick,email,qianmo_dot,con_qianmo_dot,status")->page($p.",".PAGE_NUM_DEFAULT)->select();

		$this->assign("uList",$uList);
		$this->assign("page",$page);
		$this->assign("map",$map);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 注册
	 */
	public function register() {
		
		$email="";
		if(isset($_GET['invate_code'])&&trim($_GET['invate_code'])!=""){
			$EmailInvate=M("EmailInvate");
			$invate_code=trim($_GET['invate_code']);
			$invate=$EmailInvate->where("invate_code='".$invate_code."'")->find();
			if(isset($invate['id'])){
				$email=$invate['invate_email'];
				$this->assign("invate_code",trim($_GET['invate_code']));
			}
		}
		/* 2013-02-18 修改 未注册好友邀请直接改为添加好友，
		 * 也不要在注册链接表示邀请人
		else if(isset($_GET['uf'])&&trim($_GET['uf'])!=""){
			$uf=explode(",", base64_decode(trim($_GET['uf'])));
			if(count($uf)>0){
				$email=$uf[1];
				Cookie::set("add_ff", $uf[0],2592000);//邀请人的EMAIL
			}
		}
		*/
		$this->assign("email",$email);
		$this->display ( DEFAULT_DISPLAY );
	}
	
//	public function save() {
//		if (isset ( $_POST ['email'] )) {
//			$User = D ( "User" );
//			if (! $User->create ()) {
//				// 如果创建失败 表示验证没有通过 输出错误提示信息
//				exit ( $User->getError () . ' [ <A HREF="javascript:history.back()">返 回</A> ]' );
//			} else {
//				// 验证通过 可以进行其他数据操作
//				$User->password = md5 ( trim ( $_POST ['password'] ) );
//				$result = $User->add ();
//				//print "ID--" . $result;
//				
//
//				if ($result !== false) {
//					if ($result > 0) {
//						$uid = $result;
//						$Ent = M ( "Ent" );
//						
//						$data ['ent_name'] = $_POST ['email'];
//						$data ['ent_reg_date'] = get_date_time ();
//						$data ['ent_master_id'] = $uid;
//						$data ['create_time'] = get_date_time ();
//						$data ['update_time'] = get_date_time ();
//						$result = $Ent->add ( $data );
//						$entId=$result;
//						$EntUser = M ( "EntUser" );
//						//$UserOrg = M ( "UserOrg" );
//						$map ['ent_id'] = $entId;
//						$map ['user_id'] = $uid;
//						$map ['update_time'] = get_date_time ();
//						$map ['updater_id'] = $uid;
//						$result = $EntUser->add ( $map );
//						//$result = $UserOrg->add ( $map );
//						$result=$this->addDefaultOrg($uid, $entId);
//						if ($result !== false) {
//							$this->assign ( "jumpUrl", "/User/info" );
//							$this->assign ( "waitSecond", 3 );
//							$this->success ( "注册成功！" );
//							return;
//						}
//					}
//				}
//			}
//		}
//		$this->assign ( "jumpUrl", "/User/register" );
//		$this->error ( "注册失败！" );
//	}
//	
	
	public function save(){
		
		if(isset($_POST['email'])&&isset($_POST['nick'])&&isset($_POST['password'])&&isset($_POST['repassword'])){
			$email=strtolower(trim($_POST['email']));
			if($email==""){
				exit('请填写邮箱！[ <A HREF="javascript:history.bawck()">返 回</A> ]');
			}
			if(!check_email_format($email)){
				exit('邮箱格式不正确！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$nick=trim($_POST['nick']);
			if($nick==""){
				exit('请填写昵称！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			if (preg_match ( "/(simplenect|阡陌|运营|管理|系统|,|#)/i", $nick )) {
				exit('昵称包含非法字符！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$nickLen=iconv("UTF-8", "GBK", $nick);
			$len=strlen($nickLen);
			if($len<4||$len>12){
				exit('昵称应为4-12个字符！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$pwd=trim($_POST['password']);
			$repwd=trim($_POST['repassword']);
			if($pwd==""){
				exit('请填写密码！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			if($pwd!=$repwd){
				exit('二次密码不一致！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$User=M("User");
			$count=$User->where("email='".$email."'")->count();
			if($count>0){
				exit('邮箱已存在！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			if(isset($_POST['head_pic'])){
				if($_FILES['head_pic']['error']!=4){
					$fileInfo=saveFile(false,0,0,"User");
					$data['avatar']=$fileInfo[0]['saveContent'];
				}
			}
			$data['email']=$email;
			$data['id']=md5($email);
			$data['nick']=$nick;
			$data['password']=md5($pwd);
			$data['status']=0;
			$data['create_time']=get_date_time();
			$data['last_login']=get_date_time();
			$data['update_time']=get_date_time();
			$User->startTrans();
			$result=$User->add($data);
			if($result!==false){
//				$user['id']=$result;
//				$user['nick']=$nick;
//				setSession(SESSION_NEW, $user);
//				redirect(C("WWW"));//TODO 到激活页面
				$uid=$data['id'];
				$invateCode="";//邮箱邀请码
				$invateId=0;//邀请链接
				if(isset($_POST['invate_code'])&&trim($_POST['invate_code'])!=""){
					$invateCode=trim($_POST['invate_code']);
					
				}
				$isEmail=1;
				if($invateCode!=""){
					$EmailInvate=M("EmailInvate");
					$invate=$EmailInvate->where("invate_code='".$invateCode."'")->find();
					if(isset($invate['id'])&&$invate['invate_email']==$email&&$invate['status']==0){
						$data=array();
						$data['id']=$invate['id'];
						$data['status']=1;
						$data['register_email']=$email;
						$result=$EmailInvate->save($data);
						if($result===false){
							$User->rollback();
							exit('注册失败！[ <A HREF="javascript:history.back()">返 回</A> ]');
						}
						$result=$User->setInc("invites","id='".$invate['user_id']."'");
						if($result===false){
							$User->rollback();
							exit('注册失败！[ <A HREF="javascript:history.back()">返 回</A> ]');
						}
						$data=array();
						$data['id']=$uid;
						$data['status']=1;
						$result=$User->save($data);
						if($result===false){
							$User->rollback();
							exit('注册失败！[ <A HREF="javascript:history.back()">返 回</A> ]');
						}
						$isEmail=0;
					}
				}else if(Cookie::is_set("invite_email")){
					$inviteEmail=trim(Cookie::get("invite_email"));
					$user=$User->where("email='".strtolower($inviteEmail)."'")->find();
					if(isset($user['id'])){
						$InvateRecord=M("InvateRecord");
						$data=array();
						$data['user_id']=$uid;
						$data['invate_id']=$user['id'];
						$data['qianmo_dot']=0; //100
						$data['create_time']=get_date_time();
						$result=$InvateRecord->add($data);
						if($result===false){
							$User->rollback();
							exit('注册失败！[ <A HREF="javascript:history.back()">返 回</A> ]');
						}
						$invateId=$user['id'];
					}else{
						$fp=fopen(".Public/Log/no_invater.log", "a+");
						fwrite($fp,get_date_time()."\t 邀请用户不存在ERROR \t EMAIL：".$inviteEmail."\n");
						fclose($fp);
					}
				}
				$User->commit();
				if($isEmail==1){
					//发送邮件
					$timeStr = time ();
					$chk = md5 ( $email . "," . $timeStr . ",qianmo20120601" );
					$ver_data = $email . "," . $timeStr . "," . $chk;
					if($invateCode!=""){
						$ver_data.=",".$invateCode.",1";
					}else if($invateId>0){
						$ver_data.=",".$invateId.",2";
					}
					$url = C ( 'WWW' ) . "/User/activate/verify/" . urlencode ( base64_encode ( $ver_data ) );
					$msg = "尊敬的SimpleNect用户，" . $email . "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" . $url . "'>" . $url . "</a>";
					$this->sendMail($email, "请激活账号完成注册！", $msg);
				}
				
				//好友邀请
				/* 2013-02-18 修改 未注册好友邀请直接改为添加好友，
				 * 也不要在注册链接表示邀请人
				if(Cookie::is_set("add_ff")){
					$fromEmail=trim(Cookie::get("add_ff"));
					$sql="select * from kx_mailing_addfriend where user='".$fromEmail."' and friend='".$email."'";
					$Model=new Model();
					$mf=$Model->query($sql);
					if(isset($mf[0]['id'])){
						$sql="insert into user_msg (user,title,content) values ('".$fromEmail."','add_friend','".$mf[0]['invite_msg']."')";
						$result=$Model->execute($sql);
						Cookie::delete("add_ff");
					}
					
				}
				*/
				$this->reg_add_friend($email);
				redirect(C("WWW")."/User/account_verify?email=".$email);
			}else{
				$User->rollback();
				exit('注册失败！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
		}else{
			exit('缺少必要的参数！[ <A HREF="javascript:history.back()">返 回</A> ]');
		}
	}
	
	
	/**
	 * 
	 * 注册时未激活，后续账号激活入口
	 */
	public function to_active(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		$User=M("User");
		$user=$User->where("id='".get_user_id()."'")->find();
		if(isset($user['id'])){
			if($user['status']==1){
				$this->assign("error","该账号已激活！");
			}else{
				$timeStr = time ();
				$email=$user['email'];
				$chk = md5 ( $email . "," . $timeStr . ",qianmo20120601" );
				$ver_data = $email . "," . $timeStr . "," . $chk;
				$url = C ( 'WWW' ) . "/User/activate/verify/" . urlencode ( base64_encode ( $ver_data ) );
				$msg = "尊敬的SimpleNect用户，" . $email . "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" . $url . "'>" . $url . "</a>";
				$this->sendMail($email, "请激活账号完成注册！", $msg);
				redirect(C("WWW")."/User/account_verify?email=".$email);
			}
		}else{
			$this->assign("error","该账号不存在！");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	/**
	 * 激活验证邮件页面
	 */
	public function account_verify(){
		if(isset($_GET['email'])&&trim($_GET['email'])!=""){
			$email=trim($_GET['email']);
			$eArr=explode("@", $email);
			$mailLogin="";
			switch ($eArr[1]){
				case "163.com":$mailLogin="http://mail.163.com";break;
				case "126.com":$mailLogin="http://mail.126.com";break;
				case "qq.com":$mailLogin="http://mail.qq.com";break;
				case "sohu.com":$mailLogin="http://mail.sohu.com";break;
				case "hotmail.com":$mailLogin="http://mail.live.com";break;
				case "gmail.com":$mailLogin="http://mail.google.com";break;
				case "yahoo.cn":$mailLogin="http://mail.yahoo.cn";break;
				case "sina.com":$mailLogin="http://mail.sina.com.cn";break;
				case "139.com":$mailLogin="http://mail.139.com";break;
				case "wo.com.cn":$mailLogin="http://mail.wo.com.cn";break;
				case "189.cn":$mailLogin="http://mail.189.cn";break;
				default:;
			}
			if($mailLogin!=""){
				$this->assign("mailLogin",$mailLogin);
			}
			$this->assign("email",$email);
			$this->display(DEFAULT_DISPLAY);
			exit;
		}
		$this->error_msg("注册邮箱不存在！");		
	}
	/**
	 * 激活成功自动跳转页面
	 */
	public function verify_success(){

		$this->display(DEFAULT_DISPLAY);
	}
	/**
	 * 更改邮箱注册账户
	 */
	public function register_4(){
		if(isset($_GET['email'])&&trim($_GET['email'])!=""){
			$User=M("User");
			$status=$User->where("email='".$_GET['email']."'")->getField("status");
			if($status!=2){
				$this->error_msg("已激活的账号不能修改邮箱！");
			}
			$this->assign("email",$_GET['email']);
			$this->display(DEFAULT_DISPLAY);
			exit;
		}
		$this->error_msg("您的操作非法！");		
	}
	/**
	 * 激活账号
	 */
	public function activate(){
		if (isset ( $_GET ['verify'] ) && null != $_GET ['verify'] && "" != trim ( $_GET ['verify'] )) {
			$now = time ();
			$data = urldecode ( trim ( $_GET ['verify'] ) );
			$dataBase = base64_decode ( $data );
			$dataArray = explode ( ",", $dataBase );		
			$dataCount=count ( $dataArray );
			if ($dataCount == 3||$dataCount==5) {
				$chk = md5 ( $dataArray [0] . "," . $dataArray [1] . ",qianmo20120601" );
				if ($chk == $dataArray [2]) {
					//验证正确
					//判断实效
					if ($dataArray [1] + 24 * 3600 > $now) {
						//验证有效
						$User=M("User");
						$result=$User->where("email='".$dataArray[0]."'")->setField(array('status','active_time','last_login'),array(1,get_date_time(),get_date_time()));
						//TODO 邀请人邀请人数加1
						if($dataCount==5){
							if($dataArray[4]==1){
								$invateCode=$dataArray[3];
								$EmailInvate=M("EmailInvate");
								$invate=$EmailInvate->where("invate_code='".$invateCode."'")->find();
								if(isset($invate['id'])&&$invate['invate_email']==$dataArray[0]&&$invate['status']==0){
									$data=array();
									$data['id']=$invate['id'];
									$data['status']=1;
									$data['register_email']=$dataArray[0];
									$result=$EmailInvate->save($data);
									if($result!==false){
										$result=$User->setInc("invites","id=".$invate['user_id']);
									}								
								}
							}else if($dataArray[4]==2){
								$invateId=$dataArray[3];
								$result=$User->setInc("invites","id='".$invateId."'");
								if($result!==false){
									if(Cookie::is_set("invite_email")){
										Cookie::delete("invite_email");
									}
								}
							}
						}
						if($result!==false){
							$user=$User->where("email='".$dataArray[0]."'")->find();
							if(Session::is_set('active')){
								Session::set("active", null);
							}
							setSession(SESSION_NEW,$user);
							redirect(C("WWW")."/User/verify_success");
						}
						$this->error_msg("激活失败！");
					} else {
						$this->assign ( "error", "链接已经失效！" );
					}
				
				} else {
					$this->assign ( "error", "链接验证错误！" );
				}
			
			} else {
				$this->assign ( "error", "链接错误！" );
			}
		
		} else {
			$this->assign ( "error", "链接非法！" );
		}
		$this->error_msg("页面不存在！");
	}
	
	
	
	
	
	
	public function check(){
		if(isset($_POST['email'])){
			$email=trim($_POST['email']);
			if($email==""){
				$this->ajaxReturn(0,"",0);
			}
			$User=M("User");
			$count=$User->where("email='".$email."'")->count();
			if($count==0){
				$this->ajaxReturn(1,"OK",1);
			}
		}
		$this->ajaxReturn(0,"",0);
	}
	
	public function edit(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_POST['nick'])&&trim($_POST['nick'])!=""){
			//$nick=trim($_POST['nick']);
			$data['nick']=trim($_POST['nick']);
			$data['id']=get_user_id();
			$User=M("User");
			$result=$User->save($data);
			if($result!==false){
				$_SESSION['nick']=$data['nick'];
				redirect(C("WWW")."/User/info",2,"修改昵称成功！");
			}
		}
		$this->display(DEFAULT_DISPLAY);
	}
	/**
	 * 
	 * 用户登录接口
	 */
	public function clientin(){
		$status=0;
		$desc="error parameters";
		if (isset ( $_POST ['email'] ) && isset ( $_POST ['password'] )) {
			$email = trim ( $_POST ['email'] );
			$password = trim ( $_POST ['password'] );
			if (null != $email && "" != $email && null != $password && "" != $password) {
				$User = M ( "User" );
				$map ['email'] = $email;
				$map ['password'] = md5 ( $password );
				$user = $User->where ( $map )->find();
				if(isset($user['id'])&&$user['id']!=""){
					$this->assign("user",$user);
					$status=1;
					$desc="OK";
					$this->returnList($status, $desc);
					return;
				}else{
					$desc="账号或密码不正确！";
				}
			}else{
				$desc="请填写账号及密码！";
			}
	    }else{
	    	$desc="缺少账号或密码！";
	    }
		$this->returnList($status, $desc);
  }
	
	
  	/**
  	 * 
  	 * 用户个人中心
  	 */
	public function info(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 上传头像
	 */
	public function avatar(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		
		if($_FILES['avatar']['error']!=4){
			$fileInfo=saveFile(true,50,50,"User");
			$data['id']=get_user_id();
			$User=M("User");
			$user=$User->where($data)->find();
			$data['avatar']=$fileInfo[0]['saveContent'];
			$result=$User->save($data);
			if($result!==false){
				if($user['avatar']!=null&&trim($user['avatar'])!=""){
					delUserAvatar($user['avatar']);
				}
				$_SESSION['avatar']=$data['avatar'];
				redirect(C("WWW")."/User/info");
			}else{
				redirect(C("WWW")."/User/info",2,"上传/修改头像失败，请重新上传！");
			}
		}else{
			exit('请上传一张图片！[ <A HREF="javascript:history.back()">返 回</A> ]');
		}
	}
	/**
	 * 
	 * 用户修改密码
	 */
	public function changePwd(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_POST['oldPwd'])&&isset($_POST['password'])&&isset($_POST['repassword'])){
			$oldPwd=trim($_POST['oldPwd']);
			$pwd=trim($_POST['password']);
			$repwd=trim($_POST['repassword']);
			$status=1;
			$code=0;
			$oldMsg=0;
			if($oldPwd==""){
				$status=0;
				$oldMsg=1;
			}
			if($pwd==""){
				$status=0;
				$this->assign("pwd",0);
			}else{
				if($repwd!=$pwd){
					$status=0;
					$this->assign("repwd",0);
				}
			}
			if($status){
				$User=M("User");
				$user=$User->where("id='".get_user_id()."'")->find();
				if(md5($oldPwd)==$user['password']){
					$data['id']=get_user_id();
					$data['password']=md5($pwd);
					$result=$User->save($data);
					if($result!==false){
						$code=1;
					}
					$this->assign("code",$code);
				}else{
					$oldMsg=2;
				}
			}
			if($oldMsg>0){
				$this->assign("oldMsg",$oldMsg);
			}
			
		}
		
		$this->display(DEFAULT_DISPLAY);
	}
	

	/**
	 * 用户登陆
	 * 
	 */
	public function login() {
		//echo $_POST['name'];
		if (isset ( $_POST ['email'] )) {
			
			$email=strtolower(trim($_POST ['email']));
			$pwd=trim($_POST ['password']) ;
			if($email==""||$pwd==""){
				$this->assign ( "email", $email);
				$this->assign ( "error_msg", "账号或密码错误" );
				$this->display ( DEFAULT_DISPLAY );
				return;
			}
			$User = M ( "User" );
//			if(!$User->autoCheckToken($_POST)){
//				$this->assign ( "email", $_POST ['email'] );
//				$this->assign ( "error_msg", "登录出错" );
//				$this->display ( DEFAULT_DISPLAY );
//				return;
//			}
			$map ['email'] = $email;
			$map ['password'] = md5 ( $pwd );
			
			$user = $User->where ( $map )
				->find ();
			//print_r( $user['id']);
			//$this->display();
			//return ;
			if (isset ( $user ['id'] ) && trim($user ['id'])!="") {
				if ($user ['status'] == 1||$user['status']==0) {
					//设置登录用户SESSION
					

					//更新登录时间及登陆IP信息
					$data ['id'] = $user ['id'];
					$data ['last_login'] = get_date_time ();
					$result = $User->save ( $data );
				
					setSession ( SESSION_NEW, $user );
					redirect ( "/" );
					
					return;
				}
			} else {
				$this->assign ( "email", $_POST ['email'] );
				$this->assign ( "error_msg", "账号或密码错误" );
				$this->display ( DEFAULT_DISPLAY );
				return;
			}
		}
		//echo "111";
		$this->display ( DEFAULT_DISPLAY );
	}
	
	/**
	 * 用户注销
	 */
	public function logout() {
		if (isset ( $_SESSION ['nick'] )) {
			Session::clear ();
		}
		redirect ( "/" );
	}
	
	/**
	 * 
	 * 忘记密码
	 */
	public function findPwd(){
		$step=1;
		if(isset($_POST['email'])&&null!=$_POST['email']&&""!=trim($_POST['email'])){
			$code=0;
			$User=M("User");
			$email=trim($_POST['email']);
			$user=$User->where("email='".$email."'")->find();
			if(isset($user['id'])&&$user['id']!=""){
				$timeStr=time();
				$chk=md5($email.",".$timeStr.",kx2011");
				$data=$email.",".$timeStr.",".$chk;
				//print $data;
				$url=C('WWW')."/User/resetPwd/verify/".urlencode(base64_encode($data));
				$to = $email;
				$subject = "SimpleNect用户密码重置提示函";
				$msg = "尊敬的用户，" . $email . "<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接重置密码：<a href='".$url."'>".$url."</a>";
				$send_re=$this->sendMail ( $to, $subject, $msg );
				if($send_re===true){
					$code=1; //发送成功
					$step=2;
				}else{
					
					$code=2;//邮件发送失败
				}
			}else{
				$code=0;//账号不存在
			}
			$this->assign("code",$code);
			$this->assign("email",$email);
			
		}
		$this->assign("step",$step);
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	/**
	 * 
	 *密码重置（实效密码重置链接）页面
	 */
	public function resetPwd(){
		if(isset($_GET['verify'])&&null!=$_GET['verify']&&""!=trim($_GET['verify'])){
			$now=time();
			$data=urldecode(trim($_GET['verify']));
			$dataBase=base64_decode($data);
			$dataArray=explode(",", $dataBase);
			//print_r($dataArray);
			if(count($dataArray)==3){
				$chk=md5($dataArray[0].",".$dataArray[1].",kx2011");
				if($chk==$dataArray[2]){
				 	//验证正确
					//判断实效
				 	if($dataArray[1]+24*3600>$now){
				  	//验证有效
				  		$this->assign("email",$dataArray[0]);
						$chkcode=md5($dataArray[0]."2011kx");
				 		$this->assign("chkcode",$chkcode);
					}else{
						$this->assign("error","链接已经失效！");
					}
				
				}else{
					$this->assign("error","链接验证错误！");
				}
				
			}else{
				$this->assign("error","链接错误！");
			}
		
		}else{
			$this->assign("error","链接非法！");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 *密码重置
	 */
	public function rePwd(){
		$code=0;
		if(isset($_POST['email'])&&null!=$_POST['email']&&""!=trim($_POST['email'])&&isset($_POST['password'])&&null!=$_POST['password']&&""!=trim($_POST['password'])&&isset($_POST['repassword'])&&isset($_POST['chkcode'])){
			$email=trim($_POST['email']);
			$password=trim($_POST['password']);
			$repassword=trim($_POST['repassword']);
			$chkcode=trim($_POST['chkcode']);
			$chk=md5($email."2011kx");
			//验证是否正确
			if($chk==$chkcode){
				if($password==$repassword){
				  $User=M("User");
				  $pwd=md5($password);
				  $sql="update kx_user set password='".$pwd."' where email='".$email."'"; 
				  $result=$User->execute($sql);
				  if($result!==false){
				  	$code=1; //重置成功
				  }
				}else{
					$code=2;
					$this->assign("email",$email);
					$this->assign("chkcode",$chkcode);
				}
			}
		}
		$this->assign("code",$code);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * C/S用户登录接口
	 */
	public function clogin() {
		
		if (isset ( $_POST ['email'] ) && isset ( $_POST ['password'] )) {
			$email = strtolower(trim ( $_POST ['email'] ));
			$password = trim ( $_POST ['password'] );
			if (null != $email && "" != $email && null != $password && "" != $password) {
				$User = M ( "User" );
				$map ['email'] = $email;
				$map ['password'] = md5 ( $password );
				$user = $User->where ( $map )
					->find ();
				if (isset ( $user ['id'] ) && $user ['id']!= "") {
					if ($user ['status'] == 1) {
						//设置登录用户SESSION
						//更新登录时间
						$data ['id'] = $user ['id'];
						$data ['last_login'] = get_date_time ();
						$result = $User->save ( $data );
						if ($result !== false) {
							setSession ( SESSION_NEW, $user );
							//print $_SESSION['UID'];
							//企业列表
							$Ent = M ( "Ent" );
							//根据用户ID查询是否是某些企业的管理员
							$ueList1 = $Ent->where ( "ent_master_id='" . $user ['id'] . "' and ent_status=1" )
								->findAll ();
							$entIds = "";
							if (count ( $ueList1 ) > 0) {
								$this->assign ( "num1", count ( $ueList1 ) );
								$this->assign ( "ueList1", $ueList1 );
								$entIds = $entIds . "(";
								for($i = 0; $i < count ( $ueList1 ); $i ++) {
									$entIds = $entIds . $ueList1 [$i] ['id'];
									if ($i < (count ( $ueList1 ) - 1)) {
										$entIds = $entIds . ",";
									}
								}
								$entIds = $entIds . ")";
							}
							$sql_o = "select distinct e.id as ent_id ,e.ent_name as ent_name from kx_ent e,kx_user_org uo where e.ent_status=1 and uo.ent_id=e.id and uo.user_id='" . $user ['id']."'";
							if ("" != $entIds) {
								$sql_o = $sql_o . " and e.id not in " . $entIds;
							}
							$ueList2 = $Ent->query ( $sql_o );
							if (count ( $ueList2 ) > 0) {
								$this->assign ( "num2", count ( $ueList2 ) );
								$this->assign ( "ueList2", $ueList2 );
							}
							
							$this->assign ( "desc", "loginSuccess" );
							$this->assign ( "status", 1 );
							$this->display ();
							return;
						}
					
					} else {
						$this->assign ( "desc", "账号被封禁" );
						$this->assign ( "status", 0 );
						$this->display ();
						return;
					}
				}
			}
		
		}
		$this->assign ( "desc", "notLogin" );
		$this->assign ( "status", 0 );
		$this->display ();
	}
	
	/**
	 * 
	 * 二次登陆交互，写COOKIE，清除SESSION
	 */
	public function ent() {
		if (isLogin ()) {
			if (isset ( $_POST ['id'] ) && $_POST ['id'] > 0) {
				$Ent = M ( "Ent" );
				$ent = $Ent->where ( "id=" . $_POST ['id'] . " and ent_status=1" )
					->find ();
				
				if (isset ( $ent ['id'] ) && $ent ['id'] > 0) {
					
					//判断企业用户状态
					$EntUser=M("EntUser");
					$num=$EntUser->where("status=1 and user_id='".$_SESSION['UID']."' and ent_id=".$_POST['id'])->count();
					if($num==0){
					
						$this->assign ( "desc", "login ent failed ,your account in this ent is forbidden" );
						$this->assign ( "status", 0 );
						$this->display ();
						Session::clear ();
						return;
					}
					
					$count = $Ent->where ( "id=" . $_POST ['id'] . " and ent_master_id='" . $_SESSION ['UID']."'" )
						->count ();
					if ($count > 0) {
						$count = 1;
					}
					//print time();
					setOurCookie ( $_SESSION ['UID'], $_POST ['id'], $count, time () );
					Session::clear ();
					$user = get_clogin_user ();
					if ($user !== false) {
						$this->assign ( "user", $user );
						$this->assign ( "ent", $ent );
						$this->assign ( "desc", "entMsg" );
						$this->assign ( "status", 1 );
					} else {
						$this->assign ( "desc", "notLogin,try again" );
						$this->assign ( "status", 0 );
					}
					$this->display ();
					return;
				}
			}
			$this->assign ( "desc", "entId error" );
			$this->assign ( "status", 0 );
		
		} else {
			$this->assign ( "desc", "notLogin" );
			$this->assign ( "status", 0 );
		}
		$this->display ();
	}
	
//	/**
//	 * 
//	 * 用户添加接口
//	 */
//	public function add() {
//		$status = 0;
//		$desc = "error parameters";
//		if (! is_ent_master ()) {
//			$desc = "notLogin or noRight";
//			$this->returnList ( $status, $desc );
//			return;
//		}
//		if (isset ( $_POST ['email'] ) && "" != trim ( $_POST ['email'] ) && isset ( $_POST ['nick'] ) && "" != $_POST ['nick'] && isset ( $_POST ['orgId'] ) && $_POST ['orgId'] > 0 && isset ( $_POST ['pwd'] ) && "" != trim ( $_POST ['pwd'] ) && isset ( $_POST ['status'] ) && $_POST ['status'] >= 0) {
//			
//			$email = $_POST ['email'];
//			$entId = Cookie::get ( "ent_id" );
//			$orgId = $_POST ['orgId'];
//			$pwd = trim ( $_POST ['pwd'] );
//			$entUserStatus = $_POST ['status'];
//			$Org = M ( "Org" );
//			//判断所在企业是否存在这个岗位
//			$ocount = $Org->where ( "id=" . $orgId . " and ent_id=" . $entId )
//				->count ();
//			if ($ocount == 0) {
//				$desc = " org not exists";
//				$this->returnList ( $status, $desc );
//				return;
//			}
//			$EntUser = M ( "EntUser" );
//			$User = M ( "User" );
//			$UserOrg = M ( "UserOrg" );
//			$data ['email'] = $email;
//			$user = $User->where ( $data )
//				->find ();
//			$data ['ent_id'] = $entId;
//			$Ent = M ( "Ent" );
//			$ent = $Ent->find ( $entId );
//			$pwdStr = "";
//			
//			if (isset ( $user ['id'] ) && $user ['id'] > 0) {
//				//用户已经存在
//				$data1 = array ();
//				$uid = $user ['id'];
//				$data1 ['user_id'] = $uid;
//				$data1 ['ent_id'] = $entId;
//				$data1 ['org_id'] = $orgId; //用户可以有多个岗位
//				//TODO 
//				$count1 = $UserOrg->where ( $data1 )
//					->count ();
//				if ($count1 == 0) {
//					//$data1['org_id']=$orgId;//现在这里的话 用户只有一个岗位
//					$data1 ['update_time'] = get_date_time ();
//					$data1 ['updater_id'] = get_cuser_id ();
//					$result = $UserOrg->add ( $data1 );
//					$map ['ent_id'] = $entId;
//					$map ['user_id'] = $uid;
//					$map ['status'] = $entUserStatus;
//					$map ['update_time'] = get_date_time ();
//					$map ['updater_id'] = get_cuser_id ();
//					$result = $EntUser->add ( $map );
//					if ($result !== false) {
//						$Ent = M ( "Ent" );
//						$Ent->setInc ( "ent_user_num", "id=" . $entId );
//						//TODO 发送邮件
//						
//						$this->assign ( "uid", $uid );
//						$status = 1;
//						$to = $email;
//						$subject = "快享企业用户注册提醒";
//						$msg = "尊敬的用户，" . $user ['nick'] . "<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;欢迎您使用快享， 您现在被 " . $ent ['ent_name'] . " 的管理员添加到该企业组中，您可以通过登陆界面选择改企业登陆！";
//						$send_re=$this->sendMail ( $to, $subject, $msg );
//						if($send_re===true){
//							$desc = "add user success";
//						}else{
//							$desc = "add user success,but sent mail failed";
//						}
//					
//						update_ent_version ( $entId );
//					} else {
//						$desc = "add user error, try again";
//						$this->returnList ( $status, $desc );
//						return;
//					}
//				} else {
//					$desc = "user already exists";
//					$this->returnList ( $status, $desc );
//					return;
//				}
//			
//			} else {
//				//用户不存在
//				//6位纯数字随机数
//				//$rand=rand_string(6,1);
//				$map ['email'] = $email;
//				//$map['password']=md5(trim($rand));
//				$map ['password'] = md5 ( $pwd );
//				$map ['nick'] = $_POST ['nick'];
//				$map ['create_time'] = get_date_time ();
//				$map ['update_time'] = get_date_time ();
//				$map ['last_login'] = get_date_time ();
//				$result = $User->add ( $map );
//				if ($result !== false) {
//					$data1 = array ();
//					$uid = $result;
//					$data1 ['user_id'] = $uid;
//					$data1 ['ent_id'] = $entId;
//					$data1 ['org_id'] = $orgId;
//					$data1 ['update_time'] = get_date_time ();
//					$data1 ['updater_id'] = get_cuser_id ();
//					$result = $UserOrg->add ( $data1 );
//					$map ['ent_id'] = $entId;
//					$map ['user_id'] = $uid;
//					$map ['status'] = $entUserStatus;
//					$map ['update_time'] = get_date_time ();
//					$map ['updater_id'] = get_cuser_id ();
//					$result = $EntUser->add ( $map );
//					if ($result !== false) {
//						$Ent = M ( "Ent" );
//						$Ent->setInc ( "ent_user_num", "id=" . $entId );
//						$this->assign ( "uid", $uid );
//						$status = 1;
//						//TODO 发送邮件
//						//print $rand;
//						$to = $email;
//						$subject = "快享企业用户注册提醒";
//						$msg = "尊敬的用户，" . $user ['nick'] . "<br />&nbsp;&nbsp;您好！ <br /> &nbsp;&nbsp;欢迎您使用快享，您现在被 " . $ent ['ent_name'] . "的管理员添加到该企业群中，您的初始密码：" . $pwd . " ，请妥善保管！<br />&nbsp;&nbsp;快享软件下载地址：http://www.kx.com/download";
//						$send_re=$this->sendMail ( $to, $subject, $msg );
//						//print $send_re;
//						if($send_re){
//							$desc = "add user success";
//						}else{
//							$desc = "add user success,but sent mail failed";
//						}
//						
//						update_ent_version ( $entId );
//					} else {
//						$desc = "add user error, try again";
//						$this->returnList ( $status, $desc );
//						return;
//					}
//				} else {
//					$desc = "add user error,try again";
//				}
//			}
//		}
//		$this->returnList ( $status, $desc );
//	
//	}
	
	/**
	 * 
	 * 企业管理员/用户修改基本信息接口
	 */
	public function update() {
		$status = 0;
		$desc = "error parameters";
		if (! is_client_login ()) {
			$desc = "notLogin";
			$this->returnList ( $status, $desc );
			return;
		}
		if (isset ( $_POST ['id'] ) && trim($_POST ['id'])!="" && isset ( $_POST ['nick'] ) && "" != trim ( $_POST ['nick'] )) {
			$id = $_POST ['id'];
			$nick = $_POST ['nick'];
			$orgId = 0;
			$entId = Cookie::get ( "ent_id" );
			$User = M ( "User" );
			//用户自行修改信息时不传入参数ORGID，即使传入也将被忽略
			if (is_ent_master ()) {
//				if (isset ( $_POST ['orgId'] ) && $_POST ['orgId'] > 0) {
//					$orgId = $_POST ['orgId'];
//					$UserOrg = M ( "UserOrg" );
//					$data ['user_id'] = $id;
//					$data ['ent_id'] = $entId;
//					$uo = $UserOrg->where ( $data )
//						->find ();
//					if (! (isset ( $uo ['id'] ) && $uo ['id'] > 0)) {
//						$desc = " ent user not exists";
//						$this->returnList ( $status, $desc );
//						return;
//					}
					$map ['id'] = $id;
					$map ['nick'] = $nick;
					$map ['update_time'] = get_date_time ();
					$result = $User->save ( $map );
					if ($result !== false) {
						$desc = "updater user success";
						$status = 1;
						update_ent_version ( $entId );
//						//如果一个企业用户可以有多个岗位一下需要作修改
//						//修改岗位可能会使2个岗位相同
//						//TODO 
//						$data ['id'] = $uo ['id'];
//						$data ['org_id'] = $orgId;
//						$data ['updater_id'] = get_cuser_id ();
//						$data ['update_time'] = get_date_time ();
//						$result = $UserOrg->sava ( $data );
//						if ($result !== false) {
//							$desc = "updater user success";
//							$status = 1;
//							update_ent_version ( $entId );
//						} else {
//							$desc = "update user error";
//						}
					
					} else {
						$desc = "update user error ,try again";
					}
//				} else {
//					$desc = "error parameters , no  orgId or error";
//				}
			
			} else {
				//修改用户信息
				if (get_cuser_id () == $id) {
					$map ['id'] = $id;
					$map ['nick'] = $nick;
					$map ['update_time'] = get_date_time ();
					$result = $User->save ( $map );
					if ($result !== false) {
						$status = 1;
						$desc = "update user success";
						update_ent_version ( $entId );
					} else {
						$desc = "update user error,try again";
					
		//$this->returnList($status, $desc);
					//return;
					}
				} else {
					$desc = "update user error,userId error";
				
		//$this->returnList($status, $desc);
				//return;
				}
			}
		}
		$this->returnList ( $status, $desc );
	}
	
	/**
	 * 
	 * //用户/企业管理员修改密码接口
	 * 用户修改密码接口
	 */
	public function pwd() {
		$status = 0;
		$desc = "error parameters";
		if (! is_client_login ()) {
			$desc = "notLogin";
			$this->returnList ( $status, $desc );
			return;
		}
		if (isset ( $_POST ['id'] ) && trim($_POST ['id']) != "" && isset ( $_POST ['password'] ) && null != $_POST ['password'] && "" != trim ( $_POST ['password'] )) {
			if ( get_cuser_id () == $_POST ['id']) {
			//if (is_ent_master () || get_cuser_id () == $_POST ['id']) {
				$id = trim($_POST ['id']);
				
				$password = trim ( $_POST ['password'] );
				$entId = Cookie::get ( "ent_id" );
//				if (is_ent_master ()) {
//					$EntUser = M ( "EntUser" );
//					$count = $EntUser->where ( "user_id=" . $id . " and ent_id=" . $entId )
//						->count ();
//					if ($count == 0) {
//						$desc = "update password fail,you can not update other ent user";
//						$this->returnList ( $status, $desc );
//						return;
//					}
//				}
				$User = M ( "User" ); //更改的用户要是这个企业的用户
				$user = $User->where("id='".$id."'")->find ();
				if (isset ( $user ['id'] ) && $user ['id'] != "") {
//					if (is_ent_master ()) {
//						$data ['id'] = $user ['id'];
//						$data ['password'] = md5 ( $password );
//						$result = $User->save ( $data );
//						if ($result !== false) {
//							$status = 1;
//							$desc = "update password success";
//							$to = $user ['email'];
//							$subject = "密码修改提醒";
//							$msg = "尊敬的用户，" . $user ['nick'] . "<br />&nbsp;&nbsp;您好！ <br /> &nbsp;&nbsp;您的密码已被管理员修改，你的密码为：" . $password . "，请妥善保管！";
//							$send_re=$this->sendMail ( $to, $subject, $msg );
//							if($send_re===true){
//								$desc = "update password success";
//							}else{
//								$desc = "update password success,but sent mail failed";
//							}
//							update_ent_version ( $entId );
//						} else {
//							$desc = "update password fail ,try again";
//						}
//					} else {
						if (isset ( $_POST ['oldPassword'] ) && null != $_POST ['oldPassword'] && "" != $_POST ['oldPassword']) {
							$oldPwd = trim ( $_POST ['oldPassword'] );
							if ($user ['password'] == md5 ( $oldPwd )) {
								$data ['id'] = $user ['id'];
								$data ['password'] = md5 ( $password );
								$result = $User->save ( $data );
								if ($result !== false) {
									$status = 1;
									$desc = "update password success";
//									$to = $user ['email'];
//									$subject = "密码修改提醒";
//									$msg = "尊敬的用户，" . $user ['nick'] . "<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;您的密码已被管理员修改，你的密码为：" . $password . "，请妥善保管！";
//									$send_re=$this->sendMail ( $to, $subject, $msg );
//									if($send_re===true){
//										$desc = "update password success";
//									}else{
//										$desc = "update password success,but sent mail failed";
//									}
									update_ent_version ( $entId );
								} else {
									$desc = "update password fail ,try again";
								}
							} else {
								$desc = "update password fail , error oldPassword";
							}
						} else {
							$desc = "update password fail ,need oldPassword";
						}
					//}
				
				}
			} else {
				$desc = "update password fail ,error user try to update password";
			}
		}
		$this->returnList ( $status, $desc );
	}
	
	
	
	
	

	private function sendMail($to, $subject, $msg,$fromNick=false) {
		import ( '@.Util.Mail.Mail' );
		//print $to;
		//$mail = new Mail ();
		//$re = $mail->mail_php ( $to, $subject, $msg );
		$re=mail_php ( $to, $subject, $msg,$fromNick );
		return $re;
		//$this->display ();
	}
	
	/**
	 * 
	 * 企业管理员注册时，添加默认组织结构
	 * @param  $userId
	 * @param  $entId
	 */
	private function addDefaultOrg($userId,$entId){
		$Org=M("Org");
		$now=get_date_time();
		$data['ent_id']=$entId;
		$data['name']="总经理";
		$data['parent_id']=0;
		$data['updater_id']=$userId;
		$data['create_time']=$now;
		$data['update_time']=$now;
		$orgId=$Org->add($data);
		if($orgId!==false){
			$dataList=array();
			$dataList[0]['ent_id']=$entId;
			$dataList[0]['name']="部门一";
			$dataList[0]['parent_id']=$orgId;
			$dataList[0]['updater_id']=$userId;
			$dataList[0]['create_time']=$now;
			$dataList[0]['update_time']=$now;
			$dataList[1]['ent_id']=$entId;
			$dataList[1]['name']="部门二";
			$dataList[1]['parent_id']=$orgId;
			$dataList[1]['updater_id']=$userId;
			$dataList[1]['create_time']=$now;
			$dataList[1]['update_time']=$now;
			$result=$Org->addAll($dataList);
			if($result!==false){
				return true;
			}else{
				$Org->where("id=".$orgId)->delete();
				return false;
			}
		}
		return false;
	}
	
	/**
	 * 
	 * 登陆接口测试
	 */
	public function cloginForm() {
		$this->display ( DEFAULT_DISPLAY );
	}
	
	/**
	 * 
	 * 二次登陆接口测试..
	 */
	public function entChoose() {
		if (isLogin ()) {
			$this->display ( DEFAULT_DISPLAY );
		} else {
			redirect ( "/User/cloginForm" );
		}
	}
	
	public function addForm() {
		if (! is_ent_master ()) {
			$this->assign ( "error", "notLogin or noRight" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$this->display ( DEFAULT_DISPLAY );
	}
	
	public function updateForm() {
		if (! is_client_login ()) {
			$this->assign ( "error", "notLogin" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$this->display ( DEFAULT_DISPLAY );
	}
	
	public function pwdForm() {
		if (! is_client_login ()) {
			$this->assign ( "error", "notLogin" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$this->display ( DEFAULT_DISPLAY );
	}
	
	/**
	 * 
	 * 早期的邀请好友注册（加入团队等）
	 */
	public function invate(){
		$status = 0;
		$desc = "error parameters";
		if(isset($_POST['my_email'])&&trim($_POST['my_email'])!=""&&isset($_POST['invate_email'])&&trim($_POST['invate_email'])!=""
		   &&isset($_POST['my_name'])&&trim($_POST['my_name'])!=""&&isset($_POST['invate_name'])&&trim($_POST['invate_name'])!=""
		   &&isset($_POST['group_id'])&&isset($_POST['group_name'])&&trim($_POST['group_name'])!=""){
		   $my_email=trim($_POST['my_email']);
		   $invate_email=trim($_POST['invate_email']);
		   if(!check_email_format($my_email)||!check_email_format($invate_email)){
		   		$desc="check the email";
		   		$this->returnList($status, $desc);
		   }
		   $my_name=trim($_POST['my_name']);
		   $invate_name=trim($_POST['invate_name']);
		   $group_id=intval($_POST['group_id']);
		   if(!($group_id==-1||$group_id>0)){
		   		$desc="group id error";
		   		$this->returnList($status, $desc);
		   }
		   $group_name=trim($_POST['group_name']);
		   $User=M("User");
		   $user=$User->where("email='".$my_email."'")->find();
		   if(isset($user['id'])&&$user['id']>0){
		   		$data['user_id']=$user['id'];
		   		$data['user_name']=$my_name;
		   		$data['invate_email']=$invate_email;
		   		$data['invate_name']=$invate_name;
		   		$data['group_id']=$group_id;//TODO 
		   		$data['group_name']=$group_name;
		   		$data['invate_code']=md5(uniqid(rand()));
		   		$data['qianmo_dot']=0;
		   		$data['create_time']=get_date_time();
		   		$data['status']=0;
		   		$EmailInvate=M("EmailInvate");
		   		$result=$EmailInvate->add($data);
		   		if($result!==false){
		   			$status=1;
		   			$desc="OK";
		   			$url=C("WWW")."/User/register/invate_code/".$data['invate_code'];
		   			if($data['group_id']==-1){
		   				$msg = "尊敬的" . $invate_name . "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;".$my_name." 邀请您成为TA的好友，赶快注册并使用阡陌软件吧！<a href='" . $url . "'>" . $url . "</a>";
		   			}else{
		   				$msg = "尊敬的" . $invate_name . "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;".$my_name." 邀请您加入“".$group_name."”群，赶快注册并使用阡陌软件吧！<a href='" . $url . "'>" . $url . "</a>";
		   			}
		   			$this->sendMail($invate_email, "请激活账号完成注册！", $msg);
		   		}else{
		   			$desc="add invate msg error";
		   		}
		   }else{
		   		$desc=" user not exists";
		   }
		  
	    }
	    $this->returnList($status, $desc);
	}
	
	public function invateForm(){
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 用户协议
	 */
	public function protocol(){
		$this->assign("title","用户协议");
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 批量注册用户
	 */
	public function reg_more(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	/**
	 * 
	 * 批量注册用户保存
	 */
	public function reg_save(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if($_FILES['csv_file']['error']===4){
			$this->assign("error","请上传CSV文件！");
		}else{
			$type=array ('csv');
			$fileUpload=saveFile(false,0,0,"UserReg",$type);
			if($fileUpload===false){
				$this->assign("error","上传文件失败！");
			}else{
				$fileInfo=$fileUpload[0]['saveContent'];
				$file=C("UPLOAD_PATH")."/".getPicUri($fileInfo)."/".getPicName($fileInfo);
				
				$fp=fopen($file, "r");
				if($fp){
					$errorMsg=array();
				
					$User=M("User");
					while(!feof($fp)) {
				
							
							$str=fgets($fp);
			        		$str=trim(mb_convert_encoding($str, "UTF-8","GBK"));
			        		if($str==""||$str=="电子邮箱,用户名,初始密码"){
			        			continue;
			        		}
			        		$strArr=explode(",", $str);
			        		if(count($strArr)!=3){
			        			$num=count($errorMsg);
			        			$errorMsg[$num]="格式错误：".$str;
			        			continue;
			        		}
			        		$data=array();
			        		$data['email']=strtolower(trim($strArr[0]));
			        		if(!check_email_format($data['email'])){
			        			$num=count($errorMsg);
			        			$errorMsg[$num]="邮箱格式错误：".$data['email'];
			        			
			        			continue;
			        		}
			        		
			        		$count=$User->where($data)->count();
			        		if($count>0){
			        			$num=count($errorMsg);
			        			$errorMsg[$num]="邮箱已被他人注册：".$data['email'];
			        			
			        			continue;
			        		}
			        		$data['nick']=trim($strArr[1]);
			        		if(preg_match ( "/(simplenect|阡陌|运营|管理|系统|,|#)/", $data['nick'] )){
			        			$num=count($errorMsg);
			        			$errorMsg[$num]="用户名包含非法字符，注册邮箱：".$data['email'];
			        			
			        			continue;
			        		}
			        		$data['password']=md5(trim($strArr[2]));
			        		$data['status']=0;
			        		$data['create_time']=get_date_time();
			        		$data['last_login']=get_date_time();
			        		$data['update_time']=get_date_time();
			        		$data['invate_init']=2;
			        		$result=$User->add($data);
			        		if($result===false){
			        			$num=count($errorMsg);
			        			$errorMsg[$num]="注册失败邮箱：".$data['email'];
			        			
			        			continue;
			        		}
					
		  	  		}
		  	  		if(count($errorMsg)>0){
		  	  			$this->assign("errorMsg",$errorMsg);
		  	  		}else{
		  	  			$this->assign("OK","OK");
		  	  		}
				}else{
					$this->assign("error","打开上传文件失败！");
				}
				fclose($fp);
				
			}
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	public function invate_msg(){
		$ckey="";
		if(isset($_GET['ckey'])&&trim($_GET['ckey'])!=""){
			$ckey=trim($_GET['ckey']);
			$ckeyFile="/home/admin/php/invate_msg_ckey.txt";
			if(file_exists($ckeyFile)){
				$fkey="";
				$fp=fopen($ckeyFile, "r");
				if($fp){
					$fkey=trim(fgets($fp));
				}else{
					echo 'open key error';
					fclose($fp);
					exit();
				}
				fclose($fp);
				if($fkey!=$ckey){
					echo 'key error';
					exit();
				}
			}else{
			  echo 'not find key ';
			  exit();
			}
		}else{
			echo "no key";
			exit();
		}
		
		
		$sql="select * from kx_mailing_addfriend where is_sendemail=0";
		$Model=new Model();
		$mailList=$Model->query($sql);
		//print_r($mailList);
		$User=M("User");
		if(count($mailList)>0){
			$sendOkIds=array();
			$siteUrl=C("WWW");
			for($i=0;$i<count($mailList);$i++){
				//echo $i."--";
				$sendEmail="";
				$sendReason="";
				$fromEmail="";
				$sendWho=$mailList[$i]['send_who'];
				$sendReasonType=$mailList[$i]['send_reason_type'];
	
				//0 friend is unregister when user invite;
				//1 friend is offline when user invite;
				//2 user is offline when friend agree;
				$result=false;
			
				switch ($sendReasonType) {
						case 0:{
							$sendReason=$mailList[$i]['invite_content'];
							$fromEmail=trim($mailList[$i]['user']);
							$data2=array();
							$data2['email']=$fromEmail;
							$user=$User->where($data2)->field("id,nick")->find();
							$fromNick=$fromEmail;
							if(isset($user['id'])){
								$fromNick=$user['nick'];
							}
							$sendEmail=trim($mailList[$i]['friend']);
							/* 2013-02-18 修改 未注册好友邀请直接改为添加好友，
							 * 也不要在注册链接表示邀请人
							$paramUrl=base64_encode($fromEmail.",".$sendEmail);
							$regUrl=C("WWW")."/User/register?uf=".$paramUrl;
							*/
							$regUrl=C("WWW")."/User/register";
							$emailHtml=$this->send_invate_reg($fromNick, $sendReason,$regUrl);
							$result=$this->sendMail($sendEmail, "SimpleNect好友邀请信息！", $emailHtml);
						
							break;
						}
						case 1:{
							$fromEmail=trim($mailList[$i]['user']);
							$sendEmail=trim($mailList[$i]['friend']);
							$data2=array();
							$data2['email']=$fromEmail;
							$user=$User->where($data2)->field("id,nick")->find();
							$fromNick=$fromEmail;
							if(isset($user['id'])){
								$fromNick=$user['nick'];
							}
							
							$sendReason="希望加你为好友，请及时登录SimpleNect客户端，确认邀请信息。";
							$emailHtml=$this->send_invate_tip($fromNick, $sendReason,$siteUrl);
					
							$result=$this->sendMail($sendEmail, "SimpleNect好友邀请提示信息！", $emailHtml);

							break;
						}
						case 2:{
							$fromEmail=trim($mailList[$i]['friend']);
							$sendEmail=trim($mailList[$i]['user']);
							$data2=array();
							$data2['email']=$fromEmail;
							$user=$User->where($data2)->field("id,nick")->find();
							$fromNick=$fromEmail;
							if(isset($user['id'])){
								$fromNick=$user['nick'];
							}
							
							$sendReason="通过了您的好友邀请，请登录SimpleNect客户端，现在你们可以进行通讯了。";
							$emailHtml=$this->send_invate_tip($fromNick, $sendReason,$siteUrl);
							$result=$this->sendMail($sendEmail, "SimpleNect好友邀请提示信息！", $emailHtml);
							break;
						}
						default:;break;
				}
				//'0=friend; 1=user; 2=all;
//				if($sendWho==0){
//					
//					
//				}else if($sendWho==1){
//					$fromEmail=trim($mailList[$i]['friend']);
//					$sendEmail=trim($mailList[$i]['user']);
//					$emailHtml=$this->send_invate_msg($fromEmail, $sendReason,$siteUrl);
//					$result=$this->sendMail($sendEmail, "SimpleNect好友邀请信息！", $emailHtml);
//				}else if($sendWho==2){
//					$fromEmail=trim($mailList[$i]['friend']);
//					$sendEmail=trim($mailList[$i]['user']);
//					$emailHtml=$this->send_invate_msg($fromEmail, $sendReason,$siteUrl);
//					$result1=$this->sendMail($sendEmail, "SimpleNect好友邀请信息！", $emailHtml);
//					$fromEmail=trim($mailList[$i]['user']);
//					$sendEmail=trim($mailList[$i]['friend']);
//					$emailHtml=$this->send_invate_msg($fromEmail, $sendReason,$siteUrl);
//					$result2=$this->sendMail($sendEmail, "SimpleNect好友邀请信息！", $emailHtml);
//					if($result1===true&&$result2===true){
//						$result=true;
//					}
//				}
				if($result===true){
					$id=$mailList[$i]['id'];
					$sendOkIds[$id]=$id;
				}
			}
			
			if(count($sendOkIds)>0){
				$sql="update kx_mailing_addfriend set is_del=1,is_sendemail=1 where id in (".implode(",", $sendOkIds).")";
				$result=$Model->execute($sql);
				//print $Model->getLastSql();
				if($result===false){
					echo "fail";
				}else{
					echo "OK";
				}
			}
		}
		$ckeyFile="/home/admin/php/invate_msg_ckey.txt";
		$fp=fopen($ckeyFile, "w");
		fwrite($fp, uniqid());
		fclose($fp);
		
		
	
	}
	
	/**
	 * 
	 * 邀请注册邮件
	 * @param unknown_type $fromEmail
	 * @param unknown_type $sendReason
	 * @param unknown_type $siteUrl
	 */
	private function  send_invate_reg($fromEmail,$sendReason,$siteUrl){
		$emailHtml='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
					<html xmlns="http://www.w3.org/1999/xhtml">
					<head>
					
					</head>
					<body>
					<div class="main" style="width:100%;color:#000000;background-color:f8f8f8;font:12px/1.5 Microsoft Yahei,宋体,arial,\5b8b\4f53;">
						<div class="content" style="width:600px;margin:0 auto;font-size:16px;">
							<div class="title" style="width:600px;height:64px;line-height:64px;">
								<span style="font-size:18px;color:#0e5bbf;">'.$fromEmail.'</span>&nbsp;邀请您一起使用办公协同软件：SimpleNect
							</div>
							<div class="invate_msg" style="color:#838383;line-height:45px;word-wrap: break-word;">
							&nbsp;&nbsp;&nbsp;&nbsp;“'.$sendReason.'”
							</div>
							<div class="download_area" style="height:64px;width:222px;margin-left:203px;margin-top:18px;">
							<a href="'.C("WWW").'">
							<img src="'.C("STATIC").'/Img/email_download.jpg" style="border:none;"/>
							</a>
							</div>
							<div class="fun_area" style="width:548px;margin-left:30px;margin-top:48px;">
								<div class="fun_area_title" style="">SimpleNect能够：</div>
								<div class="fun_img">
								<img src="'.C("STATIC").'/Img/email_fun.jpg" />
								</div>
								<div class="fun_area_text" style="margin-top:20px;line-height:35px;word-wrap: break-word;color:#838383;">
								SimpleNect大大<span style="font-size:17px;color:#000000;">简化</span>了共享文件和打印机的操作，更把共享的范围从局域 网扩展到整个<span style="font-size:17px;color:#000000;">互联网</span>，也就是说A用户在上海，B用户在北京，两人仍然可以通过SimpleNect<span style="font-size:17px;color:#000000;">共享</span>自己电脑里的文件或打印机
								</div>
								<div class="fun_area_link" style="margin:10px 0 10px 0;height:26px;line-height:26px;text-align:right;">
								<a href="'.$siteUrl.'" style="color:#0e5bbf;text-decoration:underline;">访问SimpleNect网站</a>
								</div>
							</div>
							<div class="content_foot" style="height:50px;">
							
							</div>
						</div>
					</div>
					
					</body>
					</html>';
		return $emailHtml;
	}
	/**
	 * 
	 * 好友邀请提示信息
	 * @param $fromEmail
	 * @param $sendReason
	 * @param $siteUrl
	 */
	private function  send_invate_tip($fromEmail,$sendReason,$siteUrl){
	$emailHtml='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
					<html xmlns="http://www.w3.org/1999/xhtml">
					<head>
					
					</head>
					<body>
					<div class="main" style="width:100%;color:#000000;background-color:f8f8f8;font:12px/1.5 Microsoft Yahei,宋体,arial,\5b8b\4f53;">
						<div class="content" style="width:600px;margin:0 auto;font-size:16px;">
							<div class="title" style="width:600px;height:50px;line-height:50px;">
								<span style="font-size:18px;color:#0e5bbf;">'.$fromEmail.'</span>&nbsp;'.$sendReason.'
							</div>
							<div class="fun_area" style="width:548px;margin-left:30px;margin-top:48px;">
								<div class="fun_area_link" style="margin:10px 0 10px 0;height:26px;line-height:26px;text-align:right;">
								<a href="'.$siteUrl.'" style="color:#0e5bbf;text-decoration:underline;">访问SimpleNect网站</a>
								</div>
							</div>
							<div class="content_foot" style="height:50px;">
							
							</div>
						</div>
					</div>
					
					</body>
					</html>';
		return $emailHtml;
	}
//	public function test(){
//		$this->display();
//	}
	
	
	/**
	 * 
	 * 客户端用户注册接口
	 */
	public function cadd(){
		$status=0;
		$desc="error param";
		if(isset($_POST['email'])&&isset($_POST['nick'])&&isset($_POST['password'])){
			$email=strtolower(trim($_POST['email']));
			if($email==""){
				$desc="请填写邮箱！";
				$this->returnList($status, $desc);
			}
			if(!check_email_format($email)){
				$desc="邮箱格式不正确！";
				$this->returnList($status, $desc);
			}
			$nick=trim($_POST['nick']);
			if($nick==""){
				$desc="请填写昵称！";
				$this->returnList($status, $desc);
			}
			if (preg_match ( "/(simplenect|运营|管理|系统|,|#)/i", $nick )) {
				$desc="昵称包含非法字符！";
				$this->returnList($status, $desc);
			}
			$nickLen=iconv("UTF-8", "GBK", $nick);
			$len=strlen($nickLen);
			if($len<4||$len>12){
				$desc="昵称应为4-12个字符！";
				$this->returnList($status, $desc);
			}
			$pwd=trim($_POST['password']);
			if($pwd==""){
				$desc="请填写密码！";
				$this->returnList($status, $desc);
			}
	
			$User=M("User");
			$count=$User->where("email='".$email."'")->count();
			if($count>0){
				$desc="邮箱已存在！";
				$this->returnList($status, $desc);
			}

			$data['email']=$email;
			$data['nick']=$nick;
			$data['password']=md5($pwd);
			$data['status']=0;
			$data['create_time']=get_date_time();
			$data['last_login']=get_date_time();
			$data['update_time']=get_date_time();

			$result=$User->add($data);
			if($result!==false){
				//发送邮件
				$timeStr = time ();
				$chk = md5 ( $email . "," . $timeStr . ",qianmo20120601" );
				$ver_data = $email . "," . $timeStr . "," . $chk;

				$url = C ( 'WWW' ) . "/User/activate/verify/" . urlencode ( base64_encode ( $ver_data ) );
				$msg = "尊敬的SimpleNect用户，" . $email . "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" . $url . "'>" . $url . "</a>";
				$this->sendMail($email, "请激活账号完成注册！", $msg);
				$status=1;
				$desc="OK";
				$this->reg_add_friend($email);
			}else{
				$desc="注册失败！";
			}
		}else{
			$desc="缺少必要的参数！";
		}
		$this->returnList($status, $desc);
	
	}
	
	/**
	 *2013-02-18
	 *新注册用户自动加好友（若其有好友邀请记录）
	 *@param $regEmail 注册用户的Email
	 */
	private function reg_add_friend($regEmail){
		$Model=new Model();
		$sql="select id,user,friend from kx_mailing_addfriend where send_reason_type=0 and friend='".$regEmail."'";
		$inviteList=$Model->query($sql);
		if(count($inviteList)>0){
			$now=get_date_time();
			$Model->startTrans();
			for($i=0;$i<count($inviteList);$i++){			
				$user=$inviteList[$i]['user'];
				$friend=$inviteList[$i]['friend'];
				$sql="insert ignore into kx_user_friend (user,friend,create_time) values ('".$user."','".$friend."','".$now."')";
				$result=$Model->execute($sql);
				if($result===false){
					$Model->rollback();
					return false;
				}
				$sql="insert ignore into kx_user_friend (user,friend,create_time) values ('".$friend."','".$user."','".$now."')";
				$result=$Model->execute($sql);
				if($result===false){
					$Model->rollback();
					return false;
				}
			}
			$sql="update kx_mailing_addfriend set is_del=1 where send_reason_type=0 and friend='".$regEmail."'";
			$result=$Model->execute($sql);
			if($result===false){
				$Model->rollback();
				return false;
			}
			$Model->commit();
		}
		return true;
	}
	
	


}