

jQuery(function($) {
    var $modal = $('#editor-modal'),
        $editor = $('#editor'),
        $editorTitle = $('#editor-title'),
        ft = FooTable.init('#editing-example', {
            "columns": $.get('static/paymentheaders.json'),
            "rows": $.get(baseurl + '/payments/'),
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
                    $editor.find('#contract').val(values.contract);
                    $editor.find('#rent').val(values.rent);
                    $editor.find('#utilities').val(values.utilities);
                    $editor.find('#salestax').val(values.salestax);
                    $editor.find('#paymentdate').val(values.paymentdate);
                    $modal.data('row', row);
                    $editorTitle.text('Edit row #' + values.id);
                    $modal.modal('show');
                },
                deleteRow: function(row){
                    if (confirm('Are you sure you want to delete the row?')){
                        $.ajax({
                            url: baseurl + "/payments/"+row.val().id + '/',
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
                contract: $editor.find('#contract').val(),
                rent: $editor.find('#rent').val(),
                utilities: $editor.find('#utilities').val(),
                salestax: $editor.find('#salestax').val(),
                paymentdate: $editor.find('#paymentdate').val()
            };

        if (row instanceof FooTable.Row){
            
            var myData = {
                "id": values.id,
                "contract": values.contract,
                "rent": values.rent,
                "utilities": values.utilities,
                "salestax": values.salestax,
                "paymentdate": values.paymentdate
            };
            
            $.ajax({
                url: baseurl + "/payments/"+ values.id + '/',
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
            $.post(baseurl + "/payments/",{
				"id": values.id,
                "contract": values.contract,
                "rent": values.rent,
                "utilities": values.utilities,
                "salestax": values.salestax,
                "paymentdate": values.paymentdate
            });
            values.id = uid++;
            ft.rows.add(values);
        }
        $modal.modal('hide');
    });
 
});
