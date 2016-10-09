$(function(){
    // 给 window 对象绑定 scroll 事件
    $(window).bind("scroll", function(){

        var scrollTopNum = $(document).scrollTop(), // 获取网页文档对象滚动条的垂直偏移
            winHeight = $(window).height(), // 获取浏览器当前窗口的高度
            returnTop = $("div.returnTop");

        // 滚动条的垂直偏移大于 0 时显示，反之隐藏
        (scrollTopNum > winHeight*2.5 ) ? returnTop.fadeIn("fast") : returnTop.fadeOut("fast");

        // 给 IE6 定位
        if (!-[1,]&&!window.XMLHttpRequest) {
            returnTop.css("top", scrollTopNum + winHeight - 200);    
        } 

    });

    // 点击按钮后，滚动条的垂直方向的值逐渐变为0，也就是滑动向上的效果
    $("div.returnTop").click(function() {
        $("html, body").animate({ scrollTop: 0 }, 100);
    });
    
});

$.fn.anchorGoWhere = function(options){
    var obj = jQuery(this);
    var defaults = {target:1, timer:1000};
    var o = jQuery.extend(defaults,options);
    obj.each(function(i){
        jQuery(obj[i]).click(function(){
            var _rel = jQuery(this).attr("href").substr(1);
            switch(o.target){
                case 1: 
                    var targetTop = jQuery("#"+_rel).offset().top;
                    jQuery("html,body").animate({scrollTop:targetTop}, o.timer);
                    break;
                case 2:
                    var targetLeft = jQuery("#"+_rel).offset().left;
                    jQuery("html,body").animate({scrollLeft:targetLeft}, o.timer);
                    break;
            }
            return false;
        });
    });
};



// $(document).ready(function(){
//    $(".blog_title").toggle(function(){
//      $(this).next(".blog_time").next(".blog_text").animate({height: 'toggle', opacity: 'toggle'}, "slow");
//    },function(){
//      $(this).next(".blog_time").next(".blog_text").animate({height: 'toggle', opacity: 'toggle'}, "slow");
//    });
// });

// $(function(){
//  $(".menu_guide").css({"color":"#000000"});
// });
// function showSend(id){
//  if(id!=null&&id>0){
//      $(".blog_send_"+id).show();
//  }
// }
// function showComment(id){
//  if(id!=null&&id>0){
//      $(".comment_"+id).load("/blog/c_list?id="+id);
//  }
// }

// function sendComment(id){
//  if(id!=null&&id>0){
//      var msg=$(".blog_send_"+id+" textarea").val();
//      msg=$.trim(msg);
//      if(msg==""){
//          alert("请填写评论内容！");
//      }
//      $.post("/blog/add_comment/",{"id":id,"msg":msg},function(data){
//              if(data.status==0){
//                  alert("评论失败，请重试");
//              }else{
//                  $(".comment_"+id+" ul").prepend(data.data);
//                  $(".blog_send_"+id+" textarea").val("");
//                  $(".blog_send_"+id).hide();
                    
//              }
//          },"json");
//  }else{
//      alert("参数有误！");
//  }
// }
// $(".btn_cancel").click(function(){
//  $(this).parent().parent().hide();
// });
$(function(){
    $("#top_comment").click(function(){
        $(this).hide();
        $("#msg_content").css({"height":"91px","border-bottom":"1px solid #c8c8c8"});
        $(".send_btn_top").fadeIn("fast");
        $("#msg_content")[0].focus();
    });
    
    $("#msg_content").focus(function(){
        $("#top_comment").hide();
        $(this).prev("textarea").css({"height":"91px","border-bottom":"1px solid #c8c8c8"});
        $(".send_btn_top").fadeIn("fast");
    });
    
    $(".btn_cancel_top").click(function(){
        $("#msg_content").val("");
        $("#top_comment").show();
        $("#msg_content").css({"height":"33px","border-bottom":"1px solid #b5dbe8"});
        $(".send_btn_top").fadeOut("fast");
        
    });
    
    $("#scroll_comment").click(function(){
        $(this).hide();
        $("#msg_content3").css({"height":"91px","border-bottom":"1px solid #c8c8c8"});
        $(".send_btn_scroll").fadeIn("fast");
        $("#msg_content3")[0].focus();
    });
    
    $("#msg_content3").focus(function(){
        $("#scroll_comment").hide();
        $(this).prev("textarea").css({"height":"91px","border-bottom":"1px solid #c8c8c8"});
        $(".send_btn_scroll").fadeIn("fast");
    });
    
    $(".btn_cancel_scroll").click(function(){
        $("#msg_content3").val("");
        $("#scroll_comment").show();
        $("#msg_content3").css({"height":"33px","border-bottom":"1px solid #b5dbe8"});
        $(".send_btn_scroll").fadeOut("fast");
        
    });
});


    function checkMsg(){
        var msg=$("#msg_content").val();
        msg=$.trim(msg);
        $.ajax({type:"post",url:"/MsgBoard/check_msg",async:false,dataType:"json",
            success:function(data){document.getElementById('form1').value =data.id;}});
        if(msg=="")
            return false;
        return true;
    }

    function checkMsg2(){
        var msg=$("#msg_content2").val();
        msg=$.trim(msg);
        $.ajax({ type:"post",url:"/MsgBoard/check_msg",async:false,dataType:"json",
            success:function(data){document.getElementById('form2').value =data.id;}});
        if(msg=="")
            return false;
        return true;
    }

    function checkMsg3(){
        var msg=$.trim($("#msg_content3").val());
        if(msg=="")
        $.ajax({type:"post",url: "/MsgBoard/check_msg",async:false,dataType:"json",
            success:function(data){document.getElementById('form3').value =data.id;}});
            return false;
        return true;
    }
    function replyMsg(mid){
        if(mid>0){
            $("#msg_form").hide();
            $("#reply_msg").val(mid);
            var reply_u=$("#user_"+mid).html();
            $("#reply_u").html("回复“"+reply_u+"”：");
            var _reply=$("#user_"+mid).parent(".board_user").parent(".board_area").parent("li");
            var _left=_reply.offset().left; //左绝对距离 
            var _top=_reply.offset().top+_reply.outerHeight(); //上绝对距离,此处要加上div的高度 
            $(".reply_form").css({'position':'absolute','left':_left+'px','top':_top+'px'});
            $(".reply_form").show(); 
        }
    
    }
    function replyClose(){
        $(".reply_form").hide(); 
    }

    function delMsg(mid){
        if(mid>0){
            if(confirm("确定要删除此留言吗？")){
                $.post("/MsgBoard/del_msg",{"id":mid},function(data){
                    if(data.status==1){
                        $("#msg_id_"+mid).remove();
                    }else{
                        alert("删除留言失败！");
                    }
                },"json");
            }

        }
    }

    function vote_up(pid){
        if(pid>0){
            $.post("/forums/vote",{"id":pid,"v":0},function(data){
                if(data.status==1){
                    var v = $("#vote_"+pid).text();
                    $("#vote_"+pid).text(parseInt(v)+1);
                        alert("投票成功！");
                    }else{
                        alert("投票失败！");
                    }
            },"json");
        }
    }
    function vote_down(pid){
        if(pid>0){
            $.post("/forums/vote",{"id":pid,"v":1},function(data){
                if(data.status==1){
                    var v = $("#vote_"+pid).text();
                    $("#vote_"+pid).text(v-1);
                        alert("投票成功！");
                }else{
                        alert("投票失败！");
                }
            },"json");
        }
    }

