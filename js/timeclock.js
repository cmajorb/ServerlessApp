var isLunch = false;

function clockIn() {
  var notification = document.getElementById("notification");
  notification.classList.remove('alert-info');
  notification.classList.add('alert-success');
  notification.innerHTML = 'Clocked in';
  notification.style.visibility = 'visible';
  setTimeout(function () {notification.style.visibility='hidden'}, 5000);
  document.getElementById("clockIn").disabled = true;
  document.getElementById("clockOut").disabled = false;
}

function clockOut() {
  var notification = document.getElementById("notification");
  notification.classList.remove('alert-info');
  notification.classList.add('alert-success');
  notification.innerHTML = 'Clocked out';
  notification.style.visibility = 'visible';
  setTimeout(function () {notification.style.visibility='hidden'}, 5000);
  document.getElementById("clockOut").disabled = true;
  document.getElementById("clockIn").disabled = false;
}

function switchJob(selectObject) {
  console.log(selectObject);
  var value = selectObject.options[selectObject.selectedIndex].innerHTML;
  var notification = document.getElementById("notification");
  notification.classList.remove('alert-success');
  notification.classList.add('alert-info');
  notification.innerHTML = 'Switched to ' + value;
  notification.style.visibility = 'visible';
  setTimeout(function () {notification.style.visibility='hidden'}, 5000);
}

function lunch() {
  var notification = document.getElementById("notification");
  notification.classList.remove('alert-success');
  notification.classList.add('alert-info');
  var lunch = document.getElementById("lunch");

  if(isLunch) {
    notification.innerHTML = 'Stopped Lunch Break';
    lunch.innerHTML='Start Lunch Break';
    lunch.classList.remove('btn-info');
    lunch.classList.add('btn-primary');
    isLunch = false;
  } else {
    notification.innerHTML = 'Started Lunch Break';
    lunch.innerHTML='Stop Lunch Break';
    lunch.classList.remove('btn-primary');
    lunch.classList.add('btn-info');
    isLunch = true;
  }

  notification.style.visibility = 'visible';

  setTimeout(function () {notification.style.visibility='hidden'}, 5000);

}
