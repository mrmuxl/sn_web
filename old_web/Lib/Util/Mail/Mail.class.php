<?php
//class Mail extends Think{
require("phpmailer.php");//下载的文件必须放在该文件所在目录
	function mail_php($to, $subject, $msg,$fromNick=false) {
		
		$mail = new PHPMailer (); //建立邮件发送类
		$mail->IsSMTP (); // 使用SMTP方式发送
		$mail->IsHTML(true);//是否使用HTML格式
		$mail->CharSet="UTF-8";
		
		$mail->Host = "mail.simplenect.cn"; // 您的企业邮局域名
		$mail->SMTPAuth = true; // 启用SMTP验证功能
		$mail->Username = "noreply@simplenect.cn"; // 邮局用户名(请填写完整的email地址)
		$mail->Password = "o86w9OQUTPW1"; // 邮局密码
		
		$mail->From = "noreply@simplenect.cn"; //邮件发送者email地址
		
		if($fromNick!==false){
			$mail->FromName = $fromNick;
		}else{
			$mail->FromName = "SimpleNect";
		}
		$mail->AddAddress ( "$to", "" ); //收件人地址，可以替换成任何想要接收邮件的email信箱,格式是AddAddress("收件人email","收件人姓名")
		//$mail->AddReplyTo("", "");
		//$mail->AddAttachment("/var/tmp/file.tar.gz"); // 添加附件
	
		$mail->Subject = $subject; //邮件标题
		$mail->Body = $msg; //邮件内容
		$mail->AltBody = ""; //附加信息，可以省略
		if (! $mail->Send ()) {
//			echo "邮件发送失败. <p>";
			//echo "error: " . $mail->ErrorInfo;
			//exit ();
			//return $mail->ErrorInfo;
			return false;
		}
		//echo "success";
	
		return true;
	}
//}