<?php
/**
 * 
 * 版本发布
 * @author mokeming@163.com
 *
 */
class PubAction extends CommonAction{
	
	/**
	 * 
	 * 发布列表页
	 */
	public function index(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$Pub=M("Pub");
		$count=$Pub->count();
		$p=1;
		if(isset($_GET['p'])&&intval($_GET['p'])>0){
			$p=intval($_GET['p']);
		}
		$perNum=24;
		$pubList=$Pub->order("id desc")->page($p.",".$perNum)->select();
		$Page=new Page($count, $perNum);
		$page=$Page->show();
		$this->assign("page",$page);
		$this->assign("pubList",$pubList);
		$this->display(DEFAULT_ADMIN);
	}
	
	/**
	 * 
	 * 新增发布信息
	 */
	public function add(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$this->display(DEFAULT_ADMIN);
	}
	
	
	/**
	 * 
	 * 保存发布信息
	 */
	public function save(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_POST['ver'])&&isset($_POST['desc'])){
			$data['ver']=trim($_POST['ver']);
			if($data['ver']==""){
				$this->error_msg("请填写版本号！");
			}
			if(trim($_POST['desc'])==""){
				$this->error_msg("请填写功能描述！");
			}
			$Pub=M("Pub");
			$count=$Pub->where($data)->count();
			if($count>0){
				$this->error_msg("版本号已存在！");
			}
			$data['pub_desc']=trim($_POST['desc']);
			
			if($_FILES['ins']['error']!==4||$_FILES['patch']['error']!==4){

				$insFile="";
				$patchFile="";
				if($_FILES['ins']['error']!==4){
					$insFile=$_FILES['ins']['name'];
					if(file_exists("./Public/LiveUp/Install/".$insFile)){
						$this->error_msg("该安装包已经存在！");
					}
				}
				if($_FILES['patch']['error']!==4){
					$patchFile=$_FILES['patch']['name'];
					if(file_exists("./Public/LiveUp/Install/".$data['ver']."/".$patchFile)){
						$this->error_msg("该补丁包已经存在！");
					}
				}
				$info=$this->save_file();
				if($info===false){
					$this->error_msg("上传文件失败！");
				}
				for($i=0;$i<count($info);$i++){
					if($info[$i]['name']==$insFile){
						$result=rename($info[$i]['savepath'].$info[$i]['savename'], "./Public/LiveUp/Install/".$insFile);
						if($result===false){
							$this->error_msg("上传安装包失败！");
						}
						$data['install_file']=$insFile;
					}elseif($info[$i]['name']==$patchFile){
						mkdir("./Public/LiveUp/Install/".$data['ver']."/");
						$result=rename($info[$i]['savepath'].$info[$i]['savename'], "./Public/LiveUp/Install/".$data['ver']."/".$patchFile);
						if($result===false){
							$this->error_msg("上传补丁包失败！");
						}
						$data['patch_file']=$data['ver']."/".$patchFile;
					}
				}
			}
			$data['create_time']=get_date_time();
			$result=$Pub->add($data);
			if($result===false){
				$this->error_msg("新增发布失败！");
			}
			redirect(C("WWW")."/Pub");
			
		}else{
			$this->error_msg("缺少必要参数！");
		}
	}
	
	/**
	 * 
	 * 编辑发布
	 */
	public function edit(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['id'])&&intval($_GET['id'])>0){
			$data['id']=intval($_GET['id']);
			$Pub=M("Pub");
			$pub=$Pub->find($data['id']);
			if(isset($pub['id'])){
				$this->assign("pub",$pub);
			}else{
				$this->error_msg("选择的发布不存在！");
			}
			$this->display(DEFAULT_ADMIN);
		}else{
			$this->error_msg("请选择一个有效的发布！");
		}
	}
	
	/**
	 * 
	 * 更新发布信息
	 */
	public function update(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_POST['id'])&&intval($_POST['id'])>0&&isset($_POST['ver'])&&isset($_POST['desc'])){
			$data['id']=intval($_POST['id']);
			$data['ver']=trim($_POST['ver']);
			if($data['ver']==""){
				$this->error_msg("请填写版本号！");
			}
			$data['pub_desc']=trim($_POST['desc']);
			if($data['pub_desc']==""){
				$this->error_msg("请填写功能描述！");
			}
			$Pub=M("Pub");
			$count=$Pub->where("ver='".$data['ver']."' and id!=".$data['id'])->count();
			if($count>0){
				$this->error_msg("版本号已存在！");
			}
			if($_FILES['ins']['error']!==4||$_FILES['patch']['error']!==4){

				$insFile="";
				$patchFile="";
				if($_FILES['ins']['error']!==4){
					$insFile=$_FILES['ins']['name'];
					
				}
				if($_FILES['patch']['error']!==4){
					$patchFile=$_FILES['patch']['name'];
					
				}
				$info=$this->save_file();
				if($info===false){
					$this->error_msg("上传文件失败！");
				}
				for($i=0;$i<count($info);$i++){
					if($info[$i]['name']==$insFile){
						$result=rename($info[$i]['savepath'].$info[$i]['savename'], "./Public/LiveUp/Install/".$insFile);
						if($result===false){
							$this->error_msg("上传安装包失败！");
						}
						$data['install_file']=$insFile;
					}elseif($info[$i]['name']==$patchFile){
						mkdir("./Public/LiveUp/Install/".$data['ver']."/");
						$result=rename($info[$i]['savepath'].$info[$i]['savename'], "./Public/LiveUp/Install/".$data['ver']."/".$patchFile);
						if($result===false){
							$this->error_msg("上传补丁包失败！");
						}
						$data['patch_file']=$data['ver']."/".$patchFile;
					}
				}
			}
			$result=$Pub->save($data);
			if($result===false){
				$this->error_msg("编辑发布失败！");
			}
			redirect(C("WWW")."/Pub");
		}else{
			$this->error_msg("参数非法！");
		}
		
	}
	
	
	private function save_file(){
		import ( "ORG.Net.UploadFile" );
		
		$upload = new UploadFile (); // 实例化上传类
		
	
		$upload->maxSize = 52428800; // 设置附件上传大小
		
		$upload->allowExts = array ('zip','jpg' ); // 设置附件上传类型
	
		$date = date ( "Y/m/d" );
		$upload->savePath = './Public/LiveUp/Install/'; // 设置附件上传目录
		muti_mkdir ( $upload->savePath );
		//设置是否生成缩略图及其最大宽、高
		$upload->saveRule = "uniqid"; //文件名生成规则
		
		if (! $upload->upload ()) { // 上传错误提示错误信息
			exit ( $upload->getErrorMsg () . "  " );
			return false;
		} else { // 上传成功获取上传文件信息
			
			$info = $upload->getUploadFileInfo ();
			return $info;
		}
	}
	
	/**
	 * 
	 * AJAX确认正式发布
	 */
	public function do_pub(){
		if(!isRoot()){
			$this->ajaxReturn(0,"无权限！",0);
		}
		if(isset($_POST['id'])&&intval($_POST['id'])>0){
			$data['id']=intval($_POST['id']);
			$Pub=M("Pub");
			$pub=$Pub->where($data)->find();
			if(isset($pub['id'])){
			
				if(empty($pub['pub_time'])){
					$data['pub_time']=get_date_time();
					$result=$Pub->save($data);
					if($result===false){
						$this->ajaxReturn(0,"当前发布失败！请重试！",0);
					}
					$downHtml='
					<span>
						<a href="'.C("DOWNLOAD").'/Install/'.$pub['install_file'].'" target="_blank" title="下载">
							<img src="'.C("STATIC").'/Img/download_btn2.png" class="mypng" />
						</a>
					</span>';
					$fileName="./Tpl/default/Index/index_download.html";
					if(file_exists($fileName)){
						$fp=fopen($fileName, "w");
						if($fp){
							fwrite($fp, $downHtml);
						}else{
							$this->ajaxReturn(0,"更新发布链接失败！",0);
						}
						fclose($fp);
					}
					$this->ajaxReturn($data['pub_time'],"OK",1);
				}else{
					$this->ajaxReturn(0,"当前发布已发布！",0);
				}
			}else{
				$this->ajaxReturn(0,"当前发布不存在！",0);
			}
		}else{
			$this->ajaxReturn(0,"参数错误！",0);
		}
	}
	
	
	public function del_pub(){
		if(!isRoot()){
			$this->ajaxReturn(0,"无权限！",0);
		}
		if(isset($_POST['id'])&&intval($_POST['id'])>0){
			$data['id']=intval($_POST['id']);
			$Pub=M("Pub");
			$pub=$Pub->where($data)->find();
			if(isset($pub['id'])){
				if(empty($pub['pub_time'])){
					$result=$Pub->where($data)->delete();
					if($result===false){
						$this->ajaxReturn(0,"删除发布失败！请重试！",0);
					}
					$this->ajaxReturn(1,"OK",1);
				}else{
					$this->ajaxReturn(0,"已正式发布的不允许删除！",0);
				}
			}else{
				$this->ajaxReturn(0,"要删除的发布不存在！",0);
			}
		}else{
			$this->ajaxReturn(0,"参数错误！",0);
		}
	}
	
	
}