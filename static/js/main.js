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
    var checkbox1=document.getElementById("selectAllmember");
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
    var allcheck=document.getElementsByName("chkMember");
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

function editeProject(project_id) {
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
            project_id:project_id,
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

function deleteProject(id) {
    var r = confirm("是否删除项目，所有信息清空？")
    if (r === true) {
        setCSRFToken()

    $.ajax({
        type: 'POST',
        url: '/project/delete/',
        dataType: 'json',
        data:{
            id:id,
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


function getTask(id) {

    setCSRFToken()

    $.ajax({
            url:'/project/gettask/' + id,
            type:'get',
            dataType:'json',
            success:function (res) {

                // console.log(res);

                var div = document.getElementById("modal-body");
                while(div.hasChildNodes()) {
                    div.removeChild(div.firstChild);
                }

                var dialogString =
                    '<form class="form-horizontal">' +
                        '<div class="form-group">' +
                            '<label for="projectStandardSP2" class="col-md-3 control-label">项目标准 GSP：</label>' +
                            '<div class="col-sm-3">' +
                                '<input class="form-control" id="projectStandardSP2" name="projectStandardSP2" value=' + res.gsp + '>' +
                            '</div>' +
                        '</div>' +
                        '<input type="hidden" id="taskid" name="taskid" value=' + res.id + '>' +
                        '<div class="form-group">' +
                            '<label for="projectStandardSP2" class="col-md-3 control-label">项目成员</label>' +
                        '</div>' +
                        '<div class="form-group">' +
                            '<div class="col-sm-1"></div>' +
                            '<div class="col-sm-3">' +
                                '<div class="checkbox">' +
                                    '<label>' +
                                        '<input type="checkbox" onClick="javascript:selectAll()" id="selectAllmember"> 全部添加' +
                                    '</label>' +
                                '</div>' +
                            '</div>' +
                        '</div>';

                res.members.forEach(function (member, row) {
                    var check = member.contain ? 'checked' : '';
                    var memberContent =[
                        '<div class="form-group memberContainer" name="memberContainer">' +
                            '<div class="col-sm-1"></div>' +
                                '<div class="col-sm-3">' +
                                    '<div class="checkbox">' +
                                        '<label>' +
                                            '<input type="checkbox" name="chkMember"' + check +  '>' + member.username +
                                        '</label>' +
                                    '</div>' +
                                '</div>' +
                                '<input type="hidden" name="userId" value=' + member.userid + '>' +
                                '<label for="PSP" class="col-md-3 control-label">PSP：</label>' +
                                '<div class="col-sm-3">' +
                                    '<input class="form-control" name="input_psp" value=' + member.psp + '>' +
                                '</div>' +
                            '</div>' +
                        '</div>'
                    ].join(' ');
                    dialogString += memberContent;
                });

                dialogString +=
                        '<div class="form-group">' +
                            '<div class="col-sm-6">' +
                                '<a class="btn btn-sm btn-primary btn-block" href="javascript:postTask()">确定</a>' +
                            '</div>' +
                            '<div class="col-sm-6">' +
                                '<a class="btn btn-sm btn-primary btn-block" data-dismiss="modal">取消</a>' +
                            '</div>' +
                        '</div>' +
                    '</form>';

                $('#modal-body').append(dialogString);

                $('.input-team-modal').modal('show')
            }
        })
}

function postTask() {

    setCSRFToken()

    var joined = [];
    var memberContainer = document.getElementsByName('memberContainer');
    for(var i=0;i<memberContainer.length;i++){
        var inputs = memberContainer[i].getElementsByTagName("input");
        joined.push({
            contain: inputs.chkMember.checked,
            id: inputs.userId.value,
            psp: inputs.input_psp.value
        });
    }

    // console.log(JSON.stringify(joined))

    $.ajax({
        type:'POST',
        url:'/project/task/edit_detail/',
        dataType: 'json',
        data:{
            task_id:$("#taskid").val(),
            gsp:$("#projectStandardSP2").val(),
            joined:JSON.stringify(joined)
        },
        success:function (data) {
            if (data.status == 0) {
                $('.input-team-modal').modal('toggle')
            }
            else {
                alert(data.msg)
            }
        }
    })

}

function buildEditTeam(id, name) {

    var div = document.getElementById("modal-body");
    while(div.hasChildNodes()) {
        div.removeChild(div.firstChild);
    }

    if (name == undefined) name = "";

    var dialogString =
            '<div class="modal-dialog modal-lg" role="document">' +
                '<div class="modal-content">' +
                    '<div class="modal-header">' +
                        '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>' +
                    '</div>' +
                    '<div class="modal-body">' +
                        '<form class="form-horizontal">' +
                            '<div class="form-group">' +
                                '<label for="teamName" class="col-md-3 control-label">小组名称</label>' +
                                '<div class="col-sm-6">' +
                                    '<input class="form-control" id="teamName" value=' + name + '>' +
                                '</div>' +
                            '</div>' +
                            '<div class="form-group">' +
                                '<div class="col-sm-6">' +
                                    '<a class="btn btn-sm btn-primary btn-block" href="javascript:addAndEditTeam(' + id + ')">确定</a>' +
                                '</div>' +
                                '<div class="col-sm-6">' +
                                    '<a class="btn btn-sm btn-primary btn-block" data-dismiss="modal">取消</a>' +
                                '</div>' +
                            '</div>' +
                        '</form>' +
                    '</div>' +
                '</div>' +
            '</div>';

    $('#modal-body').append(dialogString);
}

function addTeam() {
    buildEditTeam(null);
    $('.add-and-edit-team-modal').modal('show');
}

function editTeam(id, name) {
    buildEditTeam(id, name);
    $('.add-and-edit-team-modal').modal('show');
}

function addAndEditTeam(id) {

    setCSRFToken()

    var data = {};
    if (id) {
        data = {
            id: id,
            name:$("#teamName").val()
        }
    }
    else {
        data = {
            id: 0,
            name:$("#teamName").val()
        }
    }

    $.ajax({
        type:'POST',
        url:'/group/add/',
        dataType: 'json',
        data: data,
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

function deleteTeam(id) {

    setCSRFToken()

    var r = confirm("是否删除小组，包括删除所有成员？")
    if (r === true) {
        $.ajax({
        type:'POST',
        url:'/group/delete/',
        dataType: 'json',
        data: {
            id: id
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
    else {
    }
}

function addAndEditUser(id) {
    setCSRFToken()
    $.ajax({
        type:'POST',
        url:'/add/',
        dataType: 'json',
        data:{
            userid:id,
            username:$("#username").val(),
            email:$("#email").val(),
            groupid:$("#groupid").val(),
            leader:true
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

function deleteMember() {
    var r = confirm("是否删除成员？")
    if (r === true) {
    }
    else {
    }
}
