global_ccount = 0;
MAX_COLORS = 32;

window.onload=function(){
  clistItem = document.getElementById("colorList");
  clist = clistItem.value;
  colors = clist.split(",");

	box=document.getElementById("box");
	
  global_ccount = colors.length;

	if(colors != "") {
		for(var i=0; i<colors.length; i++) {
			var temp = document.createElement("input");
			var temp2 = document.createElement("div");
			var temp3 = document.createElement("p");
			temp3.className = "color_number";
			temp2.className = "holder";
			temp2.appendChild(temp3);
			temp2.appendChild(temp);
			temp.id = i;
			temp.type = "text";
			temp.className = "basicColor";
			temp.value = colors[i];
			box.appendChild(temp2);
		}
	}
  if(colors.length < MAX_COLORS) {
  	var temp = document.createElement("input");
  	var temp2 = document.createElement("div");
  	var temp3 = document.createElement("p");
  	temp3.className = "empty_label";
  	temp3.innerHTML = "new color";
  	temp2.className = "holder";
  	temp2.appendChild(temp3);
  	temp2.appendChild(temp);
  	temp.type = "text";
  	temp.className = "emptyColor";
  	temp.value = "";
  	box.appendChild(temp2);
  }

	$(".basicColor").bind("change", colorHandler);
	update();
  olist();

  /*if($("#id_colorSelect_1").prop("checked")) {
    $("#id_numberOfColors").prop('disabled',true);
  }

  $("input:radio[name=colorSelect]").click(function() {
    selectHandler($(this).val());
  });*/
}

/*selectHandler = function(value) {
  if(value == "0") {
    $("#id_numberOfColors").prop('disabled',false);
  }
  else {
    $("#id_numberOfColors").prop('disabled',true);
  }
}*/

update = function() {
	$(".basicColor").spectrum({
		preferredFormat: "hex",
		allowEmpty:true
	});
	$(".emptyColor").spectrum({
		preferredFormat: "hex",
		allowEmpty:true
	});
	$(".emptyColor").bind("change", emptyHandler);
	colorLabel();
}

colorHandler = function() {
  if($(this).val() == "" && global_ccount >= MAX_COLORS) {
  	var temp2 = document.createElement("div");
		var temp3 = document.createElement("p");
		var temp = document.createElement("input");
    temp3.innerHTML = "new color";
  	temp2.className = "holder"
 		temp3.className = "empty_label";
 		temp.type = "text";
 		temp.className = "emptyColor";
 		temp.value = "";
 		temp2.appendChild(temp3);
 		temp2.appendChild(temp);
 		box.appendChild(temp2);
  }


  if($(this).val() == "") {
    global_ccount -= 1;
		$(this).spectrum("destroy");
		$(this).prev().remove();
		$(this).parent().remove();
		$(this).remove();
    update();
	}
	olist();
}

colorLabel = function() {
	$(".color_number").each(function(index,element) {
		this.innerHTML = "Color #"+(index+1);
	});
}

emptyHandler = function() {
	if($(this).val() != "" && global_ccount < MAX_COLORS) {
		$(this).attr('class','basicColor');
		var temp2 = document.createElement("div");
		var temp3 = document.createElement("p");
		var temp = document.createElement("input");
		$(this).prev().attr('class','color_number');
    if(global_ccount + 1 < MAX_COLORS) {
  		temp3.innerHTML = "new color";
  		temp2.className = "holder"
  		temp3.className = "empty_label";
  		temp.type = "text";
  		temp.className = "emptyColor";
  		temp.value = "";
  		temp2.appendChild(temp3);
  		temp2.appendChild(temp);
  		box.appendChild(temp2);
    }
  	$(this).unbind("change", emptyHandler);
    $(this).bind("change",colorHandler);
		update();
		olist();
    global_ccount += 1;
	}
}

olist = function() {
	var ostring = "";
  var tlen = $(".basicColor").length;
	$(".basicColor").each(function(index, element) {
		ostring += $(this).val();
    //ostring += "," + index + ",";
    if(index < tlen - 1) {
      ostring += ",";
    }
	});
	$("#colorList").val(ostring);
}
