var loginform=$('#login-form');

function Login() {
    if($("#username").val()===""||$("#password").val()===""){
        err("请将用户名密码填写完整");
        return;
    }
    var next_url=window.location.search.substring(6);
    if(next_url==="")next_url='/dashboard/';
    $.ajax({
        url: '/account/login/',
        method: 'POST',
        data: loginform.serialize(),
        success: function (data) {
            if (data.code === 'success') {
                location.href = next_url;
            } else {
                var msg="";
                for(var p in data.errors)
                    msg+=p+": " +data.errors[p];
                err(msg);
            }
        },
        error: function (e) {
            err("Something wrong");
        }
    });
}
function SignUp() {
    if($("#username").val()===""||$("#password").val()===""){
        err("请将用户名密码填写完整");
        return;
    }
    $.ajax({
        url: '/account/signup/',
        method: 'POST',
        data: loginform.serialize(),
        success: function (data) {
           if (data.code === 'success') {
                alert(data.info);
            } else {
                var msg="";
                for(var p in data.errors)
                    msg+=p+": " +data.errors[p];
                err(msg);
            }
        },
        error: function (e) {
            err("Something wrong");
        }
    });
}

function ckAll(now) {
    var all = document.getElementsByName("ckUser");
    for (var i = 0; i < all.length; ++i)
        all[i].checked = now;
}

function rmUser(now) {
    var id_1=$(now).data('id');
    $.ajax({
        url: '/dashboard/delete/'+id_1+'/',
        method: 'POST',
        data: {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},

        success: function (data) {
           if(data.code === 'success')
               now.parentNode.removeChild(now);
           else {
               var msg = "";
               for (var p in data.errors)
                   msg += p + ": " + data.errors[p];
               err(msg);
           }
        }
    });

}

var rmBtn = document.getElementsByClassName("deleteOne");
for (var i = 0; i < rmBtn.length; ++i) {
    rmBtn[i].onclick = function() {
        if(confirm("真的删除吗？此操作不可撤销")) {
            rmUser(this.parentNode.parentNode);
        }
    }
}


function removeSelectUser() {
    var all = document.getElementsByName("ckUser");
    var sz = all.length;
    if(confirm("真的删除所有选中的吗？此操作不可撤销")) {
        for (var i = sz - 1; i >= 0; --i) {
            if (all[i].checked)
                rmUser(all[i].parentNode.parentNode);
        }
    }
}

function verify(name,tel,mail,qq){
    if(name===""||tel==="") {
        err("姓名、电话必填");
        return;
    }
    var regMobile = /^1(3|4|5|7|8)\d{9}$/;
    var regTel = /^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$/;
    if (tel && (!regMobile.test(tel) && !regTel.test(tel))) {
        err("请检查电话是否为固定电话或手机号！");
        return false;
    }
    var regQq = /^[1-9][0-9]{4,}$/;
    if (qq && !regQq.test(qq)) {
        err("QQ 号码不正确");
        return false;
    }
    var regMail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (mail && !regMail.test(mail)){
        err("请输入正确的邮箱");
        return false;
    }
    return true;
}

var userform=$("#user-form");
function editRecord(id) {
    var id_1 = "";
    if(id) id_1=id+'/';
    if(verify($("#name").val(),$("#phone").val(),$("#email").val(),$("#qq").val())){
        $.ajax({
            url: '/dashboard/edit/'+id_1,
            method: 'POST',
            data: userform.serialize(),
            success: function (data) {
                if(data.code === "success"){
                    alert(data.info);
                    location.href="/dashboard/";
                }
                else{
                    var msg="";
                    for(var p in data.errors)
                        msg+=p+": " +data.errors[p];
                    err(msg);
                }
            },
            error: function (e) {
                alert("Something wrong");
            }
        });
    }
}

function err(msg) {
    var node=$('.err');
    if(node){
        node.html(msg);
    }else {
        alert(msg);
    }
}