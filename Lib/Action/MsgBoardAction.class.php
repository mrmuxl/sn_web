<?php
/**
 * 
 * 留言板
 * @author mokeming
 *
 */
class MsgBoardAction extends CommonAction{
	
	public function msg_index(){
		$MsgBoard=M("MsgBoard");
		$now=get_date();
       	$prev=get_date(-2592000);//30天之前
       	$now.=" 23:59:59";
       	$msgList=$MsgBoard->where("reply_id=0 and is_del=0 and create_time between '".$prev."' and '".$now."'")->order("create_time desc")->select();;
      // 	krsort ($msgList);
       	$replyList=array();//回复的信息列表
       //	$notFindList=array();//这此msg列表中未找到回复的信息
//       	for($i=(count($msgList)-1);$i>=0;$i--){
//     		$msgId=$msgList[$i]['id'];
//     		$msgContent=$msgList[$i]['msg'];
//     		$replyId=$msgList[$i]['reply_id'];
//     		$replyList[$msgId]['msg']=$msgContent;
//     		if($replyId>0){
//     			if(isset($replyList[$replyId])){
//     				$msgList[$i]['reply']=$replyList[$replyId]['msg'];
//     			}else{
//     			
//     			}
//     		}
//       	}
       //	ksort($msgList);
       	//print_r($msgList);
       	$replyIds=array();
       	$userIds=array();
       	for($i=0;$i<count($msgList);$i++){
       		//$replyId=$msgList[$i]['reply_id'];
       		$replyId=$msgList[$i]['id'];
       		$userId=$msgList[$i]['user_id'];
       		if($replyId>0){
       			if(!isset($replyIds[$replyId])){
       				$replyIds[$replyId]=$replyId;
       			}
       		}
       		if($userId>0){	
       			if(!isset($userIds[$userId])){
       				$userIds[$userId]=$userId;
       			}
       		}
       	}
       	if(count($replyIds)>0){
       		$reList=$MsgBoard->where("reply_id>0 and is_del=0 and reply_id in (".implode(",", $replyIds).")")->order("create_time")->field('id,reply_id,msg')->select();
       		$replyList=array();
       		for($i=0;$i<count($reList);$i++){
       			$reId=$reList[$i]['reply_id'];
       			if(!isset($replyList[$reId])){
       				$replyList[$reId]=array();	
       			}
       			$num=count($replyList[$reId]);
       			$replyList[$reId][$num]=$reList[$i];
       		}
       		$this->assign("replyList",$replyList);
       	}
		if(count($userIds)>0){
       		$User=M("User");
       		$userList=$User->where("id in ('".implode("','", $userIds)."')")->getField("id,avatar");
       		$this->assign("userList",$userList);
       	}
       	$this->assign("msgList",$msgList);
      	$this->assign("title","留言板");
		$this->display(DEFAULT_DISPLAY);
	}
	
	public function add_form(){
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 新增留言
	 */
	public function add_msg(){
		if(isset($_POST['msg'])&&trim($_POST['msg'])!=""){
			$MsgBoard=M("MsgBoard");
//			if(!$MsgBoard->autoCheckToken($_POST)){
//				exit("非法提交表单！");
//			}
			$data['msg']=strip_tags(trim($_POST['msg']));//去除HTML标签
			$data['ip']=get_user_ip();
			$data['create_time']=get_date_time();
			if(isset($_POST['reply'])&&$_POST['reply']>0){
				$data['reply_id']=intval($_POST['reply']);
				$mb=$MsgBoard->find($data['reply_id']);
				if(isset($mb['id'])&&$mb['id']==$data['reply_id']){
					;
				}else{
					exit("您要回复的留言不存在！");
				}
			}else{
				$data['reply_id']=0;
			}
			if(isLogin()){
				$data['user_id']=get_user_id();
				$data['user_nick']=$_SESSION['nick'];
			}
			$result=$MsgBoard->add($data);
			if($result!==false){
				//$send_from=1;
				//if(isset($_POST['send_from'])&&$_POST['send_from']>0){
				//	$send_from=intval($_POST['send_from']);
				//}
				//if($send_from==1)	
				//	redirect(C("WWW"));
				redirect(C("WWW")."/MsgBoard/msg_index");
				
			}else{
				exit("发表留言出错！");
			}
		}else{
			exit("请填写留言内容！");
		}
	}
	
	public function del_msg(){
		if(!isRoot()){
			$this->ajaxReturn(0,"权限不够！",0);
		}
		if(isset($_POST['id'])&&intval($_POST['id'])>0){
			$mid=intval($_POST['id']);
			$MsgBoard=M("MsgBoard");
			$result=$MsgBoard->where("id=".$mid)->delete();
			if($result!==false){
				$this->ajaxReturn(1,"删除留言成功！",1);
			}else{
				$this->ajaxReturn(0,"删除留言失败！",0);
			}
		}else{
			$this->ajaxReturn(0,"参数错误！",0);
		}
	}
}