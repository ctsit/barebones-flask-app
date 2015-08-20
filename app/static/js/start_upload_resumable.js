$(document).ready(function() {
    // Max chunk size is set to 10MB
    var r = Utils.get_resumable_instance();
    var file_select = document.getElementById("file-select");
    var file_drop = document.getElementById('file-drop');


if(! (file_select && file_drop)) {
   return;
}


if(! r.support) {
    console.log("Resumable.js is Not Supported.");
}
else {
    console.log("Resumable.js Works");
    r.assignBrowse(document.getElementById('file-select'));
    r.assignDrop(document.getElementById('file-drop'));
    $("#pause-button").hide();
    $("#cancel-button").hide();

    var danger_class = 'file-progress-list-item list-group-item list-group-item-danger';
    var success_class = 'file-progress-list-item list-group-item list-group-item-success';

    // Handle file add event
    r.on('fileAdded', function(file) {
        // Show progress pabr
        $("#file-upload-progress-bar").show();
        var link_prefix = '<a href="#" id="file-progress-list-item-' + file.uniqueIdentifier
            + '" class="file-progress-list-item list-group-item list-group-item-info">';
        var span_1 = '<span id="file-status-'+file.uniqueIdentifier+'" class="file-status pull-right">Uploading</span>';
        var span_2 = '<span id="file-progress-' + file.uniqueIdentifier
            + '" class="file-progress-status pull-right">0%</span>';
        var link_suffix = '</a>';
        $('#files-list').append(link_prefix + span_1 + file.fileName + span_2 + link_suffix);
        r.upload();
    });

   r.on('pause', function() {
       $('.file-status').each(function() {
           if($(this).html()!="Success") {
               $(this).html('Paused');
           }
       });
   });

   r.on('complete', function() {
       // Hide pause/resume when the upload has completed
       $("#pause-button").hide();
       $("#cancel-button").hide();         
       $("#file-upload-progress-bar").hide(); 
   });

   r.on('fileSuccess', function(file,message){
       // Reflect that the file upload has completed
       $('#file-status-'+file.uniqueIdentifier).html('Success');
       $('#file-progress-list-item-'+file.uniqueIdentifier).attr('class', success_class);
   });

   r.on('fileError', function(file, message) {

       $('#file-status-' + file.uniqueIdentifier).html('Error');
       $('#file-progress-list-item-'+file.uniqueIdentifier).attr('class', danger_class);
   });

    r.on('fileProgress', function(file) {
        // Handle progress for both the file and the overall upload
        $('#file-progress-'+file.uniqueIdentifier).html(Math.floor(file.progress()*100) + '%');
        $('#file-upload-progress').attr('aria-valuenow',r.progress()*100);
        $('#file-upload-progress').css('width', Math.floor(r.progress()*100) + '%');
        $('#file-upload-progress').html(Math.floor(r.progress()*100) + '%');
    });

    r.on('cancel', function() {
        $('.file-progress-status').html('');
        $('.file-status').each(function() {
            if($(this).html()!="Success") {
                $(this).html('Cancelled');
            }
        });
        $('.file-progress-list-item').attr('class', danger_class);
        $("#file-upload-progress-bar").hide();
    });

    r.on('uploadStart', function() {
        $('.file-status').each(function() {
            if($(this).html()!="Success") {
                $(this).html('Uploading');
            }
        });
        // Show pause, hide resume
        $("#pause-button").show();
        $("#cancel-button").show();
        $("#files-status").show();
    });

    $("#pause-button").click(function() {
        var currentvalue = $("#pause-button").text();
        if(currentvalue=="Pause") {
            r.pause();
            $("#pause-button").text("Start");
        }
        else if(currentvalue=="Start") {
            r.upload();
            $("#pause-button").text("Pause");
        }
    });

    $("#cancel-button").click(function() {
        r.cancel();
    });
}
});
