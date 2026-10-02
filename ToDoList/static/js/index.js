// 完成任务
function checkIconClick(e) {
    let checkIcon = e.target;
    let task_id = checkIcon.dataset.id;
    if (task_id) {
        fetch("/change/" + task_id).then(response => response.json()).then(data => {
            if (data.status) {
                checkIcon.src = "/static/img/check.png";
                checkIcon.parentElement.classList.add("check");
            } else {
                checkIcon.src = "/static/img/circle.png";
                checkIcon.parentElement.classList.remove("check");
            }
        })
    }
}


let checkIcons = document.getElementsByClassName("todoCheckIcon")
// 为每个checkIcon添加点击事件
for(let i=0; i<checkIcons.length; i++) {
    checkIcons[i].onclick = checkIconClick
}

