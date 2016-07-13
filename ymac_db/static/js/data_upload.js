var token = "aa6d124ce6331547c6743e14f6bcf3cd1695fec5";
var server = "ymac-dc3-app1:8080";
var formFields = [];
var tableData = {};
var currentRepo = {};
var outputRequest = "";
var layer, map, ojson;
var download = false;
var googleEarthData = "";
var infowindow;
var lookups = {};
var drive_map = { "X:":"//YMAC-DC3-FS1/Spatial_WKG", 
                    "W:":"//YMAC-DC3-FS1/Spatial_Pub", 
                    "V:":"//YMAC-DC3-FS1/Spatial_Data",
                    "K:":"//YMAC-DC3-FS1/Research",
                    "Z:":"//YMAC-DC3-FS1/Heritage"                   
};
var bad_drives = [ "G:", "C:"];
var params;


var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });

    cb(matches);
  };
};


function showResults( json ) {
			// The following is to write out the full return object
			// for visualization of the example
            console.log(json);
            if (json.status == "SUCCESS"){
                alert( json.statusMessage )
            } else {
                alert("FAILURE " + json.statusMessage + " check " + json.id + " on FMEServer")
            }
}

function runDataDownload() {
	var repository = document.getElementById("repo_selector").value;
	var workspace = $("#repository").text();
	var form = $("#output_form");
	var inputs = $(".form-control");
	var checks = $(".checkbox");
	params = { "publishedParameters" : [] };
	publishedParameters = params.publishedParameters;
    //REFACTOR THIS
    //IMPORTANT SOURCE PATH VALUES MUST BE IN ARRAY 
	inputs.each(function (i, el) {
        var obj = { "name" : "", "value" : null }
		if (el.id != "repo_selector") {

            if ( el.id == "" ){
                el.id = formFields[i-1];
            }
			if (el.type == "select-multiple") {
                var multiselect = [];
				var name = el.id;
                try {
                    $('#' + el.id + " :checked").each(function (i, sm) {
                        multiselect.push(sm.value);
                });}
                catch(err){console.log("There was an error" + i + " " + el.id + " " + sm)}
                if (multiselect.length > 0) {
                    publishedParameters.push({"name":name, 'value':multiselect});
                }
			} 
            else if (el.id == "source_path") { 
            var paths = []
            var drive = el.value.substring(0,2);
            //Remap drive and replace backslashes
            paths.push(el.value.replace(drive, drive_map[drive]).replace(/\\/g,"/"));
            obj.name = el.id;
            obj.value = paths;
            publishedParameters.push(obj);
            } /*else if ( el.id == "name" and el.value != "") {
                var names = [];
                names.push(el.value);
                obj.name = el.id;
                obj.value = names;
                publishedParameters.push(obj);
            }*/
            else {
                obj.name = el.id;
                obj.value = el.value;
                if (obj.value != "") {
				publishedParameters.push(obj);
                }
			}
			// Remove trailing & from string
		}
	});
    //TODO fix this 
	checks.each(function (i, c) {
		var checkbox = $(c).find('input');
		if (checkbox.prop("checked")) {
			params += checkbox[0].id + "=True";
		}
	});
	FMEServer.submitSyncJob(workspace, repository, params, showResults);
}


