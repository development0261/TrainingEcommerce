$('#slider1, #slider2, #slider3').owlCarousel({
    loop: false,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: false,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: false,
        },
        1000: {
            items: 1,
            nav: true,
            loop: true,
            autoplay: false,
        }
    }
})

$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var ele = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log(data)
            ele.innerText = data.quantity

            document.getElementById("amount").innerHTML = data.amount
            document.getElementById("totalamount").innerHTML = data.totalamount



        }
    })
})

$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var ele = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log(data)
            ele.innerText = data.quantity
            document.getElementById("amount").innerHTML = data.amount
            document.getElementById("totalamount").innerHTML = data.totalamount
                // ele.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var ele = this
    console.log(id)
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log(data)
            document.getElementById("amount").innerHTML = data.amount
            document.getElementById("totalamount").innerHTML = data.totalamount

            document.getElementById("removecart").remove()
        }
    })
})


$(document).ready(function() {
    $('#formvalidation').validate({
        rules: {
            username: {
                require: true
            }
        },
        messages: {
            require: "please Enter Your name",
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});