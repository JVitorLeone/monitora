$(document).ready(function () {
    feather.replace();
    
    $("#loading").hide();

    // Cadastro do produto
    function isUrlValid(url) {
        return /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url);
    }

    $("#busca_produto").click(function(){
        url = $("#id_url").val();
        if (isUrlValid(url)){
            console.log("estive aqui");
            $("#loading").show();
            $.ajax({
                method: 'POST',
                url: 'ajax/busca_preco/',
                data: {
                    'url': url
                },
                dataType: 'json',
                async: 'true',
                cache: 'false',
                success: function(response){
                    if (response.hasOwnProperty('Error')){
                        console.log("estiveaqui");
                        $("#messages").append('<div class="alert alert-danger col"><button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button><span data-feather="alert-circle" id="alert-icon"></span>' + response['Error'] + '</div>');
                        feather.replace();
                        $("#loading").hide();
                    } else {
                        console.log(response);
                        $("#loading").hide();
                        $("#url_form").remove();
                        $("form #id_url").val(response['url']);
                        $("form #id_url").attr("readonly", true);
                        $("#id_preco_atual").val(response['preco_produto']);
                        $("#id_preco_atual").attr("readonly", true);
                        $("#confirma_cadastro_form").fadeIn();
                    }
                },
                failure: function(){
                    console.log("fail");
                } 
            });
        } else {
            $("#messages").append('<div class="alert alert-danger col"><button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button><span data-feather="alert-circle" id="alert-icon"></span>URL Inválida</div>')
            feather.replace();
            $("#loading").hide();
        
        }
        
    });


    // Adiciona produto através do botão no card
    $(".adiciona_produto").off('click').on('click', function(){
        var this_btn = $(this)
        var prod_id = $(this).attr('prod_id');
        console.log("estive aqui - id = " + prod_id);
        $.ajax({
            method: 'POST',
            url: 'ajax/adiciona_produto/',
            data: {
                'produto_id': prod_id,
            },
            dataType: 'json',
            async: 'true',
            cache: 'false',
            success: function(response){
                console.log(response);
                this_btn.replaceWith('<button title="Este produto já está na sua lista" class="btn btn-success adiciona_produto disabled" prod_id="{{ prod_user.id_produto }}"><span class="adiciona_icon" data-feather="check"></span></button>');
                feather.replace();
            },
            failure: function(){
                console.log("fail");
            }
            
        });
        
    });

    

    /* PAINEL */

    $(".delete_prod_btn").click(function(){
        var prod_id = $(this).attr('prod_id');
        console.log(prod_id);
        $("#deleteProdModal").show();
        $("#deleteProdModal").addClass("show");
        $("#delete_close").click(function() {
            $("#deleteProdModal").hide();
            $("#deleteProdModal").removeClass("show");
        });
        $(".deleteBtn").off('click').on('click', function(){
            
            $.ajax({
                method: 'POST',
                url: 'ajax/delete_prod/',
                data: {
                    'id_produto': prod_id,
                },
                dataType: 'json',
                async: 'true',
                cache: 'false',
                success: function(response){
                    console.log("estive aqui");
                    console.log(response);
                    if(response.hasOwnProperty('error')){
                        $("#messages").append('<div class="alert alert-painel alert-danger col"><button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button><span data-feather="alert-circle" id="alert-icon"></span>' + response['error'] + '</div>');
                        feather.replace();
                    } else {
                        $("#messages").append('<div class="alert alert-painel alert-success col"><button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button><span data-feather="alert-circle" id="alert-icon"></span>' + response['success'] + '</div>');
                        $("div[id=" + prod_id + "]").remove();
                    }
                    
                },
                failure: function(){
                    console.log("fail");
                }
                
            });
            $("#deleteProdModal").hide();
            $("#deleteProdModal").removeClass("show");
            
        });
    });

    
    /*
    $(".list-group-item").click(function() {
        $(".list-group-item").removeClass("active");
        $(this).addClass("active");
    });

    $("#button-produto").click(function () {
        $(".detalhes-user").hide();
        $(".detalhes-produtos").fadeIn();
    });

    $("#button-detalhes").click(function () {
        $(".detalhes-produtos").hide();
        $(".detalhes-user").fadeIn();
    });
    */

    function scrollBottom () {
        $('html,body').animate({scrollTop: $(".produtos").offset().top});
    }

    $("#index-btn").on("click", scrollBottom);

    var url = location.href;
    if (url.indexOf('painel') >= 0){
        $("#navLink-Inicio").removeClass("active");
        $("#navLink-Produtos").removeClass("active");
        $("#navLink-Sobre").removeClass("active");
    } else if (url.indexOf('produto') >= 0) {
        $("#navLink-Produtos").addClass("active");
        $("#navLink-Inicio").removeClass("active");
        $("#navLink-Sobre").removeClass("active");
    }

    $(window).scroll(function() {
        // checks if window is scrolled more than 80px, adds/removes 'scrolled' class
        scrolledPixels = $(window).scrollTop();
        $(".divCentro").css("top", scrolledPixels + 150);
        if($(this).scrollTop() > 80) { 
            $('.navbar').addClass('scrolled');
            $('.show').addClass('scrolled');
            $('#navbarDropdown').addClass('scrolled');
        } else {
            $('.navbar').removeClass('scrolled');
            $('.show').removeClass('scrolled');
            $('#navbarDropdown').removeClass('scrolled');
        }
    });

    function tiraMargem() {
        if ($("#user-item").hasClass('show') || $("#not-item").hasClass('show')){
            $('#dropdown-menu-user').css("margin-left", "0");
            $('#dropdown-notif').css("margin-left", "0");
        } else {
            $('#dropdown-menu-user').css("margin-left", "-68px");
            $('#dropdown-notif').css("margin-left", "-68px");
        }
    }    

    $("#navbarDropdown-user").on('click', tiraMargem);
    $("#dropdown_notification").on('click', tiraMargem);
    
    // Chart - Detalhes produtos
    console.log(hist);
    var precos = new Array();
    var datas = new Array();
    for (h in hist){
        var number = hist[h].preco.match(/\d+/g).map(Number);
        var data = hist[h].data.slice(0,16);
        console.log(number[0]);
        precos.push(number[0]);
        datas.push(data);   
    }

    console.log(precos);

    var ctx = $("#myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: datas,
            datasets: [{
                label: 'Preço',
                data: precos,
                backgroundColor: 'rgba(0, 170, 30, 0.2)',
                borderColor: 'rgb(0, 170, 30)',
                pointBackgroundColor: 'rgb(0, 170, 30)',
                borderWidth: 3
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            }
        }
    });
});