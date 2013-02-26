<?php

class SoftRecordAction extends CommonAction {
	
	/**
	 * 
	 * 记录软件装机信息、登录记录
	 */
	public function record(){
		if(isset($_POST['ver'])&&isset($_POST['clientIdentifie'])&&isset($_POST['md5str'])){
			$ver=trim($_POST['ver']);
			$client=trim($_POST['clientIdentifie']);
			$md5str=trim($_POST['md5str']);
			$verify=md5($ver.$client."123456");
			if($verify===$md5str){
				$SoftRecord=M("SoftRecord");
				$count=$SoftRecord->where("client_identifie='".$client."' and login_time < curdate()")->count();
				if($count==0){
					$data['is_new']=1;
				}else{
					$data['is_new']=0;
				}
				$data['version']=$ver;
				$data['client_identifie']=$client;
				$data['login_time']=get_date_time();
				$data['is_uninstall']=0;
				$result=$SoftRecord->add($data);
			}
		}
	}
	
	
	/**
	 * 
	 * 软件卸载
	 */
	public function Uninstall(){
		if(isset($_POST['ver'])&&isset($_POST['clientIdentifie'])&&isset($_POST['md5str'])){
			$ver=trim($_POST['ver']);
			$client=trim($_POST['clientIdentifie']);
			$md5str=trim($_POST['md5str']);
			$verify=md5($ver.$client."123456");
			if($verify===$md5str){
				$SoftRecord=M("SoftRecord");
				$data['is_new']=0;
				$data['version']=$ver;
				$data['client_identifie']=$client;
				$data['login_time']=get_date_time();
				$data['is_uninstall']=1;
				$result=$SoftRecord->add($data);
			}
		}
	}
	
	/**
	 * 
	 * 用户装机统计、登录统计
	 */
	public function tongji(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$type=1;
		if(isset($_GET['type'])&&$_GET['type']>0){
			$type=intval(trim($_GET['type']));
		}
		//今日登录的注册用户数
		$User=M("User");
		$curLoginNum=$User->where("date(last_login)=curdate()")->count();
		$this->assign("curLoginNum",$curLoginNum);
		
		
		$SoftRecord=M("SoftRecord");
		$sql="select count(*) as num from (select distinct client_identifie from kx_soft_record where is_uninstall=0 ) t";
		$allUserNum=$SoftRecord->query($sql);
		$this->assign("allUserNum",$allUserNum[0]['num']);
		
		//$sql="select count(*) as login_num,login_time from (select client_identifie,date(login_time) as login_time from kx_soft_record where is_uninstall=0 group by client_identifie,date(login_time)) t group by t.login_time order by login_num desc limit 1";
		//$maxLoginMsg=$SoftRecord->query($sql);
		//$this->assign("maxLoginMsg",$maxLoginMsg[0]);
		$TongjiRecord=M("TongjiRecord");
		$maxLoginMsg=$TongjiRecord->order("all_num desc")->field("tongji_day as login_time,all_num as login_num")->find();
		$this->assign("maxLoginMsg",$maxLoginMsg);
		if($type==1){
			if(isset($_GET['day'])&&trim($_GET['day'])!=""){
				$day=trim($_GET['day']);
			}else{
				$day=date("Y-m-d");
			}
			$this->assign("day",$day);
			$this->day_tongji($day);
		}else{
			$this->month_tongji();
		}
		$this->assign("type",$type);
		$this->display(DEFAULT_ADMIN);
		
	}
	
	/**
	 * 
	 * 每日统计
	 */
	private function day_tongji($day){
		//新用户数
		$SoftRecord=M("SoftRecord");
		//$sql="select max(client_identifie) as client_identifie,count(*) as login_num from kx_soft_record where is_new=1 and is_uninstall=0 and date(login_time)='".$day."' group by client_identifie";
		$sql="select count(*) as num from (select max(client_identifie) as client_identifie,count(*) as login_num from kx_soft_record where is_new=1 and is_uninstall=0 and date(login_time)='".$day."' group by client_identifie)t";
		$newList=$SoftRecord->query($sql);
		//$this->assign("newList",$newList);
		$this->assign("newCount",$newList[0]['num']);
		//$sql="select max(client_identifie) as client_identifie,count(*) as login_num from kx_soft_record where is_new=0 and is_uninstall=0 and date(login_time)='".$day."' group by client_identifie";
		$sql="select count(*) as num from (select max(client_identifie) as client_identifie,count(*) as login_num from kx_soft_record where is_new=0 and is_uninstall=0 and date(login_time)='".$day."' group by client_identifie)t";
		$oldList=$SoftRecord->query($sql);
		//$this->assign("oldList",$oldList);
		$this->assign("oldCount",$oldList[0]['num']);
		$this->assign("dayCount",$newList[0]['num']+$oldList[0]['num']);
		$sql="select count(*) as num from (select distinct client_identifie from kx_soft_record where is_uninstall=1 and date(login_time)='".$day."') t";
		$uninstallNum=$SoftRecord->query($sql);
		$this->assign("uninstallNum",$uninstallNum[0]['num']);
		$User=M("User");
		//2013-02-07修改  注册的用户（可以未激活）
		$registUserNum=$User->where("date(create_time)='".$day."'")->count();
		$this->assign("regUserNum",$registUserNum);
	}
	