//邮件自动完成提示插件
var mailArr=new Array("@qq.com","@sina.com","@163.com","@126.com","@sohu.com", "@gmail.com","@hotmail.com","@msn.com");
(function(){
    $.fn.mailAutoTip = function(options){
        var setting = {
            subBox:"#MailAutoTip",/*提示框ID*/
            subOp:"li",/*options*/
            id:"#email",/*文本框ID*/
            mailArr:mailArr,//数组对象
            hoverClass:"on",/*选中效果*/
            _cur:0 /*当前的index*/
        };
        var opts = $.extend({}, setting, options || {});
       
        //tipFun函数
        var tipFun = function(_v,o){
            opts._cur=0;
            var _that=o;
            $(opts.subBox).show();
            var str="<ul>";
            str += "<li id=\"e_type\">&nbsp;请选择邮箱类型:</li>";
            var e=_v.indexOf("@");
            if(e==-1){
                $.each(opts.mailArr,function(s,m){
                    str+='<li><a href="javascript:void(0)"  >' + _v + m + "</a></li>";                          
                });
            }else{
                var _sh=_v.substring(0,e)
                var _se=_v.substring(e);
                var ind = 0;
                $.each(opts.mailArr, function (s,m) {
                    if(m.indexOf(_se)!=-1){
                        str += '<li><a href="javascript:void(0)" >' + _sh + m + "</a></li>";
                        ind = 1;
                    }
                });
                if(ind==0){
                    str += '<li><a class="cur_val" href="javascript:void(0)" >' + _v + "</a></li>";
                }
            }
            str+="</ul>";
            $(opts.subBox).html(str); 

            /*绑定hover事件*/
            $(opts.subBox).find(opts.subOp).hover(function(){
                var _that=$(this);
                _that.addClass(opts.hoverClass);                       
            },function(){
                var _that=$(this);
                _that.removeClass(opts.hoverClass)          
            });
            /*绑定click事件*/
            $(opts.subBox).find(opts.subOp).each(function(){
                $(this).click(function(e){
                    if($(e.target).attr("id")!="e_type"){
                        $(opts.id).val($(e.target).html());
                        $(opts.subBox).hide();
                        e.stopPropagation();
                    }
                });                                           
            })
        };

        /*itemFun*/
        var itemFun = function(){
            var _tempArr=$(opts.subBox).find(opts.subOp);
            var _size=_tempArr.size();
            for(var i=0;i<_size;i++){
                _tempArr.eq(i).removeClass(opts.hoverClass);
            }
            
            if(_size>1){
                if(opts._cur>_size-1){
                    opts._cur=1;    
                }
                if(opts._cur<1){
                    opts._cur=_size-1;  
                }
                _tempArr.eq(opts._cur).addClass(opts.hoverClass);
            }else{
                opts._cur=1;    
            }
        };

        $(opts.id).keyup(function(e){
            var _that=$(this);
            if(_that.val()!=""){
                if(e.keyCode!=38 && e.keyCode!=40 && e.keyCode!=13 && e.keyCode!=27){
                    var _inputVal=_that.val();
                    tipFun(_inputVal,_that);
                }
            }else{
                $(opts.subBox).hide();
            }
        });

        /*点击页面其他地方关闭提示层*/
        $(document).bind("click",function(e){
            $(opts.subBox).hide();
        });
        
        $(document).keydown(function(e){
            switch(e.keyCode){
                case 40://下键
                    opts._cur++;
                    itemFun()
                    break;
                case 38://上键
                    opts._cur--;
                    itemFun()
                    break;
                default:
                   break;
            }
        })
        /*文本框keydown*/
        $(opts.id).keydown(function(e){
            var _temp = $(opts.subBox).find(opts.subOp);
            if(e.keyCode == 13){
                if(opts._cur!=0){
                    $(this).val(_temp.eq(opts._cur).text());
                    opts._cur = 0;
                }
                $(opts.subBox).hide();
                e.stopPropagation();
            }                             
        });

    }     
})(jQuery);