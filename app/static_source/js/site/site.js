(function($){
    var $classes = {
        FsrHolder: 'fsr-holder',
        FsrImage: 'image-full',
    };

    function slugify(text){
        return text.toLowerCase()
            .replace(/ /g,'-')
            .replace(/[-]+/g, '-')
            .replace(/[^\w-]+/g,'');
    }

    $(document).ready(function() {
        var sections = $('.section');
        var titles = [];
        var anchors = [];
        sections.each(function(i, item){
            var title = $(item).data('title');
            console.log(title);
            var anchor = slugify(title);
            titles.push(title);
            anchors.push(anchor);
        });
        $('#fullpage').fullpage({
            anchors: anchors,
            //sectionsColor: ['#C63D0F', '#1BBC9B', '#7E8F7C'],
            navigation: true,
            navigationPosition: 'right',
            navigationTooltips: titles,
            bigSectionsDestination: 'top',
            responsiveWidth: 992,
            scrollBar: true,
            fixedElements: '#header-nav',
        });

        fullscreener($('.' + $classes.FsrImage));
    });

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

   /**
    * parse_srcset - A much simplified version of https://github.com/albell/parse-srcset
    *
    * @param string str
    * @returns array of objects of the form {url: $url, width: $width}, sorted in order of increasing width
    */
   function _parse_srcset(str) {
       var arr = str.split(', ');
       var srcset = new Array();
       for (var i in arr)
       {
           var tokens = arr[i].split(' ');
           var url = tokens[0];
           var w = tokens[1].replace('w', '');
           srcset.push({url: url, width: w});
       }

       srcset.sort(function (a, b) {
           return parseFloat(a.w) - parseFloat(b.w);
       });
       return srcset;
   }
})(jQuery);
