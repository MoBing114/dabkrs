jQuery(function(){
    jQuery('.web2py_htmltable').unhighlight();
    var v = jQuery('#w2p_keywords').val();
    if (v) jQuery('.web2py_htmltable').highlight(v);
    ///
    jQuery('#w2p_keywords').bind('keyup', function() {
        jQuery('.web2py_htmltable').unhighlight();
        var v = jQuery(this).val();
        if (v) jQuery('.web2py_htmltable').highlight(v);
    });
});
