jQuery(document).ready(function(){
    jQuery('.slovo').on('mouseenter', function() {
        jQuery('.iskomyi-text').unhighlight();
        var v = jQuery(this).attr('slovo');
        if (v!='') jQuery('.iskomyi-text').highlight(v);
    });
    jQuery('.slovo').on('mouseleave', function() {
        jQuery('.iskomyi-text').unhighlight();
    });
});
