(function($){
    'use strict';

    // Menu
    var mainmenu = $('#mainmenu');
    $('#mainmenu-trigger').waypoint(function(direction){
        if( direction === 'up' ){
            mainmenu.removeClass('stuck');
        } else {
            mainmenu.addClass('stuck');
        }
    }, { offset: -25 });

    // Selects
    $('select').chosen({disable_search_threshold: 10});

    // Slider
    var bulletgroup = $('.slider-bulletgroup');

    if( bulletgroup.length !== 1 ){
        return;
    }

    bulletgroup.stick_in_parent();

    var bullets = $('.slider-bullet'),
        current = 0;

    $('.slider').on('click', '[data-bullet]', function(){
        var index = this.getAttribute('data-bullet'),
            selector = '[data-slide="'+index+'"]';

        $(window).scrollTo(selector, 600);
    });

    $('.slide').waypoint(function(direction){
        bullets.eq(current).removeClass('is-current');
        current = this.getAttribute('data-slide');
        if( direction === 'up' ){
            current -= 1;
            if( current < 0 ){ current = 0; }
        }
        bullets.eq(current).addClass('is-current');
    });
})(jQuery);

// Menu
(function($){
    'use strict';

    var header = $('#header'),
        submenu = $('#mainmenu-sub').hide();

    function showSubmenu(){
        submenu.show();
        header.on('mouseleave', hideSubmenu);
    }

    function hideSubmenu(){
        submenu.hide();
        header.off('mouseleave', hideSubmenu);
    }

    $('#mainmenu-trigger .mainnav-item > a').on('mouseover', function(){
        if( this.getAttribute('data-trigger-subnav') !== null ){
            showSubmenu();
        } else {
            hideSubmenu();
        }
    });


    // Fixed
    var mainmenu = $('#mainmenu'),
        fixedSubmenu = $('#mainmenu-fixedsub').hide();

    function showFixedSubmenu(){
        fixedSubmenu.show();
        header.on('mouseleave', hideFixedSubmenu);
    }

    function hideFixedSubmenu(){
        fixedSubmenu.hide();
        header.off('mouseleave', hideFixedSubmenu);
    }


    mainmenu.find('.mainnav-item > a').on('mouseover', function(){
        if( this.getAttribute('data-trigger-subnav') !== null ){
            showFixedSubmenu();
        } else {
            hideFixedSubmenu();
        }
    });


})(jQuery);

// onDomReady
jQuery(function(){
    $('.fancybox-media').fancybox({
        openEffect  : 'none',
        closeEffect : 'none',
        helpers : {
            media : {}
        }
    });
});