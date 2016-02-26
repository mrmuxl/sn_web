<?php
/**
 * 
 * 论坛帖子模块
 * @author mokeming
 *
 */

class BlogAction extends  CommonAction {
	
	
	/**
	 * 
	 * 编辑器图片上传
	 */
	public function forumImgUpload(){
		if(!isLogin()){
			$this->ajaxReturn(0,"未登录！",0);
		}
		if ($_FILES ['Filedata'] ['error'] !== 4) {
			$fileInfo = saveFile ( false, 0, 0, "forum" );
			if ($fileInfo === false) {
				echo '{"error" : 1, "message" : "上传图片失败，请重试！"}';
				exit;
			}
			$saveContent = $fileInfo [0] ['saveContent'];
			$filePath = getPicUri ( $saveContent );
			$fileName = getPicName ( $saveContent );
			//$image = C ( 'UPLOAD_PATH' ) . "/" . $filePath . "/" . $fileName;
			$image = C("IMG"). "/" . $filePath . "/" . $fileName;
			//add_water($image);
			echo '{"error" : 0, "url" : "'.$image.'"}';
			exit;
		}
	}

	/**
	 * 
	 * 发表新帖
	 */
	public function new_posts(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		
		//if(isset($_GET['fid'])&&intval($_GET['fid'])>0){
			//$fid=intval($_GET['fid']);
			$fid=1;
			$type=1;
			if(isset($_GET['type'])&&intval($_GET['type'])==2){
				$type=2;
			}
			$this->assign("post_type",$type);
			$this->assign("fid",$fid);
		//}
		//else{
		//	$this->error_msg("请选择一个版块！");
		//}
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	
	/**
	 * 
	 * 保存主帖
	 */
	public function save(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_POST['fid'])&&isset($_POST['title'])&&isset($_POST['forum_msg'])&&isset($_POST['type'])){
			
			if(intval($_POST['fid'])>0){
				$data['forum_id']=intval($_POST['fid']);
			}else{
				$this->error_msg("请选择一个版块");
			}
			if(trim($_POST['title'])!=""){
				$data['title']=trim($_POST['title']);
			}else{
				$this->error_msg("请填写标题！");
			}
			$msg="";
			if(trim($_POST['forum_msg'])==""){
				$this->error_msg("请填写帖子内容！");	
			}
			
			$type=1;
			if(intval($_POST['type'])==2){
				$type=2;
			}
			$data['tid']=0;
			$data['post_type']=$type;
	
			$data['user_id']=get_user_id();
			
			$now=get_date_time();
			$data['create_time']=$now;
			$data['update_time']=$now;
			$data['last_uid']=get_user_id();
			$data['last_time']=$now;
			$Mpost=M("ForumMpost");
			
			$Mpost->startTrans();
			$result=$Mpost->add($data);
			if($result!==false){
				$tid=$result;
				$Posts=M("ForumPosts");
				//$msg=$this->html2bbcode(trim($_POST['forum_msg']));
				$msg=trim($_POST['forum_msg']);
				
				//将img标签中的width与height替换为空
				$msg=preg_replace("/(\<img.*)height=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
				$msg=preg_replace("/(\<img.*)width=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
					
				//去掉div标签
				$pattern1='/<div.*?>|<\/div>/';
				$msg=preg_replace($pattern1, '', $msg);
					
				//去掉display属性
				$pattern3='/(<(\w+).*)display\:\w+\;(.*>)/';
				$msg=preg_replace($pattern3, '$1 $3', $msg);
				
				$data['content']=$msg;
				$data['tid']=$tid;
				$data['is_main']=1;
				$data['user_ip']=get_user_ip();
				unset($data['last_uid']);
				unset($data['last_time']);
				$result=$Posts->add($data);
				if($result!==false){
					$postsId=$result;
					//$result=$this->dealAttachTemp($postsId,$tid,0, $data['user_id'], $msg);
					//if($result!==false){
						$Mpost->commit();
						redirect(C("WWW")."/Blog/view?tid=".$tid);
					//}
				}
			}
			$Mpost->rollback();
			$this->error_msg("发表帖子失败！");
			
		}else{
			$this->error_msg("缺少必要的参数！");
		}
	}
	
	/**
	 * 
	 * 保存回复帖
	 */
	public function reply_save(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_POST['tid'])&&isset($_POST['forum_msg'])){
			$tid=intval($_POST['tid']);
			if($tid<=0){
				$this->error_msg("缺少必要的参数！");
			}
			$replyId=0;
			if(isset($_POST['reply'])&&intval($_POST['reply'])>0){
				$replyId=intval($_POST['reply']);
			}
			$msg="";
			if(trim($_POST['forum_msg'])!=""){
				//$msg=$this->html2bbcode(trim($_POST['forum_msg']));
				$msg=trim($_POST['forum_msg']);
				//将img标签中的width与height替换为空
				$msg=preg_replace("/(\<img.*)height=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
				$msg=preg_replace("/(\<img.*)width=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
					
				//去掉div标签
				$pattern1='/<div.*?>|<\/div>/';
				$msg=preg_replace($pattern1, '', $msg);
					
				//去掉display属性
				$pattern3='/(<(\w+).*)display\:\w+\;(.*>)/';
				$msg=preg_replace($pattern3, '$1 $3', $msg);
				$data['content']=$msg;
			}else{
				$this->error_msg("请填写帖子内容！");
			}
			$ForumPosts=M("ForumPosts");
			$rPosts=$ForumPosts->where("is_main=1 and tid=".$tid)->find();
			if(!isset($rPosts['id'])||$rPosts['is_del']==1){
				$this->error_msg("很抱歉，您回复的主题不存在或已被删除！");
			}
			if($replyId>0){
				$rep=$ForumPosts->find($replyId);
				if(!isset($rep['id'])){
					$this->error_msg("很抱歉，您回复的帖子不存在或已被删除！");
				}
			}

			$uid=get_user_id();
			$tid=$rPosts['tid'];
			$data['forum_id']=$rPosts['forum_id'];
			$data['title']="";
			$data['tid']=$tid;
			$data['reply_id']=$replyId;
			$data['post_type']=1;
			$data['is_main']=0;
			$data['user_id']=$uid;
			$data['user_ip']=get_user_ip();
			$data['create_time']=get_date_time();
			$data['update_time']=get_date_time();
			$ForumPosts->startTrans();
			$result=$ForumPosts->add($data);
			if($result!==false){
				$postsId=$result;
				//$result=$this->dealAttachTemp($postsId, $tid, $rPosts['attach'], $uid, $msg);
				//if($result!==false){
					$ForumMpost=M("ForumMpost");
					$sql="update kx_forum_mpost set reply_num=reply_num+1,last_uid=".$uid.",last_time='".$data['create_time']."' where id=".$tid;
					$result=$ForumMpost->execute($sql);
					if($result!==false){
						$ForumPosts->commit();
						redirect(C("WWW")."/Blog/view?tid=".$tid);
					}
				//}
			}
			$ForumPosts->rollback();
			$this->error_msg("回复帖子失败！");
		}else{
			$this->error_msg("缺少必要的参数！");
		}
	}
	
	
	
	/**
	 * 
	 * 帖子列表
	 */
	public function show(){
		$ForumMpost=M("ForumMpost");
		$sql="select m.id,m.forum_id,m.title,m.reply_num,m.view_num,m.create_time,p.content from kx_forum_mpost m left join kx_forum_posts p on m.id=p.tid where m.is_del=0 and p.is_main=1  order by m.top_num desc,id desc ";
		$mainList=$ForumMpost->query($sql);
		$this->assign("mainList",$mainList);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 添加评论
	 */
	public function add_comment(){
		$uid=0;
		if(isset($_POST['id'])&&intval($_POST['id'])>0&&isset($_POST['msg'])&&trim($_POST['msg'])!=""){
			$tid=intval($_POST['id']);
			$ForumPosts=M("ForumPosts");
			$rPosts=$ForumPosts->where("is_main=1 and tid=".$tid)->find();
			if(!isset($rPosts['id'])||$rPosts['is_del']==1){
				$this->ajaxReturn("","您回复的文章不存在或已经删除！",0);
			}	
			if(isLogin()){
				$uid=get_user_id();
			}
			$data['content']=htmlspecialchars(trim($_POST['msg']));
			$data['user_id']=$uid;
			$data['forum_id']=$rPosts['forum_id'];
			$data['title']="";
			$data['tid']=$tid;
			$data['reply_id']=$rPosts['id'];
			$data['post_type']=1;
			$data['is_main']=0;
			$data['user_ip']=get_user_ip();
			$data['create_time']=get_date_time();
			$data['update_time']=get_date_time();
			$ForumPosts->startTrans();
			$result=$ForumPosts->add($data);
			if($result!==false){
				$postsId=$result;
				$ForumMpost=M("ForumMpost");
				$sql="update kx_forum_mpost set reply_num=reply_num+1,last_uid=".$uid.",last_time='".$data['create_time']."' where id=".$tid;
				$result=$ForumMpost->execute($sql);
				if($result!==false){
					$ForumPosts->commit();
					if(isLogin()){
						if(isset ( $_SESSION['avatar'] )){
							$img=$_SESSION['avatar'];
							$imgUrl=C("IMG")."/".getPicUri($img)."/snap_50X50_".getPicName($img);
						}else{
							$imgUrl=C("STATIC")."/Img/snap_50X50_default_head.jpg";
						}
						$html=$this->appendHtml($imgUrl,$_SESSION['nick'] , $data['create_time'], $data['content']);
					}else{
						$imgUrl=C("STATIC")."/Img/snap_50X50_default_head.jpg";
						$html=$this->appendHtml($imgUrl,$data['user_ip'] , $data['create_time'], $data['content']);
					}
					$this->ajaxReturn($html,"OK",1);
				}
				
			}
			$ForumPosts->rollback();
			$this->ajaxReturn(0,"评论失败",0);
			
			
		}else{
			$this->ajaxReturn("","参数错误",0);
		}
	}

	private function appendHtml($img,$unick,$create_time,$msg){
		$html='<li><div class="c_uhead"><img src="'.$img.'" /></div>'.
			  '<div class="c_uname">'.$unick.'&nbsp;&nbsp;说：</div><div class="c_time">'.$create_time.'</div>'.
			  '<div class="c_content">'.$msg.'</div><div class="clear"></div></li>';
		return $html;
	}
	
	/**
	 * 
	 * 评论列表
	 */
	public function c_list(){
		if(isset($_GET['id'])&&intval($_GET['id'])>0){
			$tid=intval($_GET['id']);
			$ForumPosts=M("ForumPosts");
			$ForumMpost=M("ForumMpost");
			$posts=$ForumMpost->where("id=".$tid)->field("id,forum_id,title,reply_num,view_num,is_del,create_time")->find();
			$status=true;
			if(!isset($posts['id'])||$posts['is_del']==1){
				$this->assign("error","很抱歉，您查看的文章不存在或已被删除！");
				$status=false;
			}
			if($status){
			
				$ForumMpost->setInc("view_num","id=".$tid);
				$p=1;
				$perPage=100;
				if(isset($_GET['p'])&&intval($_GET['p'])>0){
					$p=intval($_GET['p']);
				}
				$count=$ForumPosts->where("is_main=0 and is_del=0 and tid=".$tid)->count();
				if($count>0){
					$pList=$ForumPosts->where("is_main=0 and is_del=0 and tid=".$tid)->page($p.",".$perPage)->order("id")->select();
					if(count($pList)>0){
						$uids=array();
						$pids=array();
						for($i=0;$i<count($pList);$i++){
							$uid=$pList[$i]['user_id'];
							$pid=$pList[$i]['id'];
							if(!isset($uids[$uid])){
								$uids[$uid]=$uid;
							}
							if(!isset($pids[$pid])){
								$pids[$pid]=$pid;
							}
						}
						$uList=$this->getUserMsg($uids);
						$Page=new Page($count, $perPage);
						$page=$Page->show();
						$this->assign("pList",$pList);
						$this->assign("uList",$uList);
						$this->assign("page",$page);
					}
	
				}
			}
		}else{
			$this->assign("error","请选择要查看评论的文章！");
		}
		$this->display();
	}
	
	
	/**
	 * 
	 * 查看帖子
	 */
	public function view(){
//		if(!isLogin()){
//			$callback=C("WWW").get_cur_uri();
//			$this->redirect_login($callback);
//		}
//		
		
		//$cache=new CommonCache();
		//$ffList=$cache->forumMenuCache();
		//$this->assign("ffList",$ffList);
		if(isset($_GET['tid'])&&intval($_GET['tid'])>0){
			$tid=intval($_GET['tid']);
			
			$ForumPosts=M("ForumPosts");
			$ForumMpost=M("ForumMpost");
			$posts=$ForumMpost->where("id=".$tid)->field("id,forum_id,title,reply_num,view_num,is_del,create_time")->find();
			if(!isset($posts['id'])||$posts['is_del']==1){
				$this->error_msg("很抱歉，您访问的主题不存在或已被删除！");
			}
			$this->assign("posts",$posts);
			$this->assign("tid",$tid);
			$this->assign("fid",$posts['forum_id']);
			$ForumMpost->setInc("view_num","id=".$tid);
			$p=1;
			$perPage=10;
			if(isset($_GET['p'])&&intval($_GET['p'])>0){
				$p=intval($_GET['p']);
			}
			$count=$ForumPosts->where("is_del=0 and tid=".$tid)->count();
			if($count>0){
				$pList=$ForumPosts->where("is_del=0 and tid=".$tid)->page($p.",".$perPage)->select();
				if(count($pList)>0){
					$uids=array();
					$pids=array();
					for($i=0;$i<count($pList);$i++){
						$uid=$pList[$i]['user_id'];
						$pid=$pList[$i]['id'];
						if(!isset($uids[$uid])){
							$uids[$uid]=$uid;
						}
						if(!isset($pids[$pid])){
							$pids[$pid]=$pid;
						}
					}
					//$pList=$this->dealViewContent($tid, $pList, $pids);
					$uList=$this->getUserMsg($uids);
					$Page=new Page($count, $perPage);
					$page=$Page->show();
					$this->assign("pList",$pList);
					$this->assign("uList",$uList);
					$this->assign("page",$page);
				}
//				$isFirst=0;
//				if($p==1){
//					$isFirst=1;
//				}
//				$this->assign("isFirst",$isFirst);
			}
		}else{
			$this->error_msg("很抱歉，您选择的主题不存在或已被删除！");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 处理帖子内容 主要是为了处理附件
	 * @param  $pList 帖子列表
	 * @param  $pids  帖子IDS
	 */
	private function dealViewContent($tid,$pList,$pids){
		$Attach=M("ForumAttach");
		$aList=$Attach->where("tid=".$tid." and posts_id in (".implode(",", $pids).")")->field("aid,posts_id,attach")->select();
		$aMap=array();
		if(isLogin()){
			for($i=0;$i<count($aList);$i++){
				$pid=$aList[$i]['posts_id'];
				if(!isset($aMap[$pid])){
					$aMap[$pid]['s_str']=array();
					$aMap[$pid]['r_str']=array();
				}
				$num=count($aMap[$pid]['s_str']);
				$aMap[$pid]['s_str'][$num]="[attach]".$aList[$i]['aid']."[/attach]";
				$aName=getPicPrevName($aList[$i]['attach']);
				$aMap[$pid]['r_str'][$num]="<dl class='attach'><dt><img src='".C("STATIC")."/images/luntan/attach.gif' /></dt><dd><a href='".C("WWW")."/Attach/download?id=".$aList[$i]['aid']."' target='_blank'>".$aName."</a></dd></dl>";
			}
		}else{
			for($i=0;$i<count($aList);$i++){
				$pid=$aList[$i]['posts_id'];
				if(!isset($aMap[$pid])){
					$aMap[$pid]['s_str']=array();
					$aMap[$pid]['r_str']=array();
				}
				$num=count($aMap[$pid]['s_str']);
				$aMap[$pid]['s_str'][$num]="[attach]".$aList[$i]['aid']."[/attach]";
			
				$aMap[$pid]['r_str'][$num]="<div class='locked'>你需要登录才可以下载或查看附件</div>";
			}
		}	
// 		for($i=0;$i<count($pList);$i++){
// 			$msg=$pList[$i]['content'];
// 			$pid=$pList[$i]['id'];
// 			if(isset($aMap[$pid])){
// 				$pList[$i]['content']=$this->bbcode2html($msg, $aMap[$pid]['s_str'],$aMap[$pid]['r_str']);
// 			}else{
// 				$pList[$i]['content']=$this->bbcode2html($msg, null,null);
// 			}
// 		}
	
		return $pList;

	}
	
	
	/**
	 * 
	 * 编辑帖子
	 */
	public function edit(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_GET['tid'])&&intval($_GET['tid'])>0){
			$tid=intval($_GET['tid']);	
			$ForumMpost=M("ForumMpost");
			$mpost=$ForumMpost->where("is_del=0 and id=".$tid)->field("id,user_id")->find();
			$uid=get_user_id();
			if(!isset($mpost['id'])){
				$this->error_msg("很抱歉，您选择的主题不存在或已被删除！");
			}
			if($mpost['user_id']!=$uid){
				$this->error_msg("很抱歉，您不能编辑他人的帖子！");
			}
			$ForumPosts=M("ForumPosts");
			$posts=$ForumPosts->where("is_main=1  and tid=".$tid)->field("id,tid,title,content,user_id")->find();
			
			//$msg=$posts['content'];
			//$posts['content']=$this->bbcode2html($msg, null, null);
			$this->assign("posts",$posts);
			$this->display(DEFAULT_DISPLAY);
		}else{
			$this->error_msg("请选择一个要编辑的帖子！");
		}
	}
	
	
	/**
	 * 
	 * 更新主帖
	 */
	public function update(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");	
		}
		if(isset($_POST['tid'])&&intval($_POST['tid'])>0&&isset($_POST['title'])&&isset($_POST['forum_msg'])){
			$tid=intval($_POST['tid']);
			
			if(trim($_POST['title'])!=""){
				$data['title']=trim($_POST['title']);
			}else{
				$this->error_msg("请填写标题！");
			}
			$msg="";
			if(trim($_POST['forum_msg'])==""){
				$this->error_msg("请填写帖子内容！");	
			}
			$ForumMpost=M("ForumMpost");
			$mpost=$ForumMpost->where("is_del=0 and id=".$tid)->field("id,user_id,attach")->find();
			$uid=get_user_id();
			if(!isset($mpost['id'])){
				$this->error_msg("很抱歉，您选择的主题不存在或已被删除！");
			}
			if($mpost['user_id']!=$uid){
				$this->error_msg("很抱歉，您不能编辑他人的帖子！");
			}
			$ForumPosts=M("ForumPosts");
			$posts=$ForumPosts->where("is_main=1 and tid=".$tid)->field("id,tid,title,content,user_id")->find();
			
			//$msg=$this->html2bbcode(trim($_POST['forum_msg']));
			$msg=trim($_POST['forum_msg']);
			//将img标签中的width与height替换为空
			$msg=preg_replace("/(\<img.*)height=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
			$msg=preg_replace("/(\<img.*)width=\"\d+\"(.*\/>)/", "$1 $2 ", $msg);
				
			//去掉div标签
			$pattern1='/<div.*?>|<\/div>/';
			$msg=preg_replace($pattern1, '', $msg);
				
			//去掉display属性
			$pattern3='/(<(\w+).*)display\:\w+\;(.*>)/';
			$msg=preg_replace($pattern3, '$1 $3', $msg);
			$data['id']=$posts['id'];
			$data['content']=$msg;
			$ForumPosts->startTrans();
			$result=$ForumPosts->save($data);
		
			if($result!==false){
				$postsId=$posts['id'];
				//$result=$this->dealAttachTemp($postsId, $tid, $mpost['attach'], $uid, $msg);
				//if($result!==false){
					$ForumPosts->commit();
					redirect(C("WWW")."/Blog/view?tid=".$tid);
				//}
			}
			$ForumPosts->rollback();
			$this->error_msg("编辑帖子失败！");
		}else{
			$this->error_msg("请选择一个要编辑的帖子！");
		}
	}
	
	
	
	/**
	 * 
	 * 帖子列表
	 */
	public function view_list(){
		
		//if(isset($_GET['fid'])&&intval($_GET['fid'])>0){
			//$cache=new CommonCache();
			//$ffList=$cache->forumMenuCache();
			//$this->assign("ffList",$ffList);
			//$fId=intval($_GET['fid']);
			$fId=1;
			$Forum=M("ForumForum");
			$forum=$Forum->find($fId);
			if(!isset($forum['id'])){
				$this->error_msg("很抱歉，你访问的论坛版块不存在或已删除！");
			}
			$this->assign("forum",$forum);
			$this->assign("fid",$fId);
			//$this->assign("ffList",$ffList);
			$ForumMpost=M("ForumMpost");
			$p=1;
			if(isset($_GET['p'])&&intval($_GET['p'])>0){
				$p=intval($_GET['p']);
			}
			
			$count=$ForumMpost->where("forum_id=".$fId." and is_del=0")->count();
			$today=0;
			if($count>0){
				$today=$ForumMpost->where("forum_id=".$fId." and date(create_time)=curdate() and is_del=0")->count();
				$pList=$ForumMpost->where("forum_id=".$fId." and is_del=0")->order("top_num desc,id desc")->page($p.",".PAGE_NUM_DEFAULT)->select();
				if(count($pList)>0){
				$uids=array();
					for($i=0;$i<count($pList);$i++){
						$uid=$pList[$i]['user_id'];
						if(!isset($uids[$uid])){
							$uids[$uid]=$uid;
						}
						$lastId=$pList[$i]['last_uid'];
						if(!isset($uids[$lastId])){
							$uids[$lastId]=$lastId;
						}
					}
					$uList=$this->getUserMsg($uids);
					$Page=new Page($count, PAGE_NUM_DEFAULT);
					$page=$Page->show();
					$this->assign("pList",$pList);
					$this->assign("uList",$uList);
					$this->assign("page",$page);
				}
			}
			$this->assign("totalNum",$count);
			$this->assign("todayNum",$today);
		//}else{
		//	$this->error_msg("很抱歉，你访问的论坛版块不存在或已删除！");
		//}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 论坛帖子置顶
	 */
	public function top_set(){
		if(!isRoot()){
			$this->ajaxReturn(0,"无权限！",0);
		}
		if(isset($_POST['pid'])&&intval($_POST['pid'])>0){
			$Mpost=M("ForumMpost");
			$data['id']=intval($_POST['pid']);
			$mpost=$Mpost->where($data)->find();
			if(isset($mpost['id'])&&$mpost['id']==$data['id']){
				$msg=0;//页面提示表示取消置顶
				if($mpost['top_num']==0){
					$data['top_num']=1;
				}else{
					$data['top_num']=0;
					$msg=1;//置顶
				}
				$result=$Mpost->save($data);
				if($result===false){
					$this->ajaxReturn(0,"设置失败",0);
				}else{
					$this->ajaxReturn($msg,"OK",1);
				}
			}else{
				$this->ajaxReturn(0,"帖子不存在！",0);
			}
		}
		$this->ajaxReturn(0,"未选择帖子",0);
	}
	
	/**
	 * 
	 * 获取用户信息
	 * @param array $uids 用户IDS
	 * return array 
	 * key-user_id value-user_msg
	 */
	private function getUserMsg($uids){
		$uList=array();
		if(count($uids)>0){
			$User=M("User");
			$uList2=$User->where("id in (".implode(",", $uids).")")->field("id,email,nick,avatar")->select();
			for($i=0;$i<count($uList2);$i++){
				$uid=$uList2[$i]['id'];
				$uList[$uid]=$uList2[$i];
			}
		}
		return $uList;
	}
	
	/**
	 * 
	 * AJAX删除帖子
	 * mode=1  删除主帖
	 * mode=2 删除回复帖
	 */
	public function del(){
		if(!isRoot()){
			$this->ajaxReturn(0,"无权限！",0);
		}	
		if(isset($_POST['pid'])&&intval($_POST['pid'])>0&&isset($_POST['mode'])&&intval($_POST['mode'])>0){
			$pid=intval($_POST['pid']);
			$mode=intval($_POST['mode']);
			if($mode==1){
				$Mpost=M("ForumMpost");
				$data['id']=$pid;
				$data['is_del']=1;
				$result=$Mpost->save($data);
				if($result!==false){
					$this->ajaxReturn(1,"删除成功！",1);
				}else{
					$this->ajaxReturn(0,"删除失败！",0);
				}
			}else{
				$Posts=M("ForumPosts");
				$data['id']=$pid;
				$data['is_del']=1;
				$result=$Posts->save($data);
				if($result!==false){
					$this->ajaxReturn(1,"删除成功！",1);
				}else{
					$this->ajaxReturn(0,"删除失败！",0);
				}
			}
		}else{
			$this->ajaxReturn(0,"参数错误！",0);
		}

	}
	/**
	 * 
	 * 我的帖子
	 * 
	 */
	public function post_list(){
		$user_id=0;
		if(isset($_GET['user_id'])&&intval($_GET['user_id'])>0){
			$user_id=intval($_GET['user_id']);
			if($user_id==get_user_id()){
				$this->assign("is_personal_set",1);
			}
		}elseif(isset($_GET['nick'])&&trim($_GET['nick'])!=""){
			$nick=trim($_GET['nick']);
			$User=M("User");
			$user_id=$User->where("nick_name='".$nick."'")->getField("id");
			if($user_id==get_user_id()){
				$this->assign("is_personal_set",1);
			}
		}else{
			$user_id=get_user_id();
			$this->assign("is_personal_set",1);
		}
		if(empty($user_id)){
			//$this->error_msg("访问的页面不存在或已删除！");
			redirect(C("WWW")."/User/login");
		}
		
		$User=M("User");
		$userOne=$User->find($user_id);
		$this->assign("userOne",$userOne);
		$p=1;
		if(isset($_GET['p'])&&intval($_GET['p'])>0){
			$p=intval($_GET['p']);
		}
		$perPageNum=20;
		$ForumMpost=M("ForumMpost");
//		$sql="select fm.*,ff.name as forum_name,u.nick_name
//				from oujia_forum_mpost as fm,oujia_forum_forum as ff,oujia_user as u
//					where fm.forum_id=ff.id and fm.user_id=".$user_id." and fm.last_uid=u.id order by fm.id desc limit ".($p-1)*$perPageNum.",".$perPageNum;
		$sql="select fm.*,ff.name as forum_name
				from oujia_forum_mpost as fm,oujia_forum_forum as ff
					where fm.forum_id=ff.id and fm.user_id=".$user_id." order by fm.id desc limit ".($p-1)*$perPageNum.",".$perPageNum;
		$forum_posts=$ForumMpost->query($sql);
		if(!empty($forum_posts)){
			$uids="";
			for($i=0;$i<count($forum_posts);$i++){
				$uids.=",".$forum_posts[$i]['last_uid'];
			}
			$uids=substr($uids, 1);//里面可能有重复的uid，是否要考虑去重
			$User=M("User");
			$uList2=$User->where("id in (".$uids.")")->field("id,email,nick_name,portrait")->select();
			for($i=0;$i<count($uList2);$i++){
				$uid=$uList2[$i]['id'];
				$uList[$uid]=$uList2[$i]['nick_name'];
			}
			$this->assign("uList",$uList);
			$this->assign("forum_posts",$forum_posts);
		}	
		$count=$ForumMpost->where("user_id=".$user_id)->count();
		$Page=new Page($count, $perPageNum);
		$show=$Page->show();
		$this->assign("page",$show);
		//判断是否有品牌馆
		$BrandHall = M("BrandHall");
		$bhOne=$BrandHall->where("user_id=".$user_id)->find();
		if(count($bhOne)>0){
			$this->assign("bhOne",$bhOne);
		}
		$this->assign("count_bh",count($bhOne));
		$sql="select domain_name,banner_pic,name from oujia_brand_hall where user_id=".$user_id." 
					or user_id in ( select brand_user_id from oujia_brand_auth where user_id=".$user_id.")";
		$brandHall_exits=$BrandHall->query($sql);
		$this->assign("brandHall_exits",$brandHall_exits);//是否显示Ipad管理
		$this->display(DEFAULT_NO_LEFT);
	}
	
	
	/**
	 * 
	 * 将oujia_forum_posts中的content转换为html格式
	 */
	public function content2html(){
		 ini_set('max_execution_time', 0);
		//$Test=M('Test');
		/* $ForumPosts=M('ForumPosts');
		$fpList=$ForumPosts->field('id,content')->select();
		for($i=0;$i<count($fpList);$i++){
			$data[$i]['id']=$fpList[$i]['id'];
			$data[$i]['content']=$this->bbcode2html($fpList[$i]['content']);
			echo $data[$i]['id'];
			$ForumPosts->save($data[$i]);
		}
		echo "done";exit; */
		
		$pattern1='/\[url=(.*?)\](.*?)\[\/url\]/';
		$pattern2='/\[url\](.*?)\[\/url\]/';
		
		
		$this->wipeBad($pattern1, '<a href="$1">$2</a>', '[/url]');
		$this->wipeBad($pattern2, '<a href="$1">$1</a>', '[/url]');
		
		$pattern3='/\[backcolor(.*?)\]|\[\/backcolor\]/';
		$bad="/backcolor";
		$this->wipeBad($pattern3, '', $bad);
		
		$pattern4='/\[p(.*?)\]|\[\/p\]/';
		$bad="[/p]";
		$this->wipeBad($pattern4, '', $bad);

		$pattern5='/\[i=s\]/';
		$bad="[i=s]";
		$this->wipeBad($pattern5, '<i>', $bad);

		$pattern6='/\[table\]/';
		$bad="[table]";
		$this->wipeBad($pattern6, '<table>', $bad);
		 
		$pattern7='/\[tr\]/';
		$bad="[tr]";
		$this->wipeBad($pattern7, '<tr>', $bad);
		$pattern8='/\[td\]/';
		$bad="[td]";
		$this->wipeBad($pattern8, '<td>', $bad);
		$pattern9='/\[\/table\]/';
		$bad="[/table]";
		$this->wipeBad($pattern9, '</table>', $bad);
		
		$pattern10='/\[\/tr\]/';
		$bad="[/tr]";
		$this->wipeBad($pattern10, '</tr>', $bad);
		
		$pattern11='/\[\/td\]/';
		$bad="[/td]";
		$this->wipeBad($pattern11, '</td>', $bad);
		
		
		
		$pattern12='/&lt;/';
		$bad="&lt;";
		$this->wipeBad($pattern12, '<', $bad);
		$pattern13='/&gt;/';
		$bad="&gt;";
		$this->wipeBad($pattern13, '>', $bad);
		
		$pattern12='/\[hr\]/';
		 $bad="[hr]";
		$this->wipeBad($pattern12, '<hr/>', $bad);
		
		//print_r($fpList);exit;
		//echo $result;exit;
	}
	
	/**
	 * 
	 * 转换
	 */
	private function wipeBad($pattern,$replace,$bad){
		$ForumPosts=M('ForumPosts');
		$fpList=$ForumPosts->where('content like "%'.$bad.'%"')->field('id,content')->select();
		for($i=0;$i<count($fpList);$i++){
			$data[$i]['content']=preg_replace($pattern, $replace, $fpList[$i]['content']);
			$data[$i]['id']=$fpList[$i]['id'];
			$result=$ForumPosts->save($data[$i]);
		}
		echo $result;
	}
	
	
	/**
	 * 
	 * bbcode转化为HTML
	 * @param string $msg
	 * @param array $s_str
	 * @param array $r_str
	 */
	private function bbcode2html($msg,$s_str,$r_str){
		if($msg==null||trim($msg)==""){
			return "";
		}else{
			import("@.Util.bbcode.bbcode");
			$bbcode=new bbcode();
			return $msg=$bbcode->bbcode2html($msg,$s_str,$r_str);
		}
	}


	/**
	 * 
	 * HTML转化为BBCODE
	 * @param $msg
	 */
	private function html2bbcode($msg){
		if($msg==null||trim($msg)==""){
			return "";
		}else{
			import("@.Util.bbcode.bbcode");
			$bbcode=new bbcode();
			return $msg=$bbcode->html2bbcode($msg);
		}
	}
	
}