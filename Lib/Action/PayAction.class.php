<?php 

import("@.Util.Alipay.lib.alipay_service");
import("@.Util.Alipay.lib.alipay_notify");
class PayAction extends CommonAction{
	
	/**
	 * 
	 * 创建订单
	 */
	public function pay_order(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		$qianmoDot=0;//还需支付的点数 
		if(isset($_GET['qianmo_dot'])&&doubleval($_GET['qianmo_dot'])>=0.1){
			$qianmoDot=doubleval($_GET['qianmo_dot']);
			$payMoney=$qianmoDot/10.0;
			$this->assign("payMoney",$payMoney);
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	public function pay_to_ali(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		/**************************请求参数**************************/
		
		//必填参数//
		
		//请与贵网站订单系统中的唯一订单号匹配
		$out_trade_no = date('Ymdhis');
		//订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
		$subject      = $_POST['subject'];
		//订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
		$body         = $_POST['alibody'];
		//订单总金额，显示在支付宝收银台里的“应付总额”里
		$total_fee    = $_POST['total_fee'];
		
		$AlipayOrder=M("AlipayOrder");
		$data['order_id']=$out_trade_no;
		$data['title']=$subject;
		$data['pay_money']=$total_fee;
		$data['qianmo_dot']=$total_fee*100;
		$data['add_qianmo_dot']=0;
		$data['user_id']=get_user_id();
		$data['pay_status']=0;
		$data['create_time']=get_date_time();
		$result=$AlipayOrder->add($data);

		if($result===false){
			redirect(C("WWW")."/Pay/pay_order",1,"支付订单未能生产！");
		}
		
		//扩展功能参数——默认支付方式//
		
		//默认支付方式，取值见“即时到帐接口”技术文档中的请求参数列表
		$paymethod    = '';
		//默认网银代号，代号列表见“即时到帐接口”技术文档“附录”→“银行列表”
		$defaultbank  = 'ICBC';
		
		
		//扩展功能参数——防钓鱼//
		
		//防钓鱼时间戳
		$anti_phishing_key  = '';
		//获取客户端的IP地址，建议：编写获取客户端IP地址的程序
		$exter_invoke_ip = '';
		//注意：
		//1.请慎重选择是否开启防钓鱼功能
		//2.exter_invoke_ip、anti_phishing_key一旦被使用过，那么它们就会成为必填参数
		//3.开启防钓鱼功能后，服务器、本机电脑必须支持SSL，请配置好该环境。
		//示例：
		//$exter_invoke_ip = '202.1.1.1';
		//$ali_service_timestamp = new AlipayService($aliapy_config);
		//$anti_phishing_key = $ali_service_timestamp->query_timestamp();//获取防钓鱼时间戳函数
		
		
		//扩展功能参数——其他//
		
		//商品展示地址，要用 http://格式的完整路径，不允许加?id=123这类自定义参数
		$show_url			= C("WWW").'/Pay/doc';
		//自定义参数，可存放任何内容（除=、&等特殊字符外），不会显示在页面上
		$extra_common_param = '';
		
		//扩展功能参数——分润(若要使用，请按照注释要求的格式赋值)
		$royalty_type		= "";			//提成类型，该值为固定值：10，不需要修改
		$royalty_parameters	= "";
		//注意：
		//提成信息集，与需要结合商户网站自身情况动态获取每笔交易的各分润收款账号、各分润金额、各分润说明。最多只能设置10条
		//各分润金额的总和须小于等于total_fee
		//提成信息集格式为：收款方Email_1^金额1^备注1|收款方Email_2^金额2^备注2
		//示例：
		//royalty_type 		= "10"
		//royalty_parameters= "111@126.com^0.01^分润备注一|222@126.com^0.01^分润备注二"
		
		/************************************************************/
		$aliapy_config=C("ALI_CONFIG");
		//构造要请求的参数数组
		$parameter = array(
				"service"			=> "create_direct_pay_by_user",
				"payment_type"		=> "1",
				
				"partner"			=> trim($aliapy_config['partner']),
				"_input_charset"	=> trim(strtolower($aliapy_config['input_charset'])),
		        "seller_email"		=> trim($aliapy_config['seller_email']),
		        "return_url"		=> trim($aliapy_config['return_url']),
		        "notify_url"		=> trim($aliapy_config['notify_url']),
				
				"out_trade_no"		=> $out_trade_no,
				"subject"			=> $subject,
				"body"				=> $body,
				"total_fee"			=> $total_fee,
				
				"paymethod"			=> $paymethod,
				"defaultbank"		=> $defaultbank,
				
				"anti_phishing_key"	=> $anti_phishing_key,
				"exter_invoke_ip"	=> $exter_invoke_ip,
				
				"show_url"			=> $show_url,
				"extra_common_param"=> $extra_common_param,
				
				"royalty_type"		=> $royalty_type,
				"royalty_parameters"=> $royalty_parameters
		);
		
		//构造即时到帐接口
		$alipayService = new AlipayService($aliapy_config);
		$html_text = $alipayService->create_direct_pay_by_user($parameter);
		echo $html_text;
				
	
	}
	
	public function return_url(){
		//计算得出通知验证结果
		$aliapy_config=C("ALI_CONFIG");
		$alipayNotify = new AlipayNotify($aliapy_config);
		$verify_result = $alipayNotify->verifyReturn();
		if($verify_result) {//验证成功
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			//请在这里加上商户的业务逻辑程序代码
			
			//——请根据您的业务逻辑来编写程序（以下代码仅作参考）——
		    //获取支付宝的通知返回参数，可参考技术文档中页面跳转同步通知参数列表
		    $out_trade_no	= $_GET['out_trade_no'];	//获取订单号
		    $trade_no		= $_GET['trade_no'];		//获取支付宝交易号
		    $total_fee		= $_GET['total_fee'];		//获取总价格
		
		    if($_GET['trade_status'] == 'TRADE_FINISHED' || $_GET['trade_status'] == 'TRADE_SUCCESS') {
				//判断该笔订单是否在商户网站中已经做过处理
					//如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
					//如果有做过处理，不执行商户的业务程序
				 $status=$this->deal_with_order($out_trade_no, $trade_no);
				 echo "STATUS-".$status;
		    }else {
		      echo "trade_status=".$_GET['trade_status'];
		    }
				
			echo "验证成功<br />";
			echo "trade_no=".$trade_no;
			
			//——请根据您的业务逻辑来编写程序（以上代码仅作参考）——
			
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		}
		else {
		    //验证失败
		    //如要调试，请看alipay_notify.php页面的verifyReturn函数，比对sign和mysign的值是否相等，或者检查$responseTxt有没有返回true
		    echo "验证失败";
		}
	}
	
	/**
	 * 
	 * 异步处理支付结果
	 */
	public function notify_url(){
		//计算得出通知验证结果
		$aliapy_config=C("ALI_CONFIG");
		$alipayNotify = new AlipayNotify($aliapy_config);
		$verify_result = $alipayNotify->verifyNotify();
		
		if($verify_result) {//验证成功
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			//请在这里加上商户的业务逻辑程序代
			
			//——请根据您的业务逻辑来编写程序（以下代码仅作参考）——
		    //获取支付宝的通知返回参数，可参考技术文档中服务器异步通知参数列表
		    $out_trade_no	= $_POST['out_trade_no'];	    //获取订单号
		    $trade_no		= $_POST['trade_no'];	    	//获取支付宝交易号
		    $total_fee		= $_POST['total_fee'];			//获取总价格
			$status=0;
		    if($_POST['trade_status'] == 'TRADE_FINISHED') {
				//判断该笔订单是否在商户网站中已经做过处理
					//如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
					//如果有做过处理，不执行商户的业务程序
						
				//注意：
				//该种交易状态只在两种情况下出现
				//1、开通了普通即时到账，买家付款成功后。
				//2、开通了高级即时到账，从该笔交易成功时间算起，过了签约时的可退款时限（如：三个月以内可退款、一年以内可退款等）后。
		
		        //调试用，写文本函数记录程序运行情况是否正常
		        //logResult("这里写入想要调试的代码变量值，或其他运行的结果记录");
		       $status=$this->deal_with_order($out_trade_no, $trade_no);
		    }
		    else if ($_POST['trade_status'] == 'TRADE_SUCCESS') {
				//判断该笔订单是否在商户网站中已经做过处理
					//如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
					//如果有做过处理，不执行商户的业务程序
						
				//注意：
				//该种交易状态只在一种情况下出现——开通了高级即时到账，买家付款成功后。
		
		        //调试用，写文本函数记录程序运行情况是否正常
		        //logResult("这里写入想要调试的代码变量值，或其他运行的结果记录");
		        $status=$this->deal_with_order($out_trade_no, $trade_no);
		    }
		
			//——请根据您的业务逻辑来编写程序（以上代码仅作参考）——
		    $returnType=0;
		    switch ($status){
		    	case 1:;
		    	case 2:$returnType=1;break;
		    	default:;
		    }  
		    if($returnType==1){  
				echo "success";		//请不要修改或删除
		    }else{
		    	echo "fail";
		    }
			/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		}
		else {
		    //验证失败
		    echo "fail";
		
		    //调试用，写文本函数记录程序运行情况是否正常
		    //logResult("这里写入想要调试的代码变量值，或其他运行的结果记录");
		}
	}
	
	/**
	 * 
	 * 阡陌支付说明
	 */
	public function doc(){
		
	}
	
	public function trade_list(){
		if(!isLogin()){
			redirect(C("WWW")."/User/login");
		}
		$AlipayOrder=M("AlipayOrder");
		$condition="pay_status=1";
		if(!isRoot()){
			$condition.=" and user_id=".get_user_id();
		}
		$p=1;
		if(isset($_GET['p'])&&intval($_GET['p'])>0){
			$p=intval($_GET['p']);
		}
		$count=$AlipayOrder->where($condition)->count();
		if($count>0){
			$tList=$AlipayOrder->where($condition)->order("order_id desc")->page($p.",".PAGE_NUM_DEFAULT)->select();
			$this->assign("tList",$tList);
			$Page=new Page($count, PAGE_NUM_DEFAULT);
			$page=$Page->show();
			$this->assign("page",$page);
			if(isRoot()){
				$uids=array();
				for($i=0;$i<count($tList);$i++){
					$uids[$i]=$tList[$i]['user_id'];
				}
				if(count($uids)>0){
					$uidsStr=implode(",", array_unique($uids));
					$User=M("User");
					$uList=$User->where("id in (".$uidsStr.")")->getField("id,nick");
					$this->assign("uList",$uList);
				}
			}
		}
		$this->display(DEFAULT_DISPLAY);
	}
	
	private function deal_with_order($orderId,$tradeNo){
		$status=0;//订单处理状态
		$AlipayOrder=M("AlipayOrder");
		$data['order_id']=$orderId;
		$order=$AlipayOrder->where($data)->find();
		if(isset($order['order_id'])){
			if($order['pay_status']==1){
				$status=2;//订单已处理
			}else{
				$data['pay_status']=1;
				$data['finish_time']=get_date_time();
				$data['trade_no']=$tradeNo;
				$AlipayOrder->startTrans();
				$result=$AlipayOrder->save($data);
				if($result!==false){
					$data=array();
					$User=M("User");
					$addDot=$order['qianmo_dot']+$order['add_qianmo_dot'];
					$sql="update kx_user set qianmo_dot=qianmo_dot+".$addDot." where id=".$order['user_id'];
					$result=$User->execute($sql);
					if($result===false){
						$status=3;//订单在增加用户阡陌点的时候处理失败
						$AlipayOrder->rollback();
					}else{
						$status=1;//订单处里成功
						$AlipayOrder->commit();
					}
				}else{
					$AlipayOrder->rollback();
					$status=4;//订单自身更新的时候处理失败
				}
			}
		}else{
			$status=-1;//订单不存在
		}
		return $status;
	}
}