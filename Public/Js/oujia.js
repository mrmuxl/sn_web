$(document).ready(function(){
	
	// first example
	$("#browser").treeview();
	
	// second example
	$("#navigation").treeview({
		persist: "location",
		collapsed: true,
		unique: true
	});
	
	// third example
	$("#red").treeview({
		animated: "fast",
		collapsed: true,
		unique: true,
		persist: "cookie",
		toggle: function() {
			window.console && console.log("%o was toggled", this);
		}
	});
	
	// fourth example
	$("#black, #gray").treeview({
		control: "#treecontrol",
		persist: "cookie",
		cookieId: "treeview-black"
	});

});

String.prototype.trim=function(){
    return this.replace(/(^\s*)|(\s*$)/g, "");
 }
 String.prototype.ltrim=function(){
    return this.replace(/(^\s*)/g,"");
 }
 String.prototype.rtrim=function(){
    return this.replace(/(\s*$)/g,"");
 }