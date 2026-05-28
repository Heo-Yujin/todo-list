
// ================= LOGIN =================
function login(){
    $.ajax({
        url: "/login",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            uid: $("#uid").val(),
            upwd: $("#upwd").val()
        }),
        success: function(res){
            alert("로그인 성공");

            $("#loginBox").hide();
            $("#todoBox").show();

            loadTodos();
        },
        error: function(){
            alert("로그인 실패");
        }
    });
}


// ================= TODO LIST =================
function loadTodos(){
    $.get("/todos", function(data){
        $("#list").empty();

        data.forEach(t => {
            $("#list").append(`
                <li>
                    ${t.title}
                    <button onclick="done(${t.id})">완료</button>
                    <button onclick="del(${t.id})">삭제</button>
                </li>
            `);
        });
    });
}


// ================= ADD =================
function addTodo(){
    $.ajax({
        url: "/todos",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            title: $("#title").val(),
            uid: $("#uid").val()
        }),
        success: loadTodos
    });
}


// ================= DONE =================
function done(id){
    $.ajax({
        url: "/todos/" + id,
        type: "PUT",
        success: loadTodos
    });
}


// ================= DELETE =================
function del(id){
    $.ajax({
        url: "/todos/" + id,
        type: "DELETE",
        success: loadTodos
    });
}