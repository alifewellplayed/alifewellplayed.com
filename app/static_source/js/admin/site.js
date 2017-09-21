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

        new SimpleMDE({
          element: document.getElementById("id_body"),
          autofocus: true,
        	autosave: {
        		enabled: true,
        		uniqueId: "MyUniqueID",
        		delay: 1000,
        	},
          blockStyles: {
        		bold: "__",
        		italic: "_"
        	},
          insertTexts: {
        		horizontalRule: ["", "\n\n-----\n\n"],
        		image: ["![](http://", ")"],
        		link: ["[", "](http://)"],
        		table: ["", "\n\n| Column 1 | Column 2 | Column 3 |\n| -------- | -------- | -------- |\n| Text     | Text      | Text     |\n\n"],
        	},
          parsingConfig: {
        		allowAtxHeaderWithoutSpace: true,
        		strikethrough: false,
        		underscoresBreakWords: true,
        	},
        	placeholder: "Type here...",
          previewRender: function(plainText, preview) { // Async method
        		setTimeout(function(){
        			preview.innerHTML = customMarkdownParser(plainText);
        		}, 250);

        		return "Loading...";
        	},
          promptURLs: true,
        	renderingConfig: {
        		singleLineBreaks: false,
        		codeSyntaxHighlighting: true,
        	},
        	shortcuts: {
        		drawTable: "Cmd-Alt-T"
        	},
          showIcons: ["code", "table"],
          tabSize: 2,
        });

        $('.datepicker').datepicker({
          format: 'mm/dd/yyyy',
          startDate: '0d',
          autoclose: true,
          container: '.date-time-group',
        });
        $('.timepicker').timepicker({
          timeFormat: 'g:ia',
          step: 15,
          scrollDefault: '05:00 pm',
          forceRoundTime: false,
          closeOnWindowScroll: true,
          appendTo: '.date-time-group',
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
