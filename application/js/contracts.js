

jQuery(function($) {
 
    var $modal = $('#editor-modal'),
        $editor = $('#editor'),
        $editorTitle = $('#editor-title'),
        ft = FooTable.init('#editing-example', {
            "columns": $.get('static/contractheaders.json'),
            "rows": $.get(baseurl + '/contracts/'),
            editing: {
                enabled: true,
                addRow: function(){
                    $modal.removeData('row');
                    $editor[0].reset();
                    $editorTitle.text('Add a new row');
                    $modal.modal('show');
                },
                editRow: function(row){
                    var values = row.val();
                    console.log(values);
                    $editor.find('#id').val(values.id);
                    $editor.find('#contractid').val(values.contractid);
                    $editor.find('#tenant').val(values.tenantid);
                    $editor.find('#property').val(values.propertyid);
                    $editor.find('#owner').val(values.ownerid);
                    $editor.find('#expdate').val(values.expdate);
                    $editor.find('#increasedate').val(values.increasedate);
                    $editor.find('#increasepercentage').val(values.increasepercentage);
                    $editor.find('#baserent').val(values.baserent);
                    $editor.find('#salestax').val(values.salestax);
                    $editor.find('#utilities').val(values.utilities);
                    $editor.find('#managementfee').val(values.managementfee);
                    $modal.data('row', row);
                    $editorTitle.text('Edit row #' + values.id);
                    $modal.modal('show');
                },
                deleteRow: function(row){
                    if (confirm('Are you sure you want to delete the row?')){
                        $.ajax({
                            url: baseurl + "/contracts/"+row.val().id + '/',
                            type: 'DELETE',
                            success: function(result) {
                                console.log("success");
                            }
                        });
                        row.delete();
                    }
                }
            }
        }),
        uid = 10;
        
        
  
    $editor.on('submit', function(e){
        if (this.checkValidity && !this.checkValidity()) return;
        e.preventDefault();
        console.log($editor.find('#tenant').val());
        var row = $modal.data('row'),
            values = {
                id: $editor.find('#id').val(),
                contractid: $editor.find('#contractid').val(),
                tenantid: $editor.find('#tenant').val(),
                propertyid: $editor.find('#property').val(),
                ownerid: $editor.find('#owner').val(),
                expdate: $editor.find('#expdate').val(),
                increasedate: $editor.find('#increasedate').val(),
                increasepercentage: $editor.find('#increasepercentage').val(),
                baserent: $editor.find('#baserent').val(),
                salestax: $editor.find('#salestax').val(),
                utilities: $editor.find('#utilities').val(),
                managementfee: $editor.find('#managementfee').val()
            };

        if (row instanceof FooTable.Row){
            
            var myData = {
                "contractid": values.contractid,
                "tenantid": values.tenantid,
                "propertyid": values.propertyid,
                "ownerid": values.ownerid,
                "expdate": values.expdate,
                "increasedate": values.increasedate,
                "increasepercentage": values.increasepercentage,
                "baserent": values.baserent,
                "salestax": values.salestax,
                "utilities": values.utilities,
                "managementfee": values.managementfee
            };
            
            $.ajax({
                url: baseurl + "/contracts/"+ values.id + '/',
                type: 'PATCH',
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(myData),
                success: function(result) {
                    console.log("success");
                }
            });
            
            row.val(values);
            
        } else {
            $.post(baseurl + "/contracts/",{
				"contractid": values.contractid,
                "tenantid": values.tenantid,
                "propertyid": values.propertyid,
                "ownerid": values.ownerid,
                "expdate": values.expdate,
                "increasedate": values.increasedate,
                "increasepercentage": values.increasepercentage,
                "baserent": values.baserent,
                "salestax": values.salestax,
                "utilities": values.utilities,
                "managementfee": values.managementfee
            });
            values.id = uid++;
            ft.rows.add(values);
        }
        $modal.modal('hide');
    });
 
    $.getJSON( baseurl + "/tenants/", function( json ) {
        select = document.getElementById('tenant');
        for (var i = 0; i < json.length; i++){
            var opt = document.createElement('option');
            opt.value = json[i].id;
            opt.innerHTML = json[i].name;
            select.appendChild(opt);
          }
       });

       $.getJSON( baseurl + "/properties/", function( json ) {
        select = document.getElementById('property');
        for (var i = 0; i < json.length; i++){
            var opt = document.createElement('option');
            opt.value = json[i].id;
            opt.innerHTML = json[i].name;
            select.appendChild(opt);
          }
       });

       $.getJSON( baseurl + "/owners/", function( json ) {
        select = document.getElementById('owner');
        for (var i = 0; i < json.length; i++){
            var opt = document.createElement('option');
            opt.value = json[i].id;
            opt.innerHTML = json[i].name;
            select.appendChild(opt);
          }
       });
});
