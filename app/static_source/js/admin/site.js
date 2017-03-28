(function($) {
    'use strict';

    var $body = $('body');
    var sideBarWidth = 250;
    var sideBarWidthCondensed = 250 - 70;

    $(document).ready(function() {
        $('.page-sidebar').bind('mouseenter mouseleave', sidebarMouseEnter);
        $('.site-content').bind('mouseover', sidebarMouseLeave);
        $('[data-toggle-pin="sidebar"]').click(function(){
            $body.toggleClass('menu-pin')
        });

    });

    function sidebarMouseEnter(e){
        var menuOpenCSS = 'translate(' + sideBarWidthCondensed + 'px, 0)';
        $('.page-sidebar').css({'transform': menuOpenCSS});
        $('body').addClass('sidebar-visible');
    }

    function sidebarMouseLeave(e){
        var menuClosedCSS = 'translate(0, 0)';
        $('.page-sidebar').css({'transform': menuClosedCSS});
        $body.removeClass('sidebar-visible');
    }


    $('.panel-collapse label').on('click', function(e){
        e.stopPropagation();
    })

})(window.jQuery);
