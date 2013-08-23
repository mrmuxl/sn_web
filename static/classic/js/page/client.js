require.config({
	paths: {
		"jquery": "../lib/jquery.min",
	    "file": "../service/file"
　　}
});


require(['file'], function (File){
	File.test();
});
