<?php
/**
 * 
 * 企业功能模块
 * @author Administrator
 *
 */

class EntAction extends CommonAction {
	
	public function page() {
		if (! isRoot ()) {
			$this->assign ( "error", "权限不够！" );
			$this->display ( DEFAULT_ERROR );
			return;
		}
		$Ent = M ( "Ent" );
		$p=1;
		if(isset($_GET['p'])&&$_GET['p']>0){
			$p=$_GET['p'];
		}
		$sql="select e.*, u.nick as ent_master_nick,u.email as ent_master_email  from kx_ent e,kx_user u where e.ent_master_id=u.id order by e.id desc limit ". ($p - 1) * PAGE_NUM_DEFAULT . "," . PAGE_NUM_DEFAULT;
		$list = $Ent->query($sql);
		$this->assign ( 'list', $list );
		//import ( "ORG.Util.Page" ); // 导入分页类
		$count = $Ent->count (); // 查询满足要求的总记录数
		$Page = new Page ( $count, PAGE_NUM_DEFAULT ); // 实例化分页类传入总记录数和每页显示的记录数
		$show = $Page->show (); // 分页显示输出
		$this->assign ( 'page', $show ); // 赋值分页输出
		$this->display ( DEFAULT_DISPLAY );
	}
	
	/**
	 * 
	 * AJAX 更改企业状态
	 */
	public function status(){
		if (! isRoot ()) {
			$this->ajaxReturn(0,"权限不够！",0);
		}
		if(isset($_POST['id'])&&$_POST['id']>0&&isset($_POST['status'])&&$_POST['status']>=0&&$_POST['status']<=1){
			$data['id']=$_POST['id'];
			$data['ent_status']=$_POST['status'];
			$Ent=M("Ent");
			$result=$Ent->save($data);
			if($result!==false){
				$this->ajaxReturn(1,"操作成功！",1);
			}else{
				$this->ajaxReturn(0,"操作失败！请重新尝试！",0);
			}
		}
		$this->ajaxReturn(0,"操作失败！参数错误！",0);
	}
	
	/**
	 * 
	 * 获取企业信息接口
	 */
	public function msg(){
		$status=0;
		$desc="error parameters";
		if(!is_client_login()){
			$desc="notLogin";
			$this->returnList($status, $desc);
			return;
		}
		$entId=Cookie::get("ent_id");
		$Ent=M("Ent");
		$ent=$Ent->find($entId);
		if(isset($ent['id'])&&$ent['id']>0){
			$desc="ent msg";
			$status=1;
			$this->assign("ent",$ent);
		}
		$this->returnList($status, $desc);
	}
	
	public function version(){
		$status=0;
		$desc="error parameters";
		if(!is_client_login()){
			$desc="notLogin";
			$this->returnList($status, $desc);
			return;
		}
		$entId=Cookie::get("ent_id");
		$Ent=M("Ent");
		$ent=$Ent->find($entId);
		if(isset($ent['id'])&&$ent['id']>0){
			$desc="ent version";
			$status=1;
			$this->assign("ent",$ent);
		}
		$this->returnList($status, $desc);
	}
	
	/**
	 * 
	 * 更改当前企业信息
	 */
	public function c_msg(){
		$status=0;
		$desc="error parameters";
		if(!is_ent_master()){
			$desc="notLogin Or noRight";
			$this->returnList($status, $desc);
			return;
		}
		if(isset($_POST['name'])&&""!=trim($_POST['name'])){
			$Ent=M("Ent");
			$entId=Cookie::get("ent_id");
			$data['ent_name']=trim($_POST['name']);
			$data['id']=$entId;
			$data['update_time']=get_date_time();
			$result=$Ent->save($data);
			if($result!==false){
				update_ent_version($entId);
				$status=1;
				$desc="update Ent Name Success";
			}
		}
		$this->returnList($status, $desc);
	}
	
	
	
	public function c_msgForm(){
		$this->display();
	}
}