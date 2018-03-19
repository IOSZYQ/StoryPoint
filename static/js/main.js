function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCSRFToken() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function selectAll() {
    var checkbox1=document.getElementById("selectAllItem");
    if(checkbox1.checked==true )
    {
        checkAllBox(true);
    }
    else
    {
        checkAllBox(false);
    }
}
function checkAllBox(boolValue)
{
    var allcheck=document.getElementsByName("friendId");
    for(var i=0;i<allcheck.length;i++)
        if(allcheck[i].type=="checkbox")
            allcheck[i].checked=boolValue;
}


function forgot() {

    setCSRFToken();

    $.ajax({
        type: 'POST',
        url: '/forget/',
        dataType: 'json',
        data: {
            email: $("#forgotEmail").val()
        },
        success: function (data) {
            if (data.status == 0) {
                $('.forgot-password-modal').modal('toggle')
                $('.forgot-password-finish-modal').modal('show')
            }
            else {
                alert(data.msg)
            }
        }
    });
}

function modifyPassword() {

    setCSRFToken();

    $.ajax({
        type: 'POST',
        url: '/modify_pwd/',
        dataType: 'json',
        data: {
            oldpassword: $("#oldpassword").val(),
            password1: $("#password1").val(),
            password2: $("#password2").val(),
        },
        success: function (data) {
            if (data.status == 0) {
                $('.forgot-modify-password-modal').modal('toggle')
            }
            else {
                alert(data.msg)
            }
        }
    });
}

function editeProject() {
    setCSRFToken()

    $.ajax({
        type: 'POST',
        url: '/project/edit/',
        dataType: 'json',
        data:{
            name:$("#projectName").val(),
            manager:$("#projectPm").val(),
            start_time:$("#projectDateFrom").val(),
            end_time:$("#projectDateTo").val(),
            status:$("#projectStatus").val(),
            project_id:$("#project_id").val(),
        },
        success:function (data) {
            if (data.status == 0) {
                // $('.edit-project-modal').modal('toggle')
                window.parent.location.reload()
            }
            else {
                alert(data.msg)
            }
        }
    })
}

function editeProjectInfo() {
    setCSRFToken()

    $.ajax({
        type: 'POST',
        url: '/project/edit_detail/',
        dataType: 'json',
        data:{
            project_id:$(".edit_project_id").val(),
            weight:$("#performanceWeight").val(),
            sp:$("#projectStandardSP").val(),
            impression:$("#ProjectEffectiveness").val(),
            executing:$("#ExecutionTime").val(),
            acceptance:$("#AcceptanceTime").val(),
            acceptance_serious_bug:$("#SeriousDefect").val(),
            acceptance_medium_bug:$("#IntermediateDeficiency").val(),
            acceptance_slight_bug:$("#LowLevelDefects").val(),
            release_serious_bug:$("#SeriousDefect2").val(),
            release_medium_bug:$("#IntermediateDeficiency2").val(),
            release_slight_bug:$("#LowLevelDefects2").val(),
        },
        success:function (data) {
            if (data.status == 0) {
                window.parent.location.reload()
            }
            else {
                alert(data.msg)
            }
        }
    })
}

function addTask(id) {
    setCSRFToken()

    $.ajax({
        type: 'POST',
        url: '/project/task/add/',
        dataType: 'json',
        data:{
            projectId:id,
            status:$("#taskStatus").val(),
            group:$("#taskGroup").val(),
            description:$("#taskDescription").val(),
        },
        success:function (data) {
            if (data.status == 0) {
                window.parent.location.reload()
            }
            else {
                alert(data.msg)
            }
        }
    })
}

function deleteProject() {
    var r = confirm("是否删除项目，所有信息清空？")
    if (r === true) {
    }
    else {
    }
}

function deleteAllocTeam() {
    var r = confirm("是否删除分配小组？")
    if (r === true) {
    }
    else {
    }
}


function getTask(_this) {

    setCSRFToken()
    console.log($(_this).attr('data-taskid'))
    $.ajax({
            url:'/project/gettask/',
            type:'post',
            dataType:'json',
            data:{task_id:$(_this).attr('data-taskid')},
            success:function (res) {
                console.log(res);
            }
        })
}

function addAndEditTeam(id) {
    setCSRFToken()
    $.ajax({
        type:'POST',
        url:'/group/add/',
        dataType: 'json',
        data:{
            teamId:id,
            teamName:$("#teamName").val(),
        },
        success:function (data) {
            if (data.status == 0) {
                window.parent.location.reload()
            }
            else {
                alert(data.msg)
            }
        }
    })
}

function deleteTeam() {
    var r = confirm("是否删除小组，包括删除所有成员？")
    if (r === true) {
    }
    else {
    }
}

function deletePerson() {
    var r = confirm("是否删除成员？")
    if (r === true) {
    }
    else {
    }
}
