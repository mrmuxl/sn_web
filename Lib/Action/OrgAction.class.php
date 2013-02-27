<?php
/**
 * 
 * 公司组织结构（权限策略）
 * 企业管理员享有CURD权限
 * @author Administrator
 *
 */
class OrgAction extends CommonAction{
	
	/**
	 * 
	 * 获取企业权限策略接口
	 */
	public function clist(){
		if(!is_client_login()){
			$this->assign("status",0);
			$this->assign("desc","notLogin");
			$this->display();
			return;
		}
		$entId=Cookie::get("ent_id");
		$Org=M("Org");
		$olist=$Org->where("ent_id=".$entId)->findAll();
		$this->assign("olist",$olist);
		$this->assign("num",count($olist));
		$this->assign("status",1);
		$this->assign("desc","org list");
		$this->display();
	}
	
	
	/**
	 * 
	 * 添加岗位接口
	 */
	public function add(){
		if(!is_ent_master()){
			$this->assign("status",0);
			$this->assign("desc","notLogin or noRight");
			$this->display();
			return;
		}
		if(isset($_POST['name'])&&""!=trim($_POST['name'])&&isset($_POST['parentId'])&&$_POST['parentId']>=0){
			$Org=M("Org");
			$entId=Cookie::get("ent_id");
			$data['parent_id']=$_POST['parentId'];
			if($_POST['parentId']>0){
				$num=$Org->where("id=".$_POST['parentId']." and ent_id=".$entId)->count();
				//上级权限不存在
				if($num==0){
					$this->assign("status",0);
					$this->assign("desc","parentId org not exists");
					$this->display();
					return;
				}
			}
			$data['ent_id']=$entId;
			$data['name']=$_POST['name'];
			$count=$Org->where($data)->count();
			if($count>0){
				$this->assign("status",0);
				$this->assign("desc","name already exists");
				$this->display();
				return;
			}
			$data['create_time']=get_date_time();
			$data['update_time']=get_date_time();
			$data['updater_id']=get_cuser_id();
			$result=$Org->add($data);
			if($result!==false){
				$this->assign("status",1);
				$this->assign("orgId",$result);
				$this->assign("desc","add org success");
				update_ent_version ( $entId );
			}else{
				$this->assign("status",0);
				$this->assign("desc","add error,try again");
			}
			$this->display();
			return;
		}
		$this->assign("status",0);
		$this->assign("desc","error parameters");
		$this->display();
	}
	
	public function update(){
		if(!is_ent_master()){
			$this->assign("status",0);
			$this->assign("desc","notLogin or noRight");
			$this->display();
			return;
		}
		$desc="error parameters";
		$status=0;
		if(isset($_POST['id'])&&$_POST['id']>0&&isset($_POST['name'])&&""!=trim($_POST['name'])&&isset($_POST['parentId'])&&$_POST['parentId']>=0){
			$Org=M("Org");
			$entId=Cookie::get("ent_id");
			$id=$_POST['id'];
			$name=$_POST['name'];
			$parentId=$_POST['parentId'];
			$data['id']=$id;
			$data['ent_id']=$entId;
			$count1=$Org->where($data)->count();
			//权限是否存在
			if($count1==0){
				$desc="org not exisits";
				$this->returnList($status, $desc);
				return;
			}
			
			if($_POST['parentId']>0){
				$count2=$Org->where("id=".$parentId." and ent_id=".$entId)->count();
				//上级权限是否存在
				if($count2==0){
					$desc="parentId not exisits";
					$this->returnList($status, $desc);
					return;
				}
			}
			
			$count3=$Org->where("ent_id=".$entId." and parent_id=".$parentId." and name=".$name." and id!=".$id)->count();
			//是否有重名
			if($count3>0){
				$desc="org name already exists";
				$this->returnList($status, $desc);
				return;
			}
			$data['parent_id']=$parentId;
			$data['name']=$name;
			$data['update_time']=get_date_time();
			$data['updater_id']=get_cuser_id();
			$result=$Org->save($data);
			if($result!==false){
				$status=1;
				$desc="org update success";
				update_ent_version ( $entId );
			}else{
				$desc="org update error ,try again";			
			}
			
		}
		$this->returnList($status, $desc);
	}
	
	/**
	 * 
	 * 删除组织结构
	 */
	public function del(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['id'])&&$_POST['id']>0){
			$Org=M("Org");
			$id=$_POST['id'];
			$entId=Cookie::get("ent_id");
			$Org->where("id=".$id." and ent_id=".$entId)->delete();
			//$count=$Org->where("parent_id=".$id." and ent_id=".$entId)->count();
			//print_r($childs);
			$this->delOrg($id);
//			if($count>0){
//				$desc="it has children orgs , not allow to delete";
//				$this->returnList($status, $desc);
//				return;
//			}
//			//传递的ID是其他企业的ID时，虽然返回删除成功，但DB中没有删除
//			$result=$Org->where("id=".$id." and ent_id=".$entId)->delete();
			
			$sql="update kx_user_org set org_id=-1 ,update_time=now(),updater_id='".get_cuser_id()."' where ent_id=".$entId." and org_id not in (select id from kx_org where ent_id=".$entId.")";
			$UserOrg=M("UserOrg");
			$result=$UserOrg->query($sql);
			if($result!==false){
				$status=1;
				$desc="delete org success";
				update_ent_version ( $entId );
			}else{
				$desc="delete org fail , try again";
			}
		}
		$this->returnList($status, $desc);
	}
	

	
	/**
	 * 
	 * 递归删除权限
	 * @param  $pid 父级ID
	 */
	private function delOrg($pid){
		//print $pid."<br />";
		$Org=M("Org");
		$entId=Cookie::get("ent_id");
		$childs=$Org->where("parent_id=".$pid." and ent_id=".$entId)->select();
		$Org->where("parent_id=".$pid." and ent_id=".$entId)->delete();
		for($i=0;$i<count($childs);$i++){
			$id=$childs[$i]['id'];
			$this->delOrg($id);
		}
	}
	/**
	 * 
	 * 测试添加岗位接口
	 */
	public function addForm(){
		if(!is_ent_master()){
			$this->assign("error","notLogin or noRight");
			$this->display(DEFAULT_ERROR);
			return;
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 *测试修改岗位接口
	 */
	public function updateForm(){
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