function generateForm(json) {
    ojson = json;
	var returnstring = "";
	// list of defaults to set
	var procdefaults = [];
    var dateinputs = [];
    var typeaheadinputs = [];
	json.forEach(function (param) {
        formFields.push(param.name);

		//We need to check the type of param
		var type = param.type;
		console.log(type);
		//LOOKUP_CHOICE = Select
        //FILE_OR_URL
        //INTEGER
        //STRING_OR_CHOICE # USE TYPEAHEAD TO BUILD ARRAY OF OPTIONS 
		//DIRNAME = Textbox
        //NOVALUE -- DATE
        //DATETYPE = ??? 
		switch (type) {
        case "INTEGER":
            returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<input class="form-control" id="' + param.name + '"  name="' + param.name + '" type="number"\>';
            break;
        case "FILE_OR_URL":

        	returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<input class="form-control" id="' + param.name + '"  name="source_path" type="text"\>';
            break;
        case "STRING_OR_CHOICE":
        	returnstring += '<div id="' + param.name + '" class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<input  class="typeahead form-control" type="text"\>';
            lookups[param.name] = []
            param.listOptions.forEach(function (options) {
				lookups[param.name].push(options.value)
			});
            typeaheadinputs.push(param.name);
           break;        
        case "CHOICE":
		case "LOOKUP_LISTBOX":
		case "LOOKUP_CHOICE":
			returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<select type="select" id="' + param.name + '" class="form-control">';
			param.listOptions.forEach(function (options) {
				returnstring += '<option value="' + options.value + '">' + options.caption + '</option>';
			});
			returnstring += '</select>';
			break;
		case "LISTBOX":
			returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<select multiple type="select" size="8" id="' + param.name + '" class="form-control">';
			param.listOptions.forEach(function (options) {
				returnstring += '<option value="'+ options.value + '">' + options.caption +'</option>';
			});
			returnstring += '</select>';
			break;
		case "NOVALUE":
		//	returnstring += '<div class="checkbox">';
			//returnstring += '<label><input type="checkbox" id="' + param.name + '" value="' + param.defaultValue + '">' + param.description + '</input></label>';
			//TO CHECK IF RIO AREA CODES
            if (param.name != 'rio_area_codes'){ 
            returnstring += '<div id="' + param.name + '" class="form-group required"><label for="' + param.name + '" class="control-label">' + param.description + '</label>';
			returnstring += '<div class="controls dateContainer"><div class="input-group input-append date" id="'+ param.name + 'dateRangePicker">';
			returnstring += '<input id="' + param.name + '" class="form-control" type="text" name="' + param.name + '" placeholder="Please enter a date">';	
			returnstring += '<span class="input-group-addon add-on"><span class="glyphicon glyphicon-calendar"></span></span></div></div></div>';
            dateinputs.push(param.name);
            }
            else 
            {			
                returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
                returnstring += '<input id="' + param.name + '" class="form-control" type="text"\>';
                //TODO may want to add in hint about using commas 
                }
            break;
		default:
			returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
			returnstring += '<input id="' + param.name + '" class="form-control" type="text"\>';
			procdefaults.push([param.name, param.defaultValue]);
		}
		returnstring += '</div>';
	});
	returnstring += '<input class="btn btn-default" value="Submit" onclick="runDataDownload();" />';
	$("#output-form").html(returnstring);
    //For each datePicker
    dateinputs.forEach( function(di) {
                $('#' + di + 'dateRangePicker').datepicker({
                format: "yyyy-mm-dd",
                showClear: true,
                showTodayButton: true,
            }
    )});
    //For each type ahead form
    typeaheadinputs.forEach( function (ta) {
        $("#" + ta + ' .typeahead').typeahead(null, 
        {
            name:ta,
            limit: 10,
            source: substringMatcher(lookups[ta])
    })});
	procdefaults.forEach(function (defaults) {
		console.log(defaults[0]);
		$("#" + defaults[0]).val(defaults[1]);
	});
     $('#output-form').formValidation({
        framework: 'bootstrap',
        excluded: ':disabled',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            'source_path': {
                validators: {
                    notEmpty: {
                        message: 'A file path is required'
                    },
                    regexp: {
                        regexp: /^[^CG]:.+$/i,
                        message: "Please move survey data from personal folders into W:\\Surveys. "}
                    }
                },
               trip_num: { 
               validators: { 
               between: {
                   min:0,
                   max:99,
                   message: "Seriously ??? That's a lot of trips. But ok. "
               }}}
}});
}

function generateRepos(json) {
	console.log(json);
	formFields.push(json);
	json.forEach(function (param) {
		if (Boolean(param.title.trim()) && Boolean(param.name.trim())) {
			$("#repo_selector").append($('<option></option>').attr("value", param.name).text(param.title));
		}
	});
}

$(document).ready(function () {

	FMEServer.init(server, token);

	// Test if get repositories else pop up alert
	FMEServer.getRepositoryItems($("#repository").text(), 0, generateRepos);
	//Next step is on change of update output form
	$('#repo_selector').change(function () {
		FMEServer.getWorkspaceParameters($("#repository").text(), $("#repo_selector").val(), generateForm);
		//$('#description').remove('p');
		//TODO GET repo description out.
		var selected = formFields[0].filter(function (obj) {
				if ('name' in obj && obj.name == $("#repo_selector").val()) {
					return true;
				} else {
					return false;
				}
			});
		$('#description').html(selected[0].description);
	});

	$('#repo_selector').focus(function () {
		FMEServer.getWorkspaceParameters($("#repository").text(), $("#repo_selector").val(), generateForm);
	});

});
