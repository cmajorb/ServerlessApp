

jQuery(function($) {
    var $modal = $('#editor-modal'),
        $editor = $('#editor'),
        $editorTitle = $('#editor-title'),
        ft = FooTable.init('#editing-example', {
            "columns": $.get('static/tenantheaders.json'),
            "rows": $.get(baseurl + '/tenants/'),
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
                    $editor.find('#name').val(values.name);
                    $editor.find('#email').val(values.email);
                    $modal.data('row', row);
                    $editorTitle.text('Edit row #' + values.id);
                    $modal.modal('show');
                },
                deleteRow: function(row){
                    if (confirm('Are you sure you want to delete the row?')){
                        $.ajax({
                            url: baseurl + "/tenants/"+row.val().id + '/',
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
        var row = $modal.data('row'),
            values = {
                id: $editor.find('#id').val(),
                name: $editor.find('#name').val(),
                email: $editor.find('#email').val()
            };

        if (row instanceof FooTable.Row){
            
            var myData = {
                "id": values.id,
                "name": values.name,
                "email": values.email
            };
            
            $.ajax({
                url: baseurl + "/tenants/"+ values.id + '/',
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
            $.post(baseurl + "/tenants/",{
				"id": values.id,
                "name": values.name,
                "email": values.email
            });
            values.id = uid++;
            ft.rows.add(values);
        }
        $modal.modal('hide');
    });
 
});
