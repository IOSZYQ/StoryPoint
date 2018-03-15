define(['datepicker','remodal'],function () {
    return {
        init:function () {
           this.tabChange();
           //  日期插件初始化
            $('.js-index-calendar').datepicker({
                format: 'yyyy-mm-dd'
            });
            // 创建项目点击事件
            $('.new-product').on('click',function () {
                $('[data-remodal-id=new-product]').remodal().open();
            });
            //  删除团队点击事件
            $('.js-delete-btn').on('click',function () {
                $('input[name=index]').val($(this).parent().parent().index());
                $('[data-remodal-id=delete-modal]').remodal().open();
            })
            //  弹窗中删除团队点击事件
            $('.js-deter-btn').on('click',function () {
                $('.team-content li').eq($('input[name=index]').val()).remove();
                $('[data-remodal-id=delete-modal]').remodal().close();
            })
            $('.amend-btn').on('click',function () {
                $('[data-remodal-id=team-modal]').remodal().open();
            })
        },
        tabChange:function () {
            var $li=$('.nav-list li'),
                $content=$('.content-one');
            $('.nav-list').on('click','li',function () {
                $li.removeClass('active');
                $content.addClass('display-none');
                var ind=$(this).index();
                $(this).addClass('active');
                $content.eq(ind).removeClass('display-none');
            })
        }
    }
})