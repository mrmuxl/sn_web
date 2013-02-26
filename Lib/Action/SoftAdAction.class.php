<?php 
class SoftAdAction extends CommonAction{
	
	public function ad_list(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		$SoftAd=M("SoftAd");
		$p=1;
		if(isset($_GET['p'])&&intval($_GET['p'])>0){
			$p=intval($_GET['p']);
		}
		$count=$SoftAd->count();
		$adList=$SoftAd->order("id desc")->page($p.",".PAGE_NUM_DEFAULT)->select();
		$Page=new Page($count, PAGE_NUM_DEFAULT);
		$page=$Page->show();
		$this->assign("page",$page);
		$this->assign("adList",$adList);
		$this->display(DEFAULT_ADMIN);
	}
	
	/**
	 * 
	 * 创建广告
	 */
	public function add(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		$day=date("Y-m-d");
		$this->assign("day",$day);
		$this->display(DEFAULT_ADMIN);
	}
	
	public function save(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_POST['title'])&&isset($_POST['ad_url'])&&isset($_POST['exp_day'])){
			if(trim($_POST['title'])!=""){
				$data['title']=trim($_POST['title']);
			}else{
				exit('请填写广告词！[ <A HREF="javascript:history.back()">返 回</A> ]');	
			}
			if(trim($_POST['ad_url'])!=""){
				$data['ad_url']=trim($_POST['ad_url']);
			}else{
				exit('请填写广告链接！[ <A HREF="javascript:history.back()">返 回</A> ]');	
			}
			if(trim($_POST['exp_day'])!=""){
				$data['exp_day']=trim($_POST['exp_day']);
			}else{
				exit('请填写结束日期！[ <A HREF="javascript:history.back()">返 回</A> ]');	
			}
			$data['creater_id']=get_user_id();
			$data['create_time']=get_date_time();
			$SoftAd=M("SoftAd");
			$result=$SoftAd->add($data);
			if($result!==false){
				redirect(C("WWW")."/SoftAd/ad_list");
			}else{
		
				exit('创建广告失败！[ <A HREF="javascript:history.back()">返 回</A> ]');	
		
			}
		}else{
			exit('缺少必要参数！[ <A HREF="javascript:history.back()">返 回</A> ]');
		}
		
	}
	
	/**
	 * 
	 * 广告删除 AJAX
	 */
	public function del(){
		if(!isRoot()){
			$this->ajaxReturn(0,"无权限",0);
		}
		if(isset($_POST['aid'])&&intval($_POST['aid'])>0){
			$data['id']=intval($_POST['aid']);
			$SoftAd=M("SoftAd");
			$result=$SoftAd->where($data)->delete();
			if($result===false){
				$this->ajaxReturn(0,"删除广告失败！",0);
			}
			$this->ajaxReturn(1,"OK",1);
		}else{
			$this->ajaxReturn(0,"参数错误！",0);
		}
		
	}
	
	/**
	 * 
	 * 广告获取接口
	 */
	public function getAdList(){
		$status=0;
		$desc="error";
		$SoftAd=M("SoftAd");
		$saList=$SoftAd->where("exp_day>=curdate()")->field("id,title,ad_url")->select();
		if(count($saList)>0){
			$this->assign("saList",$saList);
			$this->assign("num",count($saList));
		}
		$status=1;
		$desc="OK";
		$this->returnList($status, $desc);
	}
		
}
?>