<?php
/**
 * 
 * 企业用户
 * @author Administrator
 *
 */

class EntUserAction extends CommonAction{
	/**
	 * 
	 * 接口获取企业用户列表
	 */
	public function clist(){
		if(!is_client_login()){
			$this->assign("status",0);
			$this->assign("desc","notLogin");
			$this->display();
			return;
		}
		$entId=Cookie::get("ent_id");
		$isMaster=Cookie::get("isentmaster");
		$sql="select u.id as id ,u.email as email,u.nick as nick ,uo.org_id as org_id,eu.status as euStatus from kx_user u,kx_user_org uo ,kx_ent_user eu where  eu.user_id=u.id and eu.user_id=uo.user_id and uo.ent_id=".$entId." and eu.ent_id=".$entId;
		$sql2="select u.id as id ,u.email as email,u.nick as nick ,eu.status as euStatus from kx_user u,kx_ent_user eu where  eu.user_id=u.id and eu.ent_id=".$entId." and u.id not in(select user_id from kx_user_org where ent_id=".$entId.") ";
		if($isMaster==0){
			$sql=$sql." and eu.status=1";
			$sql2=$sql2." and eu.status=1";
		}
		$sql.=" order by u.id";
		$EntUser=M("EntUser");
		$euList=$EntUser->query($sql);
		$euListNoOrg=$EntUser->query($sql2);
		if(count($euList)>0){
			$euList2=array();
			$uid=0;
			$j=-1;
			$k=0;
			$n=1;
			for($i=0;$i<=count($euList);$i++){
				
				if($euList[$i]['id']!=$uid){
					$j=$j+1;
					$k=0;
					if($j>0){
						$euList2[$j-1]['len']=$n;
						$n=1;
					}
					if($i==count($euList)){
						break;
					}
					$euList2[$j]=$euList[$i];
					$euList2[$j]['orgs'][$k]=$euList[$i]['org_id'];
					$uid=$euList[$i]['id'];
				}else{
					$k=$k+1;
					$euList2[$j]['orgs'][$k]=$euList[$i]['org_id'];
					$n=$n+1;
				}
			}
			//print_r($euList2);
			$this->assign("euList",$euList2);
			$this->assign("num",count($euList2));
			$this->assign("euList2",$euListNoOrg);
			$this->assign("num2",count($euListNoOrg));
		}
		$this->assign("status",1);
		$this->assign("desc","ent user list");
		$this->display();
	}
	
	/**
	 * 
	 * 企业管理员修改企业用户状态
	 */
	public function status(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['id'])&&$_POST['id']>0&&isset($_POST['status'])&&$_POST['status']>=0){
			$EntUser=M("EntUser");
			$entId=Cookie::get("ent_id");
			$data['user_id']=$_POST['id'];
			$data['ent_id']=$entId;
			$eu=$EntUser->where($data)->find();
			if(isset($eu['id'])&&$eu['id']>0){
				$data['id']=$eu['id'];
				$data['status']=$_POST['status'];
				$data['updater_id']=get_cuser_id();
				$data['update_time']=get_date_time();
				$result=$EntUser->save($data);
				if($result!==false){
					$status=1;
					$desc="update ent user status success";
					update_ent_version ( $entId );
				}else{
					$desc="update ent user status fail,try again";
				}
			}else{
				$desc="no ent user exists";
			}
		}
		$this->returnList($status, $desc);
		
	}
	
	/**
	 * 
	 * 企业管理员删除用户
	 */
	public function del(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['id'])&&trim($_POST['id'])!=""){
			$EntUser=M("EntUser");
			$UserOrg=M("UserOrg");
			$entId=Cookie::get("ent_id");
			$data['user_id']=trim($_POST['id']);
			$data['ent_id']=$entId;
			$result=$EntUser->where($data)->delete();
			if($result!==false){
				$Ent=M("Ent");
				$Ent->setDec("ent_user_num","id=".Cookie::get("ent_id"));
				$result2=$UserOrg->where($data)->delete();
				$desc="delete user success";
				$status=1;
				update_ent_version ( $entId );
			}else{
				$desc="delete user fail";
			}
		}
		$this->returnList($status, $desc);
	}
	
	/**
	 * 
	 * 企业用户列表
	 * （中央服务器管理员查看）
	 */
	public function page(){
		if (! isRoot ()) {
			$this->assign ( "error", "权限不够！" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		if(isset($_GET['ent'])&&$_GET['ent']>0){
			$entId=$_GET['ent'];
			$p=1;
			if(isset($_GET['p'])&&$_GET['p']>0){
				$p=$_GET['p'];
			}
			$EntUser=M("EntUser");
			$sql="select eu.* , u.nick as nick ,u.email as email,o.id as org_id,o.name as org_name from kx_ent_user eu ,kx_user u ,kx_user_org uo,kx_org o where eu.ent_id=".$entId." and eu.user_id=u.id and eu.user_id=uo.user_id and uo.ent_id=".$entId." and uo.org_id=o.id";
			$sql_c = "select count(*) as tp_count from ( " . $sql . " ) t";
			$eu_count=$EntUser->query($sql_c);
			$count = $eu_count [0] ['tp_count'];
			$sql_l=$sql." order by eu.id desc limit ". ($p - 1) * PAGE_NUM_DEFAULT . "," . PAGE_NUM_DEFAULT;
			$euList=$EntUser->query($sql_l);
			$this->assign("euList",$euList);
			$Page = new Page ( $count, PAGE_NUM_DEFAULT ); 
			$show = $Page->show (); 
			$this->assign ( 'page', $show ); 
			$this->display ( DEFAULT_DISPLAY );
			return;
		}
		$this->assign ( "error", "参数错误！" );
		$this->display ( DEFAULT_ERROR );
	}
	
	
	

	
	public function statusForm(){
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