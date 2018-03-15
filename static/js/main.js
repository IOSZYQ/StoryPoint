function forgot() {
    $('.forgot-password-modal').modal('toggle')
    $('.forgot-password-finish-modal').modal('show')
}

function modifyPassword() {
    $('.forgot-modify-password-modal').modal('toggle')
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
