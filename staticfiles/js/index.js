const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const Buy = (id) => {
  const csrftoken = getCookie("csrftoken");
  $.ajax({
    url: `/boughts/${id}/`,
    type: "post",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (data) {
      let status = $("#buyStatus");
      status.addClass("badge-success");
      status.text(`The item ${id} has been bought successfully !`);
      setTimeout(() => {
        status.removeClass("badge-success");
        status.text("");
      }, 3000);
    },
    failure: function (data) {
      status.addClass("badge-warning");
      status.text(`The item ${id} hasn't been bought !`);
      setTimeout(() => {
        status.removeClass("badge-success");
        status.text("");
      }, 3000);
    },
  });
};
