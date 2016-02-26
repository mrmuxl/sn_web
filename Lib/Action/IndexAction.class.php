<?php
// 本文档自动生成，仅供测试运行
class IndexAction extends CommonAction
{
    /**
    +----------------------------------------------------------
    * 默认操作
    +----------------------------------------------------------
    */
    public function index()
    {
        //$this->display(THINK_PATH.'/Tpl/Autoindex/hello.html');
       // $this->display ( 'Layout:default' );

       if(isset($_GET['invite_info'])&&trim($_GET['invite_info'])!=""){
       		$email=base64_decode(trim($_GET["invite_info"]));	
       		Cookie::set("invite_email", $email,2592000);
       }
       $MsgBoard=M("MsgBoard");
       $now=get_date();
       $prev=get_date(-2592000);//30天之前
       $now.=" 23:59:59";
       $msgCount=$MsgBoard->where("is_del=0")->count();
       $this->assign("msgCount",$msgCount);
       $msgList=$MsgBoard->where("is_del=0 and reply_id=0 and create_time between '".$prev."' and '".$now."'")->order("create_time desc")->limit(5)->select();
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
       		$userList=$User->where("id in (".implode(",", $userIds).")")->getField("id,avatar");
       		$this->assign("userList",$userList);
       	}
       $this->assign("msgList",$msgList);
       $this->assign("title","首页");
	   $this->display(DEFAULT_DISPLAY);
    }
    public function index_2(){
    	$this->display();
    }

   	public function index_3(){
    	       if(isset($_GET['invite_info'])&&trim($_GET['invite_info'])!=""){
       		$email=base64_decode(trim($_GET["invite_info"]));	
       		Cookie::set("invite_email", $email);
       }
       $MsgBoard=M("MsgBoard");
       $msgList=$MsgBoard->where("is_del=0")->order("create_time desc")->limit(100)->select();
       $replyIds=array();
       $userIds=array();
       for($i=0;$i<count($msgList);$i++){
       		$replyId=$msgList[$i]['reply_id'];
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
       		$replyList=$MsgBoard->where("is_del=0 and id in (".implode(",", $replyIds).")")->getField('id,msg');
       		$this->assign("replyList",$replyList);
       	}
       	if(count($userIds)>0){
       		$User=M("User");
       		$userList=$User->where("id in (".implode(",", $userIds).")")->getField("id,avatar");
       		$this->assign("userList",$userList);
       	}
       $this->assign("msgList",$msgList);
       $this->assign("title","首页");
   		$this->display();
    }
    /**
    +----------------------------------------------------------
    * 探针模式
    +----------------------------------------------------------
    */
    public function checkEnv_kx()
    {
        load('pointer',THINK_PATH.'/Tpl/Autoindex');//载入探针函数
        $env_table = check_env();//根据当前函数获取当前环境
        echo $env_table;
    }

}
?>