(function($) {
    'use strict';

    var $body = $('body');
    var sideBarWidth = 250;
    var sideBarWidthCondensed = 250 - 70;
    var $classes = {
        FsrHolder: 'fsr-holder',
        FsrImage: 'image-full',
    };

    $(document).ready(function() {
      //  $('.page-sidebar').bind('mouseenter mouseleave', sidebarMouseEnter);
        $('.site-content').bind('mouseover', sidebarMouseLeave);
        $('[data-toggle-pin="sidebar"]').click(function(){
            $body.toggleClass('menu-pin')
        });
        fullscreener($('.' + $classes.FsrImage));
        autosize($('.autosize'));
        autosize($('.CodeMirror-wrap'));
        $('.markdown').markdownify();
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

    function fullscreener(_container) {
       _container.each(function () {
           var _this = $(this);
           //debugger;
           var _src = _this.attr('src');
           var _srcset = _this.attr('srcset');
           if (_srcset != null)
           {
               var screenWidth = $win.width();
               var src_arr = _parse_srcset(_srcset);
               for (var i in src_arr)
               {
                   if (src_arr[i].width >= screenWidth)
                   {
                       _src = src_arr[i].url;
                       break;
                   }
               }
           }
           _this.parent().addClass($classes.FsrHolder).attr('style', 'background-image: url(' + _src + ');');
       });
   }


    $('.panel-collapse label').on('click', function(e){
        e.stopPropagation();
    })

})(window.jQuery);
