$(document).ready(function () {
  // Load tasks on page load
  if (window.location.pathname === '/tasks') {
    loadTasks('all');
  }

  // Logout button
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

  // Import button
  $('#import-btn').click(function () {
    alert('Tính năng import sẽ được cập nhật sớm');
  });

  // Export button
  $('#export-btn').click(function () {
    alert('Tính năng export CSV sẽ được cập nhật sớm');
  });

  // Modal handling
  var modal = $('#task-modal');
  var addBtn = $('#add-task-btn');
  var cancelBtn = $('#cancel-btn');
  var closeSpan = $('.close');

  // Open modal
  addBtn.click(function () {
    modal.show();
  });

  // Close modal
  cancelBtn.click(function () {
    modal.hide();
    $("#task-form")[0].reset();
    $("#task-form").removeData("edit-id");
    $("#form-title").text("Tạo Task mới");
    $(".btn-save").text("Tạo Task");
  });

  closeSpan.click(function () {
    modal.hide();
    $("#task-form")[0].reset();
    $("#task-form").removeData("edit-id");
    $("#form-title").text("Tạo Task mới");
    $(".btn-save").text("Tạo Task");
  });

  // Close modal when clicking outside
  $(window).click(function (event) {
    if (event.target == modal[0]) {
      modal.hide();
      $("#task-form")[0].reset();
      $("#task-form").removeData("edit-id");
      $("#form-title").text("Tạo Task mới");
      $(".btn-save").text("Tạo Task");
    }
  });

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
        $("#task-form")[0].reset();
        $("#task-form").removeData("edit-id");
        $("#form-title").text("Tạo Task mới");
        $(".btn-save").text("Tạo Task");
        modal.hide();
        loadTasks($('.filter-btn.active').data('filter') || 'all');
      },
      error: function (xhr) {
        alert("Có lỗi xảy ra: " + xhr.responseJSON.error);
      }
    });
  });

  // Handle edit button
  $(document).on('click', '.btn-edit', function () {
    var taskId = $(this).data("task-id");
    var taskElement = $(this).closest('.task');
    var title = taskElement.find('h3').text();
    var description = taskElement.find('p:eq(0)').text() || '';
    var deadlineText = taskElement.find('p:eq(1)').text().replace('Deadline: ', '');
    var priorityText = taskElement.find('p:eq(2)').text().replace('Priority: ', '');
    var reminderText = taskElement.find('p:eq(3)').text();
    var reminderMinutes = 0;

    if (reminderText) {
      var match = reminderText.match(/(\d+) phút trước/);
      if (match) {
        reminderMinutes = match[1];
      }
    }

    // Populate form
    $("#task-title").val(title);
    $("#task-desc").val(description);
    $("#task-deadline").val(deadlineText);
    $("#task-priority").val(priorityText);
    $("#task-reminder").val(reminderMinutes);

    // Mark as edit mode
    $("#task-form").data("edit-id", taskId);
    $("#form-title").text("Sửa Task");
    $(".btn-save").text("Lưu Task");

    // Show modal
    modal.show();
  });

  // Handle delete button
  $(document).on('click', '.btn-delete', function () {
    if (confirm('Bạn có chắc chắn muốn xóa task này?')) {
      var taskId = $(this).data("task-id");
      $.ajax({
        url: "/api/task/" + taskId,
        type: "DELETE",
        success: function (response) {
          alert(response.message);
          loadTasks($('.filter-btn.active').data('filter') || 'all');
        },
        error: function (xhr) {
          alert("Có lỗi xóa task: " + xhr.responseJSON.error);
        }
      });
    }
  });

  // Handle checkbox change for task status
  $(document).on('change', '.task-status', function () {
    var taskId = $(this).data("task-id");
    var isChecked = $(this).is(":checked");
    var newStatus = isChecked ? "Completed" : "Pending";

    $.ajax({
      url: "/api/task/" + taskId,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify({
        status: newStatus
      }),
      success: function (response) {
        console.log("Task status updated: " + response.message);
        var currentFilter = $('.filter-btn.active').data('filter') || 'all';
        loadTasks(currentFilter);
      },
      error: function (xhr) {
        alert("Có lỗi cập nhật task: " + xhr.responseJSON.error);
        // Revert checkbox state on error
        $(this).prop("checked", !isChecked);
      }.bind(this)
    });
  });

  // Handle filter button clicks
  $(document).on('click', '.filter-btn', function () {
    $('.filter-btn').removeClass('active');
    $(this).addClass('active');
    var filter = $(this).data('filter');
    loadTasks(filter);
  });
});

// Function to load tasks based on filter
function loadTasks(filter) {
  $.ajax({
    url: "/api/tasks",
    type: "GET",
    data: { filter: filter },
    success: function (response) {
      renderReminders(response.tasks);
      renderTasks(response.tasks);
    },
    error: function (xhr) {
      alert("Có lỗi tải tasks: " + xhr.responseJSON.error);
    }
  });
}

function renderReminders(tasks) {
  var panel = $('#reminder-panel');
  var list = $('#reminder-list');
  list.empty();

  var now = new Date();
  var reminders = tasks.filter(function (task) {
    if (!task.deadline || !task.reminder_minutes || task.status === 'Completed') return false;
    var deadline = new Date(task.deadline);
    var reminderTime = new Date(deadline.getTime() - task.reminder_minutes * 60000);
    return now >= reminderTime && deadline > now;
  });

  if (reminders.length === 0) {
    list.append('<p class="no-reminder">Không có nhắc nhở nào.</p>');
    return;
  }

  reminders.forEach(function (task) {
    var deadline = new Date(task.deadline).toLocaleString();
    list.append('<div class="reminder-item">' +
      '<strong>' + task.title + '</strong>' +
      '<p>Deadline: ' + deadline + '</p>' +
      '<p>Nhắc trước: ' + task.reminder_minutes + ' phút</p>' +
      '</div>');
  });
}

// Function to render tasks in the UI
function renderTasks(tasks) {
  var container = $('#tasks-container');
  container.empty();

  if (tasks.length === 0) {
    container.append('<p>Chưa có task nào.</p>');
    return;
  }

  tasks.forEach(function (task) {
    var reminderLine = '';
    if (task.reminder_minutes) {
      reminderLine = '<p class="task-reminder">Nhắc nhở: ' + task.reminder_minutes + ' phút trước</p>';
    }
    var taskHtml = '<div class="task" data-task-id="' + task.id + '">' +
      '<div class="task-header">' +
      '<label>' +
      '<input type="checkbox" class="task-status" data-task-id="' + task.id + '" ' +
      (task.status === 'Completed' ? 'checked' : '') + '> ' +
      'Đã hoàn thành' +
      '</label>' +
      '<div class="task-actions">' +
      '<button class="btn-edit" data-task-id="' + task.id + '">✏️ Sửa</button>' +
      '<button class="btn-delete" data-task-id="' + task.id + '">🗑️ Xóa</button>' +
      '</div>' +
      '</div>' +
      '<h3 class="task-title">' + task.title + '</h3>' +
      '<p class="task-desc">' + (task.description || '') + '</p>' +
      '<p class="task-deadline">Deadline: ' + (task.deadline ? new Date(task.deadline).toLocaleDateString() : 'Không có') + '</p>' +
      '<p class="task-priority">Priority: ' + task.priority + '</p>' +
      reminderLine +
      '</div>';
    container.append(taskHtml);
  });
}
