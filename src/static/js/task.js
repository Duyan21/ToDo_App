$(document).ready(function () {

  // Load tasks + notifications khi vào trang
  if (window.location.pathname === '/tasks') {
    loadTasks('all');
    loadNotifications();
  }

  // Auto refresh notification mỗi 1s
  setInterval(loadNotifications, 1000);

  // Logout
  $('#logout-btn').click(function () {
    if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
      $.ajax({
        url: "/api/logout",
        type: "POST",
        success: function () {
          window.location.href = "/signin";
        }
      });
    }
  });

  // Modal
  var modal = $('#task-modal');
  var addBtn = $('#add-task-btn');
  var cancelBtn = $('#cancel-btn');
  var closeSpan = $('.close');

  function resetForm() {
    $("#task-form")[0].reset();
    $("#task-form").removeData("edit-id");
    $("#form-title").text("Tạo Task mới");
    $(".btn-save").text("Tạo Task");
  }

  addBtn.click(function () {
    modal.show();
  });

  cancelBtn.click(function () {
    modal.hide();
    resetForm();
  });

  closeSpan.click(function () {
    modal.hide();
    resetForm();
  });

  $(window).click(function (event) {
    if (event.target == modal[0]) {
      modal.hide();
      resetForm();
    }
  });

  // CREATE / EDIT TASK
  $("#task-form").submit(function (e) {
    e.preventDefault();

    var taskId = $("#task-form").data("edit-id");
    var method = taskId ? "PATCH" : "POST";
    var url = taskId ? "/api/task/" + taskId : "/api/task";

    $.ajax({
      url: url,
      type: method,
      contentType: "application/json",
      data: JSON.stringify({
        title: $("#task-title").val(),
        description: $("#task-desc").val(),
        deadline: $("#task-deadline").val(),
        priority: $("#task-priority").val(),
        reminder_minutes: $("#task-reminder").val()
      }),
      success: function (response) {
        alert(response.message);
        resetForm();
        modal.hide();
        loadTasks($('.filter-btn.active').data('filter') || 'all');
      },
      error: function (xhr) {
        alert("Có lỗi xảy ra: " + xhr.responseJSON.error);
      }
    });
  });

  // EDIT TASK
  $(document).on('click', '.btn-edit', function () {
    var taskId = $(this).data("task-id");
    var taskElement = $(this).closest('.task');

    $("#task-title").val(taskElement.find('.task-title').text());
    $("#task-desc").val(taskElement.find('.task-desc').text());

    var deadline = taskElement.data('deadline');
    if (deadline) {
      $("#task-deadline").val(deadline);
    }

    var reminder = taskElement.find('.task-reminder').data('reminder') || 0;
    $("#task-reminder").val(reminder);

    $("#task-form").data("edit-id", taskId);
    $("#form-title").text("Sửa Task");
    $(".btn-save").text("Lưu Task");

    modal.show();
  });

  // DELETE TASK
  $(document).on('click', '.btn-delete', function () {
    if (confirm('Bạn có chắc chắn muốn xóa task này?')) {
      var taskId = $(this).data("task-id");

      $.ajax({
        url: "/api/task/" + taskId,
        type: "DELETE",
        success: function (response) {
          alert(response.message);
          loadTasks($('.filter-btn.active').data('filter') || 'all');
        }
      });
    }
  });

  // UPDATE STATUS
  $(document).on('change', '.task-status', function () {
    var taskId = $(this).data("task-id");
    var isChecked = $(this).is(":checked");

    $.ajax({
      url: "/api/task/" + taskId,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify({
        status: isChecked ? "Completed" : "Pending"
      }),
      success: function () {
        loadTasks($('.filter-btn.active').data('filter') || 'all');
      }
    });
  });

  // FILTER
  $(document).on('click', '.filter-btn', function () {
    $('.filter-btn').removeClass('active');
    $(this).addClass('active');
    loadTasks($(this).data('filter'));
  });

  // CLICK notification → mark read
  $(document).on('click', '.reminder-item', function () {
    var id = $(this).data('id');

    $.ajax({
      url: "/api/notifications/" + id + "/read",
      type: "PATCH"
    });

    $(this).removeClass('unread');
  });

});


// ================= TASK =================

function loadTasks(filter) {
  $.ajax({
    url: "/api/tasks",
    type: "GET",
    data: { filter: filter },
    success: function (response) {
      renderTasks(response.tasks);
    }
  });
}


// ================= NOTIFICATION =================

function loadNotifications() {
  $.ajax({
    url: "/api/notifications",
    type: "GET",
    success: function (res) {
      renderReminders(res.notifications);

      // auto mark all as read
      markAllAsRead();
    }
  });
}

function markAllAsRead() {
  $.ajax({
    url: "/api/notifications/read-all",
    type: "PATCH"
  });
}

function renderReminders(notifications) {
  var list = $('#reminder-list');
  list.empty();

  if (!notifications || notifications.length === 0) {
    list.append('<p>Không có nhắc nhở nào.</p>');
    return;
  }

  notifications.forEach(function (n) {
    var isOverdue = n.type === "OVERDUE";

    list.append(
      '<div class="reminder-item ' + (n.is_read ? '' : 'unread') + (isOverdue ? ' overdue' : '') + '" data-id="' + n.id + '">' + n.message + '</div>'
    );
  });
}

// ================= RENDER TASK =================

function renderTasks(tasks) {
  var container = $('#tasks-container');
  container.empty();

  if (tasks.length === 0) {
    container.append('<p>Chưa có task nào.</p>');
    return;
  }

  tasks.forEach(function (task) {
    var dateStr = 'Không có';
    if (task.deadline) {
      var d = new Date(task.deadline);
      dateStr = d.toLocaleString();
    }

    var reminderLine = '';
    if (task.reminder_minutes && task.reminder_minutes > 0) {
      reminderLine =
        '<p class="task-reminder" data-reminder="' + task.reminder_minutes + '">' +
        'Nhắc: ' + task.reminder_minutes + ' phút trước</p>';
    }

    var html =
      '<div class="task" data-task-id="' + task.id + '" data-deadline="' + task.deadline + '">' +
      '<div class="task-header">' +
      '<label>' +
      '<input type="checkbox" class="task-status custom-checkbox" data-task-id="' + task.id + '" ' +
      (task.status === 'Completed' ? 'checked' : '') +
      '> Đã hoàn thành' +
      '</label>' +
      '<div class="task-actions">' +
      '<button class="btn-edit" data-task-id="' + task.id + '">✏️ Sửa</button>' +
      '<button class="btn-delete" data-task-id="' + task.id + '">🗑️ Xóa</button>' +
      '</div>' +
      '</div>' +
      '<h3 class="task-title">' + task.title + '</h3>' +
      '<p class="task-desc">' + (task.description || '') + '</p>' +
      '<p class="task-deadline">Deadline: ' + dateStr + '</p>' +
      '<p class="task-priority">Priority: ' + task.priority + '</p>' +
      reminderLine +
      '</div>';

    container.append(html);
  });
}