<?php
class OrgSelfAction extends CommonAction{
	/**
	 * 
	 * 获取企业用户自定义权限
	 */
	public function clist(){
		if(!is_client_login()){
			$this->assign("status",0);
			$this->assign("desc","notLogin");
			$this->display();
			return;
		}
		$entId=Cookie::get("ent_id");
		$OrgSelf=M("OrgSelf");
		$osList=$OrgSelf->where("ent_id=".$entId)->findAll();
		$this->assign("osList",$osList);
		$this->assign("num",count($osList));
		$this->assign("status",1);
		$this->assign("desc","org self list");
		$this->display();
	
	}
	
	/**
	 * 
	 * 设置自定义权限
	 */
	public function toSet(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['userId'])&&trim($_POST['userId'])!=""&&isset($_POST['targetUserId'])){
		  $OrgSelf=M("OrgSelf");
		  $userId=$_POST['userId'];
		  $targetUserIds=$_POST['targetUserId'];
		 
		  $entId=Cookie::get("ent_id");
		  $num=count($targetUserIds);
		  if($num==0){
		  	$result=$OrgSelf->where("user_id='".$userId."' and ent_id=".$entId)->delete();
		  	if($result!==false){
		  		$status=1;
		  		$desc="del user org self success";
		  		update_ent_version ( $entId );
		  	}else{
		  		$desc="del user org self failed";
		  	}
		  }else{
		  	$OrgSelf->where("user_id='".$userId."' and ent_id=".$entId)->delete();
		  	$dataList=array();
		  	for($i=0;$i<$num;$i++){
		  		$dataList[$i]['user_id']=$userId;
		  		$dataList[$i]['target_user_id']=$targetUserIds[$i];
		  		$dataList[$i]['ent_id']=$entId;
		  		$dataList[$i]['create_time']=get_date_time();
		  		$dataList[$i]['update_time']=get_date_time();
		  		$dataList[$i]['updater_id']=get_cuser_id();
		  	}
		  	//print_r($dataList);
		  	$result=$OrgSelf->addAll($dataList);
		  	//print $OrgSelf->getLastSql();
		  	if($result!==false){
		  		//$this->assign("osId",$result);
		  		$status=1;
		  		$desc=" org self set success";
		  		update_ent_version ( $entId );
		  	}else{
		  		$desc=" org self set fail , try again";
		  	}
		  }
		 
		}
		$this->returnList($status, $desc);
	}
	
//	/**
//	 * 
//	 * 添加企业自定义权限
//	 * 
//	 */
//	public function add(){
//		$status=0;
//		$desc="error parameters";
//		if(!is_ent_master()){
//			$desc="notLogin or noRight";
//			$this->returnList($status, $desc);
//			return;
//		}
//		if(isset($_POST['userId'])&&$_POST['userId']>0&&isset($_POST['targetUserId'])&&$_POST['targetUserId']>0){
//		  $OrgSelf=M("OrgSelf");
//		  $userId=$_POST['userId'];
//		  $targetUserId=$_POST['targetUserId'];
//		  $entId=Cookie::get("ent_id");
//		  $data['user_id']=$userId;
//		  $data['target_user_id']=$targetUserId;
//		  $data['ent_id']=$entId;
//		  $uo=$OrgSelf->where($data)->find();
//		  if(isset($uo['id'])&&$uo['id']>0){
//		  	$status=1;
//		  	$desc=" org self add success";
//		  	$this->assign("osId",$uo['id']);
//		  }else{
//		  	$data['create_time']=get_date_time();
//		  	$data['update_time']=get_date_time();
//		  	$data['updater_id']=get_cuser_id();
//		  	$result=$OrgSelf->add($data);
//		  	if($result!==false){
//		  		$this->assign("osId",$result);
//		  		$status=1;
//		  		$desc=" org self add success";
//		  		update_ent_version ( $entId );
//		  	}else{
//		  		$desc=" org self add fail , try again";
//		  	}
//		  }
//		}
//		$this->returnList($status, $desc);
//	}
//	
//	
//	/**
//	 * 
//	 * 删除自定义
//	 */
//	public function del(){
//		$status=0;
//		$desc="error parameters";
//		if(!is_ent_master()){
//			$desc="notLogin or noRight";
//			$this->returnList($status, $desc);
//			return;
//		}
//		if(isset($_POST['id'])&&$_POST['id']>0){
//			$OrgSelf=M("OrgSelf");
//			$entId=Cookie::get("ent_id");
//			$id=$_POST['id'];
//			$result=$OrgSelf->where("id=".$id." and ent_id=".$entId)->delete();
//			if($result!==false){
//				$status=1;
//				$desc=" org self delete success";
//				update_ent_version ( $entId );
//			}else{
//				$desc=" org self delete fail , try again";
//			}
//			
//		}	
//		$this->returnList($status, $desc);
//	}
//	

	

	
	
	public function addForm(){
		if(!is_ent_master()){
			$this->assign("error","notLogin or noRight");
			$this->display(DEFAULT_ERROR);
			return;
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	public function delForm(){
		if(!is_ent_master()){
			$this->assign("error","notLogin or noRight");
			$this->display(DEFAULT_ERROR);
			return;
		}
		$this->display(DEFAULT_DISPLAY);
	}
}