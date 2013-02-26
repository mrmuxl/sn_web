<?php
/**
 * 
 * 论坛版块
 * @author 莫柯明
 *
 */ 
class ForumAction extends CommonAction{
	
	/**
	 * 
	 * 版块后台列表
	 */
	public function admin_index(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		$FF=M("ForumForum");
		$ffList=$FF->select();
		$this->assign("ffList",$ffList);
		
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 添加版块
	 */
	public function add(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 保存版块
	 */
	public function save(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_POST['name'])&&trim($_POST['name'])!=""){
			$ForumForum=M("ForumForum");
			$data['name']=trim($_POST['name']);
			$data['updater_id']=get_user_id();
			$data['update_time']=get_date_time();
			$result=$ForumForum->add($data);
			if($result!==false){
				redirect(C("WWW")."/Forum/admin_index");
			}else{
				$this->error_msg("创建版块失败！");
			}
		}else{
			$this->error_msg("参数错误！");
		}
		
	}
}