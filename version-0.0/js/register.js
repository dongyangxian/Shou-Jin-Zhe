;(function(){
	$(function(){
		//设置开关，保存是否输入正确，作为表单可以提交的依据
		var oName = false
		var oPwd = false
		var cPwd = false
		var oEmail = false
		var oAll = true
		
		function serach(){
			if(oName == true && oPwd == true && cPwd == true && oEmail ==true && oAll == true){
				$('.reg_sub input').css({'background-color':'#6ac1f8'})
			}
		}
		

		//获取焦点
		$('#user_name').focus()  //用户名
		
		//用户名--失去焦点判断
		$('#user_name').keyup(function(){
			//正则表达式
			var reg1 = /^\w{6,20}$/
			
			if(!reg1.test($(this).val())){
				$(this).siblings('span').show().html('用户名是6到15个英文或数字，还可包含“_”')
				$('.reg_sub input').css({'background-color':'#999'})
			}else{
				$(this).siblings('span').hide()
				oName = true
				serach()
			}
			
		})
		
		//密码--失去焦点判断
		$('#pwd').keyup(function(){
			
			//正则表达式
			var reg1 = /^[\w!@#$%^&*]{6,20}$/
			
			if(!reg1.test($(this).val())){
				$(this).siblings('span').show().html('请输入6-20位的密码(可为字母、数字或下划线)!')
				$('.reg_sub input').css({'background-color':'#999'})
			}else{
				$(this).siblings('span').hide()
				oPwd = true
				serach()
			}
			
		})
		
		//确认密码--失去焦点判断
		$('#cpwd').keyup(function(){
			
			//正则表达式
			var reg1 = /^[\w!@#$%^&*]{6,20}$/
			
//			//先判断输入的内容是否满足条件
//			if(reg1.test($(this).val()) == 'false'){
//				$(this).siblings('span').show().html('确认密码输入有误！')
//			}else{
//				$(this).siblings('span').hide()
//				cPwd =true
//			}
//			

			//在判断是否和密码一致
			if($(this).val() == $('#pwd').val()){
				$(this).siblings('span').hide()
				cPwd = true
				serach()
				
			}else{
				$(this).siblings('span').show().html('密码不一致，请重新输入！')
				cPwd = false
				$('.reg_sub input').css({'background-color':'#999'})
			}
			
		})
		
		//邮箱--失去焦点判断
		$('#email').keyup(function(){
			
			//正则表达式
			var reg1 =  /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/
			
			if(!reg1.test($(this).val())){
				$(this).siblings('span').show().html('邮箱格式输入有误！')
				$('.reg_sub input').css({'background-color':'#999'})
			}else{
				$(this).siblings('span').hide()
				oEmail = true
				serach()
			}
			
		})
		
		
		//同意协议
		$('#allow').click(function(){
			if($(this).is(':checked')){
				$(this).siblings('span').hide()
				oAll = true
				serach()
			}else{
				$(this).siblings('span').show().html('请勾选协议！')
				$('.reg_sub input').css({'background-color':'#999'})
			}
			
		})
		
		$('form').submit(function(){
			
//			alert("用户名："+oName+"密码："+oPwd+"确认密码："+cPwd+"邮箱："+oEmail+"协议："+oAll)
			
			if(oName == true && oPwd == true && cPwd == true && oEmail ==true && oAll == true){
				
				alert('表单已提交！')
				return true
			}else{
				
				alert('表单信息输入有误，提交失败！')
				return false
			}
		})
		
		
		
	});
})()
