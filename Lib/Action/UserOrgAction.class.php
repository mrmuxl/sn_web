<?php
class UserOrgAction extends CommonAction{
	/**
	 * 
	 * 批量追加用户岗位（角色）
	 */
	public function append(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['userId'])&&$_POST['userId']>0&&isset($_POST['orgIds'])&&null!=$_POST['orgIds']){
			$userId=$_POST['userId'];
			$orgIds=$_POST['orgIds'];
			//print_r($orgIds);
			if(is_array($orgIds)&&count($orgIds)>0){
				$UserOrg=M("UserOrg");
				$entId=Cookie::get("ent_id");
				$dataList=array();
		  		for($i=0;$i<count($orgIds);$i++){
		  			if($orgIds[$i]>0){
		  				$dataList[$i]['user_id']=$userId;
		  				$dataList[$i]['org_id']=$orgIds[$i];
		  				$dataList[$i]['ent_id']=$entId;
		  				$dataList[$i]['update_time']=get_date_time();
		  				$dataList[$i]['updater_id']=get_cuser_id();
		  			}else{
		  				$desc=" user org append failed, orgIds must be gt 0";
		  				$this->returnList($status, $desc);
		  				return;
		  			}
		  		}
		  		
		  		$result=$UserOrg->addAll($dataList);
		  		if($result!==false){
		  			$status=1;
		  			$desc=" user org append success";
		  			update_ent_version ( $entId );
		  		}else{
		  			$desc=" user org append failed ,try again";
		  		}
			}elseif(!is_array($orgIds)&& is_integer((int)$orgIds)&&$orgIds>0){
				$UserOrg=M("UserOrg");
				$entId=Cookie::get("ent_id");
				$data=array();
		  		$data['user_id']=$userId;
		  		$data['org_id']=$orgIds;
		  		$data['ent_id']=$entId;
		  		$data['update_time']=get_date_time();
		  		$data['updater_id']=get_cuser_id();
		  		$result=$UserOrg->add($data);
		  		if($result!==false){
		  			$status=1;
		  			$desc=" user org append success";
		  			update_ent_version ( $entId );
		  		}else{
		  			$desc=" user org append failed ,try again";
		  		}
			}else{
				$desc="append user org failed, orgIds error";
			}
		}
		$this->returnList($status, $desc);
	
	}
	
	/**
	 * 
	 * 批量删除用户岗位（角色）
	 */
	public function del(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['userId'])&&$_POST['userId']>0&&isset($_POST['orgIds'])&&null!=$_POST['orgIds']){
			$userId=$_POST['userId'];
			$orgIds=$_POST['orgIds'];
			if(is_array($orgIds)&&count($orgIds)>0){
				$UserOrg=M("UserOrg");
				$entId=Cookie::get("ent_id");
				$orgIdsStr=implode(",", $orgIds);
				$sql="user_id=".$userId." and ent_id=".$entId." and org_id in (".$orgIdsStr.")";
				//print $orgIdsStr;
		  		$result=$UserOrg->where($sql)->delete();
		  		//print $UserOrg->getLastSql();
		  		if($result!==false){
		  			$status=1;
		  			$desc=" user org del success";
		  			update_ent_version ( $entId );
		  		}else{
		  			$desc=" user org del failed ,try again";
		  		}
			}elseif(!is_array($orgIds)&& is_integer((int)$orgIds)&&$orgIds>0){
				$orgIds=intval($orgIds);
				$UserOrg=M("UserOrg");
				$entId=Cookie::get("ent_id");
				$sql="user_id=".$userId." and ent_id=".$entId." and org_id=".$orgIds;
				//print $orgIdsStr;
		  		$result=$UserOrg->where($sql)->delete();
				if($result!==false){
		  			$status=1;
		  			$desc=" user org del success";
		  			update_ent_version ( $entId );
		  		}else{
		  			$desc=" user org del failed ,try again";
		  		}
			}else{
				$desc="del user org failed, orgIds error";
			}
		}
		$this->returnList($status, $desc);
	}
	

	
	
	//测试
	public function appendForm() {
		if (! is_ent_master ()) {
			$this->assign ( "error", "notLogin or noRight" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$this->display ( DEFAULT_DISPLAY );
	}
	public function delForm() {
		if (! is_ent_master ()) {
			$this->assign ( "error", "notLogin or noRight" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$this->display ( DEFAULT_DISPLAY );
	}
	
}