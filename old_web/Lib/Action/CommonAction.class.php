<?php
import ( "@.Util.Page" );
class CommonAction extends Action {
	//空操作  404页面
	function _empty(){
		header("HTTP/1.0 404 Not Found");
		//$this->error_msg("很抱歉，您访问的页面不存在！");
		$this->display();
		//$this->display(':Public:404');
		//header("Location: /Public/404.html");
	}
	protected  function returnList($status,$desc){
		$this->assign("status",$status);
		$this->assign("desc",$desc);
		$this->display();
		exit();
	}
	
	
/**
	 * 
	 * 返回错误提示信息
	 * @param $message 返回信息
	 * @param $type    返回状态
	 * @param $home	        返回首页地址
	 */
	function error_msg($message,$type=1,$home=null){
		$this->assign("msg",$message);
		$this->assign("type",$type);
		if($home==null){
			$home=C("WWW");
		}
		$this->assign("home",trim($home));
		$this->display("Layout:error_msg");
		exit();	
	}
	
	/**
	 * 
	 * 邀请注册成功后初始化加点
	 * @param  $userId 登录用户ID
	 * @param  $invateInit 是否是第一次登录 0=未登录，
	 * 1=邀请用户登录并初始化成功 2=非邀请用户
	 */
	protected function initInvateQianmoDot($userId,$invateInit){
		if($invateInit==0){
			$InvateRecord=M("InvateRecord");
			$ir=$InvateRecord->where("user_id='".$userId."'")->find();
			$User=M("User");
			if(isset($ir['id'])&&$ir['id']>0){
				$invateId=$ir['invate_id'];
				$qianmoDot=$ir['qianmo_dot'];
				$data['id']=$userId;
				$data['invate_init']=1;
				$User->startTrans();
				$result=$User->save($data);
				if($result!==false){
					$sql="update kx_user set qianmo_dot=qianmo_dot+".$qianmoDot." where id='".$invateId."'";
					$result=$User->execute($sql);
					if($result!==false){
						$User->commit();
					}else{
						$date=date ( "Y-m-d" );
						$fp=fopen(".Public/Log/invate_init_".$date.".log", "a+");
						fwrite($fp,get_date_time()."\t 初始化更新邀请用户阡陌点ERROR \t INVATE_ID：".$invateId."\n");
						fclose($fp);
						$User->rollback();
					}
				}else{
					$date=date ( "Y-m-d" );
					$fp=fopen(".Public/Log/invate_init_".$date.".log", "a+");
					fwrite($fp,get_date_time()."\t 初始化更新登录用户状态ERROR \t LOGIN_ID：".$userId."\t INIT_STATUS：1 \n");
					fclose($fp);
					$User->rollback();
				}
				
			}else{
				$data['id']=$userId;
				$data['invate_init']=2;
				$result=$User->save($data);
				if($result===false){
					$date=date ( "Y-m-d" );
					$fp=fopen(".Public/Log/invate_init_".$date.".log", "a+");
					fwrite($fp,get_date_time()."\t 初始化更新登录用户状态ERROR \t LOGIN_ID：".$userId."\t INIT_STATUS：2 \n");
					fclose($fp);
				}
			}
		}
	}
}