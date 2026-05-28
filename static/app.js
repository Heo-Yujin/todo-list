function load(){
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

function add(){
    $.ajax({
        url: "/todos",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            title: $("#title").val(),
            uid: "admin"
        }),
        success: load
    });
}

function done(id){
    $.ajax({
        url: "/todos/" + id,
        type: "PUT",
        success: load
    });
}

function del(id){
    $.ajax({
        url: "/todos/" + id,
        type: "DELETE",
        success: load
    });
}

load();