	private function month_tongji(){
	
	}
	
	/**
	 * 
	 * 每日卸载软件图表统计
	 */
	public function uninstall_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$this->assign("day",$day);
		$SoftRecord=M("SoftRecord");
		$sql="select * from (select client_identifie,max(login_time) as login_time from kx_soft_record where is_uninstall=1  and date(login_time)='".$day."' group by client_identifie) t order by login_time desc";
		//$srList=$SoftRecord->where("is_uninstall=1 and date(login_time)='".$day."'")->select();
		$srList=$SoftRecord->query($sql);
		$srNumByHour=array('00'=>0,'01'=>0,'02'=>0,'03'=>0,'04'=>0,'05'=>0,'06'=>0,'07'=>0,'08'=>0,'09'=>0,'10'=>0,'11'=>0,'12'=>0,'13'=>0,'14'=>0,'15'=>0,'16'=>0,'17'=>0,'18'=>0,'19'=>0,'20'=>0,'21'=>0,'22'=>0,'23'=>0);
		$clientList=array();
		for($i=0;$i<count($srList);$i++){
			$loginTime=$srList[$i]["login_time"];
			$timeArray=preg_split("/[\s:]+/", $loginTime);
			$timeKey=$timeArray[1];
			$srNumByHour[$timeKey]=$srNumByHour[$timeKey]+1;
			$clientList[$i]=$srList[$i]['client_identifie'];
		}
		$this->assign("srList",$srList);
		if(count($clientList)>0){
			$sql="select client_identifie,min(login_time) as login_time from kx_soft_record where is_new=1 and client_identifie in ('".implode("','", $clientList)."') group by client_identifie";
			$srfList=$SoftRecord->query($sql);//第一次登录时间
			$firstList=array();
			for($i=0;$i<count($srfList);$i++){
				$cid=$srfList[$i]['client_identifie'];
				$firstList[$cid]=$srfList[$i]['login_time'];
			}
			$this->assign("firstList",$firstList);
//			$sql="select client_identifie,max(login_time) as login_time from kx_soft_record where is_uninstall=1  and date(login_time)='".$day."' group by client_identifie";
//			$unTimeList=$SoftRecord->query($sql);
//			//print_r($unTimeList);
//			$unList=array();
//			for($i=0;$i<count($unTimeList);$i++){
//				$cid=$unTimeList[$i]['client_identifie'];
//				$unList[$cid]=$unTimeList[$i]['login_time'];
//			}
//			
//			$this->assign("unList",$unList);
		}
		$this->assign("srNum",$srNumByHour);
		$this->display(DEFAULT_DISPLAY);
	}
	
	public function record_by_cid(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(!isset($_GET['cid'])||trim($_GET['cid'])=="")
			exit('请选择一个MAX地址！[ <A HREF="javascript:history.back()">返 回</A> ]');
		$SoftRecord=M("SoftRecord");
		$srList=$SoftRecord->where("client_identifie='".trim($_GET['cid'])."'")->select();
		$this->assign("srList",$srList);
		$this->assign("cid",trim($_GET['cid']));
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 30天每日次数登录统计
	 */
	public function login_tongji(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$LoginRecord=M("LoginRecord");
		$lrList=$LoginRecord->where("login_day between '".$day_array[0]."' and '".$day_array[29]."'")->getField("login_day,login_num");
		$this->assign("lrList",$lrList);
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 异常客户端：总客户端
	 * 异常客户端：卸载客户端
	 */
	public function bug_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$Model=new Model();
		//bugSQL
		$sql="select count(*) as num,upload_date from (select client_identifie,date(upload_time) as upload_date from  kx_soft_bug where date(upload_time)  between '".$day_array[0]."' and '".$day_array[29]."' group by client_identifie,date(upload_time))t group by t.upload_date";
		$bugList=$Model->query($sql);
		//totalSQL
		$sql="select count(*) as num,login_date from (select client_identifie,date(login_time) as login_date from  kx_soft_record where is_uninstall=0 and date(login_time)  between '".$day_array[0]."' and '".$day_array[29]."' group by client_identifie,date(login_time))t group by t.login_date";
		$totalList=$Model->query($sql);
		//uninstallSQL
		$sql="select count(*) as num,login_date from (select client_identifie,date(login_time) as login_date from  kx_soft_record where is_uninstall=1 and date(login_time)  between '".$day_array[0]."' and '".$day_array[29]."' group by client_identifie,date(login_time))t group by t.login_date";
		$unList=$Model->query($sql);
		//newSQL
		$sql="select count(*) as num,login_date from (select client_identifie,date(login_time) as login_date from  kx_soft_record where is_new=1 and date(login_time)  between '".$day_array[0]."' and '".$day_array[29]."' group by client_identifie,date(login_time))t group by t.login_date";
		$newList=$Model->query($sql);
		
		//reggisterSQL
		$sql="select count(*) as num,date(create_time) as create_date from kx_user where date(create_time) between '".$day_array[0]."' and '".$day_array[29]."' group by date(create_time)";
		$regList=$Model->query($sql);
		
		$dataMap=array();
		for($i=0;$i<30;$i++){
			if(isset($bugList[$i])){
				$upload_date=$bugList[$i]['upload_date'];
				$dataMap[$upload_date]['bug']=$bugList[$i]['num'];
			}
			if(isset($totalList[$i])){
				$upload_date=$totalList[$i]['login_date'];
				$dataMap[$upload_date]['total']=$totalList[$i]['num'];
			}
			if(isset($unList[$i])){
				$upload_date=$unList[$i]['login_date'];
				$dataMap[$upload_date]['un']=$unList[$i]['num'];
			}
			if(isset($newList[$i])){
				$upload_date=$newList[$i]['login_date'];
				$dataMap[$upload_date]['new']=$newList[$i]['num'];
			}
			
			if(isset($regList[$i])){
				$upload_date=$regList[$i]['create_date'];
				$dataMap[$upload_date]['reg']=$regList[$i]['num'];
			}
			
		}
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	/**
	 * 
	 * 最近30天bug率(7天平均卸载率)
	 */
	public function bug_ratio_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$Model=new Model();
		$sql="select id,seven_new_num,seven_un_num,tongji_day from kx_tongji_record where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$bugList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($bugList);$i++){
			$tongji_day=$bugList[$i]['tongji_day'];
			$dataMap[$tongji_day]['ratio']=round($bugList[$i]['seven_un_num']*100/$bugList[$i]['seven_new_num'],2);
		}
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
		
	}
	
	/**
	 * 
	 * 最近30天留存率(上月登录且本月登录/上月登录数 )15天作为一个月周期
	 */
	public function remain_ratio_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$Model=new Model();
		$sql="select id,cur_mon_num,last_mon_num,tongji_day from kx_tongji_record where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$bugList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($bugList);$i++){
			$tongji_day=$bugList[$i]['tongji_day'];
			$dataMap[$tongji_day]['ratio']=round($bugList[$i]['cur_mon_num']*100/$bugList[$i]['last_mon_num'],2);
		}
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	/**
	 * 
	 * 最近30天沉默率
	 */
	public function silence_ratio_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$User=M("User");
		//激活用户数
		$actNum=$User->where("status=1")->count();
		//未激活用户数
		$noActNum=$User->where("status=0")->count();
		$this->assign("actNum",$actNum);
		$this->assign("noActNum",$noActNum);
		
		
		$Model=new Model();
		$sql="select id,no_login_num,tongji_day from kx_tongji_record where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$bugList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($bugList);$i++){
			$tongji_day=$bugList[$i]['tongji_day'];
			$dataMap[$tongji_day]['ratio']=round($bugList[$i]['no_login_num']*100/$actNum,2);
		}
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 最近30天每日局域网数量曲线图
	 */
	public function lan_line_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$Model=new Model();
		$sql="select id,lan_num,tongji_day from kx_lan_day where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$lanList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($lanList);$i++){
			$tongji_day=$lanList[$i]['tongji_day'];
			$dataMap[$tongji_day]=$lanList[$i]['lan_num'];
		}
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 最近30天每日局域网装机数、PC数堆积图
	 */
	public function lan_stack_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$type=1;
		if(isset($_GET['type'])&&intval($_GET['type'])>0){
			$type=intval($_GET['type']);
		}
		$typeName="";
		switch($type){
			case 1:$typeName="装机数";break;
			case 2:$typeName="PC数";break;
			default:;
		}
		if($typeName==""){
			$this->error_msg("当前统计行为不存在！");
		}
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$Model=new Model();
		$sql="select * from kx_lan_day where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$lanList=$Model->query($sql);
		$dataMap=array();
		if($type==1){//装机数
			for($i=0;$i<count($lanList);$i++){
				$tongji_day=$lanList[$i]['tongji_day'];
				$dataMap[$tongji_day]['num1']=$lanList[$i]['qm1'];
				$dataMap[$tongji_day]['num2']=$lanList[$i]['qm2'];
				$dataMap[$tongji_day]['num3']=$lanList[$i]['qm3'];
				$dataMap[$tongji_day]['num4']=$lanList[$i]['qm4'];
				$dataMap[$tongji_day]['num5']=$lanList[$i]['qm5'];
				$dataMap[$tongji_day]['num6']=$lanList[$i]['qm6'];
				$dataMap[$tongji_day]['num7']=$lanList[$i]['qm7'];
			}
		}elseif($type==2){
			for($i=0;$i<count($lanList);$i++){
				$tongji_day=$lanList[$i]['tongji_day'];
				$dataMap[$tongji_day]['num1']=$lanList[$i]['pc1'];
				$dataMap[$tongji_day]['num2']=$lanList[$i]['pc2'];
				$dataMap[$tongji_day]['num3']=$lanList[$i]['pc3'];
				$dataMap[$tongji_day]['num4']=$lanList[$i]['pc4'];
				$dataMap[$tongji_day]['num5']=$lanList[$i]['pc5'];
				$dataMap[$tongji_day]['num6']=$lanList[$i]['pc6'];
				$dataMap[$tongji_day]['num7']=$lanList[$i]['pc7'];
			}
		}
		$this->assign("type",$type);
		$this->assign("typeName",$typeName);
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 发布24小时内注册用户统计集合页
	 * 及当日上线注册用户行为统计集合页
	 */
	public function reg_tongji(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 发布24小时内注册用户、未激活用户、卸载用户
	 */
	public function reg_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$Model=new Model();
		$sql="select id,ver,pub_time from kx_pub where is_tongji=1";
		$pubList=$Model->query($sql);
		//print_r($pubList);
		$sql="select id,pub_id,reg_num,act_num,un_num from kx_pub_tongji";
		$ptList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($ptList);$i++){
			$pid=$ptList[$i]['pub_id'];
			$dataMap[$pid]['total']=$ptList[$i]['reg_num'];
			$dataMap[$pid]['noact']=$ptList[$i]['reg_num']-$ptList[$i]['act_num'];
			$dataMap[$pid]['un']=$ptList[$i]['un_num'];
		}
		$this->assign("pubList",$pubList);
		$this->assign("pubNum",count($pubList));
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 发布24小时内注册用户1=文件传输，2=打印，3=聊天，4=好友 堆积图
	 * 2013-02-07 修改注册用户即可（可以未激活）
	 */
	public function reg_stack_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$type=1;
		if(isset($_GET['type'])&&intval($_GET['type'])>0){
			$type=intval($_GET['type']);
		}
		$typeName="";
		$Model=new Model();
		switch ($type){
			case 1:{$typeName="文件传输次数";$sql="select id,pub_id,reg_num,trans0 as num0,trans1 as num1,trans2 as num2,trans3 as num3 from kx_pub_tongji";break;}
			case 2:{$typeName="打印次数";$sql="select id,pub_id,reg_num,print0 as num0,print1 as num1,print2 as num2,print3 as num3 from kx_pub_tongji";break;}
			case 3:{$typeName="聊天次数";$sql="select id,pub_id,reg_num,chat0 as num0,chat1 as num1,chat2 as num2,chat3 as num3 from kx_pub_tongji";break;}
			case 4:{$typeName="新增好友数";$sql="select id,pub_id,reg_num,friend0 as num0,friend1 as num1,friend2 as num2,friend3 as num3 from kx_pub_tongji";break;}
			case 5:{$typeName="邀请数";$sql="select id,pub_id,reg_num,invite0 as num0,invite1 as num1,invite2 as num2,invite3 as num3,invite4 as num4 from kx_pub_tongji";break;}
			default:$sql="";
		}
		if($sql==""){
			$this->error_msg("请选择正确的统计行为！");
		}
		$this->assign("typeName",$typeName);
		$this->assign("type",$type);
		$ptList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($ptList);$i++){
			$pid=$ptList[$i]['pub_id'];
			//行为未产生的用户
			$dataMap[$pid]['num0']=$ptList[$i]['reg_num']-$ptList[$i]['num0'];
			//行为产生的用户
			$dataMap[$pid]['num1']=$ptList[$i]['num1'];
			$dataMap[$pid]['num2']=$ptList[$i]['num2'];
			$dataMap[$pid]['num3']=$ptList[$i]['num3'];
			if($type==5){
				$dataMap[$pid]['num4']=$ptList[$i]['num4'];
			}
		}
		$sql="select id,ver,pub_time from kx_pub where is_tongji=1";
		$pubList=$Model->query($sql);
		$this->assign("pubList",$pubList);
		$this->assign("pubNum",count($pubList));
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * 当日上线注册用户行为统计：
	 * 上线注册用户、激活用户、卸载用户
	 */
	public function online_act_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$sql="select id,tongji_day,on_num,act_num,un_num from kx_act_tongji where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$Model=new Model();
		$ptList=$Model->query($sql);
		
		$dataMap=array();
		for($i=0;$i<count($ptList);$i++){
			$tDay=$ptList[$i]['tongji_day'];
			$dataMap[$tDay]['on']=$ptList[$i]['on_num'];
			$dataMap[$tDay]['act']=$ptList[$i]['act_num'];
			$dataMap[$tDay]['un']=$ptList[$i]['un_num'];
		}
		$this->assign("dataMap",$dataMap);
		
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	/**
	 * 
	 * 上线用户行为分析  1=文件传输，2=打印，3=聊天，4=好友 堆积图
	 * 5=好友邀请数，6=累计好友数
	 *
	 */
	public function online_act_stack_chart(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		$type=1;
		if(isset($_GET['type'])&&intval($_GET['type'])>0){
			$type=intval($_GET['type']);
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$date_array = explode("-", $day);
		$now = mktime(0, 0, 0, $date_array[1], $date_array[2], $date_array[0]);
		$day_array=array();
		for($i=29;$i>=1;$i--){
			$oldNow=$now-$i*86400;
			$oldday = date("Y-m-d", $oldNow);
			$day_array[(29-$i)]=$oldday;
		}
		$day_array[29]=$day;
		$typeName="";
		$Model=new Model();
		switch ($type){
			case 1:{$typeName="文件传输次数";$sql="select id,tongji_day,on_num,trans0 as num0,trans1 as num1,trans2 as num2,trans3 as num3 from kx_act_tongji";break;}
			case 2:{$typeName="打印次数";$sql="select id,tongji_day,on_num,print0 as num0,print1 as num1,print2 as num2,print3 as num3 from kx_act_tongji";break;}
			case 3:{$typeName="聊天次数";$sql="select id,tongji_day,on_num,chat0 as num0,chat1 as num1,chat2 as num2,chat3 as num3 from kx_act_tongji";break;}
			case 4:{$typeName="新增好友数";$sql="select id,tongji_day,on_num,friend0 as num0,friend1 as num1,friend2 as num2,friend3 as num3 from kx_act_tongji";break;}
			case 5:{$typeName="邀请数";$sql="select id,tongji_day,on_num,invite0 as num0,invite1 as num1,invite2 as num2,invite3 as num3,invite4 as num4 from kx_act_tongji";break;}
			case 6:{$typeName="累计好友数";$sql="select id,tongji_day,on_num,friend_all0 as num0,friend_all1 as num1,friend_all2 as num2,friend_all3 as num3 from kx_act_tongji";break;}
			default:$sql="";
		}
		if($sql==""){
			$this->error_msg("请选择正确的统计行为！");
		}
		$sql.=" where tongji_day>='".$day_array[0]."' and tongji_day<='".$day_array[29]."'";
		$this->assign("typeName",$typeName);
		$this->assign("type",$type);
		$this->assign("day_array",$day_array);
		$this->assign("day",$day);
		
		$ptList=$Model->query($sql);
		$dataMap=array();
		for($i=0;$i<count($ptList);$i++){
			$tDay=$ptList[$i]['tongji_day'];
			//行为未产生的用户
			if($type==6){
				$dataMap[$tDay]['num0']=$ptList[$i]['num0'];
			}else{
				$dataMap[$tDay]['num0']=$ptList[$i]['on_num']-$ptList[$i]['num0'];
			}
			//行为产生的用户
			$dataMap[$tDay]['num1']=$ptList[$i]['num1'];
			$dataMap[$tDay]['num2']=$ptList[$i]['num2'];
			$dataMap[$tDay]['num3']=$ptList[$i]['num3'];
			if($type==5){
				$dataMap[$tDay]['num4']=$ptList[$i]['num4'];
			}
		}
		$this->assign("dataMap",$dataMap);
		$this->display(DEFAULT_DISPLAY);
	}
	
	
	
	/**
	 * 
	 * 客户端BUG记录信息
	 */
	public function bug_msg(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$SoftBug=M("SoftBug");
		$bugList=$SoftBug->where("date(upload_time)='".$day."'")->select();
		$this->assign("bugList",$bugList);
		$this->assign("day",$day);
		
		//上传的文件
		$date2=str_replace("-", "/", $day);
		$forder="BugReport/".$date2;
		$dir=opendir(C("UPLOAD_PATH")."/".$forder);
		
		if($dir===false){
			exit('文件目录不存在！[ <A HREF="javascript:history.back()">返 回</A> ]');
		}
		$fnames=array();

		while(($filename=readdir($dir))!==false){
			
			if($filename!="."&&$filename!=".."){
				$bugFile=C("UPLOAD_PATH")."/".$forder."/".$filename;
				$ctime=filectime($bugFile);
				$fSize=filesize($bugFile);
				if(!isset($fnames[$ctime])){
					$fnames[$ctime]=array();
				}
				$num=count($fnames[$ctime]);
				$data=array();
				$data['size']=$fSize;
				$data['time']=$ctime;
				$data['name']=$filename;
				$fnames[$ctime][$num]=$data;
			}
			
		}
	
		closedir($dir);
		ksort($fnames);
		$this->assign("fnames",$fnames);
		$this->assign("forder",$forder);
		
		$this->display(DEFAULT_DISPLAY);
	}
	
	/**
	 * 
	 * BUG日志
	 * type=s 服务端
	 * type=c 客户端
	 */
	public function bug_log(){
		if(!isRoot()){
			redirect(C("WWW")."/User/login");
		}
		if(isset($_GET['day'])&&trim($_GET['day'])!=""){
			$day=trim($_GET['day']);
		}else{
			$day=date("Y-m-d");
		}
		$type="";
		if(isset($_GET['type'])&&trim($_GET['type'])!=""){
			$type=trim($_GET['type']);
		}
		$log="";
		if($type=="c"){
			$file="/home/admin/php/www/kx/Public/Log/client_log/soft_bug_".$day.".log";
			if(!file_exists($file)){
				exit('当日日志文件不存在！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$log=file_get_contents($file);
		}else if($type=="s"){
			if($day==date("Y-m-d")){
				$file="/home/admin/udtserver/udt4/app/qm_error.log";
			}else{
				$file="/home/admin/php/www/kx/Public/Log/server_log/qm_error.log-".$day;
			}
			if(!file_exists($file)){
				exit('当日日志文件不存在！[ <A HREF="javascript:history.back()">返 回</A> ]');
			}
			$log=file_get_contents($file);
		}else{
			exit('请选择一个日志类型！[ <A HREF="javascript:history.back()">返 回</A> ]');
		}
		$log=str_replace("\n", "<br />", $log);
		header("Content-Type: text/html; charset=GBK");
		echo $log;
		//$this->assign("log",$log);
		//$this->display();
	}
	
	/**
	 * 
	 * 登录时长记录
	 */
	public function utime(){
		if(isset($_POST['clientIdentifie'])&&trim($_POST['clientIdentifie'])!=""
		&&isset($_POST['day'])&trim($_POST['day'])!=""&&isset($_POST['utime'])&&intval($_POST['utime'])>0){
			$data['client_identifie']=trim($_POST['clientIdentifie']);
			$data['tongji_day']=trim($_POST['day']);
			$SoftUtime=M("SoftUtime");
			$su=$SoftUtime->where($data)->find();
			$data['utime']=intval($_POST['utime']);
			if(isset($su['id'])){
				$data['id']=$su['id'];
				$result=$SoftUtime->save($data);
			}else{
				$data['create_time']=get_date_time();
				$result=$SoftUtime->add($data);
			}
			if($result!==false){
				$this->ajaxReturn(0,"OK",1);
			}else{
				$this->ajaxReturn(0,"error",0);
			}
		}else{
			$this->ajaxReturn(0,"param error",0);
		}
	}
	
	/**
	 * 
	 * 局域网数据统计
	 * 软件启动后提交数据
	 */
	public function lan_record(){
		if(isset($_POST['pc'])&&intval($_POST['pc'])>0
		&&isset($_POST['qm'])&&intval($_POST['qm'])>0){
			$data['ip']=get_user_ip();
			$data['tongji_day']=get_date();
			$LanTongji=M("LanTongji");
			$lt=$LanTongji->where($data)->find();
			if(isset($lt['id'])){
				$data2=array();
				if(intval($_POST['pc'])>$lt['pc_num']){
					$data2['pc_num']=intval($_POST['pc']);
				}
				if(intval($_POST['qm'])>$lt['qm_num']){
					$data2['qm_num']=intval($_POST['qm']);
				}
				if(count($data2)>0){
					$data2['id']=$lt['id'];
					$result=$LanTongji->save($data2);
					if($result!==false){
						$this->ajaxReturn(0,"OK",1);
					}else{
						$this->ajaxReturn(0,"error",0);
					}
				}else{
					$this->ajaxReturn(0,"OK",1);
				}
			}else{
				$data['pc_num']=intval($_POST['pc']);
				$data['qm_num']=intval($_POST['qm']);
				$result=$LanTongji->add($data);
				if($result!==false){
					$this->ajaxReturn(0,"OK",1);
				}else{
					$this->ajaxReturn(0,"error",0);
				}
			}
		}else{
			$this->ajaxReturn(0,"param error",0);
		}
	}
	
	/**
	 * 
	 * 发布24小时内统计数据记录
	 */
	public function pub_record(){
		if(isset($_POST['email'])&&trim($_POST['email'])!=""&&isset($_POST['type'])&&intval($_POST['type'])>0
		&&isset($_POST['num'])&&intval($_POST['num'])>0){
			$obj=intval($_POST['type']);
			if($obj>5){
				$this->ajaxReturn(0,"type error",0);
			}
			$data['email']=strtolower(trim($_POST['email']));
			$User=M("User");
			$count=$User->where($data)->count();
			if($count==0){
				$this->ajaxReturn(0,"user not exists",0);
			}
			$data['tongji_time']=get_date_time();
			$data['obj']=$obj;
			$data['obj_val']=intval($_POST['num']);
			$PubRecord=M("PubRecord");
			$result=$PubRecord->add($data);
			if($result!==false){
				$this->ajaxReturn(0,"OK",1);
			}else{
				$this->ajaxReturn(0,"error",0);
			}
		}else{
			$this->ajaxReturn(0,"param error",0);
		}
	}
	
	/**
	 * 
	 * 每日统计注册24小时内注册信息
	 * 2013-02-07修改 只要是注册即可
	 */
	public function pub_tongji(){
		$ckey="";
		if(isset($_GET['ckey'])&&trim($_GET['ckey'])!=""){
			$ckey=trim($_GET['ckey']);
			$ckeyFile="/home/admin/php/pub_tongji_ckey.txt";
			if(file_exists($ckeyFile)){
				$fkey="";
				$fp=fopen($ckeyFile, "r");
				if($fp){
					$fkey=trim(fgets($fp));
				}else{
					echo 'open key error';
					fclose($fp);
					exit();
				}
				fclose($fp);
				if($fkey!=$ckey){
					echo 'key error';
					exit();
				}
			}else{
			  echo 'not find key ';
			  exit();
			}
		}else{
			echo "no key";
			exit();
		}
		$Model=new Model();
		$tjTime=get_date_time(-90000);//1天1小时
		$sql="select id,pub_time from kx_pub where is_tongji=0 and pub_time< '".$tjTime."'";
		//echo $sql;
		$pubList=$Model->query($sql);
		if(count($pubList)>0){
			for($i=0;$i<count($pubList);$i++){
				$pubTime=$pubList[$i]['pub_time'];
				$pid=$pubList[$i]['id'];
				$sql="insert into kx_pub_tongji (pub_id,reg_num) values (".$pid.", (select count(*) from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY)));";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set act_num=(select count(*) from kx_user where active_time >='".$pubTime."' and active_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) and status=1 ) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set un_num=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=5 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				$sql="update kx_pub_tongji set trans0=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=1 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set trans1=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=1 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num=1 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set trans2=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=1 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=2 and t.obj_num<=4 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set trans3=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=1 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=5 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				$sql="update kx_pub_tongji set print0=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=2 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set print1=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=2 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num=1 and  exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set print2=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=2 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=2 and t.obj_num<=4 and  exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set print3=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=2 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=5 and  exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				$sql="update kx_pub_tongji set chat0=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=3 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set chat1=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=3 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num=1 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set chat2=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=3 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=2 and t.obj_num<=4 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set chat3=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=3 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=5 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				//24小时新增的好友
				$sql="update kx_pub_tongji set friend0=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=4 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where  exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set friend1=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=4 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num=1 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set friend2=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=4 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=2 and t.obj_num<=4 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set friend3=(select count(*) from (select max(obj_val) as obj_num ,max(email) as act_email from kx_pub_record where obj=4 and tongji_time>='".$pubTime."' and tongji_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) group by email) t where t.obj_num>=5 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.act_email=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				//只算邀请未注册的
				$sql="update kx_pub_tongji set invite0=(select count(*) from (select max(user) as uemail from kx_mailing_addfriend where send_reason_type=0 and create_time>='".$pubTime."' and create_time < DATE_ADD('".$pubTime."',INTERVAL 1 DAY)  group by user) t where exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.uemail=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set invite1=(select count(*) from (select max(user) as uemail,count(*) as num from kx_mailing_addfriend where send_reason_type=0 and create_time>='".$pubTime."' and create_time < DATE_ADD('".$pubTime."',INTERVAL 1 DAY)  group by user) t where t.num=1 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.uemail=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set invite2=(select count(*) from (select max(user) as uemail,count(*) as num from kx_mailing_addfriend where send_reason_type=0 and create_time>='".$pubTime."' and create_time < DATE_ADD('".$pubTime."',INTERVAL 1 DAY)  group by user) t where t.num>=2 and t.num<=3 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.uemail=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set invite3=(select count(*) from (select max(user) as uemail,count(*) as num from kx_mailing_addfriend where send_reason_type=0 and create_time>='".$pubTime."' and create_time < DATE_ADD('".$pubTime."',INTERVAL 1 DAY)  group by user) t where t.num>=4 and t.num<=5 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.uemail=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				$sql="update kx_pub_tongji set invite4=(select count(*) from (select max(user) as uemail,count(*) as num from kx_mailing_addfriend where send_reason_type=0 and create_time>='".$pubTime."' and create_time < DATE_ADD('".$pubTime."',INTERVAL 1 DAY)  group by user) t where t.num>=6 and exists (select 1 from (select email from kx_user where create_time >='".$pubTime."' and create_time< DATE_ADD('".$pubTime."',INTERVAL 1 DAY) ) t2 where t.uemail=t2.email)) where pub_id=".$pid.";";
				$result=$Model->execute($sql);
				
				$sql="update kx_pub set is_tongji=1 where id=".$pid;
				$result=$Model->execute($sql);
			}
			
		}
		$ckeyFile="/home/admin/php/pub_tongji_ckey.txt";
		$fp=fopen($ckeyFile, "w");
		fwrite($fp, uniqid());
		fclose($fp);
		echo 'ok';
		
	}
	
	
	
	
	
//	public function initData(){
//		$TongjiRecord=M("TongjiRecord");
//		for($i=29;$i>=1;$i--){
//			
//			
//			$allNumSql="update kx_tongji_record set all_num=(select count(*) as num from (select max(client_identifie) as client_identifie,count(*) as login_num from kx_soft_record where is_uninstall=0 and date(login_time)=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) group by client_identifie)t) where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
////			$newNumSql="insert into kx_tongji_record (tongji_day,new_num,un_num,seven_new_num,seven_un_num)(select DATE_SUB(CURDATE(),INTERVAL ".$i." DAY),count(*),0,0,0 from ( select max(client_identifie) as client_mac,count(*) as login_num from kx_soft_record where is_new=1 and is_uninstall=0 and date(login_time)=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) group by client_identifie)t)";
////    		$unNumSql="update kx_tongji_record set un_num=(select count(*) as num from (select distinct client_identifie from kx_soft_record where is_uninstall=1 and date(login_time)=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)) t) where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
////     		$sevenNumSql="update kx_tongji_record r,(select sum(new_num) as sum_new_num,sum(un_num) as sum_un_num from kx_tongji_record where tongji_day<=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) and tongji_day>=DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY),INTERVAL 6 DAY) ) s set r.seven_new_num=s.sum_new_num,r.seven_un_num=s.sum_un_num where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
////			$TongjiRecord->execute($newNumSql);
////			print $TongjiRecord->getLastSql();
////			$TongjiRecord->execute($unNumSql);
//			$TongjiRecord->execute($allNumSql);
//			print $TongjiRecord->getLastSql();
//			print "<br />";
//			//print $TongjiRecord->getLastSql();
//			//$TongjiRecord->execute($sevenNumSql);
//			//print "<br />";
//			//print $TongjiRecord->getLastSql();
//			
//		}
//		echo "OK";	
//	}
	
	
//	public function initMonData(){
//		$TongjiRecord=M("TongjiRecord");
//		for($i=35;$i<=60;$i++){
//			
//			//$newNumSql="insert into kx_tongji_record (tongji_day,new_num,un_num,seven_new_num,seven_un_num)(select DATE_SUB(CURDATE(),INTERVAL ".$i." DAY),count(*),0,0,0 from ( select max(client_identifie) as client_mac,count(*) as login_num from kx_soft_record where is_new=1 and is_uninstall=0 and date(login_time)=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) group by client_identifie)t)";
//    		//$unNumSql="update kx_tongji_record set un_num=(select count(*) as num from (select distinct client_identifie from kx_soft_record where is_uninstall=1 and date(login_time)=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)) t) where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
//     		//$sevenNumSql="update kx_tongji_record r,(select sum(new_num) as sum_new_num,sum(un_num) as sum_un_num from kx_tongji_record where tongji_day<=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) and tongji_day>=DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY),INTERVAL 6 DAY) ) s set r.seven_new_num=s.sum_new_num,r.seven_un_num=s.sum_un_num where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
//			
//     		$curMonSql=" update kx_tongji_record set cur_mon_num=(select count(*) from (select max(client_identifie) as client_mac from kx_soft_record t where is_uninstall= 0 and login_time >= DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) ,INTERVAL 14 DAY) and login_time <DATE_SUB(CURDATE(),INTERVAL ".($i-1)." DAY)  group by client_identifie) t where exists (select 1 from (select max(client_identifie) as client_mac from kx_soft_record  where  is_uninstall=0 and login_time >=DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) ,INTERVAL 29 DAY) and login_time < DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) ,INTERVAL 14 DAY) group by client_identifie) t2 where t.client_mac=t2.client_mac )) where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
//
//			$lastMonSql="update kx_tongji_record set last_mon_num=(select count(*) from (select max(client_identifie) as client_mac from kx_soft_record  where  is_uninstall=0 and login_time >=DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) ,INTERVAL 29 DAY) and login_time < DATE_SUB(DATE_SUB(CURDATE(),INTERVAL ".$i." DAY) ,INTERVAL 14 DAY) group by client_identifie) t2)  where tongji_day=DATE_SUB(CURDATE(),INTERVAL ".$i." DAY)";
//     		
//     		
//     		$TongjiRecord->execute($lastMonSql);
//			print $TongjiRecord->getLastSql();
//			print "<br />";
//			$TongjiRecord->execute($curMonSql);
//			print "<br />";
//
//			
//		}
//		echo "OK";
//	}


	
//	public function recordForm(){
//		$ver="2.0.3";
//		$client="ASDDSTKJDKSJ";
//		$verify=md5($ver.$client."123456");
//		print $verify;
//		$this->display();
//	}

//	public function check(){
//		//$date=date("Y-m-d");
//		//$date= get_date_time(-3600*24*1);
//		$time=time();
//		$today=strftime("%Y-%m-%d", $time);
//		$SoftRecord=M("SoftRecord");
//		$i=0;
//		while (true){
//			$sql="select client_identifie from kx_soft_record where date(login_time)='".$today."' and client_identifie not in (select client_identifie from kx_soft_record where login_time<'".$today."')";
//			$list=$SoftRecord->query($sql);
//			//print_r($list);
//			//print implode(",", $list[0]['']);
//			for($j=0;$j<count($list);$j++){
//				$arr[$j]=$list[$j]['client_identifie'];
//			}
//			//print implode("','", $arr);
//			//print "<br />";
//			$sql="update kx_soft_record set is_new=1 where client_identifie in ('".implode("','", $arr)."') and date(login_time)='".$today."'";
//			$result=$SoftRecord->execute($sql);
//			print $SoftRecord->getLastSql();
//			if($result!==false){
//			
//			}else{
//				print $SoftRecord->getLastSql();
//				print "err0r";
//				break;
//			}
//			$i=$i+1;
//			$today=strftime("%Y-%m-%d", $time-3600*24*$i);
//			if($today=='2011-11-07')
//				break;
//		}
//		
//		print "ok";
//	}
	
	
}