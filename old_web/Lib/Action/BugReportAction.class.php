<?php
/**
 * BUG 日志上传
 */
class BugReportAction extends CommonAction{
	
	/**
	 * 
	 * 上传日志
	 */
	public function upload(){
	//	$bin =  file_get_contents ( 'php://input' ) ? file_get_contents ( 'php://input' ) :gzuncompress ( $GLOBALS ['HTTP_RAW_POST_DATA'] ); 
//		$str="就就kdj三看电视";
//		$bin=$this->bstr2bin($str);
//		print $bin;
		$status=0;
		$desc="upload failed";
		if(count($_FILES)>0){
			$file=saveFile("BugReport");
			if($file!==false){
				$status=1;
				$desc="upload success";
			}
		}
		
		$this->returnList($status, $desc);
	} 
	
	public function uploadForm(){
		$this->display();
	}
	
	
	public function upload_bug(){
		$status=0;
		$desc="upload failed";
		if(isset($_POST['mac'])&&trim($_POST['mac'])!=""){
			$type=array('dmp');
			$mac=trim($_POST['mac']);
			$macFile=(str_replace(":", "_", $mac)).".dmp";
			$file=saveFile(false,0,0,"BugReport",$type);
			if($file!==false){
				$fileInfo=$file[0]['saveContent'];
				$filePath=C("UPLOAD_PATH")."/".getPicUri($fileInfo);
				$fileName=getPicName($fileInfo);
				$i=1;
				$newMacFile=$macFile;
				while (true){
					if(!file_exists($filePath."/".$newMacFile)){
						break;
					}else{
						$newMacFile=$macFile."_".$i;
						$i++;
					}
				}
				
				$result=rename($filePath."/".$fileName, $filePath."/".$newMacFile);
				if($result!==false){
					$status=1;
					$desc="upload success";
				}else{
					$desc="upload failed, rename error";
				}
			}
		}else{
			$desc="upload failed, need mac";
		}
		$this->returnList($status, $desc);
	}
	
	
	
	
	/**
	 * 
	 * 上传软件BUG信息
	 */
	public function soft_bug(){
		$status=0;
		$desc="error parameters";
		if(isset($_POST['ver'])&&isset($_POST['clientIdentifie'])&&isset($_POST['code'])
			&&isset($_POST['os'])&&isset($_POST['autoStart'])&&isset($_POST['lanNum'])&&isset($_POST['email'])){
			$ver=trim($_POST['ver']);
			$client=trim($_POST['clientIdentifie']);
			$md5str=trim($_POST['code']);
			$verify=md5($ver.$client."123456");
			if($verify===$md5str){
				$data['client_identifie']=$client;
				$data['version']=$ver;
				$data['os']=trim($_POST['os']);
				$data['upload_time']=get_date_time();
				$data['auto_start']=intval($_POST['autoStart']);
				$data['lan_num']=intval($_POST['lanNum']);
				if(trim($_POST['email'])!=""){
					$data['u_email']=trim($_POST['email']);
				}
				$SoftBug=M("SoftBug");
				$result=$SoftBug->add($data);
				if($result!==false){
					$status=1;
					$desc="OK";
				}else{
					$desc="save data error";
				}
			}else{
				$desc="check error";
			}
		}
		$this->returnList($status, $desc);
	}
	
	
	/**
	 * 
	 * 上传BUG日志
	 */
	public function bug_log(){
		$status=0;
		$desc="error parameters";
		if(isset($_POST['clientIdentifie'])&&isset($_POST['log'])){
			$date2 = date ( "Y-m-d" );
			$logPath=C ( 'UPLOAD_PATH' )."/BugLog";
			$fp=fopen($logPath."/soft_bug_".$date2.".log", "a+");
			$mac=trim($_POST['clientIdentifie']);
			$log=$mac." 	START*****************\n";
			$log.=trim($_POST['log'])."\n";
			$log.=$mac." 	END*****************\n";
			fwrite($fp,$log);
			fclose($fp);
			$status=1;
			$desc="OK";
		}
		$this->returnList($status, $desc);
	}
	
	
}