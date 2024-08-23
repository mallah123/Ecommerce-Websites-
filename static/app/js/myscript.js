$(document).ready(function(){
  $("#slider1","#slider2","slider3","slider4","slider5","slider6").owlCarousel({
    items: 4,
    loop: true,
    margin: 10,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    responsive: {
      0: { items: 1 },
      600: { items: 2 },
      1000: { items: 4 }
    }
  });
});


// $(".plus-cart").click(function () {
//   var id = $(this).attr("pid").toString();
//   var eml = this.parentNode.children[2];

//   $.ajax({
//     type: "GET",
//     url: "/pluscart",
//     data: {
//       prod_id: id,
//     },
//     success: function (data) {
//       eml.innerText = data.quantity;
//       document.getElementById("amount").innerText = data.amount;
//       document.getElementById("total_amount").innerText = data.total_amount;
//     },
//   });
// });

// $(".minus-cart").click(function () {
//   var id = $(this).attr("pid").toString();
//   var eml = this.parentNode.children[2];

//   $.ajax({
//     type: "GET",
//     url: "/minuscart",
//     data: {
//       prod_id: id,
//     },
//     success: function (data) {
//       eml.innerText = data.quantity;
//       document.getElementById("amount").innerText = data.amount;
//       document.getElementById("total_amount").innerText = data.total_amount;
//     },
//   });
// });


// $(".remove-cart").click(function () {
//     var id = $(this).attr("pid").toString();
//     var eml = this
//     $.ajax({
//       type: "GET",
//       url: "/removecart",
//       data: {
//         prod_id: id,
//       },
//       success: function (data) {
//         document.getElementById("amount").innerText = data.amount;
//         document.getElementById("total_amount").innerText = data.total_amount;
//         eml.parentNode.parentNode.parentNode.parentNode.remove()
//       },
//     });
//   });
  
// Function to handle cart update actions
$(document).ready(function () {
  // Increase quantity
  $(".plus-cart").click(function (event) {
    event.preventDefault(); // Prevent default link behavior
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).siblings('#quantity'); // Get sibling element using jQuery

    $.ajax({
      type: "GET",
      url: "/pluscart",
      data: { prod_id: id },
      success: function (data) {
        console.log('Increase response:', data); // Debugging output
        if (data.success) {
          quantityElement.text(data.quantity);
          $("#amount").text(data.amount);
          $("#total_amount").text(data.total_amount);
        } else {
          alert("Failed to update quantity.");
        }
      },
      error: function () {
        alert("Error while updating quantity.");
      }
    });
  });

  // Decrease quantity
  $(".minus-cart").click(function (event) {
    event.preventDefault(); // Prevent default link behavior
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).siblings('#quantity'); // Get sibling element using jQuery

    $.ajax({
      type: "GET",
      url: "/minuscart",
      data: { prod_id: id },
      success: function (data) {
        console.log('Decrease response:', data); // Debugging output
        if (data.success) {
          var newQuantity = data.quantity;
          quantityElement.text(newQuantity);
          $("#amount").text(data.amount);
          $("#total_amount").text(data.total_amount);

          // Remove item from DOM if quantity is zero or less
          if (newQuantity <= 0) {
            $(quantityElement).closest('.row').remove(); // Remove the row containing the item
          }
        } else {
          alert("Failed to update quantity.");
        }
      },
      error: function () {
        alert("Error while updating quantity.");
      }
    });
  });

  // Remove item from cart
  $(".remove-cart").click(function (event) {
    event.preventDefault(); // Prevent default link behavior
    var id = $(this).attr("pid").toString();
    var itemElement = $(this).closest('.row'); // Get the row containing the item

    $.ajax({
      type: "GET",
      url: "/removecart",
      data: { prod_id: id },
      success: function (data) {
        console.log('Remove response:', data); // Debugging output
        if (data.success) {
          $("#amount").text(data.amount);
          $("#total_amount").text(data.total_amount);
          itemElement.remove(); // Remove the row containing the item
        } else {
          alert("Failed to remove item.");
        }
      },
      error: function () {
        alert("Error while removing item.");
      }
    });
  });
});
