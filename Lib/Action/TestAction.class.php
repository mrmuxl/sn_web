<?php 
class TestAction extends  CommonAction{

	
	
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
		   		$data['qianmo_dot']=100;
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
	
	
	
	private function sendMail($to, $subject, $msg) {
		import ( '@.Util.Mail.Mail' );
		//print $to;
		//$mail = new Mail ();
		//$re = $mail->mail_php ( $to, $subject, $msg );
		$re=mail_php ( $to, $subject, $msg );
		return $re;
		//$this->display ();
	}
	
	public function invateForm(){
		$this->display(DEFAULT_DISPLAY);
	}
} 
