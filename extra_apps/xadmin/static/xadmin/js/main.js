

requirejs.config({
    paths:{
        jquery:['lib/jquery.min'],
        modernizr:['lib/modernizr'],
        datepicker:['lib/datepicker.min'],
        remodal:['lib/remodal.min'],
    },
    waitSeconds: 0,
    urlArgs: "version=0.1"
});

require(['jquery','modernizr'],function (){
    init();
    function init(){
        if($('html').hasClass('lt-ie9')){
            if($('input').length > 0 || $('textarea').length > 0){
                require(['placeholder'],function(placeholder){
                    $('input').placeholder();
                });
            }
        }
        if($('input[type="text"]').length != 0){
            var theVal  = '';
            $('input[type="text"]').parent().on('blur','input[type="text"]',function (){
                if($(this).prop('name') != 'english_name'){
                    theVal = $(this).val();
                    $(this).val(theVal.replace(/\s/g,''));
                }
            });
        }

        var routeId = $('.js-route-flag');

        //FORM同步提交报错处理(统一)
        if(routeId.hasClass('product-list-flag')){
            require(['product-list'],function(list){
                list.init();
            });
        }

    }
});